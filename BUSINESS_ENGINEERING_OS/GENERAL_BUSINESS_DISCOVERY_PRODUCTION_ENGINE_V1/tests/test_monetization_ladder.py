import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from monetization_ladder import EvidenceError, MonetizationEvidence, route


class MonetizationLadderTests(unittest.TestCase):
    def test_no_artifact_stays_m0(self):
        self.assertEqual(route(MonetizationEvidence("CF-01"))["disposition"], "M0_INTERNAL_PROOF_REQUIRED")

    def test_artifact_without_delta_stays_m0(self):
        self.assertEqual(route(MonetizationEvidence("X", technical_artifact=True))["disposition"], "M0_INTERNAL_PROOF_REQUIRED")

    def test_delta_requires_artifact(self):
        with self.assertRaises(EvidenceError):
            route(MonetizationEvidence("X", nontrivial_delta=True))

    def test_buyer_role_required_before_offer_spec(self):
        r = route(MonetizationEvidence("X", technical_artifact=True, nontrivial_delta=True))
        self.assertEqual(r["disposition"], "M0_BUYER_ROLE_REQUIRED")

    def test_ow01_current_evidence_routes_m1(self):
        r = route(MonetizationEvidence("OW-01", True, True, True))
        self.assertEqual(r["disposition"], "M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN")
        self.assertFalse(r["proof_boundary"]["technical_artifact_is_market_proof"])

    def test_one_paid_diagnostic_only_routes_m2(self):
        r = route(MonetizationEvidence("X", True, True, True, paid_diagnostic_transactions=1))
        self.assertEqual(r["disposition"], "M2_PAID_DIAGNOSTIC_PROVEN_IMPLEMENTATION_NOT_PROVEN")

    def test_implementation_without_diagnostic_is_invalid(self):
        with self.assertRaises(EvidenceError):
            route(MonetizationEvidence("X", True, True, True, paid_implementation_transactions=1))

    def test_paid_implementation_routes_m3(self):
        r = route(MonetizationEvidence("X", True, True, True, paid_diagnostic_transactions=1, paid_implementation_transactions=1))
        self.assertEqual(r["disposition"], "M3_IMPLEMENTATION_PROVEN_RECURRING_NOT_PROVEN")

    def test_one_recurring_cycle_not_enough(self):
        r = route(MonetizationEvidence("X", True, True, True, paid_diagnostic_transactions=1, paid_implementation_transactions=1, paid_recurring_cycles=1))
        self.assertEqual(r["disposition"], "M3_IMPLEMENTATION_PROVEN_RECURRING_NOT_PROVEN")

    def test_two_recurring_cycles_routes_m4(self):
        r = route(MonetizationEvidence("X", True, True, True, paid_diagnostic_transactions=1, paid_implementation_transactions=1, paid_recurring_cycles=2, independent_customer_contexts_same_workflow=2))
        self.assertEqual(r["disposition"], "M4_RECURRING_VALIDATED_SOFTWARE_NOT_PROVEN")

    def test_three_customer_contexts_routes_only_software_candidate(self):
        r = route(MonetizationEvidence("X", True, True, True, paid_diagnostic_transactions=3, paid_implementation_transactions=3, paid_recurring_cycles=3, independent_customer_contexts_same_workflow=3))
        self.assertEqual(r["disposition"], "M5_SOFTWARE_CANDIDATE_NOT_SAAS_PROVEN")
        self.assertFalse(r["proof_boundary"]["software_candidate_is_saas_proven"])

    def test_external_authorization_does_not_promote_evidence(self):
        r = route(MonetizationEvidence("OW-01", True, True, True, external_action_authorized=True))
        self.assertEqual(r["disposition"], "M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN")


if __name__ == "__main__":
    unittest.main()
