#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

QUESTION_CLASSES = ["ACTOR_BELIEF", "AI_AUDIBLE", "DEAD_SCENE", "GEOGRAPHY", "MYSTERY", "SFX_MASKING"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    if manifest.get("status") != "READY_FOR_PASS_A":
        errors.append("MANIFEST_NOT_READY_FOR_PASS_A")
    if manifest.get("question_classes") != QUESTION_CLASSES:
        errors.append("MANIFEST_SIX_QUESTION_CLASSES_MISMATCH")
    files = manifest.get("files") or {}
    if set(files) != {"stereo_target"}:
        errors.append("PASS_A_PUBLIC_FILES_MUST_BE_STEREO_TARGET_ONLY")
    target = files.get("stereo_target") or {}
    if not target.get("sha256"):
        errors.append("PASS_A_TARGET_SHA_MISSING")
    if target.get("playback") != "PASS_A_FIRST":
        errors.append("PASS_A_TARGET_PLAYBACK_FLAG_MISSING")
    forbidden_keys = {"machine_qc_status", "mono_folddown", "phone_band_mono", "pass_b_candidates", "identity_mode"}
    if forbidden_keys & set(manifest):
        errors.append("PASS_A_MANIFEST_CONTAINS_SEALED_INFORMATION")
    return errors


def validate_notes(notes: dict, manifest: dict) -> list[str]:
    errors: list[str] = []
    if notes.get("schema_version") != "ivdivo.room917_p003b_pass_a_notes/1.0":
        errors.append("PASS_A_NOTES_SCHEMA_MISMATCH")
    if notes.get("status") != "COMPLETE":
        errors.append("PASS_A_NOTES_NOT_COMPLETE")
    if notes.get("package_id") != manifest.get("package_id"):
        errors.append("PASS_A_PACKAGE_ID_MISMATCH")
    target_sha = ((manifest.get("files") or {}).get("stereo_target") or {}).get("sha256")
    if notes.get("target_sha256") != target_sha:
        errors.append("PASS_A_TARGET_SHA_MISMATCH")
    answers = notes.get("answers")
    if not isinstance(answers, list):
        errors.append("PASS_A_ANSWERS_NOT_LIST")
        return errors
    classes = [row.get("question_class") for row in answers if isinstance(row, dict)]
    if classes != QUESTION_CLASSES:
        errors.append("PASS_A_ANSWERS_MUST_CONTAIN_EXACT_SIX_CLASSES_IN_LOCKED_ORDER")
    for row in answers:
        if not isinstance(row, dict):
            errors.append("PASS_A_ANSWER_NOT_OBJECT")
            continue
        if not str(row.get("answer") or "").strip():
            errors.append(f"PASS_A_EMPTY_ANSWER:{row.get('question_class')}")
    return errors


def freeze(manifest_path: Path, notes_path: Path, out_path: Path) -> int:
    manifest = load(manifest_path)
    notes = load(notes_path)
    errors = validate_manifest(manifest) + validate_notes(notes, manifest)
    receipt = {
        "schema_version": "ivdivo.room917_p003b_pass_a_freeze_receipt/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "package_id": manifest.get("package_id"),
        "status": "HOLD" if errors else "PASS_A_FROZEN_PASS_B_AUTHORIZED",
        "manifest_sha256": sha256_file(manifest_path),
        "notes_sha256": sha256_file(notes_path),
        "target_sha256": ((manifest.get("files") or {}).get("stereo_target") or {}).get("sha256"),
        "question_classes": QUESTION_CLASSES,
        "pass_a_notes_frozen": not errors,
        "pass_b_authorized": not errors,
        "pass_c_authorized": False,
        "errors": errors,
        "frozen_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "law": "PASS_B_MAY_OPEN_ONLY_IF_MANIFEST_AND_PASS_A_NOTES_BYTES_STILL_MATCH_THIS_RECEIPT; PASS_C_REMAINS_SEALED",
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(receipt["status"])
    return 0 if not errors else 4


def verify(manifest_path: Path, notes_path: Path, receipt_path: Path) -> int:
    receipt = load(receipt_path)
    errors: list[str] = []
    if receipt.get("schema_version") != "ivdivo.room917_p003b_pass_a_freeze_receipt/1.0":
        errors.append("FREEZE_RECEIPT_SCHEMA_MISMATCH")
    if receipt.get("status") != "PASS_A_FROZEN_PASS_B_AUTHORIZED" or receipt.get("pass_b_authorized") is not True:
        errors.append("FREEZE_RECEIPT_NOT_AUTHORIZED")
    if receipt.get("pass_c_authorized") is not False:
        errors.append("PASS_C_MUST_REMAIN_SEALED")
    if sha256_file(manifest_path) != receipt.get("manifest_sha256"):
        errors.append("MANIFEST_CHANGED_AFTER_PASS_A_FREEZE")
    if sha256_file(notes_path) != receipt.get("notes_sha256"):
        errors.append("PASS_A_NOTES_CHANGED_AFTER_FREEZE")
    manifest = load(manifest_path)
    notes = load(notes_path)
    errors += validate_manifest(manifest)
    errors += validate_notes(notes, manifest)
    if receipt.get("package_id") != manifest.get("package_id"):
        errors.append("RECEIPT_PACKAGE_ID_MISMATCH")
    if receipt.get("target_sha256") != ((manifest.get("files") or {}).get("stereo_target") or {}).get("sha256"):
        errors.append("RECEIPT_TARGET_SHA_MISMATCH")
    if errors:
        print("HOLD " + ";".join(sorted(set(errors))))
        return 4
    print("PASS_A_FREEZE_VERIFIED_PASS_B_MAY_OPEN")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Freeze ROOM917 P003B blind Pass A notes before any Pass B evidence is opened.")
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--notes", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--verify-receipt", type=Path)
    args = ap.parse_args()
    if args.verify_receipt:
        return verify(args.manifest, args.notes, args.verify_receipt)
    if not args.out:
        ap.error("--out is required when creating a freeze receipt")
    return freeze(args.manifest, args.notes, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
