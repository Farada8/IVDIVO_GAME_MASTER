#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FREEZE = HERE / "p003b_pass_a_freeze.py"
OPEN = HERE / "p003b_pass_b_open.py"
CLASSES = ["ACTOR_BELIEF", "AI_AUDIBLE", "DEAD_SCENE", "GEOGRAPHY", "MYSTERY", "SFX_MASKING"]
SHA = "a" * 64


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def manifest() -> dict:
    return {
        "schema_version": "room917.p003b_blind_listener_package/1.3",
        "package_id": "PKG",
        "status": "READY_FOR_PASS_A",
        "files": {"stereo_target": {"file": "TARGET.wav", "sha256": SHA, "playback": "PASS_A_FIRST"}},
        "question_classes": CLASSES,
        "questions": ["q1", "q2", "q3", "q4", "q5", "q6"],
    }


def notes() -> dict:
    return {
        "schema_version": "ivdivo.room917_p003b_pass_a_notes/1.0",
        "package_id": "PKG",
        "target_sha256": SHA,
        "status": "COMPLETE",
        "answers": [{"question_class": q, "answer": "blind note"} for q in CLASSES],
    }


def queue() -> dict:
    return {
        "schema_version": "ivdivo.room917_p003b_pass_b_verification_queue/1.0",
        "project": "ROOM917",
        "episode": "E01",
        "scope": "SCENE3",
        "status": "READY_AFTER_BLIND_PASS_A_ONLY",
        "blind_firewall": {
            "pass_a_must_not_read_this_queue": True,
            "open_queue_only_after_pass_a_notes_are_frozen": True,
        },
        "verification_candidates": [
            {
                "candidate_id": "C1",
                "question_class": "AI_AUDIBLE",
                "verify_by_ear": "Does the join sound generated?",
                "minimal_fix_if_confirmed": "Retime only the failed join.",
                "do_not_touch": ["story_text"],
            },
            {
                "candidate_id": "C2",
                "question_class": "MYSTERY",
                "verify_by_ear": "Is the missing note perceived?",
                "minimal_fix_if_confirmed": "Repair only the pitched clue asset.",
                "do_not_touch": ["unrelated_dialogue"],
            },
        ],
    }


def setup_case(q: dict | None = None) -> tuple[tempfile.TemporaryDirectory[str], dict[str, Path]]:
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    paths = {
        "manifest": root / "manifest.json",
        "notes": root / "notes.json",
        "freeze": root / "freeze.json",
        "queue": root / "queue.json",
        "receipt": root / "pass_b.json",
    }
    write(paths["manifest"], manifest()); write(paths["notes"], notes()); write(paths["queue"], q or queue())
    f = subprocess.run([
        sys.executable, str(FREEZE),
        "--manifest", str(paths["manifest"]),
        "--notes", str(paths["notes"]),
        "--out", str(paths["freeze"]),
    ], text=True, capture_output=True)
    assert f.returncode == 0, f.stdout + f.stderr
    return td, paths


def run(paths: dict[str, Path]) -> tuple[subprocess.CompletedProcess[str], dict]:
    proc = subprocess.run([
        sys.executable, str(OPEN),
        "--public-manifest", str(paths["manifest"]),
        "--pass-a-notes", str(paths["notes"]),
        "--pass-a-freeze", str(paths["freeze"]),
        "--pass-b-queue", str(paths["queue"]),
        "--out", str(paths["receipt"]),
    ], text=True, capture_output=True)
    return proc, json.loads(paths["receipt"].read_text(encoding="utf-8"))


def test_valid_freeze_opens_targeted_pass_b_not_pass_c() -> None:
    td, p = setup_case()
    try:
        proc, r = run(p)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert r["status"] == "PASS_B_AUTHORIZED"
        assert r["pass_b_authorized"] is True
        assert r["pass_c_authorized"] is False
        assert r["release_authority"] is False
        assert r["target_sha256"] == SHA
    finally:
        td.cleanup()


def test_notes_mutation_after_freeze_blocks_pass_b() -> None:
    td, p = setup_case()
    try:
        n = json.loads(p["notes"].read_text(encoding="utf-8")); n["answers"][0]["answer"] = "contaminated after queue preview"; write(p["notes"], n)
        proc, r = run(p)
        assert proc.returncode != 0
        assert "PASS_A_NOTES_CHANGED_AFTER_FREEZE" in r["errors"]
    finally:
        td.cleanup()


def test_manifest_mutation_after_freeze_blocks_pass_b() -> None:
    td, p = setup_case()
    try:
        m = json.loads(p["manifest"].read_text(encoding="utf-8")); m["questions"][0] = "contaminated prompt"; write(p["manifest"], m)
        proc, r = run(p)
        assert proc.returncode != 0
        assert "PUBLIC_MANIFEST_CHANGED_AFTER_PASS_A_FREEZE" in r["errors"]
    finally:
        td.cleanup()


def test_queue_not_ready_blocks_pass_b() -> None:
    q = queue(); q["status"] = "DRAFT"
    td, p = setup_case(q)
    try:
        proc, r = run(p)
        assert proc.returncode != 0
        assert "PASS_B_QUEUE_STATUS_INVALID" in r["errors"]
    finally:
        td.cleanup()


def test_invalid_question_class_blocks_pass_b() -> None:
    q = queue(); q["verification_candidates"][0]["question_class"] = "RETENTION"
    td, p = setup_case(q)
    try:
        proc, r = run(p)
        assert proc.returncode != 0
        assert "PASS_B_CANDIDATE_QUESTION_CLASS_INVALID:C1" in r["errors"]
    finally:
        td.cleanup()


def test_duplicate_candidate_ids_block_pass_b() -> None:
    q = queue(); q["verification_candidates"][1]["candidate_id"] = "C1"
    td, p = setup_case(q)
    try:
        proc, r = run(p)
        assert proc.returncode != 0
        assert "PASS_B_CANDIDATE_IDS_NOT_UNIQUE" in r["errors"]
    finally:
        td.cleanup()


def test_queue_without_verify_by_ear_blocks_pass_b() -> None:
    q = queue(); q["verification_candidates"][0]["verify_by_ear"] = ""
    td, p = setup_case(q)
    try:
        proc, r = run(p)
        assert proc.returncode != 0
        assert "PASS_B_VERIFY_BY_EAR_MISSING:C1" in r["errors"]
    finally:
        td.cleanup()


def test_tampered_freeze_preauthorizing_pass_c_blocks_pass_b() -> None:
    td, p = setup_case()
    try:
        f = json.loads(p["freeze"].read_text(encoding="utf-8")); f["pass_c_authorized"] = True; write(p["freeze"], f)
        proc, r = run(p)
        assert proc.returncode != 0
        assert "PASS_A_FREEZE_MUST_NOT_PREAUTHORIZE_PASS_C" in r["errors"]
    finally:
        td.cleanup()


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failures = []
    for t in tests:
        try:
            t(); print("PASS", t.__name__)
        except Exception as exc:  # noqa: BLE001
            failures.append((t.__name__, repr(exc))); print("FAIL", t.__name__, exc)
    print(f"TOTAL={len(tests)} FAILED={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
