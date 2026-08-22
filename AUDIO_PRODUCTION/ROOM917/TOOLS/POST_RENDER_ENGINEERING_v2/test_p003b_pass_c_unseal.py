#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FREEZE_TOOL = HERE / "p003b_pass_a_freeze.py"
UNSEAL_TOOL = HERE / "p003b_pass_c_unseal.py"
CLASSES = ["ACTOR_BELIEF", "AI_AUDIBLE", "DEAD_SCENE", "GEOGRAPHY", "MYSTERY", "SFX_MASKING"]
TARGET_SHA = "a" * 64


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def setup_case() -> tuple[Path, dict]:
    root = Path(tempfile.mkdtemp())
    public = {
        "schema_version": "room917.p003b_blind_listener_package/1.3",
        "package_id": "PKG1",
        "status": "READY_FOR_PASS_A",
        "files": {"stereo_target": {"file": "TARGET.wav", "sha256": TARGET_SHA, "playback": "PASS_A_FIRST"}},
        "question_classes": CLASSES,
        "questions": ["q1","q2","q3","q4","q5","q6"],
    }
    notes = {
        "schema_version": "ivdivo.room917_p003b_pass_a_notes/1.0",
        "package_id": "PKG1",
        "target_sha256": TARGET_SHA,
        "status": "COMPLETE",
        "answers": [{"question_class": q, "answer": "blind observation"} for q in CLASSES],
    }
    result = {
        "source_identity": {"identity_status": "VERIFIED", "observed_sha256": TARGET_SHA},
        "blind_listen": {"pass_a_notes_frozen": True, "pass_b_targeted_verification": "COMPLETE"},
    }
    plan = {
        "source_identity": {"observed_sha256": TARGET_SHA},
        "status": "NO_REPAIR_REQUESTED",
        "release_authorized": False,
        "repairs": [],
        "holds": [],
    }
    mp = root / "LISTENER_MANIFEST.json"
    np = root / "PASS_A_NOTES.json"
    rp = root / "PASS_A_FREEZE.json"
    resultp = root / "RESULT.json"
    planp = root / "REPAIR_PLAN.json"
    sealed_dir = root / "SEALED_PASS_C"
    sealed_dir.mkdir()
    mono = sealed_dir / "R917_BLIND_E01_MONO.wav"
    phone = sealed_dir / "R917_BLIND_E01_PHONE_PROXY.wav"
    mono.write_bytes(b"mono-proxy-bytes")
    phone.write_bytes(b"phone-proxy-bytes")
    sealed = {
        "schema_version": "room917.p003b_pass_c_sealed/1.1",
        "package_id": "PKG1",
        "status": "SEALED_UNTIL_P003B_UNSEAL_GATE",
        "open_only_after": "PASS_A_FREEZE_VERIFIED__PASS_B_COMPLETE__NO_OPEN_REPAIR_OR_POST_REPAIR_RELISTEN_RECEIPT",
        "machine_qc_status": "PASS_MACHINE_QC",
        "files": {
            "mono_folddown": {"file": mono.name, "sha256": sha(mono)},
            "phone_band_mono": {"file": phone.name, "sha256": sha(phone)},
        },
    }
    sealedp = sealed_dir / "PASS_C_MANIFEST_SEALED.json"
    write_json(mp, public); write_json(np, notes); write_json(resultp, result); write_json(planp, plan); write_json(sealedp, sealed)
    freeze = subprocess.run([sys.executable, str(FREEZE_TOOL), "--manifest", str(mp), "--notes", str(np), "--out", str(rp)], text=True, capture_output=True)
    assert freeze.returncode == 0, freeze.stdout + freeze.stderr
    return root, {"public": mp, "notes": np, "freeze": rp, "result": resultp, "plan": planp, "sealed": sealedp, "mono": mono, "phone": phone}


def run(paths: dict) -> tuple[subprocess.CompletedProcess[str], dict]:
    out = paths["public"].parent / "PASS_C_RECEIPT.json"
    proc = subprocess.run([
        sys.executable, str(UNSEAL_TOOL),
        "--public-manifest", str(paths["public"]),
        "--pass-a-notes", str(paths["notes"]),
        "--pass-a-freeze", str(paths["freeze"]),
        "--listener-result", str(paths["result"]),
        "--repair-plan", str(paths["plan"]),
        "--sealed-pass-c-manifest", str(paths["sealed"]),
        "--out", str(out),
    ], text=True, capture_output=True)
    return proc, json.loads(out.read_text(encoding="utf-8"))


def test_clean_no_repair_path_authorizes_pass_c_not_release() -> None:
    root, p = setup_case(); proc, receipt = run(p)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert receipt["status"] == "PASS_C_AUTHORIZED"
    assert receipt["pass_c_authorized"] is True
    assert receipt["release_authorized"] is False
    assert set(receipt["proxy_files"]) == {"mono_folddown", "phone_band_mono"}


def test_any_repair_blocks_until_post_repair_relisten() -> None:
    root, p = setup_case(); plan = json.loads(p["plan"].read_text())
    plan["status"] = "REPAIR_PLAN_READY"; plan["repairs"] = [{"patch_id":"P1"}]
    write_json(p["plan"], plan)
    proc, receipt = run(p)
    assert proc.returncode != 0
    assert "POST_REPAIR_RELISTEN_REQUIRED_BEFORE_PASS_C" in receipt["errors"]


def test_open_hold_blocks() -> None:
    root, p = setup_case(); plan = json.loads(p["plan"].read_text())
    plan["status"] = "HOLD"; plan["holds"] = [{"defect_id":"D1"}]
    write_json(p["plan"], plan)
    proc, receipt = run(p)
    assert proc.returncode != 0
    assert "OPEN_HOLD_DEFECTS_BLOCK_PASS_C" in receipt["errors"]


def test_pass_b_incomplete_blocks() -> None:
    root, p = setup_case(); result = json.loads(p["result"].read_text())
    result["blind_listen"]["pass_b_targeted_verification"] = "NOT_RUN"
    write_json(p["result"], result)
    proc, receipt = run(p)
    assert proc.returncode != 0
    assert "PASS_B_NOT_COMPLETE" in receipt["errors"]


def test_notes_mutation_after_freeze_blocks() -> None:
    root, p = setup_case(); notes = json.loads(p["notes"].read_text())
    notes["answers"][0]["answer"] = "changed after seeing Pass B"
    write_json(p["notes"], notes)
    proc, receipt = run(p)
    assert proc.returncode != 0
    assert "PASS_A_NOTES_CHANGED_AFTER_FREEZE" in receipt["errors"]


def test_missing_proxy_blocks() -> None:
    root, p = setup_case(); p["phone"].unlink()
    proc, receipt = run(p)
    assert proc.returncode != 0
    assert "PASS_C_PROXY_FILE_MISSING:phone_band_mono" in receipt["errors"]


def test_proxy_sha_mismatch_blocks() -> None:
    root, p = setup_case(); p["mono"].write_bytes(b"tampered")
    proc, receipt = run(p)
    assert proc.returncode != 0
    assert "PASS_C_PROXY_SHA_MISMATCH:mono_folddown" in receipt["errors"]


def test_machine_qc_hold_blocks() -> None:
    root, p = setup_case(); sealed = json.loads(p["sealed"].read_text())
    sealed["machine_qc_status"] = "HOLD_MACHINE_QC"
    write_json(p["sealed"], sealed)
    proc, receipt = run(p)
    assert proc.returncode != 0
    assert "MACHINE_QC_NOT_PASS" in receipt["errors"]


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = []
    for t in tests:
        try:
            t(); print("PASS", t.__name__)
        except Exception as exc:  # noqa: BLE001
            failed.append((t.__name__, repr(exc))); print("FAIL", t.__name__, exc)
    print(f"TOTAL={len(tests)} FAILED={len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
