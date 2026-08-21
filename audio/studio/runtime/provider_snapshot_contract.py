#!/usr/bin/env python3
"""Authenticated, secret-free provider snapshot contract.

A snapshot is evidence about provider capability, not a credential container.
It may authorize downstream capability checks only when:
- the snapshot is explicitly PASS and AUTHENTICATED;
- provenance identifies when/how it was captured;
- model/voice inventories are explicit;
- no secret-bearing fields are persisted;
- its canonical content hash matches;
- optional freshness limits are satisfied.

This module performs no network calls and never reads provider secrets.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any
import json

SCHEMA_VERSION = "ivdivo.provider_snapshot/1.0"
AUTH_STATES = {"AUTHENTICATED"}
FORBIDDEN_KEY_TOKENS = {
    "api_key", "apikey", "authorization", "bearer", "cookie", "password",
    "secret", "token", "xi-api-key", "xi_api_key",
}
NORMALIZED_FORBIDDEN_KEY_TOKENS = {token.replace("-", "_") for token in FORBIDDEN_KEY_TOKENS}


def canonical_hash(obj: Any) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def _without_hash(snapshot: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(snapshot)
    payload.pop("snapshot_hash", None)
    return payload


def snapshot_content_hash(snapshot: dict[str, Any]) -> str:
    return canonical_hash(_without_hash(snapshot))


def secret_field_hits(value: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in NORMALIZED_FORBIDDEN_KEY_TOKENS:
                hits.append(f"{path}.{key}")
            hits.extend(secret_field_hits(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(secret_field_hits(child, f"{path}[{index}]"))
    return sorted(set(hits))


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("PROVIDER_SNAPSHOT_CAPTURED_AT_TZ_REQUIRED")
    return parsed.astimezone(timezone.utc)


def seal_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(payload)
    if secret_field_hits(out):
        raise ValueError("PROVIDER_SNAPSHOT_SECRET_FIELD_FORBIDDEN")
    out["snapshot_hash"] = snapshot_content_hash(out)
    return out


def validate_provider_snapshot(
    snapshot: dict[str, Any],
    *,
    expected_provider: str | None = None,
    max_age_seconds: float | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    if not isinstance(snapshot, dict):
        return {"status": "FAIL_SNAPSHOT_TYPE", "verified": False}

    secret_hits = secret_field_hits(snapshot)
    if secret_hits:
        return {
            "status": "FAIL_SECRET_LEAK",
            "verified": False,
            "secret_field_paths": secret_hits,
        }

    if snapshot.get("schema_version") != SCHEMA_VERSION:
        return {
            "status": "FAIL_SCHEMA",
            "verified": False,
            "expected_schema_version": SCHEMA_VERSION,
            "actual_schema_version": snapshot.get("schema_version"),
        }

    provider = snapshot.get("provider")
    if not isinstance(provider, str) or not provider:
        return {"status": "FAIL_PROVIDER_IDENTITY", "verified": False}
    if expected_provider and provider.lower() != expected_provider.lower():
        return {
            "status": "FAIL_PROVIDER_MISMATCH",
            "verified": False,
            "expected_provider": expected_provider,
            "actual_provider": provider,
        }

    if snapshot.get("status") != "PASS":
        return {
            "status": "FAIL_SNAPSHOT_NOT_PASS",
            "verified": False,
            "snapshot_status": snapshot.get("status"),
        }

    authentication = snapshot.get("authentication")
    if not isinstance(authentication, dict) or authentication.get("state") not in AUTH_STATES:
        return {
            "status": "FAIL_NOT_AUTHENTICATED",
            "verified": False,
            "authentication_state": authentication.get("state") if isinstance(authentication, dict) else None,
        }
    if not authentication.get("method"):
        return {"status": "FAIL_AUTH_METHOD_MISSING", "verified": False}

    provenance = snapshot.get("provenance")
    if not isinstance(provenance, dict):
        return {"status": "FAIL_PROVENANCE_MISSING", "verified": False}
    required_provenance = ("captured_at", "capture_method", "source")
    missing_provenance = [key for key in required_provenance if not provenance.get(key)]
    if missing_provenance:
        return {
            "status": "FAIL_PROVENANCE_INCOMPLETE",
            "verified": False,
            "missing": missing_provenance,
        }

    try:
        captured_at = _parse_utc(str(provenance["captured_at"]))
    except Exception as exc:
        return {
            "status": "FAIL_CAPTURE_TIME",
            "verified": False,
            "error_type": type(exc).__name__,
        }

    if max_age_seconds is not None:
        if max_age_seconds < 0:
            raise ValueError("PROVIDER_SNAPSHOT_MAX_AGE_NEGATIVE")
        current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        age = (current - captured_at).total_seconds()
        if age < -300:
            return {"status": "FAIL_CAPTURE_TIME_IN_FUTURE", "verified": False, "age_seconds": age}
        if age > max_age_seconds:
            return {
                "status": "FAIL_STALE",
                "verified": False,
                "age_seconds": age,
                "max_age_seconds": max_age_seconds,
            }

    voices = snapshot.get("voices")
    models = snapshot.get("models")
    if not isinstance(voices, dict) or not isinstance(models, dict):
        return {
            "status": "FAIL_INVENTORY_SHAPE",
            "verified": False,
            "voices_type": type(voices).__name__,
            "models_type": type(models).__name__,
        }

    supplied_hash = snapshot.get("snapshot_hash")
    if not isinstance(supplied_hash, str) or len(supplied_hash) != 64:
        return {"status": "FAIL_HASH_MISSING", "verified": False}
    actual_hash = snapshot_content_hash(snapshot)
    if supplied_hash.lower() != actual_hash:
        return {
            "status": "FAIL_HASH_DRIFT",
            "verified": False,
            "expected_snapshot_hash": supplied_hash.lower(),
            "actual_snapshot_hash": actual_hash,
        }

    return {
        "status": "PASS",
        "verified": True,
        "provider": provider,
        "snapshot_hash": actual_hash,
        "captured_at": captured_at.isoformat(),
        "voice_count": len(voices),
        "model_count": len(models),
        "secret_fields_present": False,
    }
