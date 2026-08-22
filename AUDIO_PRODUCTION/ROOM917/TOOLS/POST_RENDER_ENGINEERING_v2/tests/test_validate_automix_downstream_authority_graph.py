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

from validate_automix_downstream_authority_graph import HOLD, PASS, evaluate  # noqa: E402

GRAPH_PATH = ROOM917_DIR / "AUTOMIX" / "ROOM917_E01_AUTOMIX_DOWNSTREAM_AUTHORITY_GRAPH_v1.json"


class ValidateAutoMixDownstreamAuthorityGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))

    def assert_hold(self, graph, reason):
        result = evaluate(graph)
        self.assertEqual(HOLD, result["status"])
        self.assertFalse(result["release_authority"])
        self.assertIn(reason, result["reasons"])

    def test_current_authority_graph_passes(self):
        result = evaluate(copy.deepcopy(self.graph))
        self.assertEqual(PASS, result["status"])
        self.assertEqual(result["node_count"], result["reachable_node_count"])
        self.assertFalse(result["release_authority"])

    def test_direct_machine_qc_to_package_bypass_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph["required_edges"].append(["RENDER_MACHINE_QC", "P003B_PACKAGE"])
        self.assert_hold(graph, "p003b_package_must_have_only_eligibility_as_authoritative_predecessor")

    def test_handoff_to_package_bypass_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph["required_edges"].append(["P003B_RENDER_QC_HANDOFF", "P003B_PACKAGE"])
        self.assert_hold(graph, "p003b_package_must_have_only_eligibility_as_authoritative_predecessor")

    def test_machine_release_bypass_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph["required_edges"].append(["P003B_AUTOMIX_ELIGIBILITY", "RELEASE_DECISION"])
        self.assert_hold(graph, "release_must_have_only_listener_qc_as_authoritative_predecessor")

    def test_release_without_listener_qc_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph["required_edges"] = [e for e in graph["required_edges"] if e != ["P003B_LISTENER_QC", "RELEASE_DECISION"]]
        graph["required_edges"].append(["PASS_A_FREEZE", "RELEASE_DECISION"])
        self.assert_hold(graph, "release_must_have_only_listener_qc_as_authoritative_predecessor")

    def test_cycle_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph["required_edges"].append(["RELEASE_DECISION", "AUTOMIX_PREFLIGHT"])
        self.assert_hold(graph, "required_graph_has_cycle")

    def test_forbidden_required_edge_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph["required_edges"].append(["REAL_RENDER_BYTES", "P003B_PACKAGE"])
        self.assert_hold(graph, "required_edge_is_forbidden:REAL_RENDER_BYTES->P003B_PACKAGE")

    def test_legacy_builder_must_be_explicitly_non_authoritative_for_automix(self):
        graph = copy.deepcopy(self.graph)
        graph["legacy_paths"]["p003b_listener_package_builder.py"] = "OK_FOR_ALL_PATHS"
        self.assert_hold(graph, "legacy_builder_not_explicitly_non_authoritative_for_automix")

    def test_unreachable_node_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph["nodes"].append("ORPHAN")
        result = evaluate(graph)
        self.assertEqual(HOLD, result["status"])
        self.assertTrue(any(x.startswith("unreachable_nodes:") for x in result["reasons"]))


if __name__ == "__main__":
    unittest.main()
