#!/usr/bin/env python3
"""Compile a deterministic ROOM917 E01 AutoMix automation plan.

Fail-closed boundaries:
- requires a PASS AutoMix production preflight result;
- accepts only explicit operations with accepted/live timing;
- never infers missing timestamps, assets, buses, speakers, gains, or spatial moves;
- rejects any non-silence operation that overlaps protected silence;
- does not render audio and never grants release authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

PASS = "PASS_AUTOMATION_PLAN_COMPILED"
HOLD = "HOLD_AUTOMATION_PLAN"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def overlaps(a0: int, a1: int, b0: int, b1: int) -> bool:
    return max(a0, b0) < min(a1, b1)


def _list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _exact_set(value: Any, expected: Iterable[str]) -> bool:
    expected = list(expected)
    return isinstance(value, list) and len(value) == len(expected) and set(value) == set(expected)


def _required_missing(op: Dict[str, Any], required: Iterable[str]) -> List[str]:
    return [key for key in required if key not in op]


def validate_time(op: Dict[str, Any], allowed_grades: set[str]) -> List[str]:
    reasons: List[str] = []
    start = op.get("start_sample")
    end = op.get("end_sample")
    if not isinstance(start, int) or isinstance(start, bool) or start < 0:
        reasons.append("start_sample_must_be_nonnegative_integer")
    if not isinstance(end, int) or isinstance(end, bool):
        reasons.append("end_sample_must_be_integer")
    if isinstance(start, int) and not isinstance(start, bool) and isinstance(end, int) and not isinstance(end, bool):
        if end <= start:
            reasons.append("end_sample_must_be_greater_than_start_sample")
    if op.get("timing_grade") not in allowed_grades:
        reasons.append("timing_grade_must_be_ACCEPTED_ALIGNMENT_or_LIVE_TIMELINE")
    return reasons


def evaluate(contract: Dict[str, Any], preflight: Dict[str, Any], source: Dict[str, Any], *, source_sha256: str, preflight_sha256: str) -> Dict[str, Any]:
    reasons: List[str] = []
    operation_errors: List[Dict[str, Any]] = []

    required_preflight = contract.get("preflight_status_required")
    if preflight.get("status") != required_preflight:
        reasons.append("preflight_status_not_PASS_AUTOMIX_EXECUTION_READY")
    if preflight.get("render_authorized") is not True:
        reasons.append("preflight_render_not_authorized")
    if preflight.get("release_authority") is not False:
        reasons.append("preflight_release_authority_boundary_invalid")

    required_buses = _list(contract.get("required_buses"))
    if not _exact_set(source.get("buses"), required_buses):
        reasons.append("source_bus_set_does_not_match_required_exact_set")

    if source.get("timing_fixture_only") is not False:
        reasons.append("source_timing_is_fixture_or_unproven")
    if source.get("production_timestamps") is not True:
        reasons.append("source_production_timestamps_not_verified")

    operations = _list(source.get("operations"))
    if not operations:
        reasons.append("operations_missing")

    allowed_operations = contract.get("allowed_operations", {})
    allowed_grades = set(allowed_operations.get("PLACE_ASSET", {}).get("timing_grade_allowed", ["ACCEPTED_ALIGNMENT", "LIVE_TIMELINE"]))
    seen_ids: set[str] = set()
    protected: List[Tuple[int, int, str]] = []
    normalized: List[Dict[str, Any]] = []

    for index, raw in enumerate(operations):
        op_reasons: List[str] = []
        if not isinstance(raw, dict):
            operation_errors.append({"index": index, "operation_id": None, "reasons": ["operation_must_be_object"]})
            continue
        op = dict(raw)
        op_type = op.get("type")
        op_id = op.get("operation_id")
        if not isinstance(op_id, str) or not op_id.strip():
            op_reasons.append("operation_id_missing_or_invalid")
        elif op_id in seen_ids:
            op_reasons.append("operation_id_duplicate")
        else:
            seen_ids.add(op_id)

        spec = allowed_operations.get(op_type)
        if not isinstance(spec, dict):
            op_reasons.append("operation_type_not_allowed")
        else:
            missing = _required_missing(op, spec.get("required", []))
            if missing:
                op_reasons.extend([f"missing_required_field:{key}" for key in missing])
            op_reasons.extend(validate_time(op, allowed_grades))

            if op_type != "PROTECTED_SILENCE":
                bus = op.get("bus")
                if bus not in required_buses:
                    op_reasons.append("bus_not_in_required_bus_set")

            if op_type == "PLACE_ASSET":
                if op.get("binding_status") != spec.get("binding_status_required"):
                    op_reasons.append("asset_binding_status_not_PASS")
                if not SHA256_RE.match(str(op.get("source_sha256", ""))):
                    op_reasons.append("asset_source_sha256_missing_or_invalid")

            elif op_type == "DUCK_WINDOW":
                if op.get("bus") not in set(spec.get("allowed_buses", [])):
                    op_reasons.append("duck_bus_forbidden")
                gain = op.get("gain_db")
                if not isinstance(gain, (int, float)) or isinstance(gain, bool) or gain > 0:
                    op_reasons.append("duck_gain_db_must_be_numeric_and_nonpositive")
                if not isinstance(op.get("trigger"), str) or not op.get("trigger", "").strip():
                    op_reasons.append("duck_trigger_missing_or_invalid")

            elif op_type == "GAIN_ENVELOPE":
                gain = op.get("gain_db")
                if not isinstance(gain, (int, float)) or isinstance(gain, bool):
                    op_reasons.append("gain_db_must_be_numeric")

            elif op_type == "SPATIAL_EVENT":
                for field in ("pan_start", "pan_end"):
                    value = op.get(field)
                    if not isinstance(value, (int, float)) or isinstance(value, bool):
                        op_reasons.append(f"{field}_must_be_numeric")
                    elif not (spec.get("pan_min", -1.0) <= value <= spec.get("pan_max", 1.0)):
                        op_reasons.append(f"{field}_out_of_range")
                if not isinstance(op.get("speaker_or_source"), str) or not op.get("speaker_or_source", "").strip():
                    op_reasons.append("speaker_or_source_missing_or_invalid")

            elif op_type == "CATE_TELEPHONE_CHAIN":
                exact_fields = {
                    "speaker": spec.get("speaker_required"),
                    "bus": spec.get("bus_required"),
                    "hpf_hz": spec.get("hpf_hz"),
                    "lpf_hz": spec.get("lpf_hz"),
                    "reverb": spec.get("reverb"),
                    "mono_core": spec.get("mono_core"),
                    "pitch_shift": spec.get("pitch_shift"),
                    "stereo_widening": spec.get("stereo_widening"),
                    "ghost_processing": spec.get("ghost_processing"),
                }
                for field, expected in exact_fields.items():
                    if op.get(field) != expected:
                        op_reasons.append(f"cate_chain_{field}_mismatch")

            elif op_type == "PROTECTED_SILENCE":
                if op.get("post_fx_sample_exact_mask") is not spec.get("post_fx_sample_exact_mask_required", True):
                    op_reasons.append("protected_silence_requires_post_fx_sample_exact_mask")
                start = op.get("start_sample")
                end = op.get("end_sample")
                if isinstance(start, int) and isinstance(end, int) and end > start:
                    protected.append((start, end, str(op_id)))

        if op_reasons:
            operation_errors.append({"index": index, "operation_id": op_id, "reasons": op_reasons})
        normalized.append(op)

    # Protected silence is absolute in v1: no non-silence operation may overlap it.
    for index, op in enumerate(normalized):
        if op.get("type") == "PROTECTED_SILENCE":
            continue
        start = op.get("start_sample")
        end = op.get("end_sample")
        if not isinstance(start, int) or not isinstance(end, int) or end <= start:
            continue
        for p0, p1, protected_id in protected:
            if overlaps(start, end, p0, p1):
                operation_errors.append({
                    "index": index,
                    "operation_id": op.get("operation_id"),
                    "reasons": [f"overlaps_protected_silence:{protected_id}"],
                })

    if operation_errors:
        reasons.append("one_or_more_operations_failed_validation")

    if reasons:
        return {
            "schema_version": "ivdivo.room917_automix_automation_plan_result/1.0",
            "project": contract.get("project", "ROOM917"),
            "episode": contract.get("episode", "E01"),
            "status": HOLD,
            "render_authority": False,
            "release_authority": False,
            "source_sha256": source_sha256,
            "preflight_sha256": preflight_sha256,
            "operation_count": len(operations),
            "reasons": reasons,
            "operation_errors": operation_errors,
            "next": "REPAIR_ONLY_EXPLICIT_FAILED_EVIDENCE_OR_OPERATION__DO_NOT_INFER_OR_RENDER",
        }

    normalized.sort(key=lambda op: (op["start_sample"], op["end_sample"], op["operation_id"]))
    bus_counts = Counter(op.get("bus") for op in normalized if op.get("bus") in required_buses)
    return {
        "schema_version": "ivdivo.room917_automix_automation_plan_result/1.0",
        "project": contract.get("project", "ROOM917"),
        "episode": contract.get("episode", "E01"),
        "status": PASS,
        "render_authority": True,
        "release_authority": False,
        "source_sha256": source_sha256,
        "preflight_sha256": preflight_sha256,
        "sample_rate_hz": contract.get("timebase", {}).get("sample_rate_hz", 48000),
        "operation_count": len(normalized),
        "bus_counts": {bus: bus_counts.get(bus, 0) for bus in required_buses},
        "operations": normalized,
        "next": "HAND_OFF_COMPILED_PLAN_TO_RENDERER__HUMAN_P003B_STILL_REQUIRED_AFTER_RENDER",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    contract_bytes = Path(args.contract).read_bytes()
    preflight_bytes = Path(args.preflight).read_bytes()
    source_bytes = Path(args.input).read_bytes()
    contract = json.loads(contract_bytes.decode("utf-8"))
    preflight = json.loads(preflight_bytes.decode("utf-8"))
    source = json.loads(source_bytes.decode("utf-8"))
    result = evaluate(
        contract,
        preflight,
        source,
        source_sha256=sha256_bytes(source_bytes),
        preflight_sha256=sha256_bytes(preflight_bytes),
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"])
    for reason in result.get("reasons", []):
        print(f"- {reason}")
    for item in result.get("operation_errors", []):
        print(f"- operation {item.get('operation_id') or item.get('index')}: {', '.join(item.get('reasons', []))}")
    return 0 if result["status"] == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
