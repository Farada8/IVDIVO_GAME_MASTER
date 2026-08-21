#!/usr/bin/env python3
"""Exact-N paid live-lineage escrow bound to trusted external-evidence receipts.

The module never dispatches, never accepts a production take, and never replays
paid work. It binds provider auth, request/result/spend evidence, live audio and
optional alignment into one immutable lineage, then requires exact-N escrow and
transaction-recoverable readback evidence.
"""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

from external_evidence_trust import (
    validate_durable_artifact_receipt,
    validate_external_evidence,
    validate_transaction_recovery_receipt,
)

LINEAGE_SCHEMA = "ivdivo.audio.live_lineage/2.0"
ESCROW_SCHEMA = "ivdivo.audio.live_lineage_escrow/2.0"
RECOVERY_SCHEMA = "ivdivo.audio.live_lineage_recovery/2.0"
PROVIDER_STATES = {"ACCEPTED", "REJECTED", "AMBIGUOUS"}


def _plain(value: Any) -> Any:
    if is_dataclass(value):
        return _plain(asdict(value))
    if isinstance(value, Mapping):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


def _canonical(value: Any) -> bytes:
    return json.dumps(_plain(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return sha256(_canonical(value)).hexdigest()


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdefABCDEF" for ch in value)


def _parse_time(value: Any) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("DISPATCH_AT_REQUIRED")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("DISPATCH_AT_INVALID") from exc
    if parsed.tzinfo is None:
        raise ValueError("DISPATCH_AT_TIMEZONE_REQUIRED")
    return parsed


def _trusted_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    lowered = value.strip().lower()
    return not lowered.startswith(("fixture:", "fixture://", "test:", "test://", "synthetic:"))


def _durable(receipt: Any, *, kind: str) -> dict[str, Any]:
    result = validate_durable_artifact_receipt(receipt, expected_kind=kind)
    if not result.get("verified"):
        raise ValueError(f"{kind}_DURABLE_RECEIPT_INVALID:{result.get('status')}")
    return result


def _require_metadata(validation: Mapping[str, Any], expected: Mapping[str, str], prefix: str) -> None:
    metadata = dict(validation.get("metadata") or {})
    for key, value in expected.items():
        if metadata.get(key) != value:
            raise ValueError(f"{prefix}_METADATA_BINDING_MISMATCH:{key}")


def compile_lineage(record: Mapping[str, Any]) -> dict[str, Any]:
    row = _plain(record)
    for key in ("project_id", "episode_id", "block_id", "provider", "provider_state", "dispatch_at"):
        if not isinstance(row.get(key), str) or not row[key].strip():
            raise ValueError(f"{key.upper()}_REQUIRED")
    state = str(row["provider_state"]).upper()
    if state not in PROVIDER_STATES:
        raise ValueError("PROVIDER_STATE_INVALID")
    source_hash = str(row.get("source_hash") or "").lower()
    request_hash = str(row.get("request_hash") or "").lower()
    if not _is_sha256(source_hash):
        raise ValueError("SOURCE_HASH_INVALID")
    if not _is_sha256(request_hash):
        raise ValueError("REQUEST_HASH_INVALID")
    dispatch_at = _parse_time(row["dispatch_at"])

    provider = validate_external_evidence(
        "AUTH_PROVIDER",
        row.get("provider_auth_receipt"),
        expected_provider=row["provider"],
        max_age_seconds=21600,
        now=dispatch_at,
    )
    if not provider.get("verified"):
        raise ValueError(f"PROVIDER_AUTH_RECEIPT_INVALID:{provider.get('status')}")

    request = _durable(row.get("request_receipt"), kind="PROVIDER_REQUEST")
    result = _durable(row.get("provider_result_receipt"), kind="PROVIDER_RESULT")
    spend = _durable(row.get("spend_receipt"), kind="SPEND_LEDGER_ENTRY")
    if request.get("content_hash") != request_hash:
        raise ValueError("REQUEST_RECEIPT_HASH_BINDING_MISMATCH")
    _require_metadata(request, {
        "project_id": row["project_id"], "block_id": row["block_id"],
        "request_hash": request_hash, "source_hash": source_hash,
    }, "REQUEST_RECEIPT")
    _require_metadata(result, {
        "block_id": row["block_id"], "request_hash": request_hash, "provider_state": state,
    }, "PROVIDER_RESULT")
    _require_metadata(spend, {
        "block_id": row["block_id"], "request_hash": request_hash, "provider_state": state,
    }, "SPEND_RECEIPT")

    result_meta = dict(result.get("metadata") or {})
    spend_meta = dict(spend.get("metadata") or {})
    provider_request_id = result_meta.get("provider_request_id")
    if state == "ACCEPTED" and not provider_request_id:
        raise ValueError("ACCEPTED_PROVIDER_REQUEST_ID_REQUIRED")
    if state == "ACCEPTED" and not _trusted_ref(spend_meta.get("charge_ref")):
        raise ValueError("ACCEPTED_CHARGE_REF_REQUIRED")

    live = None
    alignment = None
    if state == "ACCEPTED":
        live = validate_external_evidence("LIVE_AUDIO", row.get("live_audio_receipt"))
        if not live.get("verified"):
            raise ValueError(f"LIVE_AUDIO_RECEIPT_INVALID:{live.get('status')}")
        live_durable = live.get("durable") or {}
        live_meta = dict(live_durable.get("metadata") or {})
        if live_meta.get("project_id") != row["project_id"]:
            raise ValueError("LIVE_AUDIO_PROJECT_BINDING_MISMATCH")
        if live_meta.get("request_hash") != request_hash:
            raise ValueError("LIVE_AUDIO_REQUEST_BINDING_MISMATCH")
        if live_meta.get("provider_response_hash") != result.get("content_hash"):
            raise ValueError("LIVE_AUDIO_PROVIDER_RESULT_BINDING_MISMATCH")

        if row.get("alignment_receipt") is not None:
            alignment = validate_external_evidence("REAL_ALIGNMENT", row.get("alignment_receipt"))
            if not alignment.get("verified"):
                raise ValueError(f"ALIGNMENT_RECEIPT_INVALID:{alignment.get('status')}")
            align_durable = alignment.get("durable") or {}
            align_meta = dict(align_durable.get("metadata") or {})
            if align_meta.get("audio_hash") != live_durable.get("content_hash"):
                raise ValueError("ALIGNMENT_AUDIO_BINDING_MISMATCH")
            if align_meta.get("source_hash") != source_hash:
                raise ValueError("ALIGNMENT_SOURCE_BINDING_MISMATCH")
    elif row.get("live_audio_receipt") is not None or row.get("alignment_receipt") is not None:
        raise ValueError("NONACCEPTED_LINEAGE_CANNOT_ASSERT_MEDIA")

    transaction_ids = {
        validation.get("transaction_id")
        for validation in (request, result, spend)
        if validation.get("transaction_id")
    }
    if live:
        transaction_ids.add((live.get("durable") or {}).get("transaction_id"))
    if alignment:
        transaction_ids.add((alignment.get("durable") or {}).get("transaction_id"))
    transaction_ids.discard(None)
    if len(transaction_ids) != 1:
        raise ValueError("LIVE_LINEAGE_TRANSACTION_ID_MISMATCH")
    transaction_id = next(iter(transaction_ids))

    payload = {
        "schema_version": LINEAGE_SCHEMA,
        "project_id": row["project_id"],
        "episode_id": row["episode_id"],
        "block_id": row["block_id"],
        "source_hash": source_hash,
        "request_hash": request_hash,
        "provider": row["provider"],
        "provider_state": state,
        "provider_request_id": provider_request_id,
        "dispatch_at": row["dispatch_at"],
        "transaction_id": transaction_id,
        "provider_snapshot_hash": provider.get("snapshot_hash"),
        "request_content_hash": request.get("content_hash"),
        "provider_result_content_hash": result.get("content_hash"),
        "spend_content_hash": spend.get("content_hash"),
        "live_audio_content_hash": (live.get("durable") or {}).get("content_hash") if live else None,
        "alignment_content_hash": (alignment.get("durable") or {}).get("content_hash") if alignment else None,
        "provider_auth_receipt": row.get("provider_auth_receipt"),
        "request_receipt": row.get("request_receipt"),
        "provider_result_receipt": row.get("provider_result_receipt"),
        "spend_receipt": row.get("spend_receipt"),
        "live_audio_receipt": row.get("live_audio_receipt"),
        "alignment_receipt": row.get("alignment_receipt"),
        "production_take_status": "NOT_ACCEPTED",
        "take_lock": False,
        "machine_may_replay_paid_request": False,
    }
    payload["lineage_sha256"] = canonical_hash(payload)
    return payload


def verify_lineage(lineage: Mapping[str, Any]) -> dict[str, Any]:
    row = _plain(lineage)
    if row.get("schema_version") != LINEAGE_SCHEMA:
        raise ValueError("LIVE_LINEAGE_SCHEMA_UNSUPPORTED")
    expected = row.get("lineage_sha256")
    unsigned = dict(row)
    unsigned.pop("lineage_sha256", None)
    if not _is_sha256(expected) or canonical_hash(unsigned) != str(expected).lower():
        raise ValueError("LIVE_LINEAGE_HASH_MISMATCH")
    if row.get("take_lock") is not False or row.get("production_take_status") != "NOT_ACCEPTED":
        raise ValueError("LIVE_LINEAGE_CANNOT_SELF_ACCEPT_TAKE")
    if row.get("machine_may_replay_paid_request") is not False:
        raise ValueError("LIVE_LINEAGE_REPLAY_FLAG_INVALID")

    source_fields = {
        k: v for k, v in row.items() if k not in {
            "schema_version", "provider_request_id", "transaction_id", "provider_snapshot_hash",
            "request_content_hash", "provider_result_content_hash", "spend_content_hash",
            "live_audio_content_hash", "alignment_content_hash", "production_take_status",
            "take_lock", "machine_may_replay_paid_request", "lineage_sha256",
        }
    }
    rebuilt = compile_lineage(source_fields)
    for key in (
        "provider_request_id", "transaction_id", "provider_snapshot_hash", "request_content_hash",
        "provider_result_content_hash", "spend_content_hash", "live_audio_content_hash", "alignment_content_hash",
    ):
        if rebuilt.get(key) != row.get(key):
            raise ValueError(f"LIVE_LINEAGE_REBUILD_BINDING_MISMATCH:{key}")
    return {"status": "PASS", "lineage_sha256": str(expected).lower(), "provider_state": row["provider_state"]}


def compile_exact_escrow(
    lineages: Iterable[Mapping[str, Any]], *, expected_block_ids: Iterable[str],
    expected_source_hash: str, expected_request_hashes: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    source = str(expected_source_hash).lower()
    if not _is_sha256(source):
        raise ValueError("EXPECTED_SOURCE_HASH_INVALID")
    expected = [str(block_id) for block_id in expected_block_ids]
    if not expected or len(expected) != len(set(expected)):
        raise ValueError("EXPECTED_BLOCK_IDS_INVALID")

    rows = [_plain(row) for row in lineages]
    for row in rows:
        verify_lineage(row)
    ids = [row["block_id"] for row in rows]
    requests = [row["request_hash"] for row in rows]
    expected_set = set(expected)
    duplicate_blocks = sorted({x for x in ids if ids.count(x) > 1})
    duplicate_requests = sorted({x for x in requests if requests.count(x) > 1})
    request_drift = []
    if expected_request_hashes is not None:
        for row in rows:
            expected_hash = expected_request_hashes.get(row["block_id"])
            if not _is_sha256(expected_hash) or row["request_hash"] != str(expected_hash).lower():
                request_drift.append(row["block_id"])

    issues = {
        "missing_block_ids": sorted(expected_set - set(ids)),
        "duplicate_block_ids": duplicate_blocks,
        "unknown_block_ids": sorted(set(ids) - expected_set),
        "duplicate_request_hashes": duplicate_requests,
        "nonaccepted_block_ids": sorted(row["block_id"] for row in rows if row["provider_state"] != "ACCEPTED"),
        "source_drift_block_ids": sorted(row["block_id"] for row in rows if row["source_hash"] != source),
        "request_drift_block_ids": sorted(set(request_drift)),
    }
    blocked = len(rows) != len(expected) or any(issues.values())
    ordered = sorted(rows, key=lambda r: expected.index(r["block_id"]) if r["block_id"] in expected_set else len(expected))
    payload = {
        "schema_version": ESCROW_SCHEMA,
        "status": "HOLD" if blocked else "PASS_EXACT_ESCROW",
        "expected_block_ids": expected,
        "expected_source_hash": source,
        "lineage_count": len(rows),
        "issues": issues,
        "lineages": ordered,
        "provider_acceptance_is_not_take_acceptance": True,
        "auto_retry_allowed": False,
        "machine_may_replay_paid_request": False,
    }
    payload["escrow_sha256"] = canonical_hash(payload)
    return payload


def verify_escrow(escrow: Mapping[str, Any]) -> dict[str, Any]:
    row = _plain(escrow)
    if row.get("schema_version") != ESCROW_SCHEMA:
        raise ValueError("LIVE_ESCROW_SCHEMA_UNSUPPORTED")
    expected = row.get("escrow_sha256")
    unsigned = dict(row)
    unsigned.pop("escrow_sha256", None)
    if not _is_sha256(expected) or canonical_hash(unsigned) != str(expected).lower():
        raise ValueError("LIVE_ESCROW_HASH_MISMATCH")
    for lineage in row.get("lineages", []):
        verify_lineage(lineage)
    if row.get("machine_may_replay_paid_request") is not False or row.get("auto_retry_allowed") is not False:
        raise ValueError("LIVE_ESCROW_REPLAY_POLICY_INVALID")
    return {"status": "PASS", "escrow_status": row.get("status"), "escrow_sha256": str(expected).lower()}


def lineage_recovery_hashes(lineage: Mapping[str, Any]) -> list[str]:
    row = _plain(lineage)
    verify_lineage(row)
    hashes = [
        row.get("provider_snapshot_hash"), row.get("request_content_hash"), row.get("provider_result_content_hash"),
        row.get("spend_content_hash"), row.get("live_audio_content_hash"), row.get("alignment_content_hash"),
    ]
    return sorted({str(value).lower() for value in hashes if _is_sha256(value)})


def compile_recovery_proof(escrow: Mapping[str, Any], recovery_receipts: Iterable[Any]) -> dict[str, Any]:
    """Require transaction-recoverable receipts covering every lineage content hash.

    A failed receipt remains failed. We only preserve its raw transaction identity
    so diagnostics can distinguish INVALID evidence from MISSING evidence.
    """
    row = _plain(escrow)
    verify_escrow(row)
    validations: dict[str, dict[str, Any]] = {}
    duplicate_receipt_ids: set[str] = set()

    for receipt in recovery_receipts:
        raw = _plain(receipt)
        validation = validate_transaction_recovery_receipt(raw)
        tx = validation.get("transaction_id") or raw.get("transaction_id")
        if not tx:
            validations[f"invalid:{len(validations)}"] = validation
            continue
        tx = str(tx)
        if tx in validations:
            duplicate_receipt_ids.add(tx)
        validations[tx] = validation

    missing_transactions: list[str] = []
    invalid_transactions: list[str] = []
    uncovered: dict[str, list[str]] = {}
    for lineage in row.get("lineages", []):
        tx = str(lineage.get("transaction_id"))
        validation = validations.get(tx)
        if validation is None:
            missing_transactions.append(tx)
            continue
        if not validation.get("verified"):
            invalid_transactions.append(tx)
            continue
        required = set(lineage_recovery_hashes(lineage))
        recovered = set(validation.get("recovered_content_hashes") or [])
        missing_hashes = sorted(required - recovered)
        if missing_hashes:
            uncovered[tx] = missing_hashes

    issues = {
        "missing_transaction_receipts": sorted(set(missing_transactions)),
        "invalid_transaction_receipts": sorted(set(invalid_transactions)),
        "duplicate_transaction_receipts": sorted(duplicate_receipt_ids),
        "uncovered_content_hashes": uncovered,
    }
    payload = {
        "schema_version": RECOVERY_SCHEMA,
        "status": "HOLD" if any(bool(v) for v in issues.values()) else "PASS_TRANSACTION_RECOVERABLE",
        "escrow_sha256": row["escrow_sha256"],
        "issues": issues,
        "validated_transaction_ids": sorted(tx for tx, val in validations.items() if val.get("verified")),
        "auto_replay_provider": False,
        "duplicate_provider_calls_allowed": 0,
        "duplicate_charges_allowed": 0,
    }
    payload["recovery_proof_sha256"] = canonical_hash(payload)
    return payload
