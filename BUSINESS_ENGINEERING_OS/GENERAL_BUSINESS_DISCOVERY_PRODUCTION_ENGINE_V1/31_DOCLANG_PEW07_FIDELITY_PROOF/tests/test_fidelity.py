import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pew07_fidelity", ROOT / "fidelity.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)


class TestPEW07Fidelity(unittest.TestCase):
    def test_good_fixture_preserves_ampersand_logically(self):
        blocks = MOD.extract_text_blocks(ROOT / "fixtures/good.dclg.xml")
        self.assertEqual(blocks[0], "Peter Thomas & Christian Johnston")
        self.assertEqual(blocks[1], "B")

    def test_good_fixture_fidelity_passes(self):
        result = MOD.evaluate(ROOT / "fixtures/good.dclg.xml")
        self.assertTrue(result["fidelity_pass"])
        self.assertEqual(result["mismatch_count"], 0)

    def test_semantic_drift_fixture_is_detected(self):
        result = MOD.evaluate(ROOT / "fixtures/semantic_drift.dclg.xml")
        self.assertFalse(result["fidelity_pass"])
        self.assertEqual(result["mismatch_count"], 1)
        self.assertEqual(result["mismatches"][0]["expected"], "Peter Thomas & Christian Johnston")
        self.assertEqual(result["mismatches"][0]["actual"], "Peter Thomas and Christian Johnston")

    def test_structure_is_not_used_as_fidelity_proxy(self):
        good = MOD.evaluate(ROOT / "fixtures/good.dclg.xml")
        drift = MOD.evaluate(ROOT / "fixtures/semantic_drift.dclg.xml")
        self.assertEqual(good["actual_block_count"], drift["actual_block_count"])
        self.assertNotEqual(good["fidelity_pass"], drift["fidelity_pass"])

    def test_proof_boundaries_are_preserved(self):
        result = MOD.evaluate(ROOT / "fixtures/semantic_drift.dclg.xml")
        self.assertEqual(result["buyer_demand"], "UNPROVEN")
        self.assertEqual(result["wtp"], "UNKNOWN")
        self.assertFalse(result["wip_promotion"])
        self.assertFalse(result["external_action_authorized"])


if __name__ == "__main__":
    unittest.main()
