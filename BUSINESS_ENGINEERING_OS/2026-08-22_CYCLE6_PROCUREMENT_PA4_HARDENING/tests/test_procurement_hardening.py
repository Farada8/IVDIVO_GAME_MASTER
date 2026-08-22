import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).parents[1] / "engine" / "procurement_hardening.py"
spec = importlib.util.spec_from_file_location("procurement_hardening", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ProcurementHardeningTests(unittest.TestCase):
    def test_incomplete_pack_holds(self):
        s = mod.ProcurementEvidenceState()
        self.assertEqual(mod.decide_bid(s), mod.Decision.HOLD_INSUFFICIENT_EVIDENCE)

    def test_unverified_supplier_holds(self):
        s = mod.ProcurementEvidenceState(official_pack_complete=True)
        self.assertEqual(mod.decide_bid(s), mod.Decision.HOLD_INSUFFICIENT_EVIDENCE)

    def test_incomplete_join_holds(self):
        s = mod.ProcurementEvidenceState(official_pack_complete=True, supplier_profile_verified=True)
        self.assertEqual(mod.decide_bid(s), mod.Decision.HOLD_INSUFFICIENT_EVIDENCE)

    def test_unknown_mandatory_gap_holds(self):
        s = mod.ProcurementEvidenceState(True, True, True, unknown_mandatory_gap_count=1)
        self.assertEqual(mod.decide_bid(s), mod.Decision.HOLD_INSUFFICIENT_EVIDENCE)

    def test_noncurable_mandatory_gap_no_bid(self):
        s = mod.ProcurementEvidenceState(True, True, True, noncurable_mandatory_gap_count=1)
        self.assertEqual(mod.decide_bid(s), mod.Decision.NO_BID)

    def test_complete_no_fatal_gap_bids(self):
        s = mod.ProcurementEvidenceState(True, True, True)
        self.assertEqual(mod.decide_bid(s), mod.Decision.BID)

    def test_contract_value_does_not_infer_cash_need(self):
        self.assertIsNone(mod.estimated_cash_requirement_from_contract_value(1600000))

    def test_pa4_requires_same_complete_inputs(self):
        self.assertFalse(mod.pa4_ready(mod.ProcurementEvidenceState()))
        self.assertTrue(mod.pa4_ready(mod.ProcurementEvidenceState(True, True, True)))

    def test_gap_unknown_is_not_noncompliant(self):
        self.assertEqual(mod.classify_gap(requirement_met=None, curable_before_deadline=None), mod.GapState.UNKNOWN)

    def test_gap_curable_requires_positive_time_path(self):
        self.assertEqual(mod.classify_gap(requirement_met=False, curable_before_deadline=True), mod.GapState.CURABLE_BEFORE_DEADLINE)


if __name__ == "__main__":
    unittest.main()
