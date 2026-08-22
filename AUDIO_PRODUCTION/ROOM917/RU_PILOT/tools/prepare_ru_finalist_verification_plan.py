#!/usr/bin/env python3
"""Prepare a coverage-minimal ROOM917 RU finalist verification plan.

No provider call. No spend. The planner consumes real S0 receipt + human S0
screening and selects only evidence still required for CAST LOCK.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
DIAGNOSTIC_IDS = {
    "21m00Tcm4TlvDq8ikWAM": "ELENA",
    "pNInz6obpgDQGcFmaJgB": "JULIAN",
    "XrExE9yKIg1WjnnlVkGX": "MINA",
    "EXAVITQu4vr4xnSDxMaL": "CATE",
}
ALWAYS = {
    "RU_FV_ELENA_REPEAT",
    "RU_FV_JULIAN_REPEAT",
    "RU_FV_MINA_REPEAT",
    "RU_FV_CATE_REPEAT",
    "RU_FV_ELENA_JULIAN_STATUS",
    "RU_FV_CATE_DOMESTIC",
}
S0_PAIR_TO_FV = {
    "RU_S0_ELENA_MINA_RELATION": "RU_FV_ELENA_MINA_RELATION",
    "RU_S0_ELENA_JULIAN_FRICTION": "RU_FV_ELENA_JULIAN_FRICTION",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit("FAIL_FINALIST_PLAN_GATE: " + msg)


def is_sha256(value: object) -> bool:
    s = str(value or "")
    return len(s) == 64 and all(c in "0123456789abcdefABCDEF" for c in s)


def bind_block(block: dict[str, Any], bound: dict[str, str]) -> dict[str, Any]:
    out = copy.deepcopy(block)
    if out.get("voice_id"):
        old = str(out["voice_id"])
        role = DIAGNOSTIC_IDS.get(old)
        require(role is not None, f"unknown template voice id {old}")
        out["voice_id"] = bound[role]
    for turn in out.get("turns") or []:
        old = str(turn.get("voice_id") or "")
        role = DIAGNOSTIC_IDS.get(old)
        require(role is not None, f"unknown template turn voice id {old}")
        turn["voice_id"] = bound[role]
    if isinstance(out.get("voice_settings"), dict):
        vs = out["voice_settings"]
        vs.pop("similarity_boost", None)
        vs.pop("use_speaker_boost", None)
        vs.pop("speed", None)
        if "style" in vs:
            vs["style"] = 0.0
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--s0-receipt", type=Path, required=True)
    ap.add_argument("--screening", type=Path, required=True)
    ap.add_argument("--bindings", type=Path, required=True)
    ap.add_argument("--template", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    for p in (args.s0_receipt, args.screening, args.bindings, args.template):
        require(p.exists(), f"missing file: {p}")

    s0 = load(args.s0_receipt)
    screening = load(args.screening)
    bindings = load(args.bindings)
    template = load(args.template)

    require(s0.get("stage_semantics") == "S0_SCREENING_ONLY_NOT_CAST_LOCK", "S0 receipt stage semantics mismatch")
    require(s0.get("cast_locked") is False and s0.get("full_episode_rendered") is False, "S0 receipt illegally claims lock/full episode")
    require(screening.get("status") == "S0_SCREENING_PASS_TO_FINALIST_VERIFICATION", "screening must PASS_TO_FINALIST_VERIFICATION")
    require(screening.get("s0_canary_receipt_sha256") == digest(args.s0_receipt), "screening/S0 receipt hash mismatch")
    require(screening.get("pre_canary_bindings_sha256") == digest(args.bindings), "screening/bindings hash mismatch")
    require(screening.get("cast_lock") is False and screening.get("full_e01_render_allowed") is False, "screening cannot grant lock/full E01")
    require(bindings.get("status") == "PAID_S0_AUTHORIZED", "bindings status mismatch")
    require(bindings.get("canary_binding_only") is True, "bindings must remain canary-only")
    require(bindings.get("cast_lock") is False, "bindings cannot be cast lock")

    bound: dict[str, str] = {}
    for role in ROLES:
        b = (bindings.get("roles") or {}).get(role) or {}
        r = (screening.get("roles") or {}).get(role) or {}
        voice_id = str(b.get("voice_id") or "")
        require(bool(voice_id), f"{role}: missing bound voice id")
        require(str(r.get("voice_id") or "") == voice_id, f"{role}: screening voice differs from bindings")
        require(r.get("screening") == "PASS", f"{role}: S0 screening not PASS")
        require(r.get("founder_screening") == "YES", f"{role}: Founder S0 screening not YES")
        require(not (r.get("hard_reject_flags") or []), f"{role}: hard reject present")
        require(float(r.get("believability_0_5", -1)) >= 4, f"{role}: believability <4")
        require(float(r.get("russian_naturalness_0_5", -1)) >= 4, f"{role}: Russian naturalness <4")
        require(float(r.get("character_fit_0_5", -1)) >= 4, f"{role}: character fit <4")
        require(is_sha256(r.get("audio_sha256")), f"{role}: missing real S0 audio sha256")
        bound[role] = voice_id

    rendered = set(s0.get("selected_block_ids") or [])
    selected_ids = set(ALWAYS)
    pair = screening.get("pair_evidence") or {}

    em = pair.get("ELENA_MINA") or {}
    if "RU_S0_ELENA_MINA_RELATION" in rendered:
        require(em.get("rendered") is True, "ELENA_MINA rendered in S0 but screening says not rendered")
        require(em.get("screening") == "PASS", "ELENA_MINA rendered S0 pair must PASS or recast/repair before finalist")
        require(is_sha256(em.get("audio_sha256")), "ELENA_MINA accepted S0 pair missing sha256")
    else:
        selected_ids.add(S0_PAIR_TO_FV["RU_S0_ELENA_MINA_RELATION"])

    ej1 = pair.get("ELENA_JULIAN_1") or {}
    if "RU_S0_ELENA_JULIAN_FRICTION" in rendered:
        require(ej1.get("rendered") is True, "ELENA_JULIAN_1 rendered in S0 but screening says not rendered")
        require(ej1.get("screening") == "PASS", "ELENA_JULIAN_1 rendered S0 pair must PASS or recast/repair before finalist")
        require(is_sha256(ej1.get("audio_sha256")), "ELENA_JULIAN_1 accepted S0 pair missing sha256")
    else:
        selected_ids.add(S0_PAIR_TO_FV["RU_S0_ELENA_JULIAN_FRICTION"])

    blocks_by_id = {str(b.get("block_id")): b for b in template.get("blocks") or []}
    require(selected_ids <= set(blocks_by_id), "finalist template missing required block(s)")
    ordered = [bind_block(b, bound) for b in template.get("blocks") or [] if b.get("block_id") in selected_ids]
    required = len(ordered)
    require(required in (6, 7, 8), f"unexpected finalist block count {required}")

    out = {
        "schema_version": "ivdivo.room917_ru_finalist_verification_plan/1.0",
        "status": "READY_FOR_FINALIST_SPEND_AUTHORIZATION",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "model_id": "eleven_v3",
        "s0_receipt_sha256": digest(args.s0_receipt),
        "s0_screening_sha256": digest(args.screening),
        "bindings_sha256": digest(args.bindings),
        "template_sha256": digest(args.template),
        "runtime_voice_bindings": bound,
        "s0_accepted_pair_evidence": {
            "ELENA_MINA": em if em.get("screening") == "PASS" else None,
            "ELENA_JULIAN_1": ej1 if ej1.get("screening") == "PASS" else None,
        },
        "required_block_count": required,
        "selected_block_ids": [b["block_id"] for b in ordered],
        "blocks": ordered,
        "provider_call_made": False,
        "provider_spend_made": False,
        "cast_lock": False,
        "full_e01_render_allowed": False,
        "next": "EXPLICIT_FINALIST_VERIFICATION_SPEND_AUTHORIZATION",
        "hard_rules": [
            "NO_DUPLICATE_ACCEPTED_S0_PAIR_RENDER",
            "NO_PROVIDER_CALL_FROM_PLAN_COMPILER",
            "NO_CAST_LOCK_FROM_PLAN",
            "NO_FULL_E01_RENDER"
        ]
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": out["status"], "required_block_count": required, "selected_block_ids": out["selected_block_ids"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
