#!/usr/bin/env python3
"""IVDIVO Audio Studio — provider-inventory to human-audition readiness.

This module binds real provider voice IDs to provisional casting candidates and
builds immutable human-audition requirements. It cannot select a winner, cannot
voice-lock, and cannot convert metadata or synthetic fixtures into Human Signal.

v1.1 adds a backward-compatible project casting specification surface. Existing
Lesson Zero callers retain their original defaults; other projects may supply
their own roles, pronunciation terms, pair gate and fatigue window without
forking the shared audio runtime.
"""
from __future__ import annotations

from hashlib import sha256
from typing import Any, Iterable
import json

REQUIRED_CANARY_ROLES = ("NARRATOR", "ETHAN", "AOIFE")
PRONUNCIATION_TERMS = ("Ифа", "Контакт")
PERFORMANCE_STATES = ("NATURAL_RESTRAINED", "DIRECTED_CHANGE")
PAIR = ("ETHAN", "AOIFE")
DEFAULT_FATIGUE_MINIMUM_SECONDS = 480
DEFAULT_FATIGUE_TARGET_MAXIMUM_SECONDS = 600


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def _candidate_hash(role_id: str, voice_id: str) -> str:
    return sha256(f"{role_id}:{voice_id}".encode("utf-8")).hexdigest()


def _normalise_string_tuple(value: Iterable[str] | None, default: tuple[str, ...]) -> tuple[str, ...]:
    if value is None:
        return default
    return tuple(dict.fromkeys(str(item).strip() for item in value if str(item).strip()))


def _validate_cast_spec(
    *,
    required_roles: tuple[str, ...],
    pronunciation_terms: tuple[str, ...],
    performance_states: tuple[str, ...],
    pair_roles: tuple[str, ...],
    fatigue_minimum_seconds: int,
    fatigue_target_maximum_seconds: int,
) -> dict[str, Any] | None:
    if not required_roles:
        return {"status": "FAIL_CAST_SPEC", "reason": "REQUIRED_ROLES_EMPTY"}
    if not performance_states:
        return {"status": "FAIL_CAST_SPEC", "reason": "PERFORMANCE_STATES_EMPTY"}
    if pair_roles and (len(pair_roles) != 2 or any(role not in required_roles for role in pair_roles)):
        return {
            "status": "FAIL_CAST_SPEC",
            "reason": "PAIR_ROLES_INVALID",
            "pair_roles": list(pair_roles),
            "required_roles": list(required_roles),
        }
    if fatigue_minimum_seconds <= 0 or fatigue_target_maximum_seconds < fatigue_minimum_seconds:
        return {
            "status": "FAIL_CAST_SPEC",
            "reason": "FATIGUE_WINDOW_INVALID",
            "minimum_seconds": fatigue_minimum_seconds,
            "target_maximum_seconds": fatigue_target_maximum_seconds,
        }
    return None


def build_cast_readiness(
    inventory: dict[str, Any],
    *,
    candidate_voice_ids: dict[str, list[str]],
    model_id: str,
    required_roles: Iterable[str] | None = None,
    pronunciation_terms: Iterable[str] | None = None,
    performance_states: Iterable[str] | None = None,
    pair_roles: Iterable[str] | None = None,
    fatigue_minimum_seconds: int = DEFAULT_FATIGUE_MINIMUM_SECONDS,
    fatigue_target_maximum_seconds: int = DEFAULT_FATIGUE_TARGET_MAXIMUM_SECONDS,
) -> dict[str, Any]:
    """Build a fail-closed casting-readiness manifest.

    Project-specific inputs are optional. Omitting them preserves the original
    Lesson Zero contract at the semantic level: NARRATOR/ETHAN/AOIFE,
    Ифа/Контакт, ETHAN↔AOIFE and the 480–600 second fatigue gate.
    """
    roles = _normalise_string_tuple(required_roles, REQUIRED_CANARY_ROLES)
    terms = _normalise_string_tuple(pronunciation_terms, PRONUNCIATION_TERMS)
    states = _normalise_string_tuple(performance_states, PERFORMANCE_STATES)
    pair = _normalise_string_tuple(pair_roles, PAIR)

    spec_error = _validate_cast_spec(
        required_roles=roles,
        pronunciation_terms=terms,
        performance_states=states,
        pair_roles=pair,
        fatigue_minimum_seconds=fatigue_minimum_seconds,
        fatigue_target_maximum_seconds=fatigue_target_maximum_seconds,
    )
    if spec_error:
        return {
            **spec_error,
            "voice_lock": False,
            "machine_may_auto_lock": False,
            "provider_dispatch_allowed": False,
        }

    if inventory.get("status") != "PASS" or inventory.get("verified") is not True:
        return {
            "status": "HOLD_PROVIDER_INVENTORY",
            "required_roles": list(roles),
            "voice_lock": False,
            "machine_may_auto_lock": False,
            "provider_dispatch_allowed": False,
        }

    known_voice_rows = {
        row.get("voice_id"): row
        for row in inventory.get("voices", [])
        if isinstance(row, dict) and row.get("voice_id")
    }
    if model_id not in set(inventory.get("tts_model_ids", [])):
        return {
            "status": "HOLD_MODEL_BINDING",
            "missing_model_id": model_id,
            "required_roles": list(roles),
            "voice_lock": False,
            "machine_may_auto_lock": False,
            "provider_dispatch_allowed": False,
        }

    bindings: dict[str, list[dict[str, Any]]] = {}
    missing_roles: list[str] = []
    unknown_ids: dict[str, list[str]] = {}
    for role_id in roles:
        supplied = list(dict.fromkeys(candidate_voice_ids.get(role_id, [])))
        if not supplied:
            missing_roles.append(role_id)
            bindings[role_id] = []
            continue
        bad = sorted(voice_id for voice_id in supplied if voice_id not in known_voice_rows)
        if bad:
            unknown_ids[role_id] = bad
        bindings[role_id] = [
            {
                "role_id": role_id,
                "voice_id": voice_id,
                "candidate_hash": _candidate_hash(role_id, voice_id),
                "voice_metadata_hash": known_voice_rows[voice_id].get("metadata_hash"),
                "status": "PROVISIONAL_CANDIDATE",
                "voice_lock": False,
            }
            for voice_id in supplied
            if voice_id in known_voice_rows
        ]

    if unknown_ids:
        return {
            "status": "FAIL_UNKNOWN_PROVIDER_VOICE_ID",
            "unknown_voice_ids": unknown_ids,
            "required_roles": list(roles),
            "voice_lock": False,
            "machine_may_auto_lock": False,
            "provider_dispatch_allowed": False,
        }
    if missing_roles:
        return {
            "status": "HOLD_CAST_CANDIDATES",
            "missing_roles": sorted(missing_roles),
            "bindings": bindings,
            "required_roles": list(roles),
            "voice_lock": False,
            "machine_may_auto_lock": False,
            "provider_dispatch_allowed": False,
        }

    audition = {
        "pronunciation": {
            "terms": list(terms),
            "term_hashes": {term: sha256(term.encode("utf-8")).hexdigest() for term in terms},
            "evidence_scope": "PRONUNCIATION",
            "requires_heard_real_audio": True,
        },
        "multi_state": {
            "states": list(states),
            "evidence_scope": "MULTI_STATE",
            "requires_heard_real_audio": True,
        },
        "pair": {
            "roles": list(pair),
            "evidence_scope": "PAIR",
            "requires_heard_real_audio": bool(pair),
        },
        "fatigue": {
            "minimum_seconds": fatigue_minimum_seconds,
            "target_maximum_seconds": fatigue_target_maximum_seconds,
            "evidence_scope": "FATIGUE",
            "requires_heard_real_audio": True,
        },
        "performance": {
            "evidence_scope": "PERFORMANCE",
            "requires_heard_real_audio": True,
        },
    }
    payload = {
        "schema": "ivdivo.cast_readiness/1.1",
        "provider": inventory.get("provider"),
        "source_snapshot_hash": inventory.get("source_snapshot_hash"),
        "inventory_account_fingerprint_sha256": inventory.get("account_fingerprint_sha256"),
        "model_id": model_id,
        "roles": list(roles),
        "bindings": bindings,
        "audition": audition,
        "status": "READY_FOR_REAL_AUDITION",
        "provider_dispatch_allowed": False,
        "human_evidence_required": True,
        "machine_may_auto_lock": False,
        "voice_lock": False,
        "auto_substitution": False,
    }
    payload["manifest_hash"] = canonical_hash(payload)
    return payload
