import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from wave11_frontier_evaluator import PROMPTS, evaluate_frontier


class Wave11FrontierTests(unittest.TestCase):
    def test_exact_32_prompt_specs(self):
        self.assertEqual(len(PROMPTS), 32)
        self.assertEqual([row.prompt_id for row in PROMPTS], list(range(1, 33)))

    def test_graph_is_acyclic_by_construction(self):
        for row in PROMPTS:
            self.assertTrue(all(dep < row.prompt_id for dep in row.depends_on))

    def test_no_completion_means_only_prompt_01_ready(self):
        out = evaluate_frontier([])
        self.assertEqual(out["status"], "PASS_ROUTING_GRAPH")
        self.assertEqual(out["next_ready_ids"], [1])
        self.assertFalse(out["external_truth_validated"])

    def test_prompt_02_ready_only_after_01(self):
        out = evaluate_frontier([1])
        self.assertIn(2, out["next_ready_ids"])
        self.assertIn(7, out["next_ready_ids"])
        self.assertNotIn(3, out["next_ready_ids"])

    def test_illegal_completion_order_holds(self):
        out = evaluate_frontier([2])
        self.assertEqual(out["status"], "HOLD_DEPENDENCY_VIOLATION")
        self.assertEqual(out["next_ready_ids"], [])
        self.assertEqual(out["dependency_violations"][0]["missing_dependencies"], [1])

    def test_unknown_completion_id_holds(self):
        out = evaluate_frontier([99])
        self.assertEqual(out["status"], "HOLD_UNKNOWN_COMPLETION_ID")
        self.assertFalse(out["release_go"])

    def test_paid_dispatch_30_not_ready_before_explicit_29(self):
        completed = list(range(1, 29))
        out = evaluate_frontier(completed)
        self.assertEqual(out["next_ready_ids"], [29])
        row30 = next(row for row in out["rows"] if row["prompt_id"] == 30)
        self.assertEqual(row30["routing_state"], "BLOCKED_DEPENDENCY")

    def test_paid_dispatch_30_ready_after_29(self):
        completed = list(range(1, 30))
        out = evaluate_frontier(completed)
        self.assertEqual(out["next_ready_ids"], [30])
        row30 = next(row for row in out["rows"] if row["prompt_id"] == 30)
        self.assertEqual(row30["action_class"], "PAID_DISPATCH")

    def test_prompt_32_never_ready_before_31(self):
        completed = list(range(1, 31))
        out = evaluate_frontier(completed)
        self.assertEqual(out["next_ready_ids"], [31])
        row32 = next(row for row in out["rows"] if row["prompt_id"] == 32)
        self.assertEqual(row32["missing_dependencies"], [31])

    def test_router_never_grants_external_authority(self):
        out = evaluate_frontier(range(1, 33))
        self.assertFalse(out["voice_lock"])
        self.assertFalse(out["release_go"])
        self.assertFalse(out["provider_dispatch_authorized"])
        self.assertEqual(out["provider_calls_performed"], 0)
        self.assertEqual(out["paid_calls_performed"], 0)
        self.assertEqual(out["human_reviews_performed"], 0)
        self.assertEqual(out["authority_scope"], "ROUTING_ONLY_NOT_EXTERNAL_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
