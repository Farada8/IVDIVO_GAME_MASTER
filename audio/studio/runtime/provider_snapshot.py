#!/usr/bin/env python3
"""Credential-safe provider evidence snapshot and drift gate.

This module never performs network calls and never persists credentials. It converts
an authenticated provider-preflight report into a deterministic, secret-free snapshot
that can be safely reused by dispatch/restart logic.

Important boundary:
- TARGETED voice verification is enough to prove the explicitly requested voice IDs;
- it is NOT an account-wide voice inventory and must never be used to claim that all
  provider voices were enumerated;
- volatile quota/request metadata is separated from stable identity/capability data.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from typing import Any, Iterable

SCHEMA_VERSION = "ivdivo.audio.provider_snapshot/1.0"
FORBIDDEN_KEY_FRAGMENTS = (
    "api_key", "apikey", "access_token", "refresh_token", "password", "passwd",
    "client_secret", "secret_key", "authorization", "bearer_token", "xi-api-key",
)


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(obj: Any) -> str:
    return sha256(_canonical(obj)).hexdigest()


def _secret_paths(obj: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            low = str(key).lower()
            if any(fragment in low for fragment in FORBIDDEN_KEY_FRAGMENTS):
                hits.append(f"{path}.{key}")
            hits.extend(_secret_paths(value, f"{path}.{key}"))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            hits.extend(_secret_paths(value, f"{path}[{index}]"))
    return hits


def assert_secret_free(obj: Any) -> None:
    hits = _secret_paths(obj)
    if hits:
        raise ValueError("SECRET_LIKE_FIELD_FORBIDDEN:" + ",".join(sorted(hits)))


def _normalize_model(model_id: str, row: dict[str, Any]) -> dict[str, Any]:
    status = str(row.get("status") or "UNKNOWN")
    return {
        "model_id": str(model_id),
        "status": status,
        "name": row.get("name"),
        "can_do_text_to_speech": bool(row.get("can_do_text_to_speech")) if status == "PASS" else False,
        "maximum_text_length_per_request": row.get("maximum_text_length_per_request"),
        "concurrency_group": row.get("concurrency_group"),
    }


def _normalize_voice(voice_id: str, row: dict[str, Any]) -> dict[str, Any]:
    status = str(row.get("status") or "UNKNOWN")
    return {
        "voice_id": str(voice_id),
        "status": status,
        "name": row.get("name"),
        "category": row.get("category"),
        "is_legacy": row.get("is_legacy"),
    }


def compile_snapshot(preflight: dict[str, Any], *, inventory_scope: str = "TARGETED") -> dict[str, Any]:
    """Compile a deterministic secret-free provider snapshot from preflight evidence."""
    assert_secret_free(preflight)
    provider = str(preflight.get("provider") or "").strip()
    if not provider:
        raise ValueError("PROVIDER_REQUIRED")
    scope = str(inventory_scope).upper()
    if scope not in {"TARGETED", "ACCOUNT_WIDE"}:
        raise ValueError("INVENTORY_SCOPE_INVALID")

    models = {
        str(mid): _normalize_model(str(mid), row if isinstance(row, dict) else {})
        for mid, row in sorted((preflight.get("models") or {}).items())
    }
    voices = {
        str(vid): _normalize_voice(str(vid), row if isinstance(row, dict) else {})
        for vid, row in sorted((preflight.get("voices") or {}).items())
    }
    stable = {
        "provider": provider,
        "inventory_scope": scope,
        "account_inventory_complete": scope == "ACCOUNT_WIDE",
        "models": models,
        "voices": voices,
    }
    volatile = {
        "checked_at": preflight.get("checked_at"),
        "connectivity": preflight.get("connectivity"),
        "credential": preflight.get("credential"),
        "preflight_status": preflight.get("status"),
        "failures": sorted({str(x) for x in (preflight.get("failures") or [])}),
        "models_request_meta": deepcopy(preflight.get("models_request_meta")),
        "http_status": preflight.get("http_status"),
        "secret_env_present": bool(preflight.get("secret_env_present")),
    }
    authenticated = volatile["credential"] == "PASS"
    status = "PASS" if authenticated and volatile["preflight_status"] == "PASS" else "HOLD"
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "authenticated": authenticated,
        "stable": stable,
        "volatile": volatile,
        "stable_snapshot_hash": canonical_hash(stable),
        "volatile_snapshot_hash": canonical_hash(volatile),
        "secret_persisted": False,
        "machine_may_infer_unlisted_voices": False,
    }
    return snapshot


def verify_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    assert_secret_free(snapshot)
    if snapshot.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("PROVIDER_SNAPSHOT_SCHEMA_UNSUPPORTED")
    stable = snapshot.get("stable")
    volatile = snapshot.get("volatile")
    if not isinstance(stable, dict) or not isinstance(volatile, dict):
        raise ValueError("PROVIDER_SNAPSHOT_PAYLOAD_MISSING")
    if canonical_hash(stable) != snapshot.get("stable_snapshot_hash"):
        raise ValueError("PROVIDER_STABLE_SNAPSHOT_HASH_MISMATCH")
    if canonical_hash(volatile) != snapshot.get("volatile_snapshot_hash"):
        raise ValueError("PROVIDER_VOLATILE_SNAPSHOT_HASH_MISMATCH")
    return {
        "status": "PASS",
        "authenticated": snapshot.get("authenticated") is True,
        "stable_snapshot_hash": snapshot["stable_snapshot_hash"],
    }


def dispatch_capability_gate(
    snapshot: dict[str, Any], *, required_model_ids: Iterable[str], required_voice_ids: Iterable[str]
) -> dict[str, Any]:
    """Fail closed for explicitly required capabilities; never auto-substitute."""
    try:
        verify_snapshot(snapshot)
    except ValueError as exc:
        return {"status": "HOLD", "reason": str(exc), "auto_substitution": False}
    if snapshot.get("authenticated") is not True or snapshot.get("status") != "PASS":
        return {"status": "HOLD", "reason": "AUTHENTICATED_PASS_SNAPSHOT_REQUIRED", "auto_substitution": False}

    stable = snapshot["stable"]
    models = stable.get("models") or {}
    voices = stable.get("voices") or {}
    missing_models = sorted({str(mid) for mid in required_model_ids if (models.get(str(mid)) or {}).get("status") != "PASS"})
    missing_voices = sorted({str(vid) for vid in required_voice_ids if (voices.get(str(vid)) or {}).get("status") != "PASS"})
    if missing_models or missing_voices:
        return {
            "status": "HOLD",
            "reason": "REQUIRED_PROVIDER_CAPABILITY_MISSING",
            "missing_model_ids": missing_models,
            "missing_voice_ids": missing_voices,
            "auto_substitution": False,
        }
    return {
        "status": "PASS",
        "stable_snapshot_hash": snapshot["stable_snapshot_hash"],
        "inventory_scope": stable.get("inventory_scope"),
        "account_inventory_complete": stable.get("account_inventory_complete") is True,
        "auto_substitution": False,
    }


def compare_stable_snapshots(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    """Separate material capability drift from harmless volatile metadata change."""
    verify_snapshot(previous)
    verify_snapshot(current)
    if previous["stable_snapshot_hash"] == current["stable_snapshot_hash"]:
        return {
            "status": "PASS_NO_STABLE_DRIFT",
            "stable_drift": False,
            "volatile_changed": previous.get("volatile_snapshot_hash") != current.get("volatile_snapshot_hash"),
            "auto_substitution": False,
        }
    return {
        "status": "HOLD_STABLE_CAPABILITY_DRIFT",
        "stable_drift": True,
        "previous_stable_snapshot_hash": previous["stable_snapshot_hash"],
        "current_stable_snapshot_hash": current["stable_snapshot_hash"],
        "auto_substitution": False,
    }
