#!/usr/bin/env python3
"""IVDIVO Audio Studio — secret-free AUTH_PROVIDER artifact intake.

Consumes the durable evidence bundle emitted by the read-only provider workflow,
revalidates the canonical AUTH_PROVIDER receipt, binds it to the exact GitHub
Actions run/attempt, optionally compares a prior authenticated snapshot, and
compiles a provider-neutral inventory. It never reads provider credentials,
performs provider calls, selects a voice, locks a voice, or authorizes spend.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import argparse
import json
import re

from external_evidence_trust import validate_provider_auth_receipt
from provider_inventory_compiler import compile_provider_inventory
from provider_snapshot_contract import canonical_hash, validate_provider_snapshot
from provider_snapshot_diff import compare_provider_snapshots

_FORBIDDEN_KEY_FRAGMENTS = (
    "api_key",
    "apikey",
    "authorization",
    "access_token",
    "private_key",
    "password",
    "bearer_token",
)


def _secret_key_hits(value: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = re.sub(r"[^a-z0-9]+", "_", str(key).lower()).strip("_")
            if any(fragment in normalized for fragment in _FORBIDDEN_KEY_FRAGMENTS):
                hits.append(f"{path}.{key}")
            hits.extend(_secret_key_hits(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(_secret_key_hits(child, f"{path}[{index}]"))
    return hits


def _positive_decimal_identity(value: int | str) -> str | None:
    text = str(value).strip()
    if not text.isdecimal():
        return None
    if int(text) <= 0:
        return None
    return str(int(text))


def _expected_source_ref(repository: str, run_id: str) -> str:
    return f"https://github.com/{repository}/actions/runs/{run_id}"


def intake_provider_evidence(
    payload: dict[str, Any],
    *,
    repository: str,
    run_id: int | str,
    run_attempt: int | str,
    snapshot_file: dict[str, Any] | None = None,
    prior_snapshot: dict[str, Any] | None = None,
    max_age_seconds: float = 21600,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Validate one provider evidence bundle and derive its next admissible state."""
    normalized_run_id = _positive_decimal_identity(run_id)
    normalized_attempt = _positive_decimal_identity(run_attempt)
    if normalized_run_id is None or normalized_attempt is None:
        return {
            "schema": "ivdivo.provider_evidence_intake/1.0",
            "status": "FAIL_WORKFLOW_RUN_IDENTITY_SHAPE",
            "verified": False,
            "provider_calls_performed": 0,
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }
    if not isinstance(repository, str) or repository.count("/") != 1 or any(part.strip() == "" for part in repository.split("/")):
        return {
            "schema": "ivdivo.provider_evidence_intake/1.0",
            "status": "FAIL_REPOSITORY_IDENTITY_SHAPE",
            "verified": False,
            "provider_calls_performed": 0,
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }

    secret_hits = _secret_key_hits(payload)
    if secret_hits:
        return {
            "schema": "ivdivo.provider_evidence_intake/1.0",
            "status": "FAIL_SECRET_BEARING_FIELD",
            "verified": False,
            "secret_field_paths": sorted(secret_hits),
            "provider_calls_performed": 0,
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }

    trust = validate_provider_auth_receipt(
        payload,
        expected_provider="elevenlabs",
        max_age_seconds=max_age_seconds,
        now=now,
    )
    if not trust.get("verified"):
        return {
            "schema": "ivdivo.provider_evidence_intake/1.0",
            "status": "HOLD_AUTH_PROVIDER_INVALID",
            "verified": False,
            "trust": trust,
            "provider_calls_performed": 0,
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }

    expected_transaction = f"{normalized_run_id}:{normalized_attempt}"
    expected_ref = _expected_source_ref(repository, normalized_run_id)
    durable = payload.get("durable_receipt") if isinstance(payload.get("durable_receipt"), dict) else {}
    if str(durable.get("transaction_id")) != expected_transaction:
        return {
            "schema": "ivdivo.provider_evidence_intake/1.0",
            "status": "FAIL_WORKFLOW_TRANSACTION_LINEAGE",
            "verified": False,
            "expected_transaction_id": expected_transaction,
            "actual_transaction_id": durable.get("transaction_id"),
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }
    if durable.get("source_ref") != expected_ref or trust.get("source_ref") != expected_ref:
        return {
            "schema": "ivdivo.provider_evidence_intake/1.0",
            "status": "FAIL_WORKFLOW_SOURCE_REF_LINEAGE",
            "verified": False,
            "expected_source_ref": expected_ref,
            "actual_source_ref": durable.get("source_ref"),
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }

    snapshot = payload.get("snapshot")
    if not isinstance(snapshot, dict):
        raise ValueError("AUTH_PROVIDER_VALIDATION_RETURNED_WITHOUT_SNAPSHOT")

    if snapshot_file is not None:
        snapshot_file_validation = validate_provider_snapshot(
            snapshot_file,
            expected_provider="elevenlabs",
            max_age_seconds=max_age_seconds,
            now=now,
        )
        if not snapshot_file_validation.get("verified"):
            return {
                "schema": "ivdivo.provider_evidence_intake/1.0",
                "status": "FAIL_ARTIFACT_SNAPSHOT_FILE_INVALID",
                "verified": False,
                "snapshot_file_validation": snapshot_file_validation,
                "provider_dispatch_allowed": False,
                "voice_lock": False,
            }
        if snapshot_file_validation.get("snapshot_hash") != trust.get("snapshot_hash"):
            return {
                "schema": "ivdivo.provider_evidence_intake/1.0",
                "status": "FAIL_ARTIFACT_PACKET_SNAPSHOT_DRIFT",
                "verified": False,
                "packet_snapshot_hash": trust.get("snapshot_hash"),
                "file_snapshot_hash": snapshot_file_validation.get("snapshot_hash"),
                "provider_dispatch_allowed": False,
                "voice_lock": False,
            }

    inventory = compile_provider_inventory(
        snapshot,
        expected_provider="elevenlabs",
        max_age_seconds=max_age_seconds,
        now=now,
    )
    if inventory.get("status") != "PASS" or inventory.get("verified") is not True:
        return {
            "schema": "ivdivo.provider_evidence_intake/1.0",
            "status": "HOLD_PROVIDER_CAPABILITY_INCOMPLETE",
            "verified": False,
            "auth_provider": trust,
            "inventory": inventory,
            "provider_dispatch_allowed": False,
            "voice_lock": False,
        }

    repeatability: dict[str, Any] | None = None
    if prior_snapshot is not None:
        repeatability = compare_provider_snapshots(
            prior_snapshot,
            snapshot,
            expected_provider="elevenlabs",
            max_age_seconds=max_age_seconds,
            now=now,
        )
        if not repeatability.get("verified"):
            return {
                "schema": "ivdivo.provider_evidence_intake/1.0",
                "status": "FAIL_PROVIDER_REPEATABILITY",
                "verified": False,
                "auth_provider": trust,
                "repeatability": repeatability,
                "provider_dispatch_allowed": False,
                "voice_lock": False,
            }

    next_state = "REPEATABILITY_REQUIRED" if prior_snapshot is None else "CAST_BINDING_REQUIRED"
    if repeatability and repeatability.get("capability_drift"):
        next_state = "CAPABILITY_DRIFT_REVALIDATION_REQUIRED"

    output = {
        "schema": "ivdivo.provider_evidence_intake/1.0",
        "status": "PASS_AUTH_PROVIDER_INTAKE",
        "verified": True,
        "provider": "elevenlabs",
        "repository": repository,
        "workflow_run_id": normalized_run_id,
        "workflow_run_attempt": normalized_attempt,
        "transaction_id": expected_transaction,
        "source_ref": expected_ref,
        "snapshot_hash": trust["snapshot_hash"],
        "account_fingerprint_sha256": snapshot.get("account", {}).get("fingerprint_sha256"),
        "readback_strength": trust.get("readback_strength"),
        "inventory": inventory,
        "repeatability": repeatability,
        "next_state": next_state,
        "provider_calls_performed": 0,
        "paid_synthesis_calls": 0,
        "provider_dispatch_allowed": False,
        "machine_may_auto_lock": False,
        "voice_lock": False,
        "artistic_selection_claimed": False,
    }
    output["intake_hash"] = canonical_hash(output)
    return output


def _load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(prog="ivdivo-provider-evidence-intake")
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--snapshot-file")
    parser.add_argument("--prior-snapshot")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-attempt", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = intake_provider_evidence(
        _load_json(args.receipt),
        repository=args.repository,
        run_id=args.run_id,
        run_attempt=args.run_attempt,
        snapshot_file=_load_json(args.snapshot_file) if args.snapshot_file else None,
        prior_snapshot=_load_json(args.prior_snapshot) if args.prior_snapshot else None,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result.get("status"),
        "verified": result.get("verified"),
        "next_state": result.get("next_state"),
        "snapshot_hash": result.get("snapshot_hash"),
        "intake_hash": result.get("intake_hash"),
    }, ensure_ascii=False, indent=2, sort_keys=True))
    if result.get("verified") is not True:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
