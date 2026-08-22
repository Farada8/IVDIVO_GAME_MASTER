#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GATE = ROOT / "AUDIO_PRODUCTION/ROOM917/TOOLS/POST_RENDER_ENGINEERING_v2/sound_asset_binding_gate.py"
CONTRACT = ROOT / "AUDIO_PRODUCTION/ROOM917/SOUND_DESIGN/ROOM917_E01_CURRENT_BRANCH_SOUND_ASSET_CONTRACT_v1.json"
IDENTITY = ROOT / "AUDIO_PRODUCTION/ROOM917/SOUND_DESIGN/ROOM917_E01_EN_RU_SHARED_SOUND_IDENTITY_MAP_v1.json"


def write_wav(path: Path, seconds: float = 0.05) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = int(48000 * seconds)
    silence_frame = (0).to_bytes(3, "little", signed=True) * 2
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(3)
        w.setframerate(48000)
        w.writeframes(silence_frame * frames)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate(asset_id: str, path: Path, *, audition: str = "PASS", mono: str = "PASS", phone: str = "PASS") -> dict:
    return {
        "asset_id": asset_id,
        "candidate_id": f"TEST__{asset_id}",
        "path": str(path),
        "sha256": sha256(path),
        "size_bytes": path.stat().st_size,
        "sample_rate_hz": 48000,
        "bit_depth": 24,
        "channels": 2,
        "gain_db": -12.0,
        "audition_status": audition,
        "mono_status": mono,
        "phone_proxy_status": phone,
        "loop_seam_status": "PASS",
        "false_clue_audit_status": "PASS",
    }


def run_gate(candidates: dict, work: Path) -> tuple[subprocess.CompletedProcess[str], dict, dict, dict]:
    cpath = work / "candidates.json"
    out = work / "bindings.json"
    shared_out = work / "shared_bindings.json"
    report = work / "report.json"
    cpath.write_text(json.dumps({"candidates": candidates}, indent=2) + "\n", encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            str(GATE),
            "--contract", str(CONTRACT),
            "--candidates", str(cpath),
            "--out-bindings", str(out),
            "--report", str(report),
            "--shared-map", str(IDENTITY),
            "--out-shared-bindings", str(shared_out),
        ],
        text=True,
        capture_output=True,
    )
    assert out.exists(), proc.stdout + proc.stderr
    assert report.exists(), proc.stdout + proc.stderr
    assert shared_out.exists(), proc.stdout + proc.stderr
    return (
        proc,
        json.loads(out.read_text(encoding="utf-8")),
        json.loads(report.read_text(encoding="utf-8")),
        json.loads(shared_out.read_text(encoding="utf-8")),
    )


def test_atomic_hold_blocks_all_renderer_bindings() -> None:
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        a = work / "s10.wav"
        b = work / "s13.wav"
        write_wav(a)
        write_wav(b)
        payload = {
            "S10_SELECTOR_916": candidate("S10_SELECTOR_916", a),
            "S13_INTERNAL_DOUBLE_RING_OLD": candidate("S13_INTERNAL_DOUBLE_RING_OLD", b, audition="HOLD"),
        }
        proc, bindings, report, shared = run_gate(payload, work)
        assert proc.returncode != 0, proc.stdout + proc.stderr
        assert report["status"] == "HOLD"
        assert bindings == {}, "atomic gate leaked partial renderer bindings"
        assert shared == {}, "shared identity leaked while source binding set was HOLD"
        statuses = {row["asset_id"]: row["status"] for row in report["rows"]}
        assert statuses["S10_SELECTOR_916"] == "PASS"
        assert statuses["S13_INTERNAL_DOUBLE_RING_OLD"] == "HOLD"
        assert report["renderer_bindings_suppressed_on_hold"] is True


def test_shared_identity_emitted_only_after_atomic_pass() -> None:
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        a = work / "s10.wav"
        b = work / "s13.wav"
        write_wav(a)
        write_wav(b)
        payload = {
            "S10_SELECTOR_916": candidate("S10_SELECTOR_916", a),
            "S13_INTERNAL_DOUBLE_RING_OLD": candidate("S13_INTERNAL_DOUBLE_RING_OLD", b),
        }
        proc, bindings, report, shared = run_gate(payload, work)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert report["status"] == "PASS"
        assert "S10_SELECTOR_916" in bindings
        assert "S13_INTERNAL_DOUBLE_RING_OLD" in bindings
        assert "NORMAL_916_SELECTOR_CLACK" in shared
        assert "IMPOSSIBLE_INTERNAL_DOUBLE_RING" in shared
        assert shared["NORMAL_916_SELECTOR_CLACK"]["sha256"] == bindings["S10_SELECTOR_916"]["sha256"]
        assert shared["IMPOSSIBLE_INTERNAL_DOUBLE_RING"]["sha256"] == bindings["S13_INTERNAL_DOUBLE_RING_OLD"]["sha256"]
        assert "NORMAL_916_SELECTOR_CLACK" in report["shared_byte_bindings_emitted"]
        assert "IMPOSSIBLE_INTERNAL_DOUBLE_RING" in report["shared_byte_bindings_emitted"]


def main() -> int:
    tests = [
        test_atomic_hold_blocks_all_renderer_bindings,
        test_shared_identity_emitted_only_after_atomic_pass,
    ]
    failures = []
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:  # noqa: BLE001
            failures.append((test.__name__, repr(exc)))
            print(f"FAIL {test.__name__}: {exc}")
    if failures:
        return 1
    print(f"PASS all={len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
