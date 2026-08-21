#!/usr/bin/env python3
"""IVDIVO Audio Studio — authenticated ProviderSnapshot repeatability diff.

Consumes only secret-free ProviderSnapshot objects that already satisfy the
canonical provider snapshot contract. It distinguishes account identity,
capability inventory and volatile usage drift. It never performs provider calls,
never substitutes a missing voice/model, and never turns repeatability into an
artistic or release claim.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Mapping

from provider_snapshot_contract import canonical_hash, validate_provider_snapshot


def _map_delta(first: Mapping[str, Any], second: Mapping[str, Any]) -> dict[str, Any]:
    first_keys = set(first)
    second_keys = set(second)
    added = sorted(second_keys - first_keys)
    removed = sorted(first_keys - second_keys)
    changed = sorted(
        key for key in first_keys & second_keys
        if canonical_hash(first[key]) != canonical_hash(second[key])
    )
    return {"added": added, "removed": removed, "changed": changed}


def _without_capture_time(value: Any) -> Any:
    if not isinstance(value, dict):
        return deepcopy(value)
    out = deepcopy(value)
    out.pop("captured_at", None)
    return out


def compare_provider_snapshots(
    first: dict[str, Any],
    second: dict[str, Any],
    *,
    expected_provider: str = "elevenlabs",
    max_age_seconds: float | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Compare two authenticated snapshots without laundering either into truth.

    Both snapshots are independently validated. A different account fingerprint
    is a hard failure. Capability changes are observations requiring downstream
    revalidation, not automatic substitutions or failures by themselves.
    """
    first_validation = validate_provider_snapshot(
        first, expected_provider=expected_provider, max_age_seconds=max_age_seconds, now=now
    )
    second_validation = validate_provider_snapshot(
        second, expected_provider=expected_provider, max_age_seconds=max_age_seconds, now=now
    )
    if not first_validation.get("verified"):
        return {"status": "FAIL_FIRST_SNAPSHOT", "verified": False, "first": first_validation}
    if not second_validation.get("verified"):
        return {"status": "FAIL_SECOND_SNAPSHOT", "verified": False, "second": second_validation}

    first_fp = first.get("account", {}).get("fingerprint_sha256")
    second_fp = second.get("account", {}).get("fingerprint_sha256")
    if first_fp != second_fp:
        return {
            "status": "FAIL_ACCOUNT_IDENTITY_DRIFT",
            "verified": False,
            "first_snapshot_hash": first_validation["snapshot_hash"],
            "second_snapshot_hash": second_validation["snapshot_hash"],
        }

    model_delta = _map_delta(first.get("models", {}), second.get("models", {}))
    voice_delta = _map_delta(first.get("voices", {}), second.get("voices", {}))
    account_changed = canonical_hash(first.get("account", {})) != canonical_hash(second.get("account", {}))
    volatile_changed = canonical_hash(_without_capture_time(first.get("volatile", {}))) != canonical_hash(
        _without_capture_time(second.get("volatile", {}))
    )
    capability_drift = any(model_delta[key] or voice_delta[key] for key in ("added", "removed", "changed"))

    return {
        "status": "PASS_CAPABILITY_DRIFT_OBSERVED" if capability_drift else "PASS_REPEATABLE_CAPABILITY_SET",
        "verified": True,
        "provider": expected_provider,
        "account_fingerprint_sha256": first_fp,
        "first_snapshot_hash": first_validation["snapshot_hash"],
        "second_snapshot_hash": second_validation["snapshot_hash"],
        "models": model_delta,
        "voices": voice_delta,
        "account_metadata_changed": account_changed,
        "volatile_usage_changed": volatile_changed,
        "capability_drift": capability_drift,
        "dispatch_revalidation_required": capability_drift,
        "auto_substitution": False,
        "authority_scope": "OBSERVATIONAL_ONLY",
    }
