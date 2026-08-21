#!/usr/bin/env python3
"""IVDIVO Audio Studio class-specific external-evidence trust adapters.

This module closes the boundary between caller-supplied claims and admissible
provider/human/live-audio/alignment/economics/recovery evidence.  It does not
make external truth cryptographically self-proving: production callers must
still obtain receipts from trusted acquisition/submission/storage surfaces.
Its job is to ensure a bare boolean, ``verified=True`` flag, pointer, or hash
cannot satisfy an external evidence class by itself.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping
import json
import string

from provider_snapshot_contract import validate_provider_snapshot


class ReadbackStrength(str, Enum):
    POINTER_PRESENT = "POINTER_PRESENT"
    POINTER_READABLE = "POINTER_READABLE"
    CONTENT_HASH_VERIFIED = "CONTENT_HASH_VERIFIED"
    TRANSACTION_RECOVERABLE = "TRANSACTION_RECOVERABLE"


READBACK_RANK = {
    ReadbackStrength.POINTER_PRESENT.value: 1,
    ReadbackStrength.POINTER_READABLE.value: 2,
    ReadbackStrength.CONTENT_HASH_VERIFIED.value: 3,
    ReadbackStrength.TRANSACTION_RECOVERABLE.value: 4,
}

EXTERNAL_EVIDENCE_CLASSES = {
    "AUTH_PROVIDER",
    "HUMAN_REVIEW",
    "LIVE_AUDIO",
    "REAL_ALIGNMENT",
    "MEASURED_ECONOMICS",
    "DURABLE_RAW_ASSET",
    "DURABLE_RECOVERY",
    "CROSS_PROJECT_LIVE",
}

TRUSTED_REVIEWER_IDENTITY_CLASSES = {
    "FOUNDER",
    "TRUSTED_HUMAN_REVIEWER",
    "DOMAIN_REVIEWER",
    "BLIND_LISTENER",
}

HUMAN_REVIEW_SCOPES = {
    "MULTI_STATE",
    "PRONUNCIATION",
    "FATIGUE",
    "PERFORMANCE",
    "PAIR",
    "BLIND_LISTENER",
}

ARTIFACT_KIND_BY_CLASS = {
    "LIVE_AUDIO": "RAW_AUDIO",
    "REAL_ALIGNMENT": "ALIGNMENT",
    "MEASURED_ECONOMICS": "ECONOMICS_LEDGER",
    "DURABLE_RAW_ASSET": "RAW_AUDIO",
    "CROSS_PROJECT_LIVE": "CROSS_PROJECT_LIVE_REPORT",
}


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def _mapping(value: Any) -> dict[str, Any]:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in string.hexdigits for ch in value)


def _parse_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _trusted_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    lowered = value.strip().lower()
    return not lowered.startswith(("fixture:", "fixture://", "test:", "test://", "synthetic:"))


@dataclass(frozen=True)
class DurableArtifactReceipt:
    artifact_id: str
    artifact_kind: str
    storage_provider: str
    source_ref: str
    content_hash: str
    size_bytes: int
    written_at: str
    readback_at: str
    readback_hash: str
    readback_strength: str
    transaction_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReviewerAttestationReceipt:
    reviewer_ref: str
    reviewer_identity_class: str
    submission_ref: str
    submission_hash: str
    task_pack_hash: str
    artifact_hash: str
    candidate_hash: str
    decision: str
    submitted_at: str
    review_scope: str
    synthetic_fixture: bool
    durable_receipt: DurableArtifactReceipt | dict[str, Any]


@dataclass(frozen=True)
class TransactionRecoveryReceipt:
    transaction_id: str
    recovered_at: str
    recovered_content_hashes: list[str]
    durable_readback_strength: str
    duplicate_provider_calls: int
    duplicate_charges: int
    unresolved_ambiguities: int
    recovery_manifest_ref: str
    recovery_manifest_hash: str
    synthetic_fixture: bool = False


def validate_durable_artifact_receipt(
    receipt: DurableArtifactReceipt | Mapping[str, Any] | None,
    *,
    expected_kind: str | None = None,
    minimum_strength: str = ReadbackStrength.CONTENT_HASH_VERIFIED.value,
) -> dict[str, Any]:
    row = _mapping(receipt)
    if not row:
        return {"status": "HOLD_DURABLE_RECEIPT_MISSING", "verified": False}
    if not row.get("artifact_id") or not row.get("storage_provider") or not _trusted_ref(row.get("source_ref")):
        return {"status": "FAIL_DURABLE_IDENTITY", "verified": False}
    if expected_kind and row.get("artifact_kind") != expected_kind:
        return {
            "status": "FAIL_ARTIFACT_KIND",
            "verified": False,
            "expected_kind": expected_kind,
            "actual_kind": row.get("artifact_kind"),
        }
    if not _is_sha256(row.get("content_hash")) or not _is_sha256(row.get("readback_hash")):
        return {"status": "FAIL_DURABLE_HASH_SHAPE", "verified": False}
    if row["content_hash"].lower() != row["readback_hash"].lower():
        return {"status": "FAIL_DURABLE_READBACK_HASH_DRIFT", "verified": False}
    if not isinstance(row.get("size_bytes"), int) or row["size_bytes"] <= 0:
        return {"status": "FAIL_DURABLE_SIZE", "verified": False}
    written_at = _parse_utc(row.get("written_at"))
    readback_at = _parse_utc(row.get("readback_at"))
    if written_at is None or readback_at is None or readback_at < written_at:
        return {"status": "FAIL_DURABLE_TIMESTAMPS", "verified": False}
    actual_rank = READBACK_RANK.get(str(row.get("readback_strength")), 0)
    required_rank = READBACK_RANK.get(str(minimum_strength), 0)
    if required_rank == 0:
        raise ValueError("UNKNOWN_MINIMUM_READBACK_STRENGTH")
    if actual_rank < required_rank:
        return {
            "status": "HOLD_DURABLE_READBACK_STRENGTH",
            "verified": False,
            "actual": row.get("readback_strength"),
            "required": minimum_strength,
        }
    return {
        "status": "PASS",
        "verified": True,
        "artifact_id": row["artifact_id"],
        "artifact_kind": row.get("artifact_kind"),
        "content_hash": row["content_hash"].lower(),
        "source_ref": row["source_ref"],
        "readback_strength": row["readback_strength"],
        "transaction_id": row.get("transaction_id"),
        "metadata": dict(row.get("metadata") or {}),
    }


def validate_reviewer_attestation_receipt(
    receipt: ReviewerAttestationReceipt | Mapping[str, Any] | None,
    *,
    expected_scope: str | None = None,
) -> dict[str, Any]:
    row = _mapping(receipt)
    if not row:
        return {"status": "HOLD_HUMAN_ATTESTATION_MISSING", "verified": False}
    if row.get("synthetic_fixture") is not False:
        return {"status": "FAIL_SYNTHETIC_HUMAN_EVIDENCE", "verified": False}
    if row.get("reviewer_identity_class") not in TRUSTED_REVIEWER_IDENTITY_CLASSES:
        return {"status": "FAIL_REVIEWER_IDENTITY_CLASS", "verified": False}
    if not _trusted_ref(row.get("reviewer_ref")) or not _trusted_ref(row.get("submission_ref")):
        return {"status": "FAIL_REVIEWER_SOURCE_REF", "verified": False}
    if row.get("review_scope") not in HUMAN_REVIEW_SCOPES:
        return {"status": "FAIL_REVIEW_SCOPE", "verified": False}
    if expected_scope and row.get("review_scope") != expected_scope:
        return {
            "status": "FAIL_REVIEW_SCOPE_MISMATCH",
            "verified": False,
            "expected_scope": expected_scope,
            "actual_scope": row.get("review_scope"),
        }
    for key in ("submission_hash", "task_pack_hash", "artifact_hash", "candidate_hash"):
        if not _is_sha256(row.get(key)):
            return {"status": f"FAIL_{key.upper()}_SHAPE", "verified": False}
    if row.get("decision") not in {"PASS", "FAIL", "HOLD"}:
        return {"status": "FAIL_REVIEW_DECISION", "verified": False}
    if _parse_utc(row.get("submitted_at")) is None:
        return {"status": "FAIL_REVIEW_TIMESTAMP", "verified": False}
    durable = validate_durable_artifact_receipt(row.get("durable_receipt"), expected_kind="HUMAN_ATTESTATION")
    if not durable.get("verified"):
        return {"status": "HOLD_HUMAN_ATTESTATION_DURABILITY", "verified": False, "durable": durable}
    if durable.get("content_hash") != row["submission_hash"].lower():
        return {"status": "FAIL_HUMAN_SUBMISSION_HASH_BINDING", "verified": False}
    return {
        "status": "PASS" if row["decision"] == "PASS" else f"REVIEW_{row['decision']}",
        "verified": row["decision"] == "PASS",
        "review_scope": row["review_scope"],
        "reviewer_identity_class": row["reviewer_identity_class"],
        "submission_hash": row["submission_hash"].lower(),
        "artifact_hash": row["artifact_hash"].lower(),
        "candidate_hash": row["candidate_hash"].lower(),
        "durable": durable,
    }


def validate_transaction_recovery_receipt(
    receipt: TransactionRecoveryReceipt | Mapping[str, Any] | None,
) -> dict[str, Any]:
    row = _mapping(receipt)
    if not row:
        return {"status": "HOLD_RECOVERY_RECEIPT_MISSING", "verified": False}
    if row.get("synthetic_fixture") is not False:
        return {"status": "FAIL_SYNTHETIC_RECOVERY_EVIDENCE", "verified": False}
    if not row.get("transaction_id") or not _trusted_ref(row.get("recovery_manifest_ref")):
        return {"status": "FAIL_RECOVERY_IDENTITY", "verified": False}
    if _parse_utc(row.get("recovered_at")) is None:
        return {"status": "FAIL_RECOVERY_TIMESTAMP", "verified": False}
    hashes = row.get("recovered_content_hashes")
    if not isinstance(hashes, list) or not hashes or any(not _is_sha256(value) for value in hashes):
        return {"status": "FAIL_RECOVERY_CONTENT_HASHES", "verified": False}
    if not _is_sha256(row.get("recovery_manifest_hash")):
        return {"status": "FAIL_RECOVERY_MANIFEST_HASH", "verified": False}
    if row.get("durable_readback_strength") != ReadbackStrength.TRANSACTION_RECOVERABLE.value:
        return {"status": "HOLD_RECOVERY_NOT_TRANSACTION_RECOVERABLE", "verified": False}
    for key in ("duplicate_provider_calls", "duplicate_charges", "unresolved_ambiguities"):
        if row.get(key) != 0:
            return {"status": f"FAIL_RECOVERY_{key.upper()}", "verified": False, "actual": row.get(key)}
    return {
        "status": "PASS",
        "verified": True,
        "transaction_id": row["transaction_id"],
        "recovered_content_hashes": sorted(value.lower() for value in hashes),
        "recovery_manifest_hash": row["recovery_manifest_hash"].lower(),
    }


def validate_provider_auth_receipt(
    payload: Mapping[str, Any] | None,
    *,
    expected_provider: str | None = None,
    max_age_seconds: float = 21600,
    now: datetime | None = None,
) -> dict[str, Any]:
    row = _mapping(payload)
    snapshot = row.get("snapshot")
    if not isinstance(snapshot, dict):
        return {"status": "HOLD_PROVIDER_SNAPSHOT_MISSING", "verified": False}
    validated = validate_provider_snapshot(
        snapshot,
        expected_provider=expected_provider,
        max_age_seconds=max_age_seconds,
        now=now,
    )
    if not validated.get("verified"):
        return {"status": "HOLD_PROVIDER_SNAPSHOT_INVALID", "verified": False, "provider": validated}
    durable = validate_durable_artifact_receipt(row.get("durable_receipt"), expected_kind="PROVIDER_SNAPSHOT")
    if not durable.get("verified"):
        return {"status": "HOLD_PROVIDER_SNAPSHOT_NOT_DURABLE", "verified": False, "durable": durable}
    if durable.get("content_hash") != validated.get("snapshot_hash"):
        return {"status": "FAIL_PROVIDER_SNAPSHOT_DURABLE_HASH_BINDING", "verified": False}
    return {
        "status": "PASS",
        "verified": True,
        "provider": validated.get("provider"),
        "snapshot_hash": validated.get("snapshot_hash"),
        "source_ref": durable.get("source_ref"),
        "captured_at": validated.get("captured_at"),
        "readback_strength": durable.get("readback_strength"),
    }


def _validate_artifact_class(evidence_class: str, payload: Any) -> dict[str, Any]:
    expected_kind = ARTIFACT_KIND_BY_CLASS[evidence_class]
    durable = validate_durable_artifact_receipt(payload, expected_kind=expected_kind)
    if not durable.get("verified"):
        return durable
    metadata = durable.get("metadata", {})
    if evidence_class == "LIVE_AUDIO":
        required = ("project_id", "request_hash", "provider_response_hash")
        if any(not metadata.get(key) for key in required) or any(
            not _is_sha256(metadata.get(key)) for key in ("request_hash", "provider_response_hash")
        ):
            return {"status": "FAIL_LIVE_AUDIO_LINEAGE", "verified": False}
    elif evidence_class == "REAL_ALIGNMENT":
        if not _is_sha256(metadata.get("audio_hash")) or not _is_sha256(metadata.get("source_hash")):
            return {"status": "FAIL_ALIGNMENT_LINEAGE", "verified": False}
        if metadata.get("coverage_complete") is not True:
            return {"status": "HOLD_ALIGNMENT_COVERAGE", "verified": False}
    elif evidence_class == "MEASURED_ECONOMICS":
        if metadata.get("measured") is not True:
            return {"status": "HOLD_ECONOMICS_NOT_MEASURED", "verified": False}
        charges = metadata.get("provider_charge_refs")
        if not isinstance(charges, list) or not charges or not all(_trusted_ref(ref) for ref in charges):
            return {"status": "HOLD_ECONOMICS_CHARGE_PROVENANCE", "verified": False}
        if not _trusted_ref(metadata.get("manual_minutes_source_ref")):
            return {"status": "HOLD_ECONOMICS_HUMAN_TIME_PROVENANCE", "verified": False}
    elif evidence_class == "CROSS_PROJECT_LIVE":
        projects = metadata.get("project_ids")
        hashes = metadata.get("live_evidence_hashes")
        if not isinstance(projects, list) or len(set(projects)) < 2:
            return {"status": "HOLD_CROSS_PROJECT_REPLICATION", "verified": False}
        if not isinstance(hashes, list) or len(hashes) < 2 or any(not _is_sha256(value) for value in hashes):
            return {"status": "HOLD_CROSS_PROJECT_LIVE_HASHES", "verified": False}
    return {"status": "PASS", "verified": True, "durable": durable}


def validate_external_evidence(
    evidence_class: str,
    payload: Any,
    *,
    expected_scope: str | None = None,
    expected_provider: str | None = None,
    max_age_seconds: float = 21600,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Validate one evidence class from its original receipt shape.

    A bare ``True``, ``verified=True`` dictionary or content pointer is never
    sufficient because every external class is routed to a class-specific
    validator here.
    """
    if evidence_class not in EXTERNAL_EVIDENCE_CLASSES:
        return {"status": "FAIL_UNKNOWN_EVIDENCE_CLASS", "verified": False}
    if payload is True or payload is False or payload is None:
        return {"status": "HOLD_CLASS_SPECIFIC_RECEIPT_REQUIRED", "verified": False}
    if evidence_class == "AUTH_PROVIDER":
        result = validate_provider_auth_receipt(
            payload,
            expected_provider=expected_provider,
            max_age_seconds=max_age_seconds,
            now=now,
        )
    elif evidence_class == "HUMAN_REVIEW":
        result = validate_reviewer_attestation_receipt(payload, expected_scope=expected_scope)
    elif evidence_class == "DURABLE_RECOVERY":
        result = validate_transaction_recovery_receipt(payload)
    else:
        result = _validate_artifact_class(evidence_class, payload)
    return {
        **result,
        "evidence_class": evidence_class,
        "expected_scope": expected_scope,
        "claim_source_validated": bool(result.get("verified")),
    }


def build_external_evidence_binding(
    evidence_class: str,
    payload: Any,
    *,
    claim_scope: str,
    expected_scope: str | None = None,
    expected_provider: str | None = None,
    max_age_seconds: float = 21600,
    now: datetime | None = None,
) -> dict[str, Any]:
    validation = validate_external_evidence(
        evidence_class,
        payload,
        expected_scope=expected_scope,
        expected_provider=expected_provider,
        max_age_seconds=max_age_seconds,
        now=now,
    )
    if not validation.get("verified"):
        return {
            "schema": "ivdivo.external_evidence_binding/1.0",
            "status": "HOLD",
            "evidence_class": evidence_class,
            "claim_scope": claim_scope,
            "validation": validation,
            "binding_hash": None,
        }
    binding = {
        "schema": "ivdivo.external_evidence_binding/1.0",
        "status": "PASS",
        "evidence_class": evidence_class,
        "claim_scope": claim_scope,
        "validation": validation,
        "validator": "ivdivo.audio.external_evidence_trust/1.0",
    }
    binding["binding_hash"] = canonical_hash(binding)
    return binding
