#!/usr/bin/env python3
"""Provider/project-neutral contracts for evidence-gated post-render engineering.

This module is deliberately stricter than any single project pilot. It does not render
Audio and does not infer artistic truth from signal level alone. It validates evidence
needed before a downstream renderer may touch accepted master bytes.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Any, Iterable
import json
import math

ACCEPTED_TIMING_GRADES = {"ACCEPTED_ALIGNMENT", "LIVE_TIMELINE"}
SEMANTIC_GRADES = {
    "SCRIPT_SOUND_MASTER_EXPLICIT", "ROOM_CONTRACT_REQUIRED",
    "DIRECTORIAL_INFERENCE", *ACCEPTED_TIMING_GRADES,
}
PATCHABLE_CLASSIFICATIONS = {"MISSING_ROOM_OR_AMBIENCE_SUPPORT"}
HUMAN_LISTEN_STATES = {"PASS", "FAIL", "HOLD"}


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(obj: Any) -> str:
    return sha256(canonical_json_bytes(obj)).hexdigest()


def _finite(value: Any, field: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"INVALID_NUMBER:{field}") from exc
    if not math.isfinite(out):
        raise ValueError(f"INVALID_NUMBER:{field}")
    return out


def canonical_interval(obj: dict[str, Any]) -> dict[str, float]:
    """Normalize read-only legacy aliases to canonical seconds fields."""
    if "start_seconds" in obj:
        start = _finite(obj["start_seconds"], "start_seconds")
    elif "start_s" in obj:
        start = _finite(obj["start_s"], "start_s")
    else:
        raise ValueError("INTERVAL_START_MISSING")
    if "end_seconds" in obj:
        end = _finite(obj["end_seconds"], "end_seconds")
    elif "end_s" in obj:
        end = _finite(obj["end_s"], "end_s")
    else:
        raise ValueError("INTERVAL_END_MISSING")
    if end <= start:
        raise ValueError("INTERVAL_ORDER_INVALID")
    return {"start_seconds": start, "end_seconds": end, "duration_seconds": end - start}


def intervals_overlap(a: dict[str, Any], b: dict[str, Any]) -> bool:
    aa, bb = canonical_interval(a), canonical_interval(b)
    return max(aa["start_seconds"], bb["start_seconds"]) < min(aa["end_seconds"], bb["end_seconds"])


def validate_timing_evidence(record: dict[str, Any]) -> dict[str, Any]:
    grade = record.get("evidence_grade") or record.get("timing_evidence_grade")
    if grade not in ACCEPTED_TIMING_GRADES:
        raise ValueError("TIMING_EVIDENCE_NOT_ACCEPTED")
    interval = canonical_interval(record)
    source = record.get("source") or record.get("timing_source")
    if not source:
        raise ValueError("TIMING_SOURCE_MISSING")
    return {"status": "PASS", "grade": grade, "source": source, **interval}


def validate_cue_lineage(lineage: dict[str, Any]) -> dict[str, Any]:
    blocks = lineage.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("CUE_LINEAGE_BLOCKS_MISSING")
    seen: set[str] = set()
    timed = 0
    protected_semantic_unresolved = 0
    for index, block in enumerate(blocks):
        bid = block.get("block_id")
        if not bid or bid in seen:
            raise ValueError(f"CUE_LINEAGE_BLOCK_ID_INVALID:{index}")
        seen.add(str(bid))
        for field in ("scene_id", "room_id", "required_bed", "required_cues", "prohibited", "evidence_grade"):
            if field not in block:
                raise ValueError(f"CUE_LINEAGE_FIELD_MISSING:{bid}:{field}")
        if block["evidence_grade"] not in SEMANTIC_GRADES:
            raise ValueError(f"CUE_LINEAGE_GRADE_INVALID:{bid}")
        has_time = any(k in block for k in ("start_seconds", "end_seconds", "start_s", "end_s"))
        if has_time:
            validate_timing_evidence(block)
            timed += 1
        if block.get("protected_pause") and not has_time:
            protected_semantic_unresolved += 1
    return {
        "status": "PASS",
        "block_count": len(blocks),
        "timed_block_count": timed,
        "timing_complete": timed == len(blocks),
        "protected_semantic_unresolved": protected_semantic_unresolved,
        "lineage_hash": canonical_hash(lineage),
    }


def protected_timing_coverage(lineage: dict[str, Any]) -> dict[str, Any]:
    unresolved: list[str] = []
    exact: list[dict[str, Any]] = []
    for block in lineage.get("blocks", []):
        if not block.get("protected_pause"):
            continue
        try:
            iv = canonical_interval(block)
        except ValueError:
            unresolved.append(str(block.get("block_id")))
            continue
        exact.append({"block_id": block.get("block_id"), **iv})
    for index, item in enumerate(lineage.get("protected_global", [])):
        try:
            iv = canonical_interval(item)
        except ValueError:
            unresolved.append(str(item.get("id") or f"protected_global:{index}"))
            continue
        exact.append({"block_id": item.get("id") or f"protected_global:{index}", **iv})
    return {"status": "PASS" if not unresolved else "HOLD", "unresolved": unresolved, "exact_ranges": exact, "complete": not unresolved}


def validate_master_identity(expected_sha256: str, actual_sha256: str) -> dict[str, Any]:
    if not expected_sha256 or len(expected_sha256) != 64:
        raise ValueError("MASTER_EXPECTED_SHA256_INVALID")
    if not actual_sha256 or len(actual_sha256) != 64:
        raise ValueError("MASTER_ACTUAL_SHA256_INVALID")
    if expected_sha256.lower() != actual_sha256.lower():
        raise ValueError("MASTER_IDENTITY_MISMATCH")
    return {"status": "PASS", "sha256": actual_sha256.lower()}


def validate_asset_binding(binding: dict[str, Any]) -> dict[str, Any]:
    required = ("asset_id", "sha256", "sample_rate_hz", "channels", "gain_db", "rights_status")
    missing = [f for f in required if binding.get(f) is None]
    if missing:
        raise ValueError("ASSET_BINDING_FIELDS_MISSING:" + ",".join(missing))
    if len(str(binding["sha256"])) != 64:
        raise ValueError("ASSET_SHA256_INVALID")
    if int(binding["sample_rate_hz"]) != 48000:
        raise ValueError("ASSET_SAMPLE_RATE_NOT_CANONICAL")
    if int(binding["channels"]) not in (1, 2):
        raise ValueError("ASSET_CHANNELS_UNSUPPORTED")
    gain = _finite(binding["gain_db"], "gain_db")
    if gain > 0:
        raise ValueError("POSITIVE_PATCH_GAIN_FORBIDDEN")
    if binding["rights_status"] not in {"CLEARED", "OWNED", "GENERATED_WITH_RIGHTS"}:
        raise ValueError("ASSET_RIGHTS_NOT_CLEARED")
    return {"status": "PASS", "asset_id": binding["asset_id"], "gain_db": gain}


def validate_human_listen_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    state = evidence.get("status")
    if state not in HUMAN_LISTEN_STATES:
        raise ValueError("HUMAN_LISTEN_STATUS_INVALID")
    if evidence.get("reviewer_type") not in {"HUMAN_LISTENER", "HUMAN_ENGINEER", "HUMAN_DIRECTOR"}:
        raise ValueError("HUMAN_LISTEN_REVIEWER_INVALID")
    if not evidence.get("artifact_sha256"):
        raise ValueError("HUMAN_LISTEN_ARTIFACT_IDENTITY_MISSING")
    if not evidence.get("reviewed_at"):
        raise ValueError("HUMAN_LISTEN_TIMESTAMP_MISSING")
    return {"status": state, "artifact_sha256": evidence["artifact_sha256"], "reviewer_type": evidence["reviewer_type"]}


@dataclass(frozen=True)
class PatchAuthorization:
    status: str
    reasons: tuple[str, ...]
    patch_id: str | None = None
    authorization_hash: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def authorize_patch(*, classification: dict[str, Any], lineage: dict[str, Any], source_master_expected_sha256: str, source_master_actual_sha256: str, asset_binding: dict[str, Any], patch_id: str) -> PatchAuthorization:
    """Fail closed. Signal level is never enough to authorize modification."""
    reasons: list[str] = []
    try:
        iv = canonical_interval(classification)
    except ValueError as exc:
        return PatchAuthorization("HOLD", (str(exc),), patch_id)
    if classification.get("classification") not in PATCHABLE_CLASSIFICATIONS:
        reasons.append("CLASSIFICATION_NOT_PATCHABLE")
    if not classification.get("patch_candidate", classification.get("patch_authorized", False)):
        reasons.append("CLASSIFIER_DID_NOT_NOMINATE_PATCH")
    try:
        validate_master_identity(source_master_expected_sha256, source_master_actual_sha256)
    except ValueError as exc:
        reasons.append(str(exc))
    try:
        validate_asset_binding(asset_binding)
    except ValueError as exc:
        reasons.append(str(exc))
    coverage = protected_timing_coverage(lineage)
    if not coverage["complete"]:
        reasons.append("PROTECTED_TIMING_INCOMPLETE")
    overlapping_blocks: list[dict[str, Any]] = []
    for block in lineage.get("blocks", []):
        try:
            biv = canonical_interval(block)
            validate_timing_evidence(block)
        except ValueError:
            continue
        if max(iv["start_seconds"], biv["start_seconds"]) < min(iv["end_seconds"], biv["end_seconds"]):
            overlapping_blocks.append(block)
    if not overlapping_blocks:
        reasons.append("NO_ACCEPTED_TIMED_BLOCK")
    beds = {str(b.get("required_bed")) for b in overlapping_blocks}
    if len(beds) != 1:
        reasons.append("PATCH_CROSSES_BED_DOMAINS")
    for protected in coverage["exact_ranges"]:
        if intervals_overlap(iv, protected):
            reasons.append("PATCH_OVERLAPS_PROTECTED_RANGE")
            break
    if reasons:
        return PatchAuthorization("HOLD", tuple(sorted(set(reasons))), patch_id)
    payload = {
        "patch_id": patch_id,
        "interval": iv,
        "source_master_sha256": source_master_actual_sha256.lower(),
        "asset_id": asset_binding["asset_id"],
        "asset_sha256": asset_binding["sha256"].lower(),
        "gain_db": float(asset_binding["gain_db"]),
        "bed_domain": next(iter(beds)),
        "lineage_hash": canonical_hash(lineage),
    }
    return PatchAuthorization("AUTHORIZED", tuple(), patch_id, canonical_hash(payload))


def promotion_gate(project_results: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Domain promotion needs two independent real project results and human evidence."""
    valid: list[str] = []
    missing: list[str] = []
    for result in project_results:
        pid = str(result.get("project_id") or "UNKNOWN")
        if result.get("synthetic_only"):
            missing.append(f"{pid}:SYNTHETIC_ONLY")
            continue
        required = (
            result.get("locked_source") is True,
            result.get("real_audio_bytes") is True,
            result.get("real_defect_caught") is True,
            result.get("selective_repair_regression_pass") is True,
            result.get("human_listen_pass") is True,
        )
        if all(required):
            valid.append(pid)
        else:
            missing.append(f"{pid}:EVIDENCE_INCOMPLETE")
    independent = sorted(set(valid))
    return {"status": "DOMAIN_PROMOTED" if len(independent) >= 2 else "HOLD", "qualified_projects": independent, "missing": missing, "minimum_projects": 2, "no_story_facts_in_universal_learning": True}
