#!/usr/bin/env python3
"""Authenticated, secret-free provider snapshot contract.

This is a provenance/integrity contract for capability snapshots. It prevents
accidental/stale/weak snapshot files from authorizing paid provider dispatch.
It is not a cryptographic proof that an operator could never forge a file; the
trusted production path is the paired read-only snapshot acquirer.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any
import json
import string

SCHEMA_VERSION = "ivdivo.provider_snapshot/1.0"
PRODUCTION_CAPTURE_METHOD = "DIRECT_AUTHENTICATED_READ_ONLY_API"
ELEVENLABS_AUTH_METHOD = "XI_API_KEY_RUNTIME_ENV"
ELEVENLABS_CAPTURE_ENGINE = "ivdivo.elevenlabs_snapshot_acquirer/1.0"
ELEVENLABS_REQUIRED_SOURCE_PATHS = {
    "/v1/user",
    "/v1/user/subscription",
    "/v1/models",
    "/v2/voices",
}
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


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in string.hexdigits for char in value)
    )


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
    if not isinstance(authentication, dict) or authentication.get("state") != "AUTHENTICATED":
        return {
            "status": "FAIL_NOT_AUTHENTICATED",
            "verified": False,
            "authentication_state": authentication.get("state") if isinstance(authentication, dict) else None,
        }
    if authentication.get("credential_persisted") is not False:
        return {"status": "FAIL_CREDENTIAL_PERSISTENCE_UNPROVEN", "verified": False}

    provenance = snapshot.get("provenance")
    if not isinstance(provenance, dict):
        return {"status": "FAIL_PROVENANCE_MISSING", "verified": False}
    required_provenance = ("captured_at", "capture_method", "capture_engine", "source")
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

    source = provenance.get("source")
    if not isinstance(source, list) or not source:
        return {"status": "FAIL_SOURCE_EVIDENCE_MISSING", "verified": False}
    invalid_source_rows = [
        row for row in source
        if not isinstance(row, dict)
        or not isinstance(row.get("path"), str)
        or row.get("http_status") != 200
    ]
    if invalid_source_rows:
        return {
            "status": "FAIL_SOURCE_EVIDENCE",
            "verified": False,
            "invalid_source_count": len(invalid_source_rows),
        }

    if provider.lower() == "elevenlabs":
        if authentication.get("method") != ELEVENLABS_AUTH_METHOD:
            return {
                "status": "FAIL_AUTH_METHOD",
                "verified": False,
                "expected_auth_method": ELEVENLABS_AUTH_METHOD,
                "actual_auth_method": authentication.get("method"),
            }
        if provenance.get("capture_method") != PRODUCTION_CAPTURE_METHOD:
            return {
                "status": "FAIL_CAPTURE_METHOD",
                "verified": False,
                "expected_capture_method": PRODUCTION_CAPTURE_METHOD,
                "actual_capture_method": provenance.get("capture_method"),
            }
        if provenance.get("capture_engine") != ELEVENLABS_CAPTURE_ENGINE:
            return {
                "status": "FAIL_CAPTURE_ENGINE",
                "verified": False,
                "expected_capture_engine": ELEVENLABS_CAPTURE_ENGINE,
                "actual_capture_engine": provenance.get("capture_engine"),
            }
        source_paths = {row["path"] for row in source}
        missing_paths = sorted(ELEVENLABS_REQUIRED_SOURCE_PATHS - source_paths)
        if missing_paths:
            return {
                "status": "FAIL_SOURCE_COVERAGE",
                "verified": False,
                "missing_paths": missing_paths,
            }

    account = snapshot.get("account")
    if not isinstance(account, dict) or not _is_sha256(account.get("fingerprint_sha256")):
        return {"status": "FAIL_ACCOUNT_FINGERPRINT", "verified": False}

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
    if not _is_sha256(supplied_hash):
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
        "production_capture_contract": True,
    }
