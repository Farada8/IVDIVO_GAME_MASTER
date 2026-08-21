from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ivdivo_next_action", ROOT / "tools" / "ivdivo_next_action.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def explicit_state() -> dict:
    return {
        "schema_version": "ivdivo.execution_state/1.2",
        "authority_sources": [{"ref": "AUTH", "status": "CANON"}],
        "current_source": {"ref": "SOURCE", "status": "LOCKED"},
        "blocked_reasons": [],
        "unresolved_fatal_major": [],
        "state_revision": "r1",
        "state_status": "ACTIVE",
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
    }


def legacy_state() -> dict:
    return {
        "schema_version": "ivdivo.project_execution_state/legacy",
        "updated": "2026-08-21T13:42:00+01:00",
        "status": "ACTIVE",
        "current_blocker": None,
        "next_action": {
            "stage": "TEST_ACTION",
            "safe": True,
            "zero_cost": True,
            "reversible": True,
            "tool_executable_here": True,
        },
        "continuation_policy": {
            "default_continue_when_unblocked": True,
            "require_repeated_continuation_word": False,
            "safe_zero_cost_reversible_only": True,
        },
    }


class NextActionResolverTests(unittest.TestCase):
    def assert_stop(self, state: dict, reason: str) -> None:
        result = MODULE.resolve(state)
        self.assertEqual(result["decision"], "STOP")
        self.assertEqual(result["reason"], reason)

    def test_explicit_continue(self):
        self.assertEqual(MODULE.resolve(explicit_state())["decision"], "CONTINUE")

    def test_explicit_stale_stops(self):
        state = explicit_state(); state["selected_next_action"]["freshness_valid"] = False
        self.assert_stop(state, "STALE_OR_UNVERIFIED_FRONTIER")

    def test_explicit_authority_stops(self):
        state = explicit_state(); state["selected_next_action"]["authority_unambiguous"] = False
        self.assert_stop(state, "AUTHORITY_UNRESOLVED")

    def test_explicit_dependency_stops(self):
        state = explicit_state(); state["selected_next_action"]["dependencies_pass"] = False
        self.assert_stop(state, "DEPENDENCY_GATE_NOT_PASS")

    def test_founder_decision_gate_stops(self):
        state = explicit_state(); state["selected_next_action"]["requires_new_founder_choice"] = True
        self.assert_stop(state, "DECISION_GATE")

    def test_human_evidence_stops(self):
        state = explicit_state(); state["selected_next_action"]["requires_human_evidence"] = True
        self.assert_stop(state, "HUMAN_EVIDENCE_REQUIRED")

    def test_provider_gate(self):
        state = explicit_state(); state["selected_next_action"].update(requires_external_provider=True, external_provider_available=False)
        self.assert_stop(state, "EXTERNAL_PROVIDER_REQUIRED")
        state["selected_next_action"]["external_provider_available"] = True
        self.assertEqual(MODULE.resolve(state)["decision"], "CONTINUE")

    def test_locked_layer_gate(self):
        state = explicit_state(); state["selected_next_action"].update(reopens_locked_layer=True, locked_layer_reopen_authorized=False)
        self.assert_stop(state, "LOCKED_LAYER_REOPEN_NOT_AUTHORIZED")
        state["selected_next_action"]["locked_layer_reopen_authorized"] = True
        self.assertEqual(MODULE.resolve(state)["decision"], "CONTINUE")

    def test_irreversible_gate(self):
        state = explicit_state(); state["selected_next_action"].update(irreversible_high_impact=True, approval_present=False)
        self.assert_stop(state, "IRREVERSIBLE_APPROVAL_REQUIRED")
        state["selected_next_action"]["approval_present"] = True
        self.assertEqual(MODULE.resolve(state)["decision"], "CONTINUE")

    def test_fatal_major_stops(self):
        state = explicit_state(); state["unresolved_fatal_major"] = [{"severity": "MAJOR"}]
        self.assert_stop(state, "FATAL_MAJOR_UNRESOLVED")

    def test_frontier_conflict_stops(self):
        state = explicit_state(); state["state_status"] = "FRONTIER_CONFLICT"
        self.assert_stop(state, "STATE_STATUS:FRONTIER_CONFLICT")

    def test_legacy_unblocked_compatible_state_continues(self):
        result = MODULE.resolve(legacy_state())
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["contract_mode"], "LEGACY_COMPAT")

    def test_legacy_paid_flag_without_provider_metadata_stops(self):
        state = legacy_state(); state["next_action"]["zero_cost"] = False
        self.assert_stop(state, "PROVIDER_GATE_METADATA_REQUIRED")

    def test_legacy_nonreversible_without_approval_metadata_stops(self):
        state = legacy_state(); state["next_action"]["reversible"] = False
        self.assert_stop(state, "IRREVERSIBLE_GATE_METADATA_REQUIRED")

    def test_legacy_unsafe_without_safety_clearance_stops(self):
        state = legacy_state(); state["next_action"]["safe"] = False
        self.assert_stop(state, "SAFETY_CLEARANCE_REQUIRED")

    def test_legacy_current_blocker_stops(self):
        state = legacy_state(); state["current_blocker"] = {"type": "MISSING_REAL_EVIDENCE", "subtype": "ASSET_PERSISTENCE_REQUIRED"}
        self.assert_stop(state, "CURRENT_BLOCKER:ASSET_PERSISTENCE_REQUIRED")

    def test_legacy_tool_unavailable_stops(self):
        state = legacy_state(); state["next_action"]["tool_executable_here"] = False
        self.assert_stop(state, "TOOL_RUNTIME_LIMITATION")

    def test_legacy_provider_available_can_continue_even_if_paid(self):
        state = legacy_state(); state["next_action"].update(requires_external_provider=True, external_provider_available=True, zero_cost=False)
        self.assertEqual(MODULE.resolve(state)["decision"], "CONTINUE")

    def test_legacy_provider_missing_stops(self):
        state = legacy_state(); state["next_action"].update(requires_external_provider=True, external_provider_available=False)
        self.assert_stop(state, "EXTERNAL_PROVIDER_REQUIRED")


if __name__ == "__main__":
    unittest.main()
