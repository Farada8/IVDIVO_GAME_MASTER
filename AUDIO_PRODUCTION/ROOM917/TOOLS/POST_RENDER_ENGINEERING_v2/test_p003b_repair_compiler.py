#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPILER = HERE / "p003b_repair_compiler.py"


def base_result() -> dict:
    return {
        "schema_version": "ivdivo.room917_p003b_listener_qc_result/1.2",
        "project": "ROOM917",
        "episode": "E01",
        "authority": "THE_INSURABLE_FIRE",
        "source_identity": {
            "expected_duration_seconds": 658.190,
            "target_identity_mode": "IMMUTABLE_SOURCE_MASTER",
            "allowed_target_identity_mode": ["IMMUTABLE_SOURCE_MASTER", "PROVENANCE_VERIFIED_DERIVED_CANDIDATE"],
            "observed_sha256": "a" * 64,
            "identity_status": "VERIFIED",
        },
        "blind_listen": {
            "pass_a_story_free": "COMPLETE",
            "pass_a_notes_frozen": True,
            "pass_b_targeted_verification": "COMPLETE",
        },
        "defects": [],
    }


def defect(**overrides) -> dict:
    d = {
        "defect_id": "D001",
        "start_seconds": 100.0,
        "end_seconds": 101.2,
        "question_class": "GEOGRAPHY",
        "severity": "MAJOR",
        "confidence": "HIGH",
        "heard": "Actor position collapses to center during movement.",
        "scene_failure": "Movement geography becomes ambiguous.",
        "failure_layer": "MIX",
        "smallest_repair_scope": "100.000-101.200 actor placement automation only",
        "minimal_fix": "Restore the established lateral position without changing dialogue take.",
        "do_not_touch": ["DIALOGUE_TAKE", "STORY_TEXT", "SCENE3"],
        "regression_tests": ["STEREO_POSITION", "MONO_INTELLIGIBILITY"],
        "status": "REPAIR",
    }
    d.update(overrides)
    return d


def run(payload: dict) -> tuple[subprocess.CompletedProcess[str], dict]:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        src = td / "result.json"
        out = td / "plan.json"
        src.write_text(json.dumps(payload), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(COMPILER), "--result", str(src), "--out", str(out)], text=True, capture_output=True)
        return proc, json.loads(out.read_text(encoding="utf-8"))


def test_valid_mix_defect_compiles_local_patch() -> None:
    p = base_result(); p["defects"] = [defect()]
    proc, out = run(p)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert out["status"] == "REPAIR_PLAN_READY"
    assert len(out["repairs"]) == 1
    r = out["repairs"][0]
    assert r["action"] == "LOCAL_MIX_PATCH"
    assert r["start_seconds"] == 100.0 and r["end_seconds"] == 101.2
    assert out["whole_episode_rerender_authorized"] is False
    assert out["release_authorized"] is False


def test_unknown_layer_is_hold_not_patch() -> None:
    p = base_result(); p["defects"] = [defect(failure_layer="UNKNOWN")]
    proc, out = run(p)
    assert proc.returncode != 0
    assert out["repairs"] == []
    assert any("UNKNOWN_FAILURE_LAYER_REQUIRES_LISTEN_OR_DIAGNOSIS" in h["reasons"] for h in out["holds"])


def test_broad_scope_is_forbidden() -> None:
    p = base_result(); p["defects"] = [defect(smallest_repair_scope="whole episode full rerender")]
    proc, out = run(p)
    assert proc.returncode != 0
    assert out["repairs"] == []
    assert any("BROAD_SCOPE_FORBIDDEN" in h["reasons"] for h in out["holds"])


def test_identity_unverified_blocks_all() -> None:
    p = base_result(); p["source_identity"]["identity_status"] = "UNVERIFIED"; p["defects"] = [defect()]
    proc, out = run(p)
    assert proc.returncode != 0
    assert out["repairs"] == []
    assert "SOURCE_IDENTITY_NOT_VERIFIED" in out["gate_errors"]


def test_pass_a_must_be_frozen() -> None:
    p = base_result(); p["blind_listen"]["pass_a_notes_frozen"] = False; p["defects"] = [defect()]
    proc, out = run(p)
    assert proc.returncode != 0
    assert out["repairs"] == []
    assert "PASS_A_NOTES_NOT_FROZEN" in out["gate_errors"]


def test_keep_is_ignored() -> None:
    p = base_result(); p["defects"] = [defect(status="KEEP")]
    proc, out = run(p)
    assert proc.returncode == 0
    assert out["status"] == "NO_REPAIR_REQUESTED"
    assert out["repairs"] == []
    assert out["ignored_keep_defects"] == ["D001"]


def test_fatal_never_auto_compiles() -> None:
    p = base_result(); p["defects"] = [defect(severity="FATAL")]
    proc, out = run(p)
    assert proc.returncode != 0
    assert out["repairs"] == []
    assert any("FATAL_REQUIRES_MANUAL_REOPEN_OR_EXPLICIT_REPAIR_AUTHORITY" in h["reasons"] for h in out["holds"])


def test_scene3_direct_audible_local_mix_defect_can_compile_without_reopening_story() -> None:
    p = base_result(); p["defects"] = [defect(start_seconds=500.0, end_seconds=500.4, defect_id="S3R01", question_class="SFX_MASKING", heard="A transient masks one consonant in the identified current master.", scene_failure="One clue word becomes unclear.", smallest_repair_scope="500.000-500.400 SFX gain automation only", minimal_fix="Reduce only the masking transient under the word.", do_not_touch=["SCENE3_DIALOGUE_TAKE","SCENE3_TIMING","STORY_TEXT"])]
    proc, out = run(p)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert out["status"] == "REPAIR_PLAN_READY"
    assert out["repairs"][0]["action"] == "LOCAL_MIX_PATCH"
    assert out["story_rewrite_authorized"] is False


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
