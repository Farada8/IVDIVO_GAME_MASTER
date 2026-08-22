import sys
import unittest
from pathlib import Path

DELTA_ROOT = Path(__file__).resolve().parents[1]
if str(DELTA_ROOT) not in sys.path:
    sys.path.insert(0, str(DELTA_ROOT))

from engine.evidence_delta_guards import (
    HistoricalAnalogUse,
    historical_analog_admissible,
    bind_formation_evidence,
    split_blocker_state,
    can_assert_bid_decision,
)


class Cycle7EvidenceDeltaTests(unittest.TestCase):
    def test_historical_analog_allowed_for_retrieval_hint(self):
        self.assertTrue(historical_analog_admissible(HistoricalAnalogUse.RETRIEVAL_HINT))

    def test_historical_analog_forbidden_as_current_requirement(self):
        self.assertFalse(historical_analog_admissible(HistoricalAnalogUse.CURRENT_REQUIREMENT))

    def test_formation_doc_verifies_legal_name(self):
        binding = bind_formation_evidence("legal_name", "SYNTHESIS-IVDIVO LIMITED")
        self.assertTrue(binding.verified)
        self.assertTrue(binding.admissible)

    def test_formation_doc_cannot_verify_insurance(self):
        binding = bind_formation_evidence("insurance", "present")
        self.assertFalse(binding.verified)
        self.assertFalse(binding.admissible)
        self.assertIsNone(binding.value)

    def test_partial_identity_does_not_unlock_join(self):
        state = split_blocker_state(
            current_pack_complete=False,
            supplier_identity_verified=True,
            supplier_capability_complete=False,
        )
        self.assertEqual(state["supplier_side"], "PARTIAL_IDENTITY_ONLY")
        self.assertEqual(state["state"], "HOLD_MISSING_AUTHORITY")
        self.assertFalse(state["requirement_join_unlocked"])

    def test_full_pack_without_capability_holds_supplier_side(self):
        state = split_blocker_state(
            current_pack_complete=True,
            supplier_identity_verified=True,
            supplier_capability_complete=False,
        )
        self.assertEqual(state["state"], "HOLD_CAPABILITY_EVIDENCE")
        self.assertFalse(can_assert_bid_decision(True, False))

    def test_bid_decision_requires_both_sides(self):
        self.assertTrue(can_assert_bid_decision(True, True))
        self.assertFalse(can_assert_bid_decision(False, True))
        self.assertFalse(can_assert_bid_decision(True, False))


if __name__ == "__main__":
    unittest.main()
