#!/usr/bin/env python3
"""ROOM917 E01 render-manifest compiler and fail-closed machine receipt QC.

This module never renders audio and never grants release authority. It bridges a
passed automation plan to a deterministic output manifest, then validates a
receipt produced from real render bytes before the human P003B listener gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List

MANIFEST_PASS = "PASS_RENDER_MANIFEST_COMPILED"
MANIFEST_HOLD = "HOLD_RENDER_MANIFEST"
QC_PASS = "PASS_RENDER_MACHINE_QC"
QC_HOLD = "HOLD_RENDER_MACHINE_QC"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_bytes(path: str) -> tuple[bytes, Dict[str, Any]]:
    data = Path(path).read_bytes()
    return data, json.loads(data.decode("utf-8"))


def compile_manifest(contract: Dict[str, Any], plan: Dict[str, Any], source_master: Dict[str, Any], *, plan_sha256: str, output_root: str) -> Dict[str, Any]:
    reasons: List[str] = []
    plan_contract = contract.get("compiled_plan", {})
    source_contract = contract.get("source_master", {})

    if plan.get("status") != plan_contract.get("status_required"):
        reasons.append("compiled_plan_status_not_pass")
    if plan.get("render_authority") is not plan_contract.get("render_authority_required", True):
        reasons.append("compiled_plan_render_authority_missing")
    if plan.get("release_authority") is not plan_contract.get("release_authority_required", False):
        reasons.append("compiled_plan_release_boundary_invalid")
    if not SHA256_RE.match(plan_sha256):
        reasons.append("compiled_plan_sha256_invalid")

    expected_master_sha = source_contract.get("sha256_required")
    if source_master.get("sha256") != expected_master_sha:
        reasons.append("source_master_sha256_mismatch")
    if source_master.get("exact_bytes_verified") is not source_contract.get("exact_bytes_verified_required", True):
        reasons.append("source_master_exact_bytes_not_verified")
    if not isinstance(output_root, str) or not output_root.strip():
        reasons.append("output_root_missing")

    if reasons:
        return {
            "schema_version": "ivdivo.room917_render_manifest_result/1.0",
            "status": MANIFEST_HOLD,
            "render_authority": False,
            "release_authority": False,
            "reasons": reasons,
            "next": "SUPPLY_REAL_SOURCE_MASTER_AND_PASSED_COMPILED_PLAN__DO_NOT_RENDER",
        }

    fmt = contract["render_format"]
    outputs = contract["required_outputs"]
    stems = []
    for bus in contract["required_buses"]:
        stems.append({
            "kind": "STEM",
            "bus": bus,
            "file_name": outputs["stems"][bus],
            "relative_path": f"{output_root.rstrip('/')}/{outputs['stems'][bus]}",
            "sample_rate_hz": fmt["sample_rate_hz"],
            "bit_depth": fmt["bit_depth"],
            "channels": fmt["stem_channels"],
        })

    return {
        "schema_version": "ivdivo.room917_render_manifest_result/1.0",
        "project": contract.get("project", "ROOM917"),
        "episode": contract.get("episode", "E01"),
        "status": MANIFEST_PASS,
        "render_authority": True,
        "release_authority": False,
        "source_master_sha256": source_master["sha256"],
        "source_master_exact_bytes_verified": True,
        "compiled_plan_sha256": plan_sha256,
        "output_root": output_root.rstrip("/"),
        "full_mix": {
            "kind": "FULL_MIX",
            "file_name": outputs["full_mix"],
            "relative_path": f"{output_root.rstrip('/')}/{outputs['full_mix']}",
            "sample_rate_hz": fmt["sample_rate_hz"],
            "bit_depth": fmt["bit_depth"],
            "channels": fmt["full_mix_channels"],
        },
        "stems": stems,
        "post_render_machine_qc_required": True,
        "human_gate_after_machine_pass": contract.get("human_gate_after_machine_pass"),
        "next": "RENDER_EXACT_MANIFEST__MEASURE_REAL_OUTPUT_BYTES__VALIDATE_RECEIPT",
    }


def validate_receipt(contract: Dict[str, Any], manifest: Dict[str, Any], receipt: Dict[str, Any], *, manifest_sha256: str) -> Dict[str, Any]:
    reasons: List[str] = []
    details: List[str] = []

    if manifest.get("status") != MANIFEST_PASS or manifest.get("render_authority") is not True:
        reasons.append("manifest_not_render_authorized")
    if manifest.get("release_authority") is not False:
        reasons.append("manifest_release_boundary_invalid")
    if receipt.get("manifest_sha256") != manifest_sha256:
        reasons.append("receipt_manifest_sha256_mismatch")
    if receipt.get("source_master_sha256") != manifest.get("source_master_sha256"):
        reasons.append("receipt_source_master_sha256_mismatch")
    if receipt.get("compiled_plan_sha256") != manifest.get("compiled_plan_sha256"):
        reasons.append("receipt_compiled_plan_sha256_mismatch")
    if receipt.get("measurement_source") != "REAL_RENDER_BYTES":
        reasons.append("machine_qc_not_measured_from_real_render_bytes")

    expected_files: Dict[str, Dict[str, Any]] = {}
    full_mix = manifest.get("full_mix") if isinstance(manifest.get("full_mix"), dict) else {}
    if full_mix.get("file_name"):
        expected_files[full_mix["file_name"]] = full_mix
    for stem in manifest.get("stems", []) if isinstance(manifest.get("stems"), list) else []:
        if isinstance(stem, dict) and stem.get("file_name"):
            expected_files[stem["file_name"]] = stem

    outputs = receipt.get("outputs") if isinstance(receipt.get("outputs"), list) else []
    actual_by_name = {o.get("file_name"): o for o in outputs if isinstance(o, dict) and o.get("file_name")}
    if set(actual_by_name) != set(expected_files):
        missing = sorted(set(expected_files) - set(actual_by_name))
        extra = sorted(set(actual_by_name) - set(expected_files))
        if missing:
            details.append("missing_outputs:" + ",".join(missing))
        if extra:
            details.append("extra_outputs:" + ",".join(extra))
        reasons.append("render_output_set_mismatch")

    full_sample_count = None
    for name, expected in expected_files.items():
        actual = actual_by_name.get(name)
        if not actual:
            continue
        if actual.get("exists") is not True:
            details.append(f"{name}:file_not_confirmed_existing")
            reasons.append("one_or_more_outputs_invalid")
        if not SHA256_RE.match(str(actual.get("sha256", ""))):
            details.append(f"{name}:sha256_missing_or_invalid")
            reasons.append("one_or_more_outputs_invalid")
        for field in ("sample_rate_hz", "bit_depth", "channels"):
            if actual.get(field) != expected.get(field):
                details.append(f"{name}:{field}_mismatch")
                reasons.append("one_or_more_outputs_invalid")
        sample_count = actual.get("sample_count")
        if not isinstance(sample_count, int) or isinstance(sample_count, bool) or sample_count <= 0:
            details.append(f"{name}:sample_count_invalid")
            reasons.append("one_or_more_outputs_invalid")
        if actual.get("start_offset_samples") != 0:
            details.append(f"{name}:start_offset_samples_not_zero")
            reasons.append("one_or_more_outputs_invalid")
        if expected.get("kind") == "FULL_MIX" and isinstance(sample_count, int) and sample_count > 0:
            full_sample_count = sample_count

    if full_sample_count is not None:
        for name, expected in expected_files.items():
            if expected.get("kind") != "STEM":
                continue
            actual = actual_by_name.get(name, {})
            if actual.get("sample_count") != full_sample_count:
                details.append(f"{name}:sample_count_not_equal_full_mix")
                reasons.append("stem_sample_count_mismatch")

    req = contract.get("receipt_requirements", {})
    null = receipt.get("stem_sum_null") if isinstance(receipt.get("stem_sum_null"), dict) else {}
    max_lsb = null.get("max_abs_lsb")
    if not isinstance(max_lsb, (int, float)) or isinstance(max_lsb, bool) or max_lsb > req.get("stem_sum_null_max_abs_lsb", 1):
        reasons.append("stem_sum_null_exceeds_one_lsb")
    if null.get("sample_offset") != 0:
        reasons.append("stem_sum_null_sample_offset_nonzero")
    if full_sample_count is not None and null.get("compared_samples") != full_sample_count:
        reasons.append("stem_sum_null_compared_sample_count_mismatch")

    boolean_requirements = {
        "protected_silence_post_fx_sample_exact_pass": "protected_silence_post_fx_sample_exact_failed",
        "clue_sfx_survival_pass": "clue_sfx_survival_failed",
        "scene3_lineage_preserved": "scene3_lineage_not_preserved",
        "mono_survival_pass": "mono_survival_failed",
        "phone_proxy_survival_pass": "phone_proxy_survival_failed",
    }
    for field, failure in boolean_requirements.items():
        if receipt.get(field) is not req.get(field, True):
            reasons.append(failure)

    metrics = receipt.get("full_mix_metrics") if isinstance(receipt.get("full_mix_metrics"), dict) else {}
    qc = contract.get("master_qc", {})
    lufs = metrics.get("integrated_lufs")
    if not isinstance(lufs, (int, float)) or isinstance(lufs, bool) or abs(lufs - qc.get("integrated_lufs_target", -16.0)) > qc.get("integrated_lufs_tolerance_lu", 0.5):
        reasons.append("integrated_lufs_out_of_profile")
    peak = metrics.get("true_peak_dbtp")
    if not isinstance(peak, (int, float)) or isinstance(peak, bool) or peak > qc.get("true_peak_max_dbtp", -1.0):
        reasons.append("true_peak_out_of_profile")
    lra = metrics.get("lra_lu")
    if not isinstance(lra, (int, float)) or isinstance(lra, bool) or lra > qc.get("lra_max_lu", 11.0):
        reasons.append("lra_out_of_profile")

    # Deduplicate category reasons while preserving deterministic order.
    reasons = list(dict.fromkeys(reasons))
    status = QC_PASS if not reasons else QC_HOLD
    return {
        "schema_version": "ivdivo.room917_render_machine_qc_result/1.0",
        "project": contract.get("project", "ROOM917"),
        "episode": contract.get("episode", "E01"),
        "status": status,
        "render_receipt_accepted": not reasons,
        "release_authority": False,
        "manifest_sha256": manifest_sha256,
        "reasons": reasons,
        "details": details,
        "next": (
            "BUILD_IDENTIFIED_AUDIO_PACKAGE_AND_RUN_P003B_LISTENER_QC_RED_TEAM"
            if not reasons
            else "REPAIR_ONLY_FAILED_RENDER_OR_MEASUREMENT_LAYER__DO_NOT_RELEASE"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    c = sub.add_parser("compile")
    c.add_argument("--contract", required=True)
    c.add_argument("--plan", required=True)
    c.add_argument("--source-master", required=True)
    c.add_argument("--output-root", required=True)
    c.add_argument("--out", required=True)

    v = sub.add_parser("validate")
    v.add_argument("--contract", required=True)
    v.add_argument("--manifest", required=True)
    v.add_argument("--receipt", required=True)
    v.add_argument("--out", required=True)

    args = parser.parse_args()
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))

    if args.command == "compile":
        plan_bytes, plan = _load_bytes(args.plan)
        source_master = json.loads(Path(args.source_master).read_text(encoding="utf-8"))
        result = compile_manifest(contract, plan, source_master, plan_sha256=_sha(plan_bytes), output_root=args.output_root)
        pass_status = MANIFEST_PASS
    else:
        manifest_bytes, manifest = _load_bytes(args.manifest)
        receipt = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
        result = validate_receipt(contract, manifest, receipt, manifest_sha256=_sha(manifest_bytes))
        pass_status = QC_PASS

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"])
    for reason in result.get("reasons", []):
        print(f"- {reason}")
    for detail in result.get("details", []):
        print(f"- {detail}")
    return 0 if result["status"] == pass_status else 2


if __name__ == "__main__":
    raise SystemExit(main())
