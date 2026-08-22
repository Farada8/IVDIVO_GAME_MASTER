#!/usr/bin/env python3
"""Compile ROOM917 RU pre-canary voice bindings candidate.

This stage deliberately uses provider snapshot + shortlist + human provider-preview
review only. It does NOT require or claim acting, pronunciation-on-script, pair
chemistry, repeat-take, or Founder cast-credibility evidence; those facts can only
exist after bounded canary audio has been generated and listened to.

The strongest output is READY_FOR_PAID_CANARY_AUTHORIZATION. A separate explicit
spend authorization remains required, and CAST LOCK remains false.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
PRE_CANARY_PASS_FIELDS = (
    "preview_listen",
    "provider_identity_check",
    "provider_durability_check",
    "plausible_for_canary",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL_RU_PRE_CANARY_BINDING_GATE: " + message)


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
    ap.add_argument("--review", type=Path, required=True, help="PRE-CANARY provider-preview review")
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
    require(review.get("status") == "PRE_CANARY_REVIEW_COMPLETE", "review status must be PRE_CANARY_REVIEW_COMPLETE")
    require(review.get("provider_snapshot_sha256") == snapshot_hash, "review/provider snapshot hash mismatch")
    require(review.get("shortlist_proposal_sha256") == shortlist_hash, "review/shortlist hash mismatch")
    require(review.get("all_selected_voice_ids_unique") == "PASS", "all_selected_voice_ids_unique must PASS")
    require(review.get("acting_evidence_complete") is False, "pre-canary review must not claim acting evidence complete")
    require(review.get("paid_s0_authorized") is False, "review must not contain paid authorization")
    require(review.get("cast_lock") is False, "review must not claim CAST LOCK")
    require(review.get("full_e01_render_allowed") is False, "review must not claim full E01 permission")

    # These gates are impossible before canary audio exists; reject any attempt to
    # smuggle a post-canary PASS upstream into the provider-preview review.
    require(review.get("pronunciation_canary_gate") in (None, "NOT_RUN_YET"), "pronunciation canary gate must not be pre-passed")
    require(review.get("pair_tests") in (None, "NOT_RUN_YET"), "pair tests must not be pre-passed")
    require(review.get("repeat_take_identity_consistency") in (None, "NOT_RUN_YET"), "repeat-take consistency must not be pre-passed")
    require(review.get("founder_cast_credibility") in (None, "NOT_RUN_YET"), "Founder cast credibility must not be pre-passed")

    selected: dict[str, dict[str, Any]] = {}
    selected_ids: list[str] = []
    for role in ROLES:
        review_row = (review.get("roles") or {}).get(role) or {}
        voice_id = str(review_row.get("selected_voice_id") or "")
        require(bool(voice_id), f"{role}: selected_voice_id missing")
        shortlist_rows = role_candidates(shortlist, role)
        require(voice_id in shortlist_rows, f"{role}: selected voice absent from sealed shortlist")
        candidate = shortlist_rows[voice_id]

        for field in PRE_CANARY_PASS_FIELDS:
            require(review_row.get(field) == "PASS", f"{role}: {field} must PASS")
        require(candidate.get("ru_verified") is True, f"{role}: shortlist candidate does not carry ru_verified=true")
        require(candidate.get("binding_eligible") is False, f"{role}: shortlist must remain non-binding review artifact")
        notice = candidate.get("notice_period")
        require(isinstance(notice, (int, float)) and not isinstance(notice, bool) and float(notice) >= 365, f"{role}: notice period below 365 or missing")
        require(candidate.get("disable_at_unix") in (None, 0, "", "0"), f"{role}: active disable_at_unix blocks canary binding")

        selected_ids.append(voice_id)
        selected[role] = {
            "voice_id": voice_id,
            "provider_name": candidate.get("provider_name") or review_row.get("provider_name"),
            "preview_listen": "PASS",
            "provider_identity_check": "PASS",
            "provider_durability_check": "PASS",
            "plausible_for_canary": "PASS",
            "provider_notice_period": notice,
            "provider_disable_at_unix": candidate.get("disable_at_unix"),
            "canary_binding_only": True,
            "acting_evidence": "NOT_YET_GENERATED",
        }

    require(len(set(selected_ids)) == len(ROLES), "selected voice IDs must be unique across four roles")

    out = {
        "schema_version": "ivdivo.room917_ru_s0_native_bindings_candidate/2.0",
        "status": "READY_FOR_PAID_CANARY_AUTHORIZATION",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "provider": "ElevenLabs",
        "model_id": "eleven_v3",
        "provider_snapshot_path": str(args.provider_snapshot),
        "provider_snapshot_sha256": snapshot_hash,
        "shortlist_path": str(args.shortlist),
        "shortlist_sha256": shortlist_hash,
        "pre_canary_review_path": str(args.review),
        "pre_canary_review_sha256": sha256(args.review),
        "roles": selected,
        "pre_canary_binding_gate": "PASS",
        "canary_binding_only": True,
        "acting_evidence_complete": False,
        "pronunciation_gate": "NOT_RUN_YET",
        "pair_tests": "NOT_RUN_YET",
        "founder_credibility_gate": "NOT_RUN_YET",
        "founder_paid_canary_authorized": False,
        "paid_s0_authorized": False,
        "cast_lock": False,
        "full_episode_render_allowed": False,
        "authorization_rule": "A separate explicit founder spend authorization may authorize bounded S0 canary generation only. Acting evidence and CAST LOCK occur downstream after real canary audio and human listening.",
        "next": "EXPLICIT_FOUNDER_PAID_CANARY_AUTHORIZATION_OR_STOP",
        "hard_rules": [
            "PRE_CANARY_BINDING_IS_NOT_CAST_APPROVAL",
            "NO_ACTING_SCORE_BEFORE_CANARY_AUDIO",
            "NO_PAIR_PASS_BEFORE_PAIR_AUDIO",
            "NO_FOUNDER_CAST_PASS_BEFORE_CANARY_LISTEN",
            "NO_CAST_LOCK",
            "NO_FULL_EPISODE_RENDER"
        ]
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "roles": {role: out["roles"][role]["voice_id"] for role in ROLES},
        "pre_canary_binding_gate": "PASS",
        "acting_evidence_complete": False,
        "founder_paid_canary_authorized": False,
        "cast_lock": False,
        "out": str(args.out)
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
