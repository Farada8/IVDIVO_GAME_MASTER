#!/usr/bin/env python3
"""Typed proof manifests for Audio Studio claims.

Prevents code/test evidence from being laundered into provider, human, live-audio,
real-alignment, durable-recovery, measured-economics or cross-project claims.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Iterable

SCHEMA_VERSION = "ivdivo.audio.proof_manifest/1.1"
EVIDENCE_CLASSES = {
    "SOURCE_AUTHORITY", "CODE_TEST", "GITHUB_CI", "AUTH_PROVIDER", "LIVE_AUDIO",
    "REAL_ALIGNMENT", "HUMAN_REVIEW", "MEASURED_ECONOMICS", "DURABLE_RECOVERY",
    "CROSS_PROJECT_REAL",
}
CLAIM_REQUIREMENTS = {
    "CODE_READY": {"CODE_TEST"},
    "CI_GREEN": {"GITHUB_CI"},
    "PROVIDER_AUTHENTICATED": {"AUTH_PROVIDER"},
    "LIVE_AUDIO_ACCEPTED_AS_PROVIDER_EVIDENCE": {"AUTH_PROVIDER", "LIVE_AUDIO"},
    "REAL_ALIGNMENT_PASS": {"LIVE_AUDIO", "REAL_ALIGNMENT"},
    "HUMAN_QUALITY_PASS": {"HUMAN_REVIEW"},
    "MEASURED_ECONOMICS_PASS": {"MEASURED_ECONOMICS"},
    "DURABLE_RECOVERY_PASS": {"DURABLE_RECOVERY"},
    "CROSS_PROJECT_PORTABILITY_PASS": {"CROSS_PROJECT_REAL"},
    "V1_RELEASE_EVIDENCE_COMPLETE": {
        "SOURCE_AUTHORITY", "GITHUB_CI", "AUTH_PROVIDER", "LIVE_AUDIO", "REAL_ALIGNMENT",
        "HUMAN_REVIEW", "MEASURED_ECONOMICS", "DURABLE_RECOVERY", "CROSS_PROJECT_REAL"
    },
}


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(obj: Any) -> str:
    return sha256(_canonical(obj)).hexdigest()


def _valid_sha(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdefABCDEF" for c in value)


def compile_proof_manifest(*, claim: str, subject: str, evidence: Iterable[dict[str, Any]]) -> dict[str, Any]:
    claim = str(claim).upper()
    if claim not in CLAIM_REQUIREMENTS:
        raise ValueError("PROOF_CLAIM_UNKNOWN")
    if not subject:
        raise ValueError("PROOF_SUBJECT_REQUIRED")
    rows: list[dict[str, Any]] = []
    classes: set[str] = set()
    for index, item in enumerate(evidence):
        cls = str(item.get("evidence_class") or "").upper()
        if cls not in EVIDENCE_CLASSES:
            raise ValueError(f"PROOF_EVIDENCE_CLASS_INVALID:{index}")
        if not item.get("ref"):
            raise ValueError(f"PROOF_EVIDENCE_REF_REQUIRED:{index}")
        sha = item.get("sha256")
        if sha is not None and not _valid_sha(sha):
            raise ValueError(f"PROOF_EVIDENCE_SHA_INVALID:{index}")
        verified = item.get("verified") is True
        row = {
            "evidence_class": cls,
            "ref": str(item["ref"]),
            "sha256": str(sha).lower() if _valid_sha(sha) else None,
            "verified": verified,
            "observed_at": item.get("observed_at"),
        }
        rows.append(row)
        if verified:
            classes.add(cls)
    required = CLAIM_REQUIREMENTS[claim]
    missing = sorted(required - classes)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "claim": claim,
        "subject": subject,
        "required_evidence_classes": sorted(required),
        "verified_evidence_classes": sorted(classes),
        "missing_evidence_classes": missing,
        "status": "PROVEN" if not missing else "HOLD_UNPROVEN",
        "evidence": rows,
        "machine_may_upgrade_claim_without_required_evidence": False,
    }
    payload["proof_sha256"] = canonical_hash(payload)
    return payload


def verify_proof_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("PROOF_SCHEMA_UNSUPPORTED")
    expected = manifest.get("proof_sha256")
    unsigned = dict(manifest)
    unsigned.pop("proof_sha256", None)
    if not _valid_sha(expected) or canonical_hash(unsigned) != expected:
        raise ValueError("PROOF_HASH_MISMATCH")
    required = set(manifest.get("required_evidence_classes") or [])
    verified = set(manifest.get("verified_evidence_classes") or [])
    actual_status = "PROVEN" if required <= verified else "HOLD_UNPROVEN"
    if manifest.get("status") != actual_status:
        raise ValueError("PROOF_STATUS_INCONSISTENT")
    return {"status": "PASS", "proof_status": actual_status, "proof_sha256": expected}
