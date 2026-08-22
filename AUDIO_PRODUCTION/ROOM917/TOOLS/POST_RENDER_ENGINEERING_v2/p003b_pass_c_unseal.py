#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_PROXY_KEYS = {"mono_folddown", "phone_band_mono"}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def pass_status(value: object) -> bool:
    return str(value or "").upper().startswith("PASS")


def validate_freeze(manifest_path: Path, notes_path: Path, receipt: dict) -> list[str]:
    errors: list[str] = []
    if receipt.get("schema_version") != "ivdivo.room917_p003b_pass_a_freeze_receipt/1.0":
        errors.append("PASS_A_FREEZE_SCHEMA_MISMATCH")
    if receipt.get("status") != "PASS_A_FROZEN_PASS_B_AUTHORIZED":
        errors.append("PASS_A_FREEZE_NOT_AUTHORIZED")
    if receipt.get("pass_a_notes_frozen") is not True or receipt.get("pass_b_authorized") is not True:
        errors.append("PASS_A_FREEZE_FLAGS_INVALID")
    if receipt.get("pass_c_authorized") is not False:
        errors.append("PASS_A_RECEIPT_MUST_NOT_PREAUTHORIZE_PASS_C")
    if sha256_file(manifest_path) != receipt.get("manifest_sha256"):
        errors.append("PUBLIC_MANIFEST_CHANGED_AFTER_PASS_A_FREEZE")
    if sha256_file(notes_path) != receipt.get("notes_sha256"):
        errors.append("PASS_A_NOTES_CHANGED_AFTER_FREEZE")
    return errors


def validate_result(result: dict, freeze: dict) -> list[str]:
    errors: list[str] = []
    source = result.get("source_identity") or {}
    blind = result.get("blind_listen") or {}
    if source.get("identity_status") != "VERIFIED":
        errors.append("RESULT_SOURCE_IDENTITY_NOT_VERIFIED")
    if source.get("observed_sha256") != freeze.get("target_sha256"):
        errors.append("RESULT_TARGET_SHA_NOT_FROZEN_TARGET")
    if blind.get("pass_a_notes_frozen") is not True:
        errors.append("RESULT_PASS_A_NOT_FROZEN")
    if str(blind.get("pass_b_targeted_verification") or "").upper() not in {"COMPLETE", "PASS", "VERIFIED"}:
        errors.append("PASS_B_NOT_COMPLETE")
    return errors


def validate_repair_plan(plan: dict, freeze: dict) -> list[str]:
    errors: list[str] = []
    source = plan.get("source_identity") or {}
    if source.get("observed_sha256") != freeze.get("target_sha256"):
        errors.append("REPAIR_PLAN_TARGET_SHA_NOT_FROZEN_TARGET")
    repairs = plan.get("repairs") or []
    holds = plan.get("holds") or []
    status = plan.get("status")
    if repairs:
        errors.append("POST_REPAIR_RELISTEN_REQUIRED_BEFORE_PASS_C")
    if holds:
        errors.append("OPEN_HOLD_DEFECTS_BLOCK_PASS_C")
    if status != "NO_REPAIR_REQUESTED":
        errors.append("REPAIR_PLAN_NOT_CLEAN_NO_REPAIR_STATE")
    if plan.get("release_authorized") is not False:
        errors.append("REPAIR_PLAN_RELEASE_BOUNDARY_INVALID")
    return errors


def validate_sealed_manifest(sealed_path: Path, sealed: dict, freeze: dict) -> tuple[list[str], dict]:
    errors: list[str] = []
    verified_files: dict = {}
    if sealed.get("schema_version") != "room917.p003b_pass_c_sealed/1.1":
        errors.append("PASS_C_SEALED_SCHEMA_MISMATCH")
    if sealed.get("status") != "SEALED_UNTIL_P003B_UNSEAL_GATE":
        errors.append("PASS_C_SEALED_STATUS_INVALID")
    if sealed.get("package_id") != freeze.get("package_id"):
        errors.append("PASS_C_PACKAGE_ID_MISMATCH")
    if not pass_status(sealed.get("machine_qc_status")):
        errors.append("MACHINE_QC_NOT_PASS")
    files = sealed.get("files") or {}
    if set(files) != REQUIRED_PROXY_KEYS:
        errors.append("PASS_C_PROXY_SET_INCOMPLETE_OR_EXTRA")
        return errors, verified_files
    for key in sorted(REQUIRED_PROXY_KEYS):
        ref = files.get(key) or {}
        name = ref.get("file")
        expected_sha = ref.get("sha256")
        if not name or not expected_sha:
            errors.append(f"PASS_C_PROXY_REF_INCOMPLETE:{key}")
            continue
        path = sealed_path.parent / str(name)
        if not path.is_file():
            errors.append(f"PASS_C_PROXY_FILE_MISSING:{key}")
            continue
        observed_sha = sha256_file(path)
        if observed_sha != expected_sha:
            errors.append(f"PASS_C_PROXY_SHA_MISMATCH:{key}")
            continue
        verified_files[key] = {"file": str(name), "sha256": observed_sha}
    return errors, verified_files


def main() -> int:
    ap = argparse.ArgumentParser(description="Open ROOM917 P003B Pass C only after clean blind Pass A/Pass B and no pending repair.")
    ap.add_argument("--public-manifest", required=True, type=Path)
    ap.add_argument("--pass-a-notes", required=True, type=Path)
    ap.add_argument("--pass-a-freeze", required=True, type=Path)
    ap.add_argument("--listener-result", required=True, type=Path)
    ap.add_argument("--repair-plan", required=True, type=Path)
    ap.add_argument("--sealed-pass-c-manifest", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    public = load(args.public_manifest)
    freeze = load(args.pass_a_freeze)
    result = load(args.listener_result)
    plan = load(args.repair_plan)
    sealed = load(args.sealed_pass_c_manifest)

    errors: list[str] = []
    errors += validate_freeze(args.public_manifest, args.pass_a_notes, freeze)
    if public.get("package_id") != freeze.get("package_id"):
        errors.append("PUBLIC_MANIFEST_PACKAGE_ID_MISMATCH")
    public_target = ((public.get("files") or {}).get("stereo_target") or {}).get("sha256")
    if public_target != freeze.get("target_sha256"):
        errors.append("PUBLIC_TARGET_SHA_MISMATCH")
    errors += validate_result(result, freeze)
    errors += validate_repair_plan(plan, freeze)
    sealed_errors, verified_files = validate_sealed_manifest(args.sealed_pass_c_manifest, sealed, freeze)
    errors += sealed_errors

    receipt = {
        "schema_version": "ivdivo.room917_p003b_pass_c_unseal_receipt/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "package_id": freeze.get("package_id"),
        "target_sha256": freeze.get("target_sha256"),
        "status": "HOLD" if errors else "PASS_C_AUTHORIZED",
        "pass_c_authorized": not errors,
        "release_authorized": False,
        "proxy_files": verified_files if not errors else {},
        "errors": sorted(set(errors)),
        "authorized_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z") if not errors else None,
        "law": "PASS_C_IS_TRANSLATION_PLAYBACK_ONLY; IT_NEVER_AUTHORIZES_RELEASE. ANY_REPAIR_REQUIRES_POST_REPAIR_HUMAN_RELISTEN_BEFORE_PASS_C.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(receipt["status"] + ("" if not errors else " " + ";".join(receipt["errors"])))
    return 0 if not errors else 4


if __name__ == "__main__":
    raise SystemExit(main())
