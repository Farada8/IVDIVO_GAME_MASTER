#!/usr/bin/env python3
"""Compile a ROOM917 RU bindings *candidate* from completed human review.

This tool cannot authorize paid synthesis. Its strongest possible output status
is READY_FOR_PAID_CANARY_AUTHORIZATION with founder_paid_canary_authorized=false.
A separate explicit authorization step is still required before the existing
paid S0 workflow will accept bindings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
PAIR_TESTS = (
    "RU_PAIR_01_ELENA_MINA_LOBBY",
    "RU_PAIR_02_ELENA_JULIAN_DOORS",
    "RU_PAIR_03_ELENA_JULIAN_STATUS",
    "RU_PAIR_04_CATE_LINE_VS_CASSETTE",
)
ROLE_PASS_FIELDS = (
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


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL_RU_CAST_REVIEW_GATE: " + message)


def role_candidates(shortlist: dict[str, Any], role: str) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("voice_id")): row
        for row in (shortlist.get("roles") or {}).get(role) or []
        if row.get("voice_id")
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider-snapshot", type=Path, required=True)
    ap.add_argument("--shortlist", type=Path, required=True)
    ap.add_argument("--review", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    for path in (args.provider_snapshot, args.shortlist, args.review):
        require(path.exists(), f"missing required file: {path}")

    snapshot = load(args.provider_snapshot)
    shortlist = load(args.shortlist)
    review = load(args.review)

    snapshot_hash = sha256(args.provider_snapshot)
    shortlist_hash = sha256(args.shortlist)

    require(snapshot.get("status") == "PASS_CANDIDATES_FOUND", "provider snapshot must PASS_CANDIDATES_FOUND")
    require(shortlist.get("status") == "READY_FOR_PREVIEW_LISTEN_NOT_BINDINGS", "shortlist must be READY_FOR_PREVIEW_LISTEN_NOT_BINDINGS")
    require(shortlist.get("provider_snapshot", {}).get("sha256") == snapshot_hash, "shortlist/provider snapshot hash mismatch")
    require(review.get("status") == "REVIEW_COMPLETE", "review status must be REVIEW_COMPLETE")
    require(review.get("provider_snapshot_sha256") == snapshot_hash, "review/provider snapshot hash mismatch")
    require(review.get("shortlist_proposal_sha256") == shortlist_hash, "review/shortlist hash mismatch")
    require(review.get("pronunciation_gate") == "PASS", "pronunciation_gate must PASS")
    require(review.get("all_selected_voice_ids_unique") == "PASS", "all_selected_voice_ids_unique must PASS")
    require(review.get("paid_s0_authorized") is False, "review must not contain paid authorization")
    require(review.get("cast_lock") is False, "review must not claim CAST LOCK")
    require(review.get("full_e01_render_allowed") is False, "review must not claim full E01 permission")

    for pair_id in PAIR_TESTS:
        require((review.get("pair_tests") or {}).get(pair_id) == "PASS", f"pair test {pair_id} must PASS")

    selected: dict[str, dict[str, Any]] = {}
    selected_ids: list[str] = []
    for role in ROLES:
        review_row = (review.get("roles") or {}).get(role) or {}
        voice_id = str(review_row.get("selected_voice_id") or "")
        require(bool(voice_id), f"{role}: selected_voice_id missing")
        shortlist_rows = role_candidates(shortlist, role)
        require(voice_id in shortlist_rows, f"{role}: selected voice absent from sealed shortlist")
        candidate = shortlist_rows[voice_id]

        for field in ROLE_PASS_FIELDS:
            require(review_row.get(field) == "PASS", f"{role}: {field} must PASS")
        score = review_row.get("score_0_30")
        require(isinstance(score, (int, float)) and not isinstance(score, bool), f"{role}: score_0_30 missing")
        require(float(score) >= 24.0, f"{role}: score {score} below 24/30")
        require(review_row.get("hard_reject") is False, f"{role}: hard_reject must be false")
        require(candidate.get("ru_verified") is True, f"{role}: shortlist candidate no longer carries ru_verified=true")
        require(candidate.get("binding_eligible") is False, f"{role}: shortlist must remain non-binding review artifact")

        selected_ids.append(voice_id)
        selected[role] = {
            "voice_id": voice_id,
            "provider_name": candidate.get("provider_name") or review_row.get("provider_name"),
            "preview_listen": "PASS",
            "provider_identity_check": "PASS",
            "selection_note": f"Human review PASS {score}/30; Founder credibility PASS; binding candidate only, paid authorization still false.",
            "review_score_0_30": score,
            "provider_notice_period": candidate.get("notice_period"),
            "provider_disable_at_unix": candidate.get("disable_at_unix"),
        }

    require(len(set(selected_ids)) == len(ROLES), "selected voice IDs must be unique across four roles")

    out = {
        "schema_version": "ivdivo.room917_ru_s0_native_bindings/1.1",
        "status": "READY_FOR_PAID_CANARY_AUTHORIZATION",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "provider": "ElevenLabs",
        "model_id": "eleven_v3",
        "provider_snapshot_path": str(args.provider_snapshot),
        "provider_snapshot_sha256": snapshot_hash,
        "shortlist_path": str(args.shortlist),
        "shortlist_sha256": shortlist_hash,
        "review_path": str(args.review),
        "review_sha256": sha256(args.review),
        "roles": selected,
        "all_pair_tests": "PASS",
        "pronunciation_gate": "PASS",
        "founder_credibility_gate": "PASS",
        "founder_paid_canary_authorized": False,
        "paid_s0_authorized": False,
        "cast_lock": False,
        "full_episode_render_allowed": False,
        "authorization_rule": "A separate explicit founder spend authorization must create the final PAID_S0_AUTHORIZED bindings artifact. This compiler cannot do so.",
        "next": "EXPLICIT_FOUNDER_PAID_CANARY_AUTHORIZATION_OR_STOP"
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "roles": {role: out["roles"][role]["voice_id"] for role in ROLES},
        "founder_paid_canary_authorized": False,
        "cast_lock": False,
        "out": str(args.out)
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
