#!/usr/bin/env python3
"""Compile a ROOM917 RU CAST LOCK receipt from proved provider/review/take evidence.

This tool performs no listening, no provider calls, no TTS synthesis and no spend
authorization. It cannot infer missing human judgments or numeric scores. It only
converts already proved inputs into the lock receipt consumed by
validate_ru_cast_lock.py.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any

ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
PAIR_BY_ROLE = {
    "ELENA": (),
    "JULIAN": ("RU_PAIR_02_ELENA_JULIAN_DOORS", "RU_PAIR_03_ELENA_JULIAN_STATUS"),
    "MINA": ("RU_PAIR_01_ELENA_MINA_LOBBY",),
    "CATE": ("RU_PAIR_04_CATE_LINE_VS_CASSETTE",),
}
PAIR_SHORT = {
    "RU_PAIR_01_ELENA_MINA_LOBBY": "ELENA_MINA",
    "RU_PAIR_02_ELENA_JULIAN_DOORS": "ELENA_JULIAN_1",
    "RU_PAIR_03_ELENA_JULIAN_STATUS": "ELENA_JULIAN_2",
    "RU_PAIR_04_CATE_LINE_VS_CASSETTE": "CATE_IDENTITY",
}
REVIEW_PASS_FIELDS = (
    "preview_listen",
    "provider_identity_check",
    "native_ru_pronunciation",
    "age_character_fit",
    "naturalism",
    "microemotion_subtext",
    "precision_under_pressure",
    "repeat_take_identity_consistency",
    "founder_credibility",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected object in {path}")
    return data


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def valid_sha(value: object) -> bool:
    text = str(value or "")
    return len(text) == 64 and all(c in "0123456789abcdefABCDEF" for c in text)


def numeric_score(row: dict[str, Any], key: str, minimum: float, maximum: float, role: str) -> float:
    value = row.get(key)
    require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{role}: {key} missing")
    score = float(value)
    require(minimum <= score <= maximum, f"{role}: {key} must be {minimum}..{maximum}")
    return score


def notice_days(row: dict[str, Any]) -> int:
    for key in ("notice_period_days", "notice_period"):
        value = row.get(key)
        if value is None:
            continue
        try:
            return int(float(value))
        except (TypeError, ValueError):
            pass
    return 0


def candidate_index(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("voice_id")): row
        for row in snapshot.get("candidates") or []
        if isinstance(row, dict) and row.get("voice_id")
    }


def selected_take_rows(registry: dict[str, Any], role: str, voice_id: str) -> list[dict[str, Any]]:
    rows = []
    for row in registry.get("records") or []:
        if not isinstance(row, dict):
            continue
        if row.get("selected") is not True:
            continue
        if str(row.get("character") or "") != role:
            continue
        if str(row.get("voice_id") or "") != voice_id:
            continue
        rows.append(row)
    return rows


def normalized_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def compile_receipt(snapshot: dict[str, Any], review: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    require(snapshot.get("status") == "PASS_CANDIDATES_FOUND", "provider snapshot must PASS_CANDIDATES_FOUND")
    require(review.get("status") == "REVIEW_COMPLETE", "review must be REVIEW_COMPLETE")
    require(review.get("pronunciation_gate") == "PASS", "review pronunciation gate must PASS")
    require(review.get("all_selected_voice_ids_unique") == "PASS", "review voice-id uniqueness must PASS")
    require(review.get("paid_s0_authorized") is False, "review must not carry spend authorization")
    require(review.get("cast_lock") is False, "review must not pre-claim CAST LOCK")

    pairs = review.get("pair_tests") or {}
    for pair_id in PAIR_SHORT:
        require(pairs.get(pair_id) == "PASS", f"pair test {pair_id} must PASS")

    candidates = candidate_index(snapshot)
    out_roles: dict[str, Any] = {}
    used_ids: list[str] = []
    locked_at = utc_now()
    provider_verified_at = str(snapshot.get("generated_at") or snapshot.get("created") or "")
    require(bool(provider_verified_at), "provider snapshot timestamp missing")

    for role in ROLES:
        rr = (review.get("roles") or {}).get(role) or {}
        voice_id = str(rr.get("selected_voice_id") or "")
        require(bool(voice_id), f"{role}: selected_voice_id missing")
        require(voice_id in candidates, f"{role}: selected voice absent from provider snapshot")
        cand = candidates[voice_id]
        require(cand.get("ru_verified") is True, f"{role}: provider candidate not ru_verified")
        require(notice_days(cand) >= 365, f"{role}: notice period below 365 days")
        if cand.get("disable_at_unix") is not None:
            require(int(cand.get("disable_at_unix")) > 0, f"{role}: invalid disable_at_unix")

        for field in REVIEW_PASS_FIELDS:
            require(rr.get(field) == "PASS", f"{role}: {field} must PASS")
        score = numeric_score(rr, "score_0_30", 24.0, 30.0, role)
        naturalism_score = numeric_score(rr, "naturalism_score_0_5", 4.0, 5.0, role)
        pronunciation_score = numeric_score(rr, "pronunciation_score_0_5", 4.0, 5.0, role)
        require(rr.get("hard_reject") is False, f"{role}: hard reject present")

        takes = selected_take_rows(registry, role, voice_id)
        require(len(takes) >= 2, f"{role}: fewer than two selected accepted takes")
        unit_ids: list[str] = []
        hashes: list[str] = []
        settings_signatures: set[str] = set()
        for take in takes:
            unit_id = str(take.get("unit_id") or "")
            out_hash = str(take.get("output_sha256") or "")
            require(bool(unit_id), f"{role}: selected take missing unit_id")
            require(valid_sha(out_hash), f"{role}: selected take has invalid output sha256")
            require(take.get("model_id") == "eleven_v3", f"{role}: selected take model must be eleven_v3")
            require(str(take.get("language_code") or "") == "ru", f"{role}: selected take language must be ru")
            qc = take.get("qc") or {}
            require(qc.get("pronunciation") == "PASS", f"{role}: selected take pronunciation not PASS")
            require(qc.get("technical_artifact") == "PASS", f"{role}: selected take technical artifact gate not PASS")
            unit_ids.append(unit_id)
            hashes.append(out_hash)
            settings_signatures.add(normalized_json(take.get("voice_settings") or {}))
        require(len(set(unit_ids)) >= 2, f"{role}: selected evidence must cover at least two distinct canary units")
        require(len(settings_signatures) == 1, f"{role}: selected take voice_settings drift")

        used_ids.append(voice_id)
        pair_payload = {PAIR_SHORT[pair_id]: "PASS" for pair_id in PAIR_BY_ROLE[role]}
        out_roles[role] = {
            "role": role,
            "provider": "ElevenLabs",
            "voice_id": voice_id,
            "provider_voice_name": cand.get("name") or rr.get("provider_name") or "",
            "verified_language": "ru",
            "category": cand.get("category") or "professional",
            "notice_period_days": notice_days(cand),
            "disable_at": cand.get("disable_at_unix"),
            "model_id": "eleven_v3",
            "voice_settings": json.loads(next(iter(settings_signatures))),
            "accepted_canary_ids": unit_ids,
            "accepted_canary_sha256": hashes,
            "individual_score_raw": score,
            "naturalism_score": naturalism_score,
            "pronunciation_score": pronunciation_score,
            "pair_tests": pair_payload,
            "hard_reject_flags": [],
            "founder_credibility": "YES",
            "provider_identity_verified_at": provider_verified_at,
            "locked_at": locked_at,
        }

    require(len(set(used_ids)) == len(ROLES), "voice IDs must be unique across roles")

    return {
        "schema_version": "ivdivo.room917_ru_cast_lock_receipt/1.1",
        "date": locked_at[:10],
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "status": "LOCKED",
        "roles": out_roles,
        "global_lock_gate": {
            "all_four_roles_locked": True,
            "provider_snapshot_status": "PASS_CANDIDATES_FOUND",
            "all_provider_ids_resolve": True,
            "all_required_pair_tests_pass": True,
            "all_founder_credibility_yes": True,
            "full_e01_dialogue_render_allowed": True,
        },
        "execution_boundary": {
            "provider_calls_made_by_compiler": 0,
            "paid_synthesis_calls_made_by_compiler": 0,
            "paid_authorization_created_by_compiler": False,
            "human_listening_simulated": False,
            "story_or_dialogue_changed": False,
        },
        "invariants": [
            "NO_STORY_EDIT",
            "NO_MIX_EDIT",
            "NO_LOCK_FROM_METADATA_ONLY",
            "NO_LOCK_FROM_SINGLE_TAKE",
            "NO_LOCK_WITH_HARD_REJECT_FLAG",
            "NO_PROVIDER_CALL_OR_SPEND_BY_THIS_COMPILER",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider-snapshot", type=Path, required=True)
    ap.add_argument("--review", type=Path, required=True)
    ap.add_argument("--take-registry", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    try:
        receipt = compile_receipt(load(args.provider_snapshot), load(args.review), load(args.take_registry))
    except (ValueError, TypeError, KeyError) as exc:
        print(f"FAIL_RU_CAST_LOCK_COMPILE: {exc}", file=sys.stderr)
        return 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "roles": list(receipt["roles"]), "provider_calls": 0, "paid_synthesis_calls": 0, "out": str(args.out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
