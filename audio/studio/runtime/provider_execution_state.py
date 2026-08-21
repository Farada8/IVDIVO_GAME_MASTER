#!/usr/bin/env python3
"""IVDIVO Audio Studio — fail-closed provider-to-cast execution state resolver."""
from __future__ import annotations

from typing import Any


def resolve_provider_execution_state(
    intake: dict[str, Any] | None,
    *,
    cast_readiness: dict[str, Any] | None = None,
    human_lock_authorized: bool = False,
    pre_spend_go: bool = False,
) -> dict[str, Any]:
    """Return the strongest admissible provider/cast state without creating evidence."""
    if not isinstance(intake, dict) or intake.get("verified") is not True:
        return {
            "status": "NO_ADMISSIBLE_PROVIDER_EVIDENCE",
            "next_action": "RUN_AUTH_PROVIDER_WORKFLOW",
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }

    state = intake.get("next_state")
    if state == "REPEATABILITY_REQUIRED":
        return {
            "status": "AUTH_PROVIDER_VERIFIED",
            "next_action": "ACQUIRE_SECOND_READ_ONLY_SNAPSHOT",
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }
    if state == "CAPABILITY_DRIFT_REVALIDATION_REQUIRED":
        return {
            "status": "CAPABILITY_DRIFT_REVALIDATION_REQUIRED",
            "next_action": "REVALIDATE_CAST_BINDINGS_FROM_CURRENT_INVENTORY",
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }
    if state != "CAST_BINDING_REQUIRED":
        return {
            "status": "HOLD_UNKNOWN_PROVIDER_STATE",
            "next_action": "INSPECT_PROVIDER_INTAKE",
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }

    if not isinstance(cast_readiness, dict):
        return {
            "status": "INVENTORY_READY",
            "next_action": "BIND_PROVISIONAL_CAST_CANDIDATES",
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }
    if cast_readiness.get("status") != "READY_FOR_REAL_AUDITION":
        return {
            "status": "CAST_NOT_AUDITION_READY",
            "next_action": "REPAIR_CAST_READINESS",
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }
    if human_lock_authorized is not True:
        return {
            "status": "AUDITION_REQUIRED",
            "next_action": "COLLECT_REAL_PRONUNCIATION_MULTI_STATE_PAIR_FATIGUE_EVIDENCE",
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }
    if pre_spend_go is not True:
        return {
            "status": "HUMAN_LOCK_AUTHORIZED_PRE_SPEND_HOLD",
            "next_action": "ISSUE_EXPLICIT_PRE_SPEND_GO",
            "provider_dispatch_allowed": False,
            "voice_lock": True,
        }
    return {
        "status": "PRE_SPEND_GO_RECEIVED",
        "next_action": "RUN_CONTROLLED_PROVIDER_DISPATCH_WITH_EXISTING_SPEND_LINEAGE",
        "provider_dispatch_allowed": True,
        "voice_lock": True,
        "warning": "This state resolver does not itself prove spend ledger, request identity, capability freshness, or provider dispatch acceptance; downstream canonical gates remain mandatory.",
    }
