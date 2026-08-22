#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED_ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
REQUIRED_PAIR_KEYS = {
    "ELENA": (),
    "JULIAN": ("ELENA_JULIAN_1", "ELENA_JULIAN_2"),
    "MINA": ("ELENA_MINA",),
    "CATE": ("CATE_IDENTITY",),
}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_ru_cast_lock.py <receipt.json>")

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))

    require(data.get("project_id") == "ROOM917", "wrong project_id")
    require(data.get("locale") == "ru-RU", "wrong locale")
    roles = data.get("roles") or {}

    all_locked = True
    for role in REQUIRED_ROLES:
        r = roles.get(role)
        if not isinstance(r, dict):
            all_locked = False
            continue

        require(r.get("role") == role, f"{role}: role mismatch")
        require(r.get("provider") == "ElevenLabs", f"{role}: provider must be ElevenLabs")
        require(isinstance(r.get("voice_id"), str) and r["voice_id"].strip(), f"{role}: missing voice_id")
        require(r.get("verified_language") == "ru", f"{role}: Russian not provider-verified")
        require(int(r.get("notice_period_days", 0)) >= 365, f"{role}: notice period < 365 days")
        require(r.get("model_id") == "eleven_v3", f"{role}: wrong model")
        require(float(r.get("individual_score_raw", -1)) >= 24, f"{role}: individual score < 24")
        require(float(r.get("naturalism_score", -1)) >= 4, f"{role}: naturalism < 4")
        require(float(r.get("pronunciation_score", -1)) >= 4, f"{role}: pronunciation < 4")
        require(r.get("founder_credibility") == "YES", f"{role}: founder credibility is not YES")
        require(bool(r.get("provider_identity_verified_at")), f"{role}: provider identity timestamp missing")
        require(bool(r.get("locked_at")), f"{role}: locked_at missing")

        canaries = r.get("accepted_canary_ids") or []
        hashes = r.get("accepted_canary_sha256") or []
        require(len(canaries) >= 2, f"{role}: fewer than two accepted canaries/takes")
        require(len(hashes) >= 2, f"{role}: fewer than two accepted hashes")
        require(len(canaries) == len(hashes), f"{role}: canary/hash count mismatch")
        for h in hashes:
            require(isinstance(h, str) and len(h) == 64 and all(c in "0123456789abcdefABCDEF" for c in h), f"{role}: invalid sha256")

        pair = r.get("pair_tests") or {}
        for key in REQUIRED_PAIR_KEYS[role]:
            require(pair.get(key) == "PASS", f"{role}: pair gate {key} not PASS")

        flags = r.get("hard_reject_flags") or []
        require(len(flags) == 0, f"{role}: hard reject flags present")

    global_gate = data.get("global_lock_gate") or {}
    require(all_locked, "one or more roles are not populated")
    require(global_gate.get("provider_snapshot_status") == "PASS_CANDIDATES_FOUND", "provider snapshot not PASS_CANDIDATES_FOUND")
    require(global_gate.get("all_four_roles_locked") is True, "all_four_roles_locked must be true")
    require(global_gate.get("all_provider_ids_resolve") is True, "provider IDs not all verified")
    require(global_gate.get("all_required_pair_tests_pass") is True, "pair tests not all passed")
    require(global_gate.get("all_founder_credibility_yes") is True, "founder credibility not all YES")
    require(global_gate.get("full_e01_dialogue_render_allowed") is True, "full E01 dialogue render gate not opened")
    require(data.get("status") == "LOCKED", "receipt status must be LOCKED")

    print("PASS: ROOM917 RU CAST LOCK receipt is internally valid")


if __name__ == "__main__":
    main()
