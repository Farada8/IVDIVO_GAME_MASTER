import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.primary_evidence_guards import (
    bidder_designation_authorized,
    classify_registry_screen,
    classify_seller_invoice,
    classify_tax_evidence,
    dedupe_invoice_families,
    public_derivative_redaction_ok,
    target_bid_decision_authorized,
)


class PrimaryEvidenceGuardTests(unittest.TestCase):
    def test_registry_number_can_be_bound_from_official_screen(self):
        out = classify_registry_screen(
            registration_number="796820",
            screen_status="Normal",
            capture_timestamp=None,
            embedded_latest_event_date="2026-05-22",
        )
        self.assertTrue(out.registration_number_proven)

    def test_undated_registry_screen_cannot_assert_current_status(self):
        out = classify_registry_screen(
            registration_number="796820",
            screen_status="Normal",
            capture_timestamp=None,
            embedded_latest_event_date="2026-05-22",
        )
        self.assertFalse(out.current_status_authorized)
        self.assertEqual(out.freshness, "LOWER_BOUND_ONLY_CURRENTNESS_UNVERIFIED")

    def test_timestamped_tax_statement_does_not_equal_tax_clearance(self):
        out = classify_tax_evidence(
            registration_evidence_present=True,
            statement_timestamp="2026-08-07T20:19:00+01:00",
            historical_balance_observed=True,
            tax_clearance_certificate_present=False,
        )
        self.assertTrue(out.registration_evidence_present)
        self.assertTrue(out.historical_account_state_present)
        self.assertFalse(out.tax_clearance_proven)

    def test_historical_tax_balance_cannot_be_promoted_to_current_balance(self):
        out = classify_tax_evidence(
            registration_evidence_present=True,
            statement_timestamp="2026-08-07T20:19:00+01:00",
            historical_balance_observed=True,
            tax_clearance_certificate_present=False,
        )
        self.assertFalse(out.current_balance_authorized)

    def test_self_issued_invoice_is_delivery_record_not_payment(self):
        out = classify_seller_invoice(
            invoice_number="INV-A",
            work_scope_present=True,
            independent_payment_receipt=False,
            client_completion_corroboration=False,
        )
        self.assertTrue(out.delivery_record_present)
        self.assertFalse(out.payment_proven)
        self.assertFalse(out.third_party_completion_proven)
        self.assertEqual(out.evidence_class, "SELF_ISSUED_DELIVERY_RECORD")

    def test_independent_receipt_is_required_for_payment_proof(self):
        out = classify_seller_invoice(
            invoice_number="INV-A",
            work_scope_present=True,
            independent_payment_receipt=True,
            client_completion_corroboration=False,
        )
        self.assertTrue(out.payment_proven)

    def test_duplicate_invoice_versions_merge_not_multiply(self):
        out = dedupe_invoice_families(
            [
                {"invoice_number": "A", "work_period": "P1"},
                {"invoice_number": "A", "work_period": "P1"},
                {"invoice_number": "B", "work_period": "P2"},
            ]
        )
        self.assertEqual(out["family_count"], 2)
        self.assertFalse(out["double_count_allowed"])

    def test_conflicting_periods_are_version_conflict(self):
        out = dedupe_invoice_families(
            [
                {"invoice_number": "A", "work_period": "P1"},
                {"invoice_number": "A", "work_period": "P2"},
            ]
        )
        self.assertEqual(out["version_conflicts"], ["A"])

    def test_company_context_cannot_auto_designate_bidder(self):
        self.assertFalse(bidder_designation_authorized(explicit_case_designation=False))
        self.assertTrue(bidder_designation_authorized(explicit_case_designation=True))

    def test_public_derivative_rejects_private_fields(self):
        self.assertFalse(public_derivative_redaction_ok({"iban": "secret"}))
        self.assertTrue(public_derivative_redaction_ok({"invoice_families": 3, "scope": "EWI"}))

    def test_bid_decision_requires_all_three_preconditions(self):
        self.assertFalse(
            target_bid_decision_authorized(
                target_pack_complete=False,
                explicit_bidder_designation=False,
                supplier_packet_complete=False,
            )
        )
        self.assertFalse(
            target_bid_decision_authorized(
                target_pack_complete=True,
                explicit_bidder_designation=False,
                supplier_packet_complete=True,
            )
        )
        self.assertTrue(
            target_bid_decision_authorized(
                target_pack_complete=True,
                explicit_bidder_designation=True,
                supplier_packet_complete=True,
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
