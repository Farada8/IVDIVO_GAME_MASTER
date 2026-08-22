#!/usr/bin/env python3
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_ru_cast_lock.py"


def role(role, pair_tests):
    return {
        "role": role,
        "provider": "ElevenLabs",
        "voice_id": f"TEST_{role}_VOICE_ID",
        "provider_voice_name": f"TEST {role}",
        "verified_language": "ru",
        "category": "professional",
        "notice_period_days": 365,
        "disable_at": None,
        "model_id": "eleven_v3",
        "voice_settings": {},
        "accepted_canary_ids": [f"{role}_TAKE_A", f"{role}_TAKE_B"],
        "accepted_canary_sha256": ["a" * 64, "b" * 64],
        "individual_score_raw": 26,
        "naturalism_score": 4.5,
        "pronunciation_score": 5,
        "pair_tests": pair_tests,
        "hard_reject_flags": [],
        "founder_credibility": "YES",
        "provider_identity_verified_at": "2099-01-01T00:00:00Z",
        "locked_at": "2099-01-01T00:00:00Z"
    }


def valid_receipt():
    return {
        "schema_version": "ivdivo.room917_ru_cast_lock_receipt/1.0",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "status": "LOCKED",
        "test_only": True,
        "roles": {
            "ELENA": role("ELENA", {}),
            "JULIAN": role("JULIAN", {"ELENA_JULIAN_1": "PASS", "ELENA_JULIAN_2": "PASS"}),
            "MINA": role("MINA", {"ELENA_MINA": "PASS"}),
            "CATE": role("CATE", {"CATE_IDENTITY": "PASS"})
        },
        "global_lock_gate": {
            "provider_snapshot_status": "PASS_CANDIDATES_FOUND",
            "all_four_roles_locked": True,
            "all_provider_ids_resolve": True,
            "all_required_pair_tests_pass": True,
            "all_founder_credibility_yes": True,
            "full_e01_dialogue_render_allowed": True
        }
    }


def run(data):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "receipt.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        return subprocess.run([sys.executable, str(VALIDATOR), str(p)], capture_output=True, text=True)


def main():
    good = valid_receipt()
    r = run(good)
    assert r.returncode == 0, r.stdout + r.stderr

    bad = copy.deepcopy(good)
    bad["roles"]["ELENA"]["naturalism_score"] = 3.5
    assert run(bad).returncode != 0

    bad = copy.deepcopy(good)
    bad["roles"]["JULIAN"]["pair_tests"]["ELENA_JULIAN_1"] = "FAIL"
    assert run(bad).returncode != 0

    bad = copy.deepcopy(good)
    bad["roles"]["CATE"]["founder_credibility"] = "BORDERLINE"
    assert run(bad).returncode != 0

    bad = copy.deepcopy(good)
    bad["global_lock_gate"]["provider_snapshot_status"] = "HOLD_PROVIDER_AUTH_REQUIRED"
    assert run(bad).returncode != 0

    print("PASS: RU cast-lock validator positive and fail-closed tests")


if __name__ == "__main__":
    main()
