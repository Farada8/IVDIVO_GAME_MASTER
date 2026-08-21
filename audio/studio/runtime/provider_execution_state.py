#!/usr/bin/env python3
"""IVDIVO Audio Studio — fail-closed provider-to-cast execution state resolver.

This resolver may route from admissible AUTH_PROVIDER evidence to inventory/cast
audition preparation. It intentionally cannot authorize a human voice lock,
pre-spend GO, or paid dispatch; those remain receipt/authority-bound downstream
canonical gates.
"""
from __future__ import annotations

from typing import Any


def resolve_provider_execution_state(
    intake: dict[str, Any] | None,
    *,
    cast_readiness: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(intake, dict) or intake.get("verified") is not True:
        return {
            "status": "NO_ADMISSIBLE_PROVIDER_EVIDENCE",
            "next_action": "RUN_AUTH_PROVIDER_WORKFLOW",
            "provider_dispatch_allowed": False,
            "machine_may_auto_lock": False,
            "voice_lock": False,
        }

    state = intake.get("next_state")
    if state == "REPEATABILITY_REQUIRED":
        return {
            "status": "AUTH_PROVIDER_VERIFIED",
            "next_action": "ACQUIRE_SECOND_READ_ONLY_SNAPSHOT",
            "provider_dispatch_allowed": False,
            "machine_may_auto_lock": False,
            "voice_lock": False,
        }
    if state == "CAPABILITY_DRIFT_REVALIDATION_REQUIRED":
        return {
            "status": "CAPABILITY_DRIFT_REVALIDATION_REQUIRED",
            "next_action": "REVALIDATE_CAST_BINDINGS_FROM_CURRENT_INVENTORY",
            "provider_dispatch_allowed": False,
            "machine_may_auto_lock": False,
            "voice_lock": False,
        }
    if state != "CAST_BINDING_REQUIRED":
        return {
            "status": "HOLD_UNKNOWN_PROVIDER_STATE",
            "next_action": "INSPECT_PROVIDER_INTAKE",
            "provider_dispatch_allowed": False,
            "machine_may_auto_lock": False,
            "voice_lock": False,
        }

    if not isinstance(cast_readiness, dict):
        return {
            "status": "INVENTORY_READY",
            "next_action": "BIND_PROVISIONAL_CAST_CANDIDATES",
            "provider_dispatch_allowed": False,
            "machine_may_auto_lock": False,
            "voice_lock": False,
        }
    if cast_readiness.get("status") != "READY_FOR_REAL_AUDITION":
        return {
            "status": "CAST_NOT_AUDITION_READY",
            "next_action": "REPAIR_CAST_READINESS",
            "provider_dispatch_allowed": False,
            "machine_may_auto_lock": False,
            "voice_lock": False,
        }
    return {
        "status": "AUDITION_REQUIRED",
        "next_action": "COLLECT_REAL_PRONUNCIATION_MULTI_STATE_PAIR_FATIGUE_EVIDENCE",
        "provider_dispatch_allowed": False,
        "machine_may_auto_lock": False,
        "voice_lock": False,
        "downstream_authority": "EXISTING_RECEIPT_BASED_HUMAN_AND_SPEND_GATES",
    }
