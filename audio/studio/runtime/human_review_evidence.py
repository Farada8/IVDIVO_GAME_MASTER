#!/usr/bin/env python3
"""Append-only human review evidence ledger and lock-eligibility firewall.

The machine may validate provenance and evidence coverage. It may never convert review
signals into an artistic/voice lock automatically. Final lock remains Founder/human.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "ivdivo.audio.human_review_event/1.0"
LEDGER_VERSION = "ivdivo.audio.human_review_ledger/1.0"
REVIEWER_TYPES = {
    "HUMAN_LISTENER", "HUMAN_DIRECTOR", "LANGUAGE_REVIEWER", "AUDIO_ENGINEER", "FOUNDER"
}
DECISIONS = {"PASS", "FAIL", "HOLD"}
EVIDENCE_FAMILIES = {"PRONUNCIATION", "MULTI_STATE", "PAIR", "FATIGUE", "BLIND_LISTEN", "TECHNICAL_QC"}


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(obj: Any) -> str:
    return sha256(_canonical(obj)).hexdigest()


def _valid_sha(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdefABCDEF" for c in value)


@dataclass(frozen=True)
class ReviewEvent:
    candidate_id: str
    role_id: str
    evidence_family: str
    reviewer_type: str
    reviewer_ref: str
    artifact_sha256: str
    source_sha256: str
    reviewed_at: str
    decision: str
    scores: dict[str, float]
    hard_fails: tuple[str, ...] = ()
    notes_digest: str | None = None


def compile_event(event: ReviewEvent) -> dict[str, Any]:
    if not event.candidate_id or not event.role_id or not event.reviewer_ref or not event.reviewed_at:
        raise ValueError("HUMAN_REVIEW_IDENTITY_FIELDS_REQUIRED")
    family = event.evidence_family.upper()
    if family not in EVIDENCE_FAMILIES:
        raise ValueError("HUMAN_REVIEW_EVIDENCE_FAMILY_INVALID")
    reviewer = event.reviewer_type.upper()
    if reviewer not in REVIEWER_TYPES:
        raise ValueError("HUMAN_REVIEWER_TYPE_INVALID")
    decision = event.decision.upper()
    if decision not in DECISIONS:
        raise ValueError("HUMAN_REVIEW_DECISION_INVALID")
    if not _valid_sha(event.artifact_sha256) or not _valid_sha(event.source_sha256):
        raise ValueError("HUMAN_REVIEW_SHA256_INVALID")
    scores = {str(k): float(v) for k, v in sorted((event.scores or {}).items())}
    if any(v < 0 or v > 5 for v in scores.values()):
        raise ValueError("HUMAN_REVIEW_SCORE_OUT_OF_RANGE")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": event.candidate_id,
        "role_id": event.role_id,
        "evidence_family": family,
        "reviewer_type": reviewer,
        "reviewer_ref": event.reviewer_ref,
        "artifact_sha256": event.artifact_sha256.lower(),
        "source_sha256": event.source_sha256.lower(),
        "reviewed_at": event.reviewed_at,
        "decision": decision,
        "scores": scores,
        "hard_fails": sorted(set(event.hard_fails)),
        "notes_digest": event.notes_digest,
        "machine_generated": False,
    }
    payload["event_sha256"] = canonical_hash(payload)
    return payload


def verify_event(event: dict[str, Any]) -> dict[str, Any]:
    if event.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("HUMAN_REVIEW_EVENT_SCHEMA_UNSUPPORTED")
    expected = event.get("event_sha256")
    unsigned = dict(event)
    unsigned.pop("event_sha256", None)
    if not _valid_sha(expected) or canonical_hash(unsigned) != expected:
        raise ValueError("HUMAN_REVIEW_EVENT_HASH_MISMATCH")
    if event.get("machine_generated") is not False:
        raise ValueError("HUMAN_REVIEW_CANNOT_BE_MACHINE_GENERATED")
    return {"status": "PASS", "event_sha256": expected}


class HumanReviewLedger:
    """Small append-only hash-chain ledger. Existing entries are never rewritten."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.data = {"schema_version": LEDGER_VERSION, "events": []}
        if self.data.get("schema_version") != LEDGER_VERSION:
            raise ValueError("HUMAN_REVIEW_LEDGER_SCHEMA_UNSUPPORTED")
        self.verify_chain()

    def verify_chain(self) -> dict[str, Any]:
        prev: str | None = None
        for index, row in enumerate(self.data.get("events", [])):
            verify_event(row["event"])
            if row.get("prev_entry_sha256") != prev:
                raise ValueError(f"HUMAN_REVIEW_LEDGER_CHAIN_BROKEN:{index}")
            unsigned = {"prev_entry_sha256": prev, "event": row["event"]}
            if canonical_hash(unsigned) != row.get("entry_sha256"):
                raise ValueError(f"HUMAN_REVIEW_LEDGER_ENTRY_HASH_MISMATCH:{index}")
            prev = row["entry_sha256"]
        return {"status": "PASS", "entries": len(self.data.get("events", [])), "head_sha256": prev}

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        verify_event(event)
        if any(row["event"]["event_sha256"] == event["event_sha256"] for row in self.data["events"]):
            return {"status": "REUSE_EXISTING_EVENT", "event_sha256": event["event_sha256"]}
        prev = self.data["events"][-1]["entry_sha256"] if self.data["events"] else None
        unsigned = {"prev_entry_sha256": prev, "event": event}
        row = {**unsigned, "entry_sha256": canonical_hash(unsigned)}
        self.data["events"].append(row)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"status": "APPENDED", "entry_sha256": row["entry_sha256"], "event_sha256": event["event_sha256"]}


def lock_eligibility(
    events: Iterable[dict[str, Any]], *, candidate_id: str, role_id: str,
    required_families: Iterable[str], pair_required: bool = False,
) -> dict[str, Any]:
    """Validate evidence coverage; return eligibility for human lock decision only."""
    relevant: list[dict[str, Any]] = []
    for event in events:
        verify_event(event)
        if event.get("candidate_id") == candidate_id and event.get("role_id") == role_id:
            relevant.append(event)
    families = {str(f).upper() for f in required_families}
    if pair_required:
        families.add("PAIR")
    covered_pass: set[str] = set()
    hard_fails: set[str] = set()
    hold_or_fail: set[str] = set()
    for event in relevant:
        family = str(event.get("evidence_family")).upper()
        hard_fails.update(event.get("hard_fails") or [])
        if event.get("decision") == "PASS" and not event.get("hard_fails"):
            covered_pass.add(family)
        elif family in families:
            hold_or_fail.add(family)
    missing = sorted(families - covered_pass)
    if hard_fails:
        status = "FAIL_HARD"
    elif missing or hold_or_fail:
        status = "HOLD"
    else:
        status = "ELIGIBLE_FOR_HUMAN_LOCK_DECISION"
    return {
        "status": status,
        "candidate_id": candidate_id,
        "role_id": role_id,
        "required_families": sorted(families),
        "covered_pass_families": sorted(covered_pass),
        "missing": missing,
        "hard_fails": sorted(hard_fails),
        "machine_may_auto_lock": False,
        "voice_lock": False,
        "next_authority": "FOUNDER_OR_AUTHORIZED_HUMAN_LOCK_DECISION" if status == "ELIGIBLE_FOR_HUMAN_LOCK_DECISION" else None,
    }
