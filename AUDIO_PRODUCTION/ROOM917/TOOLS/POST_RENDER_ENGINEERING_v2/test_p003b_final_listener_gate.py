#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "p003b_final_listener_gate.py"
SHA = "a" * 64
AUTOMIX = "AUTOMIX_V1_ELIGIBILITY_VERIFIED_FULL_MIX"


def base_result(mode: str = AUTOMIX) -> dict:
    return {
        "schema_version": "ivdivo.room917_p003b_listener_qc_result/1.3",
        "project": "ROOM917",
        "episode": "E01",
        "authority": "THE_INSURABLE_FIRE",
        "source_identity": {
            "target_identity_mode": mode,
            "allowed_target_identity_mode": [
                "IMMUTABLE_SOURCE_MASTER",
                "PROVENANCE_VERIFIED_DERIVED_CANDIDATE",
                AUTOMIX,
            ],
            "observed_sha256": SHA,
            "identity_status": "VERIFIED",
        },
        "blind_listen": {
            "pass_a_story_free": "COMPLETE",
            "pass_a_notes_frozen": True,
            "pass_a_freeze_receipt_ref": "PASS_A_FREEZE.json",
            "pass_b_targeted_verification": "COMPLETE",
            "pass_c_unseal_receipt_ref": "PASS_C_RECEIPT.json",
            "pass_c_translation_playback": {
                "stereo_headphones": "PASS",
                "ordinary_speakers_or_mono": "PASS",
                "mobile_proxy": "PASS",
            },
        },
        "defects": [],
        "open_release_gates": {
            "scene3_fourth_note_perceptual_lock": "LOCKED",
            "mina_human_cast_approval": "APPROVED",
            "cate_human_cast_approval": "APPROVED",
            "assembled_master_human_listen": "CLOSED",
        },
        "final_verdict": {
            "believability": "BELIEVE",
            "release_status": "GO",
            "reason": "Human Listener QC passed all six questions after translation playback.",
        },
    }


def clean_plan() -> dict:
    return {
        "source_identity": {"observed_sha256": SHA},
        "status": "NO_REPAIR_REQUESTED",
        "release_authorized": False,
        "repairs": [],
        "holds": [],
    }


def pass_c() -> dict:
    return {
        "schema_version": "ivdivo.room917_p003b_pass_c_unseal_receipt/1.0",
        "status": "PASS_C_AUTHORIZED",
        "pass_c_authorized": True,
        "release_authorized": False,
        "target_sha256": SHA,
    }


def automix() -> dict:
    return {
        "schema_version": "ivdivo.room917_p003b_automix_eligibility/1.0",
        "status": "PASS_P003B_AUTOMIX_ELIGIBILITY",
        "eligible_for_p003b_packaging": True,
        "release_authority": False,
        "audio_sha256": SHA,
    }


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(result: dict, plan: dict | None = None, pc: dict | None = None, auto: dict | None = None) -> tuple[subprocess.CompletedProcess[str], dict]:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        rp = root / "result.json"; write(rp, result)
        out = root / "out.json"
        cmd = [sys.executable, str(TOOL), "--result", str(rp), "--out", str(out)]
        if plan is not None:
            pp = root / "plan.json"; write(pp, plan); cmd += ["--repair-plan", str(pp)]
        if pc is not None:
            cp = root / "pass_c.json"; write(cp, pc); cmd += ["--pass-c-receipt", str(cp)]
        if auto is not None:
            ap = root / "automix.json"; write(ap, auto); cmd += ["--automix-eligibility", str(ap)]
        proc = subprocess.run(cmd, text=True, capture_output=True)
        return proc, json.loads(out.read_text(encoding="utf-8"))


def test_clean_automix_go_passes_listener_gate_not_release() -> None:
    proc, out = run(base_result(), clean_plan(), pass_c(), automix())
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert out["status"] == "LISTENER_QC_GO"
    assert out["listener_qc_go"] is True
    assert out["downstream_release_gate_may_consume"] is True
    assert out["release_authority"] is False


def test_clean_immutable_source_go_does_not_require_automix_receipt() -> None:
    r = base_result("IMMUTABLE_SOURCE_MASTER")
    proc, out = run(r, clean_plan(), pass_c(), None)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert out["status"] == "LISTENER_QC_GO"


def test_automix_go_without_eligibility_holds() -> None:
    proc, out = run(base_result(), clean_plan(), pass_c(), None)
    assert proc.returncode != 0
    assert "AUTOMIX_ELIGIBILITY_RECEIPT_REQUIRED" in out["errors"]


def test_open_fourth_note_gate_blocks_go() -> None:
    r = base_result(); r["open_release_gates"]["scene3_fourth_note_perceptual_lock"] = "OPEN"
    proc, out = run(r, clean_plan(), pass_c(), automix())
    assert proc.returncode != 0
    assert "RELEASE_GATE_OPEN:scene3_fourth_note_perceptual_lock" in out["errors"]


def test_believability_borderline_blocks_go() -> None:
    r = base_result(); r["final_verdict"]["believability"] = "BORDERLINE"
    proc, out = run(r, clean_plan(), pass_c(), automix())
    assert proc.returncode != 0
    assert "GO_REQUIRES_BELIEVABILITY_BELIEVE" in out["errors"]


def test_non_keep_defect_blocks_go() -> None:
    r = base_result(); r["defects"] = [{"defect_id":"D7","status":"REPAIR"}]
    proc, out = run(r, clean_plan(), pass_c(), automix())
    assert proc.returncode != 0
    assert any(x.startswith("NON_KEEP_DEFECT_BLOCKS_GO:D7") for x in out["errors"])


def test_pass_c_target_mismatch_blocks_go() -> None:
    pc = pass_c(); pc["target_sha256"] = "b" * 64
    proc, out = run(base_result(), clean_plan(), pc, automix())
    assert proc.returncode != 0
    assert "PASS_C_TARGET_SHA_MISMATCH" in out["errors"]


def test_incomplete_mobile_translation_blocks_go() -> None:
    r = base_result(); r["blind_listen"]["pass_c_translation_playback"]["mobile_proxy"] = "NOT_RUN"
    proc, out = run(r, clean_plan(), pass_c(), automix())
    assert proc.returncode != 0
    assert "PASS_C_PLAYBACK_NOT_PASS:mobile_proxy" in out["errors"]


def test_repair_verdict_can_exit_before_pass_c_when_plan_has_local_repairs() -> None:
    r = base_result(); r["final_verdict"] = {"believability":"BORDERLINE","release_status":"REPAIR","reason":"One localized AI-audible line needs repair."}
    plan = clean_plan(); plan["status"] = "REPAIR_PLAN_READY"; plan["repairs"] = [{"patch_id":"P003B_D1"}]
    proc, out = run(r, plan, None, automix())
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert out["status"] == "LISTENER_QC_REPAIR"
    assert out["release_authority"] is False


def test_no_go_can_exit_after_frozen_pass_a_without_pass_c() -> None:
    r = base_result(); r["final_verdict"] = {"believability":"DONT_BELIEVE","release_status":"NO_GO","reason":"Actor performance is not credible."}
    proc, out = run(r, None, None, automix())
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert out["status"] == "LISTENER_QC_NO_GO"
    assert out["listener_qc_go"] is False


def test_hold_never_passes() -> None:
    r = base_result(); r["final_verdict"] = {"believability":None,"release_status":"HOLD","reason":"Human listen not finished."}
    proc, out = run(r, clean_plan(), pass_c(), automix())
    assert proc.returncode != 0
    assert out["status"] == "HOLD"


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
