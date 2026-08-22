#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "p003b_pass_a_freeze.py"
CLASSES = ["ACTOR_BELIEF", "AI_AUDIBLE", "DEAD_SCENE", "GEOGRAPHY", "MYSTERY", "SFX_MASKING"]


def manifest() -> dict:
    return {
        "schema_version": "room917.p003b_blind_listener_package/1.2",
        "package_id": "R917_E01_LISTEN_TEST",
        "status": "READY_FOR_PASS_A",
        "files": {
            "stereo_target": {
                "file": "R917_BLIND_E01_TARGET.wav",
                "sha256": "a" * 64,
                "playback": "PASS_A_FIRST",
            }
        },
        "question_classes": list(CLASSES),
        "questions": [
            "Верю ли я актёру?",
            "Где слышно ИИ?",
            "Где сцена мёртвая?",
            "Понятна ли география?",
            "Работает ли тайна?",
            "Не мешают ли SFX словам?",
        ],
    }


def notes() -> dict:
    return {
        "schema_version": "ivdivo.room917_p003b_pass_a_notes/1.0",
        "package_id": "R917_E01_LISTEN_TEST",
        "target_sha256": "a" * 64,
        "status": "COMPLETE",
        "answers": [
            {"question_class": q, "answer": f"blind answer {i}"}
            for i, q in enumerate(CLASSES, 1)
        ],
    }


def run_freeze(m: dict, n: dict) -> tuple[subprocess.CompletedProcess[str], dict, Path, Path, Path, tempfile.TemporaryDirectory[str]]:
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    mp = root / "manifest.json"
    np = root / "notes.json"
    rp = root / "receipt.json"
    mp.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    np.write_text(json.dumps(n, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--manifest", str(mp), "--notes", str(np), "--out", str(rp)],
        text=True,
        capture_output=True,
    )
    receipt = json.loads(rp.read_text(encoding="utf-8"))
    return proc, receipt, mp, np, rp, td


def verify(mp: Path, np: Path, rp: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), "--manifest", str(mp), "--notes", str(np), "--verify-receipt", str(rp)],
        text=True,
        capture_output=True,
    )


def test_valid_freeze_authorizes_pass_b_not_pass_c() -> None:
    proc, receipt, mp, np, rp, td = run_freeze(manifest(), notes())
    try:
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert receipt["status"] == "PASS_A_FROZEN_PASS_B_AUTHORIZED"
        assert receipt["pass_a_notes_frozen"] is True
        assert receipt["pass_b_authorized"] is True
        assert receipt["pass_c_authorized"] is False
        v = verify(mp, np, rp)
        assert v.returncode == 0, v.stdout + v.stderr
    finally:
        td.cleanup()


def test_wrong_order_question_classes_holds() -> None:
    m = manifest(); m["question_classes"] = list(reversed(CLASSES))
    proc, receipt, *_rest = run_freeze(m, notes())
    _rest[-1].cleanup()
    assert proc.returncode != 0
    assert "MANIFEST_SIX_QUESTION_CLASSES_MISMATCH" in receipt["errors"]


def test_wrong_order_answers_holds() -> None:
    n = notes(); n["answers"] = list(reversed(n["answers"]))
    proc, receipt, *_rest = run_freeze(manifest(), n)
    _rest[-1].cleanup()
    assert proc.returncode != 0
    assert "PASS_A_ANSWERS_MUST_CONTAIN_EXACT_SIX_CLASSES_IN_LOCKED_ORDER" in receipt["errors"]


def test_extra_public_file_or_machine_qc_leak_holds() -> None:
    m = manifest()
    m["files"]["mono_folddown"] = {"file": "MONO.wav", "sha256": "b" * 64}
    m["machine_qc_status"] = "PASS"
    proc, receipt, *_rest = run_freeze(m, notes())
    _rest[-1].cleanup()
    assert proc.returncode != 0
    assert "PASS_A_PUBLIC_FILES_MUST_BE_STEREO_TARGET_ONLY" in receipt["errors"]
    assert "PASS_A_MANIFEST_CONTAINS_SEALED_INFORMATION" in receipt["errors"]


def test_notes_change_after_freeze_invalidates_receipt() -> None:
    proc, receipt, mp, np, rp, td = run_freeze(manifest(), notes())
    try:
        assert proc.returncode == 0
        n = json.loads(np.read_text(encoding="utf-8"))
        n["answers"][0]["answer"] = "post-Pass-B contaminated rewrite"
        np.write_text(json.dumps(n, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        v = verify(mp, np, rp)
        assert v.returncode != 0
        assert "PASS_A_NOTES_CHANGED_AFTER_FREEZE" in v.stdout
    finally:
        td.cleanup()


def test_manifest_change_after_freeze_invalidates_receipt() -> None:
    proc, receipt, mp, np, rp, td = run_freeze(manifest(), notes())
    try:
        assert proc.returncode == 0
        m = json.loads(mp.read_text(encoding="utf-8"))
        m["questions"][0] = "contaminated prompt"
        mp.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        v = verify(mp, np, rp)
        assert v.returncode != 0
        assert "MANIFEST_CHANGED_AFTER_PASS_A_FREEZE" in v.stdout
    finally:
        td.cleanup()


def test_package_id_mismatch_holds() -> None:
    n = notes(); n["package_id"] = "OTHER_PACKAGE"
    proc, receipt, *_rest = run_freeze(manifest(), n)
    _rest[-1].cleanup()
    assert proc.returncode != 0
    assert "PASS_A_PACKAGE_ID_MISMATCH" in receipt["errors"]


def test_target_sha_mismatch_holds() -> None:
    n = notes(); n["target_sha256"] = "b" * 64
    proc, receipt, *_rest = run_freeze(manifest(), n)
    _rest[-1].cleanup()
    assert proc.returncode != 0
    assert "PASS_A_TARGET_SHA_MISMATCH" in receipt["errors"]


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failures = []
    for test in tests:
        try:
            test()
            print("PASS", test.__name__)
        except Exception as exc:  # noqa: BLE001
            failures.append((test.__name__, repr(exc)))
            print("FAIL", test.__name__, exc)
    print(f"TOTAL={len(tests)} FAILED={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
