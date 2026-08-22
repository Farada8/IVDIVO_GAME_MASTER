import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "01_REPLICATION_EVIDENCE.json").read_text(encoding="utf-8"))

class Cycle5ReplicationHandoffTests(unittest.TestCase):
    def test_01_exact_run32(self):
        self.assertEqual(DATA["replication"]["prompts_executed"], 32)
        self.assertEqual(DATA["replication"]["range"], "CX33-CX64")

    def test_02_next64_not_executed(self):
        self.assertEqual(DATA["replication"]["next_prompts_designed"], 64)
        self.assertEqual(DATA["replication"]["next_prompts_executed"], 0)

    def test_03_no_pa4_laundering(self):
        self.assertFalse(DATA["proof_boundary"]["pa4_satisfied_by_this_handoff"])

    def test_04_no_market_laundering(self):
        for key in ("human_signal", "buyer_wtp", "payment", "profitability", "contract"):
            self.assertFalse(DATA["proof_boundary"][key])

    def test_05_negative_sample_shortfalls_preserved(self):
        self.assertFalse(DATA["negative_evidence"]["verified_100_tender_corpus"])
        self.assertFalse(DATA["negative_evidence"]["verified_50_property_public_lead_corpus"])

    def test_06_no_outreach(self):
        self.assertFalse(DATA["negative_evidence"]["outreach_authorized"])

    def test_07_library_counts(self):
        self.assertEqual(DATA["library"]["physical"], 78)
        self.assertEqual(DATA["library"]["valid"], 68)
        self.assertEqual(DATA["library"]["unique_valid_hashes"], 58)

    def test_08_no_full_parallel_force_merge(self):
        self.assertIn("SALVAGE_UNIQUE_REPLICATION_DELTA_ONLY", DATA["disposition"])

if __name__ == "__main__":
    unittest.main()
