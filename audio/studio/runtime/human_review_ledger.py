#!/usr/bin/env python3
"""Trust-anchored append-only human review ledger.

This module preserves the useful Wave8 review-history mechanism without reviving
its old self-asserted evidence model. Every stored review must first pass the
merged ``external_evidence_trust`` human-attestation validator. PASS/FAIL/HOLD
reviews are all retained as history; only PASS coverage can create eligibility,
and the machine never performs an artistic/voice lock.
"""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from external_evidence_trust import validate_reviewer_attestation_receipt

RECORD_SCHEMA = "ivdivo.audio.human_review_record/2.0"
LEDGER_SCHEMA = "ivdivo.audio.human_review_ledger/2.0"
ADMISSIBLE_ATTESTATION_STATUSES = {"PASS", "REVIEW_FAIL", "REVIEW_HOLD"}


def _mapping(value: Any) -> dict[str, Any]:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return sha256(_canonical(value)).hexdigest()


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdefABCDEF" for ch in value)


def compile_review_record(receipt: Any, *, expected_scope: str | None = None) -> dict[str, Any]:
    """Compile one externally attested human review into immutable ledger form.

    Negative human decisions are valid history, so a structurally valid
    ``REVIEW_FAIL`` or ``REVIEW_HOLD`` is admitted even though it does not prove
    a positive quality claim.
    """
    row = _mapping(receipt)
    validation = validate_reviewer_attestation_receipt(row, expected_scope=expected_scope)
    if validation.get("status") not in ADMISSIBLE_ATTESTATION_STATUSES:
        raise ValueError(f"HUMAN_ATTESTATION_INVALID:{validation.get('status')}")

    decision = str(row.get("decision") or "").upper()
    scope = str(row.get("review_scope") or "").upper()
    candidate_hash = str(row.get("candidate_hash") or "").lower()
    artifact_hash = str(row.get("artifact_hash") or "").lower()
    submission_hash = str(row.get("submission_hash") or "").lower()
    if decision not in {"PASS", "FAIL", "HOLD"}:
        raise ValueError("HUMAN_REVIEW_DECISION_INVALID")
    if not scope:
        raise ValueError("HUMAN_REVIEW_SCOPE_REQUIRED")
    for name, value in (
        ("candidate_hash", candidate_hash),
        ("artifact_hash", artifact_hash),
        ("submission_hash", submission_hash),
    ):
        if not _is_sha256(value):
            raise ValueError(f"HUMAN_REVIEW_{name.upper()}_INVALID")

    payload = {
        "schema_version": RECORD_SCHEMA,
        "review_scope": scope,
        "decision": decision,
        "candidate_hash": candidate_hash,
        "artifact_hash": artifact_hash,
        "submission_hash": submission_hash,
        "reviewer_ref": row.get("reviewer_ref"),
        "reviewer_identity_class": row.get("reviewer_identity_class"),
        "submission_ref": row.get("submission_ref"),
        "submitted_at": row.get("submitted_at"),
        "durable_content_hash": (validation.get("durable") or {}).get("content_hash"),
        "attestation_receipt": row,
        "machine_generated": False,
    }
    payload["record_sha256"] = canonical_hash(payload)
    return payload


def verify_review_record(record: Mapping[str, Any]) -> dict[str, Any]:
    row = dict(record)
    if row.get("schema_version") != RECORD_SCHEMA:
        raise ValueError("HUMAN_REVIEW_RECORD_SCHEMA_UNSUPPORTED")
    expected = row.get("record_sha256")
    unsigned = dict(row)
    unsigned.pop("record_sha256", None)
    if not _is_sha256(expected) or canonical_hash(unsigned) != str(expected).lower():
        raise ValueError("HUMAN_REVIEW_RECORD_HASH_MISMATCH")
    if row.get("machine_generated") is not False:
        raise ValueError("HUMAN_REVIEW_RECORD_MACHINE_FLAG_INVALID")

    receipt = _mapping(row.get("attestation_receipt"))
    validation = validate_reviewer_attestation_receipt(receipt, expected_scope=row.get("review_scope"))
    if validation.get("status") not in ADMISSIBLE_ATTESTATION_STATUSES:
        raise ValueError(f"HUMAN_REVIEW_ATTESTATION_REVALIDATION_FAILED:{validation.get('status')}")
    bindings = {
        "decision": str(receipt.get("decision") or "").upper(),
        "candidate_hash": str(receipt.get("candidate_hash") or "").lower(),
        "artifact_hash": str(receipt.get("artifact_hash") or "").lower(),
        "submission_hash": str(receipt.get("submission_hash") or "").lower(),
        "reviewer_ref": receipt.get("reviewer_ref"),
        "reviewer_identity_class": receipt.get("reviewer_identity_class"),
        "submission_ref": receipt.get("submission_ref"),
        "submitted_at": receipt.get("submitted_at"),
    }
    for key, value in bindings.items():
        if row.get(key) != value:
            raise ValueError(f"HUMAN_REVIEW_RECEIPT_BINDING_MISMATCH:{key}")
    if row.get("durable_content_hash") != (validation.get("durable") or {}).get("content_hash"):
        raise ValueError("HUMAN_REVIEW_DURABLE_HASH_BINDING_MISMATCH")
    return {"status": "PASS", "record_sha256": str(expected).lower(), "decision": row["decision"]}


class HumanReviewLedger:
    """Small append-only hash-chain ledger with atomic local replacement writes."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.data = {"schema_version": LEDGER_SCHEMA, "entries": []}
        if self.data.get("schema_version") != LEDGER_SCHEMA:
            raise ValueError("HUMAN_REVIEW_LEDGER_SCHEMA_UNSUPPORTED")
        self.verify_chain()

    def verify_chain(self) -> dict[str, Any]:
        previous: str | None = None
        for index, entry in enumerate(self.data.get("entries", [])):
            verify_review_record(entry.get("record") or {})
            if entry.get("prev_entry_sha256") != previous:
                raise ValueError(f"HUMAN_REVIEW_LEDGER_CHAIN_BROKEN:{index}")
            unsigned = {"prev_entry_sha256": previous, "record": entry["record"]}
            if canonical_hash(unsigned) != entry.get("entry_sha256"):
                raise ValueError(f"HUMAN_REVIEW_LEDGER_ENTRY_HASH_MISMATCH:{index}")
            previous = entry["entry_sha256"]
        return {"status": "PASS", "entries": len(self.data.get("entries", [])), "head_sha256": previous}

    def append(self, record: Mapping[str, Any]) -> dict[str, Any]:
        row = dict(record)
        verify_review_record(row)
        record_hash = row["record_sha256"]
        if any(entry["record"]["record_sha256"] == record_hash for entry in self.data["entries"]):
            return {"status": "REUSE_EXISTING_RECORD", "record_sha256": record_hash}
        previous = self.data["entries"][-1]["entry_sha256"] if self.data["entries"] else None
        unsigned = {"prev_entry_sha256": previous, "record": row}
        entry = {**unsigned, "entry_sha256": canonical_hash(unsigned)}
        self.data["entries"].append(entry)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(self.path)
        return {"status": "APPENDED", "entry_sha256": entry["entry_sha256"], "record_sha256": record_hash}

    def records(self) -> list[dict[str, Any]]:
        self.verify_chain()
        return [dict(entry["record"]) for entry in self.data.get("entries", [])]


def candidate_review_state(
    records: Iterable[Mapping[str, Any]], *, candidate_hash: str, required_scopes: Iterable[str]
) -> dict[str, Any]:
    """Aggregate one exact candidate's attested history without auto-locking."""
    candidate = str(candidate_hash).lower()
    if not _is_sha256(candidate):
        raise ValueError("CANDIDATE_HASH_INVALID")
    scopes = {str(scope).upper() for scope in required_scopes}
    if not scopes:
        raise ValueError("REQUIRED_REVIEW_SCOPES_EMPTY")

    decisions: dict[str, set[str]] = {scope: set() for scope in scopes}
    ignored_other_candidates = 0
    for record in records:
        row = dict(record)
        verify_review_record(row)
        if row.get("candidate_hash") != candidate:
            ignored_other_candidates += 1
            continue
        scope = str(row.get("review_scope") or "").upper()
        if scope in decisions:
            decisions[scope].add(str(row.get("decision") or "").upper())

    covered: list[str] = []
    missing: list[str] = []
    conflicts: list[str] = []
    failed: list[str] = []
    held: list[str] = []
    for scope in sorted(scopes):
        values = decisions[scope]
        if "PASS" in values and "FAIL" in values:
            conflicts.append(scope)
        elif "FAIL" in values:
            failed.append(scope)
        elif "PASS" in values:
            covered.append(scope)
        elif "HOLD" in values:
            held.append(scope)
        else:
            missing.append(scope)

    if failed:
        status = "FAIL_HUMAN_REVIEW"
    elif conflicts:
        status = "HOLD_CONFLICT"
    elif missing or held:
        status = "HOLD"
    else:
        status = "ELIGIBLE_FOR_HUMAN_LOCK_DECISION"
    return {
        "status": status,
        "candidate_hash": candidate,
        "required_scopes": sorted(scopes),
        "covered_pass_scopes": covered,
        "missing_scopes": missing,
        "held_scopes": held,
        "conflicting_scopes": conflicts,
        "failed_scopes": failed,
        "ignored_other_candidate_records": ignored_other_candidates,
        "machine_may_auto_lock": False,
        "voice_lock": False,
        "next_authority": "FOUNDER_OR_AUTHORIZED_HUMAN_LOCK_DECISION" if status == "ELIGIBLE_FOR_HUMAN_LOCK_DECISION" else None,
    }
