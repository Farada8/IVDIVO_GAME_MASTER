import copy
import unittest

from market_evidence_lineage import (
    BUYER_SCHEMA,
    MONEY_SCHEMA,
    artifact_fingerprint,
    route_market_evidence,
    validate_buyer_decision_receipt,
    validate_money_receipt,
)
from public_artifact_engine import procurement_sample


def pa4_artifact():
    a = procurement_sample()
    a.pa_grade = "PA4"
    return a


def buyer_receipt(artifact, **overrides):
    h = artifact_fingerprint(artifact)
    row = {
        "schema": BUYER_SCHEMA,
        "evidence_class": "BUYER_DECISION_USE",
        "source_type": "REAL_HUMAN",
        "receipt_id": "buyer-001",
        "artifact_hash": h,
        "artifact_id": artifact.artifact_id,
        "observed_at": "2026-08-22T01:30:00+01:00",
        "buyer_role": "Bid Manager",
        "decision_use": "USED",
        "interaction_outcome": "proceeded_to_full_document_review",
    }
    row.update(overrides)
    return row


def money_receipt(artifact, buyer_hash, **overrides):
    h = artifact_fingerprint(artifact)
    row = {
        "schema": MONEY_SCHEMA,
        "evidence_class": "DEPOSIT",
        "source_type": "REAL_TRANSACTION",
        "receipt_id": "money-001",
        "artifact_hash": h,
        "artifact_id": artifact.artifact_id,
        "buyer_receipt_hash": buyer_hash,
        "observed_at": "2026-08-22T02:00:00+01:00",
        "transaction_or_po_id": "txn-001",
        "amount": 100,
        "currency": "EUR",
    }
    row.update(overrides)
    return row


class ArtifactFingerprintTests(unittest.TestCase):
    def test_artifact_hash_is_deterministic(self):
        a = pa4_artifact()
        self.assertEqual(artifact_fingerprint(a), artifact_fingerprint(copy.deepcopy(a)))

    def test_artifact_hash_changes_on_material_change(self):
        a = pa4_artifact()
        b = copy.deepcopy(a)
        b.next_action = "DIFFERENT"
        self.assertNotEqual(artifact_fingerprint(a), artifact_fingerprint(b))


class BuyerEvidenceTests(unittest.TestCase):
    def test_missing_buyer_receipt_holds(self):
        a = pa4_artifact()
        out = validate_buyer_decision_receipt(None, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        self.assertEqual(out["status"], "HOLD_NO_REAL_TARGET_USER_DECISION_USE")

    def test_synthetic_buyer_receipt_fails(self):
        a = pa4_artifact()
        r = buyer_receipt(a, source_type="SYNTHETIC")
        out = validate_buyer_decision_receipt(r, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        self.assertEqual(out["status"], "FAIL_WRONG_OR_SYNTHETIC_BUYER_EVIDENCE_CLASS")

    def test_wrong_artifact_hash_fails(self):
        a = pa4_artifact()
        r = buyer_receipt(a, artifact_hash="0" * 64)
        out = validate_buyer_decision_receipt(r, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        self.assertEqual(out["status"], "FAIL_BUYER_ARTIFACT_LINEAGE")

    def test_caller_boolean_cannot_satisfy_e3(self):
        a = pa4_artifact()
        r = buyer_receipt(a, verified=True)
        out = validate_buyer_decision_receipt(r, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        self.assertEqual(out["status"], "FAIL_CALLER_BOOLEAN_OR_LABEL_AS_EVIDENCE")

    def test_real_decision_use_passes_pa5_e3_only(self):
        a = pa4_artifact()
        out = validate_buyer_decision_receipt(buyer_receipt(a), artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        self.assertEqual(out["status"], "PASS_PA5_E3_REAL_DECISION_USE")
        self.assertEqual(out["pa_grade"], "PA5")
        self.assertEqual(out["market_grade"], "E3")
        self.assertFalse(out["payment_proven"])
        self.assertFalse(out["profitability_proven"])


class MoneyEvidenceTests(unittest.TestCase):
    def test_missing_money_holds(self):
        a = pa4_artifact()
        self.assertEqual(validate_money_receipt(None, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id, buyer_receipt_hash="x")["status"], "HOLD_NO_REAL_MONEY_DEPOSIT_OR_PO")

    def test_synthetic_money_fails(self):
        a = pa4_artifact()
        b = validate_buyer_decision_receipt(buyer_receipt(a), artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        r = money_receipt(a, b["receipt_hash"], source_type="SYNTHETIC")
        out = validate_money_receipt(r, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id, buyer_receipt_hash=b["receipt_hash"])
        self.assertEqual(out["status"], "FAIL_WRONG_OR_SYNTHETIC_MONEY_EVIDENCE_CLASS")

    def test_wrong_buyer_lineage_fails(self):
        a = pa4_artifact()
        b = validate_buyer_decision_receipt(buyer_receipt(a), artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        r = money_receipt(a, "wrong")
        out = validate_money_receipt(r, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id, buyer_receipt_hash=b["receipt_hash"])
        self.assertEqual(out["status"], "FAIL_MONEY_BUYER_LINEAGE")

    def test_zero_amount_fails(self):
        a = pa4_artifact()
        b = validate_buyer_decision_receipt(buyer_receipt(a), artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        r = money_receipt(a, b["receipt_hash"], amount=0)
        out = validate_money_receipt(r, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id, buyer_receipt_hash=b["receipt_hash"])
        self.assertEqual(out["status"], "FAIL_MONEY_AMOUNT")

    def test_real_money_passes_e4_but_not_profitability(self):
        a = pa4_artifact()
        b = validate_buyer_decision_receipt(buyer_receipt(a), artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        r = money_receipt(a, b["receipt_hash"])
        out = validate_money_receipt(r, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id, buyer_receipt_hash=b["receipt_hash"])
        self.assertEqual(out["status"], "PASS_E4_REAL_MONEY_OBSERVED")
        self.assertEqual(out["market_grade"], "E4")
        self.assertFalse(out["unit_economics_proven"])
        self.assertFalse(out["profitability_proven"])


class RouterTests(unittest.TestCase):
    def test_pa3_cannot_skip_pa4(self):
        a = procurement_sample()
        out = route_market_evidence(a)
        self.assertEqual(out["status"], "PA4_INDEPENDENT_VALIDATION_REQUIRED")
        self.assertFalse(out["external_action_authorized"])

    def test_pa4_without_real_user_stops(self):
        a = pa4_artifact()
        out = route_market_evidence(a)
        self.assertEqual(out["status"], "REAL_TARGET_USER_DECISION_USE_REQUIRED")
        self.assertFalse(out["external_action_authorized"])

    def test_real_user_without_money_reaches_e3_only(self):
        a = pa4_artifact()
        out = route_market_evidence(a, buyer_receipt=buyer_receipt(a))
        self.assertEqual(out["status"], "PA5_E3_OBSERVED_E4_NOT_PROVEN")
        self.assertEqual(out["current_market_grade"], "E3")
        self.assertFalse(out["external_action_authorized"])

    def test_real_user_and_money_reaches_e4_measurement_gate(self):
        a = pa4_artifact()
        b_raw = buyer_receipt(a)
        b = validate_buyer_decision_receipt(b_raw, artifact_hash=artifact_fingerprint(a), artifact_id=a.artifact_id)
        out = route_market_evidence(a, buyer_receipt=b_raw, money_receipt=money_receipt(a, b["receipt_hash"]))
        self.assertEqual(out["status"], "E4_REAL_MONEY_OBSERVED_MEASUREMENT_REQUIRED")
        self.assertEqual(out["current_market_grade"], "E4")
        self.assertFalse(out["external_action_authorized"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
