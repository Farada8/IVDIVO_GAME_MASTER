import sys
import unittest
from pathlib import Path

DELTA_ROOT = Path(__file__).resolve().parents[1]
if str(DELTA_ROOT) not in sys.path:
    sys.path.insert(0, str(DELTA_ROOT))

from engine.evidence_delta_guards import (
    bind_formation_evidence,
    split_blocker_state,
    can_assert_bid_decision,
)


class Cycle7EvidenceDeltaTests(unittest.TestCase):
    def test_formation_doc_verifies_legal_name(self):
        b = bind_formation_evidence("legal_name", "SYNTHESIS-IVDIVO LIMITED")
        self.assertTrue(b.verified and b.admissible)

    def test_formation_doc_cannot_verify_insurance(self):
        b = bind_formation_evidence("insurance", "present")
        self.assertFalse(b.verified or b.admissible)
        self.assertIsNone(b.value)

    def test_partial_identity_does_not_unlock_join(self):
        s = split_blocker_state(
            current_pack_complete=False,
            supplier_identity_verified=True,
            supplier_capability_complete=False,
        )
        self.assertEqual(s["supplier_side"], "PARTIAL_IDENTITY_ONLY")
        self.assertEqual(s["state"], "HOLD_MISSING_AUTHORITY")
        self.assertFalse(s["requirement_join_unlocked"])

    def test_full_pack_without_capability_holds_supplier_side(self):
        s = split_blocker_state(
            current_pack_complete=True,
            supplier_identity_verified=True,
            supplier_capability_complete=False,
        )
        self.assertEqual(s["state"], "HOLD_CAPABILITY_EVIDENCE")
        self.assertFalse(can_assert_bid_decision(True, False))

    def test_bid_decision_requires_both_sides(self):
        self.assertTrue(can_assert_bid_decision(True, True))
        self.assertFalse(can_assert_bid_decision(False, True))
        self.assertFalse(can_assert_bid_decision(True, False))


if __name__ == "__main__":
    unittest.main()
