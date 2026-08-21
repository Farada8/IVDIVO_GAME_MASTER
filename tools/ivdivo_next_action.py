#!/usr/bin/env python3
"""Fail-closed next-action resolver for persisted IVDIVO project state.

Aligned to Narrative OS Cross-Conversation State & Autopilot v1.2+.

The resolver is read-only. It never mutates canon/state, calls providers,
spends credits, or performs irreversible actions. It only decides whether the
already-selected next action may continue in the current execution context.

Two persisted shapes are supported:
1) explicit gate-contract state (state_status + selected_next_action), and
2) legacy/project-specific state (current_blocker + next_action).

Legacy fields safe/zero_cost/reversible are intentionally NOT universal
continuation prerequisites under Autopilot v1.2+. Real gates control STOP.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

STOP_STATE_STATUSES = {
    "BLOCKED",
    "AUTHORITY_UNRESOLVED",
    "FRONTIER_CONFLICT",
    "CANON_APPROVAL_REQUIRED",
    "HUMAN_EVIDENCE_REQUIRED",
    "EXTERNAL_PROVIDER_REQUIRED",
    "FATAL_MAJOR_UNRESOLVED",
    "TOOL_RUNTIME_LIMITATION",
    "HOLD",
}

EXPLICIT_REQUIRED_FLAGS = (
    "freshness_valid",
    "authority_unambiguous",
    "dependencies_pass",
    "executable_here",
    "requires_new_founder_choice",
    "requires_human_evidence",
    "requires_external_provider",
    "reopens_locked_layer",
    "irreversible_high_impact",
)


def _stop(reason: str, state: dict[str, Any], action: Any = None) -> dict[str, Any]:
    return {
        "decision": "STOP",
        "reason": reason,
        "state_revision": state.get("state_revision") or state.get("updated"),
        "selected_next_action": action
        if action is not None
        else state.get("selected_next_action") or state.get("next_action"),
    }


def _continue(state: dict[str, Any], action: dict[str, Any], mode: str) -> dict[str, Any]:
    return {
        "decision": "CONTINUE",
        "reason": (
            "fresh/usable authority + dependencies + executable action; "
            "no Founder/human/provider/locked-layer/irreversible/FATAL-MAJOR/tool blocker"
        ),
        "contract_mode": mode,
        "state_revision": state.get("state_revision") or state.get("updated"),
        "selected_next_action": action,
    }


def _check_common_action_gates(
    state: dict[str, Any], action: dict[str, Any], *, executable_key: str
) -> dict[str, Any] | None:
    if action.get(executable_key) is not True:
        return _stop("TOOL_RUNTIME_LIMITATION", state, action)

    if action.get("requires_new_founder_choice") is True:
        return _stop("DECISION_GATE", state, action)
    if action.get("requires_human_evidence") is True:
        return _stop("HUMAN_EVIDENCE_REQUIRED", state, action)

    if action.get("requires_external_provider") is True:
        if action.get("external_provider_available") is not True:
            return _stop("EXTERNAL_PROVIDER_REQUIRED", state, action)

    if action.get("reopens_locked_layer") is True:
        if action.get("locked_layer_reopen_authorized") is not True:
            return _stop("LOCKED_LAYER_REOPEN_NOT_AUTHORIZED", state, action)

    if action.get("irreversible_high_impact") is True:
        if action.get("approval_present") is not True:
            return _stop("IRREVERSIBLE_APPROVAL_REQUIRED", state, action)

    return None


def _resolve_explicit(state: dict[str, Any]) -> dict[str, Any]:
    status = str(state.get("state_status", "")).strip().upper()
    if not status:
        return _stop("STATE_STATUS_MISSING", state)
    if status in STOP_STATE_STATUSES:
        return _stop(f"STATE_STATUS:{status}", state)
    if status == "COMPLETE":
        return _stop("PROJECT_STATE_COMPLETE", state)
    if status != "ACTIVE":
        return _stop(f"UNKNOWN_STATE_STATUS:{status}", state)

    authority_sources = state.get("authority_sources")
    if not isinstance(authority_sources, list) or not authority_sources:
        return _stop("AUTHORITY_SOURCES_MISSING", state)

    source = state.get("current_source")
    if not isinstance(source, dict) or not str(source.get("ref", "")).strip():
        return _stop("CURRENT_SOURCE_MISSING", state)

    blocked = state.get("blocked_reasons")
    if not isinstance(blocked, list):
        return _stop("BLOCKED_REASONS_MISSING_OR_INVALID", state)
    if blocked:
        return _stop("BLOCKED_REASONS_PRESENT", state)

    fatal_major = state.get("unresolved_fatal_major")
    if not isinstance(fatal_major, list):
        return _stop("UNRESOLVED_FATAL_MAJOR_MISSING_OR_INVALID", state)
    if fatal_major:
        return _stop("FATAL_MAJOR_UNRESOLVED", state)

    action = state.get("selected_next_action")
    if not isinstance(action, dict):
        return _stop("SELECTED_NEXT_ACTION_MISSING_OR_INVALID", state)

    missing = [name for name in EXPLICIT_REQUIRED_FLAGS if name not in action]
    if missing:
        return _stop("ACTION_FLAGS_MISSING:" + ",".join(missing), state, action)

    if action["freshness_valid"] is not True:
        return _stop("STALE_OR_UNVERIFIED_FRONTIER", state, action)
    if action["authority_unambiguous"] is not True:
        return _stop("AUTHORITY_UNRESOLVED", state, action)
    if action["dependencies_pass"] is not True:
        return _stop("DEPENDENCY_GATE_NOT_PASS", state, action)

    stop = _check_common_action_gates(state, action, executable_key="executable_here")
    if stop:
        return stop

    return _continue(state, action, "EXPLICIT_V1_2")


def _resolve_legacy(state: dict[str, Any]) -> dict[str, Any]:
    status = str(state.get("status", "")).strip().upper()
    if status in STOP_STATE_STATUSES:
        return _stop(f"STATE_STATUS:{status}", state)

    blocker = state.get("current_blocker")
    if blocker:
        if isinstance(blocker, dict):
            label = blocker.get("subtype") or blocker.get("type") or "PRESENT"
        else:
            label = str(blocker)
        return _stop(f"CURRENT_BLOCKER:{label}", state)

    fatal_major = state.get("unresolved_fatal_major")
    if isinstance(fatal_major, list) and fatal_major:
        return _stop("FATAL_MAJOR_UNRESOLVED", state)

    action = state.get("next_action")
    if not isinstance(action, dict):
        return _stop("NEXT_ACTION_MISSING_OR_INVALID", state)

    if action.get("freshness_valid") is False:
        return _stop("STALE_OR_UNVERIFIED_FRONTIER", state, action)
    if action.get("authority_unambiguous") is False:
        return _stop("AUTHORITY_UNRESOLVED", state, action)
    if action.get("dependencies_pass") is False:
        return _stop("DEPENDENCY_GATE_NOT_PASS", state, action)

    executable_key = "tool_executable_here" if "tool_executable_here" in action else "executable_here"
    if executable_key not in action:
        return _stop("ACTION_EXECUTABILITY_MISSING", state, action)

    # Old cost/reversibility labels are not gates by themselves. If they signal
    # risk, however, the modern gate metadata must be explicit or we fail closed.
    if action.get("safe") is False and action.get("safety_clear") is not True:
        return _stop("SAFETY_CLEARANCE_REQUIRED", state, action)
    if action.get("zero_cost") is False and "requires_external_provider" not in action:
        return _stop("PROVIDER_GATE_METADATA_REQUIRED", state, action)
    if action.get("reversible") is False and "irreversible_high_impact" not in action:
        return _stop("IRREVERSIBLE_GATE_METADATA_REQUIRED", state, action)

    stop = _check_common_action_gates(state, action, executable_key=executable_key)
    if stop:
        return stop

    return _continue(state, action, "LEGACY_COMPAT")


def resolve(state: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(state, dict):
        return {"decision": "STOP", "reason": "STATE_NOT_OBJECT"}

    if "state_status" in state or "selected_next_action" in state:
        return _resolve_explicit(state)

    return _resolve_legacy(state)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed IVDIVO Autopilot v1.2+ next-action resolver"
    )
    parser.add_argument("state", type=Path, help="Path to persisted project execution-state JSON")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    args = parser.parse_args()

    try:
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if not isinstance(state, dict):
            raise TypeError("top-level execution state must be a JSON object")
    except Exception as exc:
        result = {"decision": "STOP", "reason": f"STATE_READ_ERROR:{exc}"}
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
        return 2

    result = resolve(state)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
    return 0 if result["decision"] == "CONTINUE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
