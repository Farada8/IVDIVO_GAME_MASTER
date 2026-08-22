from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
TOOL_DIR = HERE.parents[1]
ROOM917_DIR = HERE.parents[3]
sys.path.insert(0, str(TOOL_DIR))

from room917_automix_nonstop_route import evaluate  # noqa: E402

QUEUE_PATH = ROOM917_DIR / "AUTOMIX" / "ROOM917_E01_AUTOMIX_CONTINUATION_QUEUE_v1.json"


class Room917AutoMixNonStopRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))

    def test_current_local_holds_route_to_nearest_ready_safe_frontier(self):
        result = evaluate(copy.deepcopy(self.queue))
        self.assertEqual("PASS_ROUTE_DECISION", result["status"])
        self.assertEqual("CONTINUE", result["action"])
        self.assertEqual("A210_DOWNSTREAM_NO_BYPASS_REGRESSION", result["selected_id"])
        self.assertIn("A010_EXACT_MASTER_BYTES", result["blocked_local"])
        self.assertEqual([], result["blocked_global"])
        self.assertTrue(result["non_stop_preserved"])

    def test_human_evidence_gate_does_not_stop_ready_sibling(self):
        q = copy.deepcopy(self.queue)
        for row in q["obligations"]:
            if row["id"] == "A210_DOWNSTREAM_NO_BYPASS_REGRESSION":
                row["status"] = "DONE"
        result = evaluate(q)
        self.assertEqual("CONTINUE", result["action"])
        self.assertEqual("A220_DRIVE_GITHUB_DURABLE_SYNC", result["selected_id"])

    def test_global_authority_gate_stops_all_continuation(self):
        q = copy.deepcopy(self.queue)
        q["obligations"].append({
            "id": "A000_AUTHORITY_CONFLICT",
            "priority": 0,
            "status": "BLOCKED",
            "gate_type": "AUTHORITY_UNRESOLVED",
            "dependencies": [],
            "scope": "ROOM917_E01_AUTOMIX",
        })
        result = evaluate(q)
        self.assertEqual("GLOBAL_STOP", result["action"])
        self.assertIn("A000_AUTHORITY_CONFLICT", result["blocked_global"])

    def test_unknown_dependency_fails_queue_closed(self):
        q = copy.deepcopy(self.queue)
        q["obligations"][0]["dependencies"].append("DOES_NOT_EXIST")
        result = evaluate(q)
        self.assertEqual("FAIL_QUEUE_INVALID", result["status"])
        self.assertEqual("GLOBAL_STOP", result["action"])
        self.assertIn("UNKNOWN_DEPENDENCY:A001_PRODUCTION_D003_PATCH:DOES_NOT_EXIST", result["errors"])

    def test_duplicate_ids_fail_queue_closed(self):
        q = copy.deepcopy(self.queue)
        q["obligations"].append(copy.deepcopy(q["obligations"][0]))
        result = evaluate(q)
        self.assertEqual("FAIL_QUEUE_INVALID", result["status"])
        self.assertTrue(any(x.startswith("DUPLICATE_ID:") for x in result["errors"]))

    def test_blocked_gate_requires_known_gate_type(self):
        q = copy.deepcopy(self.queue)
        q["obligations"][1]["gate_type"] = "SOMETHING_UNKNOWN"
        result = evaluate(q)
        self.assertEqual("FAIL_QUEUE_INVALID", result["status"])
        self.assertIn("BLOCKED_GATE_TYPE_INVALID:A010_EXACT_MASTER_BYTES", result["errors"])

    def test_ready_obligation_waits_for_done_dependencies(self):
        q = copy.deepcopy(self.queue)
        for row in q["obligations"]:
            if row["id"] == "A140_P003B_AUTOMIX_ELIGIBILITY":
                row["status"] = "BLOCKED"
                row["gate_type"] = "DEPENDENCY_BLOCKED"
        result = evaluate(q)
        self.assertNotEqual("A210_DOWNSTREAM_NO_BYPASS_REGRESSION", result.get("selected_id"))
        self.assertNotEqual("A220_DRIVE_GITHUB_DURABLE_SYNC", result.get("selected_id"))

    def test_exhausted_ready_queue_reports_local_gate_not_false_completion(self):
        q = copy.deepcopy(self.queue)
        for row in q["obligations"]:
            if row["status"] == "READY":
                row["status"] = "DONE"
        result = evaluate(q)
        self.assertEqual("LOCAL_GATE_ONLY_NO_READY_SIBLING", result["action"])
        self.assertIsNone(result["selected_id"])
        self.assertTrue(result["blocked_local"])


if __name__ == "__main__":
    unittest.main()
