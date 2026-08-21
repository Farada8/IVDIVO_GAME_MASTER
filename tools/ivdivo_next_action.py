#!/usr/bin/env python3
"""Fail-closed IVDIVO autopilot decision helper.

Reads a persisted execution-state JSON and decides whether the declared next action
may continue automatically inside the current executing work block.

This tool is read-only. It does not call providers, spend credits, mutate canon,
write project state or authorize work beyond the governing IVDIVO authorities.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

STOP_BLOCKER_TYPES = {
    "AUTHORITY_AMBIGUITY",
    "FRONTIER_CONFLICT",
    "MISSING_REAL_EVIDENCE",
    "HUMAN_REVIEW_REQUIRED",
    "PAID_AUTHENTICATED_ACTION",
    "USER_CREDENTIAL_ACTION",
    "APPROVAL_REQUIRED",
    "FATAL_MAJOR_OPEN",
    "TOOL_UNAVAILABLE",
    "EXPLICIT_HOLD",
    "SAFETY_OR_LEGAL",
    "OTHER",
}


def blocker_present(blocker: Any) -> tuple[bool, str]:
    if blocker is None:
        return False, ""
    if isinstance(blocker, str):
        value = blocker.strip()
        if not value or value.upper() in {"NONE", "NO", "NULL"}:
            return False, ""
        return True, value
    if isinstance(blocker, dict):
        kind = str(blocker.get("type", "OTHER")).upper()
        description = str(blocker.get("description", "")).strip()
        if kind == "NONE":
            return False, ""
        if kind in STOP_BLOCKER_TYPES:
            return True, f"{kind}: {description}".rstrip(": ")
        return True, f"UNKNOWN_BLOCKER:{kind}: {description}".rstrip(": ")
    return True, f"INVALID_BLOCKER_TYPE:{type(blocker).__name__}"


def resolve(state: dict[str, Any]) -> dict[str, Any]:
    blocked, blocker_text = blocker_present(state.get("current_blocker"))
    if blocked:
        return {
            "decision": "STOP_BLOCKED",
            "reason": blocker_text,
            "next_action": state.get("next_action"),
        }

    policy = state.get("continuation_policy") or {}
    if not bool(policy.get("default_continue_when_unblocked", False)):
        return {
            "decision": "STOP_POLICY_NOT_ENABLED",
            "reason": "default_continue_when_unblocked is not true",
            "next_action": state.get("next_action"),
        }
    if bool(policy.get("require_repeated_continuation_word", True)):
        return {
            "decision": "STOP_POLICY_REQUIRES_CONTINUATION_WORD",
            "reason": "require_repeated_continuation_word is true or missing",
            "next_action": state.get("next_action"),
        }

    action = state.get("next_action")
    if isinstance(action, str):
        return {
            "decision": "STOP_ACTION_FLAGS_MISSING",
            "reason": "next_action is a string; explicit safe/zero_cost/reversible/tool_executable_here flags are required for automatic continuation",
            "next_action": action,
        }
    if not isinstance(action, dict):
        return {
            "decision": "STOP_INVALID_NEXT_ACTION",
            "reason": "next_action must be an object for automatic continuation",
            "next_action": action,
        }

    flags = {
        "safe": action.get("safe"),
        "zero_cost": action.get("zero_cost"),
        "reversible": action.get("reversible"),
        "tool_executable_here": action.get("tool_executable_here"),
    }
    missing = [name for name, value in flags.items() if value is None]
    if missing:
        return {
            "decision": "STOP_ACTION_FLAGS_MISSING",
            "reason": "missing explicit flags: " + ", ".join(missing),
            "next_action": action,
        }

    failed = [name for name, value in flags.items() if value is not True]
    if failed:
        return {
            "decision": "STOP_ACTION_NOT_AUTO_EXECUTABLE",
            "reason": "not all auto-continuation gates are true: " + ", ".join(failed),
            "next_action": action,
        }

    return {
        "decision": "CONTINUE",
        "reason": "no blocker and next action is safe + zero_cost + reversible + tool_executable_here",
        "next_action": action,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("state", type=Path, help="Path to a persisted IVDIVO execution-state JSON")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    try:
        state = json.loads(args.state.read_text(encoding="utf-8"))
    except Exception as exc:
        result = {"decision": "STOP_STATE_READ_ERROR", "reason": str(exc)}
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
        return 2

    result = resolve(state)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
    return 0 if result["decision"] == "CONTINUE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
