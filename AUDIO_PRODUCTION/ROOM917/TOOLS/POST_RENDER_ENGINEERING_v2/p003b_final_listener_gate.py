#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

RESULT_SCHEMA = "ivdivo.room917_p003b_listener_qc_result/1.4"
PASS_B_SCHEMA = "ivdivo.room917_p003b_pass_b_open_receipt/1.0"
PASS_C_SCHEMA = "ivdivo.room917_p003b_pass_c_unseal_receipt/1.0"
AUTOMIX_SCHEMA = "ivdivo.room917_p003b_automix_eligibility/1.0"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PASS_VALUES = {"PASS", "COMPLETE", "VERIFIED", "APPROVED", "LOCKED", "CLOSED"}
CLOSED_GATE_VALUES = {"PASS", "VERIFIED", "APPROVED", "LOCKED", "CLOSED"}
AUTOMIX_MODE = "AUTOMIX_V1_ELIGIBILITY_VERIFIED_FULL_MIX"


def load(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def norm(value: object) -> str:
    return str(value or "").strip().upper()


def source_errors(result: dict[str, Any], automix: dict[str, Any] | None) -> list[str]:
    errors: list[str] = []
    source = result.get("source_identity") or {}
    mode = source.get("target_identity_mode")
    allowed = set(source.get("allowed_target_identity_mode") or [])
    observed_sha = str(source.get("observed_sha256") or "").lower()
    if result.get("schema_version") != RESULT_SCHEMA:
        errors.append("LISTENER_RESULT_SCHEMA_NOT_1_4")
    if source.get("identity_status") != "VERIFIED":
        errors.append("SOURCE_IDENTITY_NOT_VERIFIED")
    if mode not in allowed:
        errors.append("TARGET_IDENTITY_MODE_NOT_ALLOWED")
    if not SHA256_RE.match(observed_sha):
        errors.append("OBSERVED_SHA256_INVALID")
    if mode == AUTOMIX_MODE:
        if automix is None:
            errors.append("AUTOMIX_ELIGIBILITY_RECEIPT_REQUIRED")
        else:
            if automix.get("schema_version") != AUTOMIX_SCHEMA:
                errors.append("AUTOMIX_ELIGIBILITY_SCHEMA_INVALID")
            if automix.get("status") != "PASS_P003B_AUTOMIX_ELIGIBILITY":
                errors.append("AUTOMIX_ELIGIBILITY_NOT_PASS")
            if automix.get("eligible_for_p003b_packaging") is not True:
                errors.append("AUTOMIX_ELIGIBILITY_FLAG_FALSE")
            if str(automix.get("audio_sha256") or "").lower() != observed_sha:
                errors.append("AUTOMIX_ELIGIBILITY_AUDIO_SHA_MISMATCH")
            if automix.get("release_authority") is not False:
                errors.append("AUTOMIX_ELIGIBILITY_RELEASE_BOUNDARY_INVALID")
    return errors


def pass_a_errors(result: dict[str, Any]) -> list[str]:
    blind = result.get("blind_listen") or {}
    errors: list[str] = []
    if norm(blind.get("pass_a_story_free")) not in PASS_VALUES:
        errors.append("PASS_A_NOT_COMPLETE")
    if blind.get("pass_a_notes_frozen") is not True:
        errors.append("PASS_A_NOT_FROZEN")
    if not blind.get("pass_a_freeze_receipt_ref"):
        errors.append("PASS_A_FREEZE_RECEIPT_REF_MISSING")
    return errors


def pass_b_errors(result: dict[str, Any], receipt: dict[str, Any] | None) -> list[str]:
    errors: list[str] = []
    blind = result.get("blind_listen") or {}
    source = result.get("source_identity") or {}
    observed_sha = str(source.get("observed_sha256") or "").lower()
    if norm(blind.get("pass_b_targeted_verification")) not in PASS_VALUES:
        errors.append("PASS_B_NOT_COMPLETE")
    if not blind.get("pass_b_open_receipt_ref"):
        errors.append("PASS_B_OPEN_RECEIPT_REF_MISSING")
    if receipt is None:
        errors.append("PASS_B_OPEN_RECEIPT_REQUIRED")
        return errors
    if receipt.get("schema_version") != PASS_B_SCHEMA:
        errors.append("PASS_B_OPEN_RECEIPT_SCHEMA_INVALID")
    if receipt.get("status") != "PASS_B_AUTHORIZED" or receipt.get("pass_b_authorized") is not True:
        errors.append("PASS_B_OPEN_RECEIPT_NOT_AUTHORIZED")
    if receipt.get("pass_c_authorized") is not False:
        errors.append("PASS_B_OPEN_RECEIPT_MUST_NOT_PREAUTHORIZE_PASS_C")
    if receipt.get("release_authority") is not False:
        errors.append("PASS_B_OPEN_RECEIPT_RELEASE_BOUNDARY_INVALID")
    if str(receipt.get("target_sha256") or "").lower() != observed_sha:
        errors.append("PASS_B_OPEN_RECEIPT_TARGET_SHA_MISMATCH")
    return errors


def repair_plan_errors(result: dict[str, Any], plan: dict[str, Any] | None, *, require_clean: bool) -> list[str]:
    errors: list[str] = []
    if plan is None:
        return ["REPAIR_PLAN_REQUIRED"]
    source = result.get("source_identity") or {}
    plan_source = plan.get("source_identity") or {}
    if str(plan_source.get("observed_sha256") or "").lower() != str(source.get("observed_sha256") or "").lower():
        errors.append("REPAIR_PLAN_TARGET_SHA_MISMATCH")
    if plan.get("release_authorized") is not False:
        errors.append("REPAIR_PLAN_RELEASE_BOUNDARY_INVALID")
    repairs = plan.get("repairs") or []
    holds = plan.get("holds") or []
    if require_clean:
        if plan.get("status") != "NO_REPAIR_REQUESTED": errors.append("REPAIR_PLAN_NOT_CLEAN")
        if repairs: errors.append("OPEN_REPAIRS_BLOCK_GO")
        if holds: errors.append("OPEN_HOLDS_BLOCK_GO")
    elif not repairs:
        errors.append("REPAIR_VERDICT_REQUIRES_COMPILED_REPAIR")
    return errors


def pass_c_errors(result: dict[str, Any], receipt: dict[str, Any] | None) -> list[str]:
    errors: list[str] = []
    if receipt is None:
        return ["PASS_C_UNSEAL_RECEIPT_REQUIRED"]
    source = result.get("source_identity") or {}
    observed_sha = str(source.get("observed_sha256") or "").lower()
    if receipt.get("schema_version") != PASS_C_SCHEMA:
        errors.append("PASS_C_RECEIPT_SCHEMA_INVALID")
    if receipt.get("status") != "PASS_C_AUTHORIZED" or receipt.get("pass_c_authorized") is not True:
        errors.append("PASS_C_NOT_AUTHORIZED")
    if str(receipt.get("target_sha256") or "").lower() != observed_sha:
        errors.append("PASS_C_TARGET_SHA_MISMATCH")
    if receipt.get("release_authority") is not False:
        errors.append("PASS_C_RELEASE_BOUNDARY_INVALID")
    playback = (result.get("blind_listen") or {}).get("pass_c_translation_playback") or {}
    for key in ["stereo_headphones", "ordinary_speakers_or_mono", "mobile_proxy"]:
        if norm(playback.get(key)) not in PASS_VALUES:
            errors.append("PASS_C_PLAYBACK_NOT_PASS:" + key)
    if not (result.get("blind_listen") or {}).get("pass_c_unseal_receipt_ref"):
        errors.append("PASS_C_UNSEAL_RECEIPT_REF_MISSING")
    return errors


def open_gate_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    gates = result.get("open_release_gates") or {}
    required = {
        "scene3_fourth_note_perceptual_lock",
        "mina_human_cast_approval",
        "cate_human_cast_approval",
        "assembled_master_human_listen",
    }
    for key in sorted(required - set(gates)):
        errors.append("RELEASE_GATE_MISSING:" + key)
    for key in sorted(required & set(gates)):
        if norm(gates.get(key)) not in CLOSED_GATE_VALUES:
            errors.append("RELEASE_GATE_OPEN:" + key)
    return errors


def defect_errors_for_go(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for defect in result.get("defects") or []:
        status = norm(defect.get("status")) if isinstance(defect, dict) else "INVALID"
        if status != "KEEP":
            did = defect.get("defect_id") if isinstance(defect, dict) else "UNKNOWN"
            errors.append(f"NON_KEEP_DEFECT_BLOCKS_GO:{did}:{status}")
    return errors


def evaluate(result: dict[str, Any], plan: dict[str, Any] | None, pass_b: dict[str, Any] | None, pass_c: dict[str, Any] | None, automix: dict[str, Any] | None) -> dict[str, Any]:
    verdict = result.get("final_verdict") or {}
    requested = norm(verdict.get("release_status"))
    believability = norm(verdict.get("believability"))
    reason = str(verdict.get("reason") or "").strip()
    base_errors = source_errors(result, automix) + pass_a_errors(result)
    if not reason:
        base_errors.append("FINAL_VERDICT_REASON_MISSING")

    output = {
        "schema_version": "ivdivo.room917_p003b_final_listener_gate/1.1",
        "project": "ROOM917",
        "episode": result.get("episode"),
        "target_sha256": (result.get("source_identity") or {}).get("observed_sha256"),
        "requested_listener_verdict": requested,
        "believability": believability,
        "status": "HOLD",
        "listener_qc_go": False,
        "release_authority": False,
        "downstream_release_gate_may_consume": False,
        "errors": [],
        "law": "THIS_GATE_COMPILES_HUMAN_LISTENER_EVIDENCE_ONLY. IT NEVER SIMULATES LISTENING AND NEVER GRANTS PROJECT_RELEASE_AUTHORITY.",
    }

    if requested == "HOLD":
        output["errors"] = sorted(set(base_errors + ["HUMAN_LISTENER_VERDICT_HOLD"])); return output
    if requested == "NO_GO":
        output["errors"] = sorted(set(base_errors))
        if not output["errors"]: output["status"] = "LISTENER_QC_NO_GO"
        return output
    if requested == "REPAIR":
        errors = base_errors + pass_b_errors(result, pass_b) + repair_plan_errors(result, plan, require_clean=False)
        output["errors"] = sorted(set(errors))
        if not errors: output["status"] = "LISTENER_QC_REPAIR"
        return output
    if requested != "GO":
        output["errors"] = sorted(set(base_errors + ["UNKNOWN_FINAL_LISTENER_VERDICT"])); return output

    errors = base_errors
    errors += pass_b_errors(result, pass_b)
    errors += repair_plan_errors(result, plan, require_clean=True)
    errors += pass_c_errors(result, pass_c)
    errors += open_gate_errors(result)
    errors += defect_errors_for_go(result)
    if believability != "BELIEVE": errors.append("GO_REQUIRES_BELIEVABILITY_BELIEVE")
    output["errors"] = sorted(set(errors))
    if not errors:
        output["status"] = "LISTENER_QC_GO"
        output["listener_qc_go"] = True
        output["downstream_release_gate_may_consume"] = True
    return output


def main() -> int:
    ap = argparse.ArgumentParser(description="Compile ROOM917 P003B human Listener-QC evidence into GO/REPAIR/NO_GO/HOLD without granting release authority.")
    ap.add_argument("--result", required=True, type=Path)
    ap.add_argument("--repair-plan", type=Path)
    ap.add_argument("--pass-b-open-receipt", type=Path)
    ap.add_argument("--pass-c-receipt", type=Path)
    ap.add_argument("--automix-eligibility", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    outcome = evaluate(load(args.result) or {}, load(args.repair_plan), load(args.pass_b_open_receipt), load(args.pass_c_receipt), load(args.automix_eligibility))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(outcome["status"])
    for error in outcome.get("errors", []): print("- " + error)
    return 0 if outcome["status"] in {"LISTENER_QC_GO", "LISTENER_QC_REPAIR", "LISTENER_QC_NO_GO"} else 4


if __name__ == "__main__":
    raise SystemExit(main())
