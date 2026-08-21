#!/usr/bin/env python3
"""IVDIVO Audio Studio — provider-inventory to human-audition readiness.

This module binds real provider voice IDs to provisional casting candidates and
builds immutable human-audition requirements. It cannot select a winner, cannot
voice-lock, and cannot convert metadata or synthetic fixtures into Human Signal.
"""
from __future__ import annotations

from hashlib import sha256
from typing import Any
import json

REQUIRED_CANARY_ROLES = ("NARRATOR", "ETHAN", "AOIFE")
PRONUNCIATION_TERMS = ("Ифа", "Контакт")
PERFORMANCE_STATES = ("NATURAL_RESTRAINED", "DIRECTED_CHANGE")
PAIR = ("ETHAN", "AOIFE")


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def _candidate_hash(role_id: str, voice_id: str) -> str:
    return sha256(f"{role_id}:{voice_id}".encode("utf-8")).hexdigest()


def build_cast_readiness(
    inventory: dict[str, Any],
    *,
    candidate_voice_ids: dict[str, list[str]],
    model_id: str,
) -> dict[str, Any]:
    if inventory.get("status") != "PASS" or inventory.get("verified") is not True:
        return {"status": "HOLD_PROVIDER_INVENTORY", "voice_lock": False, "machine_may_auto_lock": False}

    known_voice_rows = {
        row.get("voice_id"): row
        for row in inventory.get("voices", [])
        if isinstance(row, dict) and row.get("voice_id")
    }
    if model_id not in set(inventory.get("tts_model_ids", [])):
        return {
            "status": "HOLD_MODEL_BINDING",
            "missing_model_id": model_id,
            "voice_lock": False,
            "machine_may_auto_lock": False,
        }

    bindings: dict[str, list[dict[str, Any]]] = {}
    missing_roles: list[str] = []
    unknown_ids: dict[str, list[str]] = {}
    for role_id in REQUIRED_CANARY_ROLES:
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
            "voice_lock": False,
            "machine_may_auto_lock": False,
        }
    if missing_roles:
        return {
            "status": "HOLD_CAST_CANDIDATES",
            "missing_roles": sorted(missing_roles),
            "bindings": bindings,
            "voice_lock": False,
            "machine_may_auto_lock": False,
        }

    audition = {
        "pronunciation": {
            "terms": list(PRONUNCIATION_TERMS),
            "term_hashes": {term: sha256(term.encode("utf-8")).hexdigest() for term in PRONUNCIATION_TERMS},
            "evidence_scope": "PRONUNCIATION",
            "requires_heard_real_audio": True,
        },
        "multi_state": {
            "states": list(PERFORMANCE_STATES),
            "evidence_scope": "MULTI_STATE",
            "requires_heard_real_audio": True,
        },
        "pair": {
            "roles": list(PAIR),
            "evidence_scope": "PAIR",
            "requires_heard_real_audio": True,
        },
        "fatigue": {
            "minimum_seconds": 480,
            "target_maximum_seconds": 600,
            "evidence_scope": "FATIGUE",
            "requires_heard_real_audio": True,
        },
        "performance": {
            "evidence_scope": "PERFORMANCE",
            "requires_heard_real_audio": True,
        },
    }
    payload = {
        "schema": "ivdivo.cast_readiness/1.0",
        "provider": inventory.get("provider"),
        "source_snapshot_hash": inventory.get("source_snapshot_hash"),
        "inventory_account_fingerprint_sha256": inventory.get("account_fingerprint_sha256"),
        "model_id": model_id,
        "roles": list(REQUIRED_CANARY_ROLES),
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
