#!/usr/bin/env python3
"""Universal fail-closed contracts for post-render audio repair.

This module generalizes only mechanisms proven useful in project pilots. It does not
classify artistic quality, render audio, or auto-promote project-specific facts.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable
import math

from production_control import canonical_hash

ACCEPTED_TIMING_GRADES = {"ACCEPTED_ALIGNMENT", "LIVE_TIMELINE"}
SEMANTIC_GRADES = {
    "SCRIPT_SOUND_MASTER_EXPLICIT",
    "ROOM_CONTRACT_REQUIRED",
    "DIRECTORIAL_INFERENCE",
    *ACCEPTED_TIMING_GRADES,
}
PATCHABLE_CLASSIFICATIONS = {"MISSING_ROOM_OR_AMBIENCE_SUPPORT"}
RIGHTS_PASS = {"CLEARED", "OWNED", "GENERATED_WITH_RIGHTS"}


def _finite(value: Any, field: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"INVALID_NUMBER:{field}") from exc
    if not math.isfinite(out):
        raise ValueError(f"INVALID_NUMBER:{field}")
    return out


def canonical_interval(obj: dict[str, Any]) -> dict[str, float]:
    """Normalize accepted read aliases to canonical second fields."""
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
    if start < 0 or end <= start:
        raise ValueError("INTERVAL_ORDER_INVALID")
    return {
        "start_seconds": start,
        "end_seconds": end,
        "duration_seconds": end - start,
    }


def intervals_overlap(a: dict[str, Any], b: dict[str, Any]) -> bool:
    aa, bb = canonical_interval(a), canonical_interval(b)
    return max(aa["start_seconds"], bb["start_seconds"]) < min(
        aa["end_seconds"], bb["end_seconds"]
    )


def validate_timing_evidence(record: dict[str, Any]) -> dict[str, Any]:
    grade = record.get("timing_evidence_grade") or record.get("evidence_grade")
    if grade not in ACCEPTED_TIMING_GRADES:
        raise ValueError("TIMING_EVIDENCE_NOT_ACCEPTED")
    source = record.get("timing_source") or record.get("source")
    if not source:
        raise ValueError("TIMING_SOURCE_MISSING")
    return {"status": "PASS", "grade": grade, "source": source, **canonical_interval(record)}


def validate_cue_lineage(lineage: dict[str, Any]) -> dict[str, Any]:
    blocks = lineage.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("CUE_LINEAGE_BLOCKS_MISSING")
    seen: set[str] = set()
    timed = 0
    for index, block in enumerate(blocks):
        bid = block.get("block_id")
        if not bid or str(bid) in seen:
            raise ValueError(f"CUE_LINEAGE_BLOCK_ID_INVALID:{index}")
        seen.add(str(bid))
        for field in (
            "scene_id", "room_id", "required_bed", "required_cues", "prohibited", "evidence_grade"
        ):
            if field not in block:
                raise ValueError(f"CUE_LINEAGE_FIELD_MISSING:{bid}:{field}")
        if block["evidence_grade"] not in SEMANTIC_GRADES:
            raise ValueError(f"CUE_LINEAGE_GRADE_INVALID:{bid}")
        has_time = any(k in block for k in ("start_seconds", "end_seconds", "start_s", "end_s"))
        if has_time:
            validate_timing_evidence(block)
            timed += 1
    return {
        "status": "PASS",
        "block_count": len(blocks),
        "timed_block_count": timed,
        "timing_complete": timed == len(blocks),
        "lineage_hash": canonical_hash(lineage),
    }


def protected_timing_coverage(lineage: dict[str, Any]) -> dict[str, Any]:
    """Protected semantic pauses require exact accepted timing before auto-repair."""
    unresolved: list[str] = []
    exact: list[dict[str, Any]] = []
    for block in lineage.get("blocks", []):
        if not block.get("protected_pause"):
            continue
        try:
            validate_timing_evidence(block)
            interval = canonical_interval(block)
        except ValueError:
            unresolved.append(str(block.get("block_id") or "UNKNOWN_BLOCK"))
            continue
        exact.append({"id": block.get("block_id"), **interval})
    for index, item in enumerate(lineage.get("protected_global", [])):
        try:
            validate_timing_evidence(item)
            interval = canonical_interval(item)
        except ValueError:
            unresolved.append(str(item.get("id") or f"protected_global:{index}"))
            continue
        exact.append({"id": item.get("id") or f"protected_global:{index}", **interval})
    return {
        "status": "PASS" if not unresolved else "HOLD",
        "complete": not unresolved,
        "unresolved": unresolved,
        "exact_ranges": exact,
    }


def validate_master_identity(expected_sha256: str, actual_sha256: str) -> dict[str, Any]:
    for label, value in (("EXPECTED", expected_sha256), ("ACTUAL", actual_sha256)):
        if not isinstance(value, str) or len(value) != 64:
            raise ValueError(f"MASTER_{label}_SHA256_INVALID")
    if expected_sha256.lower() != actual_sha256.lower():
        raise ValueError("MASTER_IDENTITY_MISMATCH")
    return {"status": "PASS", "sha256": actual_sha256.lower()}


def validate_asset_binding(binding: dict[str, Any]) -> dict[str, Any]:
    required = ("asset_id", "sha256", "sample_rate_hz", "channels", "gain_db", "rights_status")
    missing = [field for field in required if binding.get(field) is None]
    if missing:
        raise ValueError("ASSET_BINDING_FIELDS_MISSING:" + ",".join(missing))
    if not isinstance(binding["sha256"], str) or len(binding["sha256"]) != 64:
        raise ValueError("ASSET_SHA256_INVALID")
    if int(binding["sample_rate_hz"]) != 48000:
        raise ValueError("ASSET_SAMPLE_RATE_NOT_CANONICAL")
    if int(binding["channels"]) not in (1, 2):
        raise ValueError("ASSET_CHANNELS_UNSUPPORTED")
    gain = _finite(binding["gain_db"], "gain_db")
    if binding["rights_status"] not in RIGHTS_PASS:
        raise ValueError("ASSET_RIGHTS_NOT_CLEARED")
    return {
        "status": "PASS",
        "asset_id": binding["asset_id"],
        "asset_sha256": binding["sha256"].lower(),
        "gain_db": gain,
    }


def validate_headroom(
    *,
    source_peak_dbfs: float,
    added_signal_peak_dbfs: float,
    ceiling_dbfs: float = -1.0,
) -> dict[str, Any]:
    """Conservative worst-case coherent peak-sum guard in the amplitude domain.

    This is not a true-peak meter. It consumes measured/estimated peak evidence and
    assumes worst-case phase alignment. Silent clipping is forbidden; uncertain or
    unsafe headroom is HOLD.
    """
    source_db = _finite(source_peak_dbfs, "source_peak_dbfs")
    added_db = _finite(added_signal_peak_dbfs, "added_signal_peak_dbfs")
    ceiling = _finite(ceiling_dbfs, "ceiling_dbfs")
    if source_db > 0 or added_db > 0:
        return {
            "status": "HOLD_HEADROOM",
            "reason": "INPUT_PEAK_ABOVE_0_DBFS",
            "source_peak_dbfs": source_db,
            "added_signal_peak_dbfs": added_db,
            "ceiling_dbfs": ceiling,
        }
    source_amp = 10.0 ** (source_db / 20.0)
    added_amp = 10.0 ** (added_db / 20.0)
    predicted_amp = source_amp + added_amp
    predicted_db = 20.0 * math.log10(max(predicted_amp, 1e-12))
    status = "PASS" if predicted_db <= ceiling else "HOLD_HEADROOM"
    return {
        "status": status,
        "prediction_model": "WORST_CASE_COHERENT_AMPLITUDE_SUM",
        "predicted_peak_dbfs": predicted_db,
        "ceiling_dbfs": ceiling,
    }


@dataclass(frozen=True)
class PatchAuthorization:
    status: str
    reasons: tuple[str, ...]
    patch_id: str
    authorization_hash: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def authorize_patch(
    *,
    classification: dict[str, Any],
    lineage: dict[str, Any],
    source_master_expected_sha256: str,
    source_master_actual_sha256: str,
    asset_binding: dict[str, Any],
    patch_id: str,
    source_peak_dbfs: float,
    added_signal_peak_dbfs: float,
) -> PatchAuthorization:
    """Classifier nominates; this gate authorizes. Any missing evidence => HOLD."""
    reasons: list[str] = []
    try:
        interval = canonical_interval(classification)
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
        binding = validate_asset_binding(asset_binding)
    except ValueError as exc:
        reasons.append(str(exc))
        binding = None
    headroom = validate_headroom(
        source_peak_dbfs=source_peak_dbfs,
        added_signal_peak_dbfs=added_signal_peak_dbfs,
    )
    if headroom["status"] != "PASS":
        reasons.append("HEADROOM_NOT_PROVEN")
    coverage = protected_timing_coverage(lineage)
    if not coverage["complete"]:
        reasons.append("PROTECTED_TIMING_INCOMPLETE")

    overlapping_blocks: list[dict[str, Any]] = []
    for block in lineage.get("blocks", []):
        try:
            validate_timing_evidence(block)
            block_interval = canonical_interval(block)
        except ValueError:
            continue
        if max(interval["start_seconds"], block_interval["start_seconds"]) < min(
            interval["end_seconds"], block_interval["end_seconds"]
        ):
            overlapping_blocks.append(block)
    if not overlapping_blocks:
        reasons.append("NO_ACCEPTED_TIMED_BLOCK")
    beds = {str(block.get("required_bed")) for block in overlapping_blocks}
    if len(beds) != 1:
        reasons.append("PATCH_CROSSES_BED_DOMAINS")
    for protected in coverage["exact_ranges"]:
        if intervals_overlap(interval, protected):
            reasons.append("PATCH_OVERLAPS_PROTECTED_RANGE")
            break
    if reasons:
        return PatchAuthorization("HOLD", tuple(sorted(set(reasons))), patch_id)

    assert binding is not None
    payload = {
        "patch_id": patch_id,
        "interval": interval,
        "source_master_sha256": source_master_actual_sha256.lower(),
        "asset_id": binding["asset_id"],
        "asset_sha256": binding["asset_sha256"],
        "gain_db": binding["gain_db"],
        "bed_domain": next(iter(beds)),
        "lineage_hash": canonical_hash(lineage),
        "headroom": headroom,
    }
    return PatchAuthorization("AUTHORIZED", tuple(), patch_id, canonical_hash(payload))


def validate_human_listen_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    if evidence.get("status") not in {"PASS", "FAIL", "HOLD"}:
        raise ValueError("HUMAN_LISTEN_STATUS_INVALID")
    if evidence.get("reviewer_type") not in {"HUMAN_LISTENER", "HUMAN_ENGINEER", "HUMAN_DIRECTOR"}:
        raise ValueError("HUMAN_LISTEN_REVIEWER_INVALID")
    if not evidence.get("artifact_sha256") or not evidence.get("reviewed_at"):
        raise ValueError("HUMAN_LISTEN_PROVENANCE_MISSING")
    return {
        "status": evidence["status"],
        "reviewer_type": evidence["reviewer_type"],
        "artifact_sha256": evidence["artifact_sha256"],
        "machine_generated": False,
    }


def promotion_gate(project_results: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Universalization eligibility requires two independent real projects and human evidence."""
    qualified: list[str] = []
    holds: list[str] = []
    for result in project_results:
        project_id = str(result.get("project_id") or "UNKNOWN")
        if result.get("synthetic_only"):
            holds.append(f"{project_id}:SYNTHETIC_ONLY")
            continue
        required = (
            result.get("locked_source") is True,
            result.get("real_audio_bytes") is True,
            result.get("real_defect_caught") is True,
            result.get("selective_repair_regression_pass") is True,
            result.get("human_listen_pass") is True,
        )
        if all(required):
            qualified.append(project_id)
        else:
            holds.append(f"{project_id}:EVIDENCE_INCOMPLETE")
    unique = sorted(set(qualified))
    return {
        "status": "DOMAIN_PROMOTION_ELIGIBLE" if len(unique) >= 2 else "HOLD",
        "qualified_projects": unique,
        "holds": holds,
        "minimum_independent_projects": 2,
        "no_project_story_fact_transfer": True,
        "machine_may_change_current_authority": False,
    }
