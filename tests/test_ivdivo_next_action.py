from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ivdivo_next_action", ROOT / "tools" / "ivdivo_next_action.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def base_state() -> dict:
    return {
        "schema_version": "ivdivo.execution_state/1.1",
        "project_id": "TEST",
        "active_project": "TEST PROJECT",
        "active_line": "TEST_LINE",
        "active_branch": "main",
        "mode": "WORKING",
        "current_phase": "TEST_PHASE",
        "authority_sources": [{"ref": "AUTH", "status": "CANON"}],
        "current_source": {"ref": "SOURCE", "status": "LOCKED"},
        "completed_artifacts": [],
        "last_completed_artifact": None,
        "open_gates": [],
        "unresolved_fatal_major": [],
        "dependency_dag": {},
        "next_unblocked_obligations": ["TEST_ACTION"],
        "selected_next_action": {
            "stage": "TEST_ACTION",
            "freshness_valid": True,
            "authority_unambiguous": True,
            "dependencies_pass": True,
            "executable_here": True,
            "requires_new_founder_choice": False,
            "requires_human_evidence": False,
            "requires_external_provider": False,
            "reopens_locked_layer": False,
            "irreversible_high_impact": False,
        },
        "blocked_reasons": [],
        "state_revision": "r1",
        "state_status": "ACTIVE",
    }


class NextActionResolverTests(unittest.TestCase):
    def assert_stop(self, state: dict, reason: str) -> None:
        result = MODULE.resolve(state)
        self.assertEqual(result["decision"], "STOP")
        self.assertEqual(result["reason"], reason)

    def test_continue_when_current_unblocked_and_executable(self):
        self.assertEqual(MODULE.resolve(base_state())["decision"], "CONTINUE")

    def test_stale_frontier_stops(self):
        state = base_state()
        state["selected_next_action"]["freshness_valid"] = False
        self.assert_stop(state, "STALE_OR_UNVERIFIED_FRONTIER")

    def test_founder_decision_gate_stops(self):
        state = base_state()
        state["selected_next_action"]["requires_new_founder_choice"] = True
        self.assert_stop(state, "DECISION_GATE")

    def test_human_evidence_stops(self):
        state = base_state()
        state["selected_next_action"]["requires_human_evidence"] = True
        self.assert_stop(state, "HUMAN_EVIDENCE_REQUIRED")

    def test_missing_provider_stops_but_available_provider_continues(self):
        state = base_state()
        state["selected_next_action"].update(
            requires_external_provider=True,
            external_provider_available=False,
        )
        self.assert_stop(state, "EXTERNAL_PROVIDER_REQUIRED")
        state["selected_next_action"]["external_provider_available"] = True
        self.assertEqual(MODULE.resolve(state)["decision"], "CONTINUE")

    def test_locked_layer_requires_explicit_authority(self):
        state = base_state()
        state["selected_next_action"].update(
            reopens_locked_layer=True,
            locked_layer_reopen_authorized=False,
        )
        self.assert_stop(state, "LOCKED_LAYER_REOPEN_NOT_AUTHORIZED")
        state["selected_next_action"]["locked_layer_reopen_authorized"] = True
        self.assertEqual(MODULE.resolve(state)["decision"], "CONTINUE")

    def test_irreversible_action_requires_approval(self):
        state = base_state()
        state["selected_next_action"].update(
            irreversible_high_impact=True,
            approval_present=False,
        )
        self.assert_stop(state, "IRREVERSIBLE_APPROVAL_REQUIRED")
        state["selected_next_action"]["approval_present"] = True
        self.assertEqual(MODULE.resolve(state)["decision"], "CONTINUE")

    def test_unresolved_fatal_major_stops(self):
        state = base_state()
        state["unresolved_fatal_major"] = [{"severity": "MAJOR", "id": "M1"}]
        self.assert_stop(state, "FATAL_MAJOR_UNRESOLVED")

    def test_frontier_conflict_state_stops(self):
        state = base_state()
        state["state_status"] = "FRONTIER_CONFLICT"
        self.assert_stop(state, "STATE_STATUS:FRONTIER_CONFLICT")


if __name__ == "__main__":
    unittest.main()
