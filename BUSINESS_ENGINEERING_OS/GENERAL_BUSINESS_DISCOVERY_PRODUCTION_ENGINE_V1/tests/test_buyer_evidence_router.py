from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "runtime" / "buyer_evidence_router.py"
spec = importlib.util.spec_from_file_location("buyer_evidence_router", MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
assert spec.loader is not None
spec.loader.exec_module(mod)


class BuyerEvidenceRouterTests(unittest.TestCase):
    def test_10_slot_screening_queue_is_not_buyer_proof(self):
        out = mod.validate_screening_queue("OPP-33", [f"SCR-{i}" for i in range(10)])
        self.assertTrue(out["valid"])
        self.assertFalse(out["buyer_proof"])
        self.assertFalse(out["demand_proof"])

    def test_wrong_queue_size_fails_closed(self):
        out = mod.validate_screening_queue("OPP-36", ["A", "B"])
        self.assertFalse(out["valid"])
        self.assertEqual(out["status"], "HOLD_SCREENING_QUEUE_MUST_HAVE_10_SLOTS")

    def test_duplicate_queue_candidate_fails_closed(self):
        out = mod.validate_screening_queue("OPP-37", ["A"] * 10)
        self.assertFalse(out["valid"])
        self.assertEqual(out["status"], "HOLD_DUPLICATE_SCREENING_CANDIDATE")

    def test_public_record_is_screening_only(self):
        rec = mod.EvidenceRecord("EV1", "OPP-33", "SCR1", "Example", claim="public candidate")
        out = mod.validate_evidence(rec)
        self.assertEqual(out["status"], "ACCEPT_SCREENING_ONLY")
        self.assertFalse(out["demand_proof"])

    def test_unverified_buyer_role_fails_closed(self):
        rec = mod.EvidenceRecord(
            "EV2", "OPP-36", "SCR2", "Example", role_type="BUYER", role_verified=False,
            source_type="INTERVIEW", behavior_level="E2", claim="shared data"
        )
        out = mod.validate_evidence(rec)
        self.assertFalse(out["accepted"])
        self.assertEqual(out["status"], "HOLD_BUYER_ROLE_UNVERIFIED")

    def test_contradiction_never_averages_away(self):
        rec = mod.EvidenceRecord(
            "EV3", "OPP-37", "SCR3", "Example", source_type="OBSERVATION",
            behavior_level="E2", claim="action", contradicts=("EV0",)
        )
        out = mod.validate_evidence(rec)
        self.assertFalse(out["accepted"])
        self.assertEqual(out["status"], "HOLD_CONTRADICTION_REQUIRES_RESOLUTION")

    def test_stale_record_fails_closed(self):
        rec = mod.EvidenceRecord("EV4", "OPP-33", "SCR4", "Example", review_state="STALE")
        out = mod.validate_evidence(rec)
        self.assertFalse(out["accepted"])
        self.assertEqual(out["status"], "HOLD_STALE")

    def test_e1_verbal_only_cannot_satisfy_fatal(self):
        out = mod.fatal_test_behavior_sufficient("OPP-33", ["E1", "E1"])
        self.assertFalse(out["sufficient"])
        self.assertEqual(out["status"], "HOLD_VERBAL_ONLY")

    def test_e2_can_route_to_review_but_not_auto_pass(self):
        out = mod.fatal_test_behavior_sufficient("OPP-36", ["E1", "E2"])
        self.assertTrue(out["sufficient"])
        self.assertFalse(out["auto_pass_fatal_test"])
        self.assertFalse(out["proof_promotion"])

    def test_e5_transaction_does_not_prove_repeatability(self):
        rec = mod.EvidenceRecord(
            "EV5", "OPP-37", "SCR5", "Example", role_type="BUYER", role_verified=True,
            source_type="TRANSACTION", behavior_level="E5", claim="payment"
        )
        out = mod.validate_evidence(rec)
        self.assertTrue(out["transaction"])
        self.assertFalse(out["repeatability"])
        self.assertFalse(out["proof_promotion"])

    def test_e6_repeat_still_requires_review(self):
        rec = mod.EvidenceRecord(
            "EV6", "OPP-37", "SCR6", "Example", role_type="BUYER", role_verified=True,
            source_type="TRANSACTION", behavior_level="E6", claim="repeat"
        )
        out = mod.validate_evidence(rec)
        self.assertTrue(out["repeatability"])
        self.assertFalse(out["proof_promotion"])

    def test_next_route_is_test37_internal(self):
        out = mod.next_route()
        self.assertEqual(out["executed_next64"], 24)
        self.assertEqual(out["remaining_next64"], 40)
        self.assertEqual(out["internal_test_ready"], "TEST-37")
        self.assertFalse(out["external_action_authorized"])
        self.assertFalse(out["proof_promotion"])


if __name__ == "__main__":
    unittest.main()
