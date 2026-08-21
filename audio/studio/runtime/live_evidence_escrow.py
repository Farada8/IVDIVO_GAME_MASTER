#!/usr/bin/env python3
"""Restart-safe, secret-free provider evidence escrow.

This module binds request/spend/provider/audio/alignment/capability evidence into one
immutable lineage envelope. It never dispatches a provider, never retries paid work,
and never upgrades provider acceptance into production/take acceptance.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Iterable

SCHEMA_VERSION = "ivdivo.audio.live_evidence_lineage/1.0"
ESCROW_VERSION = "ivdivo.audio.live_evidence_escrow/1.0"
PROVIDER_STATES = {"ACCEPTED", "REJECTED", "AMBIGUOUS"}


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(obj: Any) -> str:
    return sha256(_canonical(obj)).hexdigest()


def _valid_sha(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdefABCDEF" for c in value)


def _require_sha(record: dict[str, Any], key: str) -> str:
    value = record.get(key)
    if not _valid_sha(value):
        raise ValueError(f"{key.upper()}_INVALID")
    return str(value).lower()


def compile_lineage(record: dict[str, Any]) -> dict[str, Any]:
    required_text = ("project_id", "episode_id", "block_id", "request_hash", "provider", "provider_state")
    for key in required_text:
        if not isinstance(record.get(key), str) or not str(record[key]).strip():
            raise ValueError(f"{key.upper()}_REQUIRED")
    state = str(record["provider_state"]).upper()
    if state not in PROVIDER_STATES:
        raise ValueError("PROVIDER_STATE_INVALID")
    request_hash = _require_sha(record, "request_hash")
    source_sha = _require_sha(record, "source_sha256")
    capability_hash = _require_sha(record, "capability_snapshot_sha256")

    provider_request_id = record.get("provider_request_id")
    audio_sha = record.get("audio_sha256")
    alignment_sha = record.get("alignment_sha256")
    charge_ref = record.get("charge_ref")
    audio_ref = record.get("audio_ref")
    alignment_ref = record.get("alignment_ref")

    if state == "ACCEPTED":
        if not provider_request_id:
            raise ValueError("ACCEPTED_PROVIDER_REQUEST_ID_REQUIRED")
        if not _valid_sha(audio_sha):
            raise ValueError("ACCEPTED_AUDIO_SHA256_REQUIRED")
        if not audio_ref:
            raise ValueError("ACCEPTED_AUDIO_DURABLE_REF_REQUIRED")
        if alignment_sha is not None and not _valid_sha(alignment_sha):
            raise ValueError("ALIGNMENT_SHA256_INVALID")
        if alignment_sha is not None and not alignment_ref:
            raise ValueError("ALIGNMENT_DURABLE_REF_REQUIRED")
    elif state == "AMBIGUOUS":
        if audio_sha or alignment_sha:
            raise ValueError("AMBIGUOUS_EVIDENCE_CANNOT_ASSERT_ACCEPTED_MEDIA")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "project_id": str(record["project_id"]),
        "episode_id": str(record["episode_id"]),
        "block_id": str(record["block_id"]),
        "source_sha256": source_sha,
        "request_hash": request_hash,
        "provider": str(record["provider"]),
        "provider_state": state,
        "provider_request_id": provider_request_id,
        "capability_snapshot_sha256": capability_hash,
        "audio_sha256": str(audio_sha).lower() if _valid_sha(audio_sha) else None,
        "alignment_sha256": str(alignment_sha).lower() if _valid_sha(alignment_sha) else None,
        "audio_ref": audio_ref,
        "alignment_ref": alignment_ref,
        "request_ref": record.get("request_ref"),
        "response_ref": record.get("response_ref"),
        "spend_ledger_ref": record.get("spend_ledger_ref"),
        "charge_ref": charge_ref,
        "canonical_asset_status": record.get("canonical_asset_status", "HOLD"),
        "production_take_status": "NOT_ACCEPTED",
        "take_lock": False,
        "created_at": record.get("created_at"),
        "secret_persisted": False,
    }
    payload["lineage_sha256"] = canonical_hash(payload)
    return payload


def verify_lineage(lineage: dict[str, Any]) -> dict[str, Any]:
    if lineage.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("LIVE_LINEAGE_SCHEMA_UNSUPPORTED")
    expected = lineage.get("lineage_sha256")
    unsigned = dict(lineage)
    unsigned.pop("lineage_sha256", None)
    if not _valid_sha(expected) or canonical_hash(unsigned) != expected:
        raise ValueError("LIVE_LINEAGE_HASH_MISMATCH")
    if lineage.get("secret_persisted") is not False:
        raise ValueError("LIVE_LINEAGE_SECRET_BOUNDARY_VIOLATION")
    if lineage.get("take_lock") is not False or lineage.get("production_take_status") != "NOT_ACCEPTED":
        raise ValueError("PROVIDER_EVIDENCE_CANNOT_SELF_ACCEPT_TAKE")
    return {"status": "PASS", "lineage_sha256": expected}


def compile_exact_escrow(
    lineages: Iterable[dict[str, Any]], *, expected_block_ids: Iterable[str],
    expected_source_sha256: str, expected_request_hashes: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Require exactly the expected live lineages; extras/duplicates/ambiguity fail closed."""
    if not _valid_sha(expected_source_sha256):
        raise ValueError("EXPECTED_SOURCE_SHA256_INVALID")
    expected = [str(x) for x in expected_block_ids]
    if not expected or len(set(expected)) != len(expected):
        raise ValueError("EXPECTED_BLOCK_IDS_INVALID")
    expected_set = set(expected)
    rows = list(lineages)
    verified: list[dict[str, Any]] = []
    for row in rows:
        verify_lineage(row)
        verified.append(row)

    block_ids = [str(row.get("block_id")) for row in verified]
    duplicates = sorted({bid for bid in block_ids if block_ids.count(bid) > 1})
    unknown = sorted(set(block_ids) - expected_set)
    missing = sorted(expected_set - set(block_ids))
    request_hashes = [str(row.get("request_hash")) for row in verified]
    duplicate_requests = sorted({h for h in request_hashes if request_hashes.count(h) > 1})
    ambiguous = sorted(str(row.get("block_id")) for row in verified if row.get("provider_state") == "AMBIGUOUS")
    nonaccepted = sorted(str(row.get("block_id")) for row in verified if row.get("provider_state") != "ACCEPTED")
    source_drift = sorted(str(row.get("block_id")) for row in verified if row.get("source_sha256") != expected_source_sha256.lower())
    request_drift: list[str] = []
    if expected_request_hashes:
        for row in verified:
            bid = str(row["block_id"])
            expected_hash = expected_request_hashes.get(bid)
            if not _valid_sha(expected_hash) or row.get("request_hash") != str(expected_hash).lower():
                request_drift.append(bid)

    issues = {
        "missing_block_ids": missing,
        "duplicate_block_ids": duplicates,
        "unknown_block_ids": unknown,
        "duplicate_request_hashes": duplicate_requests,
        "ambiguous_block_ids": ambiguous,
        "nonaccepted_block_ids": nonaccepted,
        "source_drift_block_ids": source_drift,
        "request_drift_block_ids": sorted(request_drift),
    }
    blocked = any(issues.values()) or len(verified) != len(expected)
    ordered = sorted(verified, key=lambda row: expected.index(str(row["block_id"])) if str(row["block_id"]) in expected_set else len(expected))
    payload = {
        "schema_version": ESCROW_VERSION,
        "status": "HOLD" if blocked else "PASS_EXACT_ESCROW",
        "expected_source_sha256": expected_source_sha256.lower(),
        "expected_block_ids": expected,
        "lineage_count": len(verified),
        "issues": issues,
        "lineages": ordered,
        "provider_acceptance_is_not_take_acceptance": True,
        "auto_retry_allowed": False,
        "machine_may_replay_paid_request": False,
    }
    payload["escrow_sha256"] = canonical_hash(payload)
    return payload


def verify_escrow(escrow: dict[str, Any]) -> dict[str, Any]:
    if escrow.get("schema_version") != ESCROW_VERSION:
        raise ValueError("LIVE_ESCROW_SCHEMA_UNSUPPORTED")
    expected = escrow.get("escrow_sha256")
    unsigned = dict(escrow)
    unsigned.pop("escrow_sha256", None)
    if not _valid_sha(expected) or canonical_hash(unsigned) != expected:
        raise ValueError("LIVE_ESCROW_HASH_MISMATCH")
    for lineage in escrow.get("lineages", []):
        verify_lineage(lineage)
    return {"status": "PASS", "escrow_sha256": expected, "escrow_status": escrow.get("status")}


def recovery_plan(escrow: dict[str, Any], *, durable_refs: Iterable[str]) -> dict[str, Any]:
    """Produce checkpoint-compatible recovery rows; never replay provider actions."""
    verify_escrow(escrow)
    durable = {str(ref) for ref in durable_refs if ref}
    required_refs: list[tuple[str, str]] = []
    for row in escrow.get("lineages", []):
        bid = str(row["block_id"])
        for field in ("request_ref", "response_ref", "audio_ref", "alignment_ref", "spend_ledger_ref"):
            ref = row.get(field)
            if ref:
                required_refs.append((f"{bid}:{field}", str(ref)))
    missing = [{"artifact_id": key, "durable_ref": ref} for key, ref in required_refs if ref not in durable]
    artifacts = [
        {
            "artifact_id": key,
            "status": "DURABLE" if ref in durable else "PENDING_WRITE",
            "durable_pointer": ref if ref in durable else None,
        }
        for key, ref in required_refs
    ]
    return {
        "status": "PASS_RECOVERABLE" if not missing else "RECOVER_VOLATILE_FIRST",
        "missing": missing,
        "checkpoint_artifacts": artifacts,
        "auto_replay_provider": False,
        "next_action": "READBACK_DURABLE_EVIDENCE" if not missing else "RECOVER_MISSING_ARTIFACTS_WITHOUT_PROVIDER_REPLAY",
    }
