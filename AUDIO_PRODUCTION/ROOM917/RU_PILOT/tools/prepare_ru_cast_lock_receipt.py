#!/usr/bin/env python3
"""Compile ROOM917 RU CAST LOCK receipt from sealed provider + audio + human evidence.

This tool makes no provider call and does not synthesize audio. It verifies that
post-canary human decisions reference real S0/finalist audio hashes and that each
role has both its S0 take and finalist repeat take before opening controlled E01
dialogue production.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
ROLE_TAKES = {
    "ELENA": ("RU_S0_ELENA_BOUNDARY", "RU_FV_ELENA_REPEAT"),
    "JULIAN": ("RU_S0_JULIAN_72", "RU_FV_JULIAN_REPEAT"),
    "MINA": ("RU_S0_MINA_INTRO", "RU_FV_MINA_REPEAT"),
    "CATE": ("RU_S0_CATE_LENI_BIRD", "RU_FV_CATE_REPEAT"),
}
PAIR_ALLOWED_BLOCKS = {
    "ELENA_MINA": {"RU_S0_ELENA_MINA_RELATION", "RU_FV_ELENA_MINA_RELATION"},
    "ELENA_JULIAN_1": {"RU_S0_ELENA_JULIAN_FRICTION", "RU_FV_ELENA_JULIAN_FRICTION"},
    "ELENA_JULIAN_2": {"RU_FV_ELENA_JULIAN_STATUS"},
    "CATE_IDENTITY": {"RU_FV_CATE_DOMESTIC"},
}
ROLE_PAIR_RECEIPT = {
    "ELENA": {},
    "JULIAN": {"ELENA_JULIAN_1": "ELENA_JULIAN_1", "ELENA_JULIAN_2": "ELENA_JULIAN_2"},
    "MINA": {"ELENA_MINA": "ELENA_MINA"},
    "CATE": {"CATE_IDENTITY": "CATE_IDENTITY"},
}
QUAL_PASS = (
    "native_ru_pronunciation",
    "age_character_fit",
    "naturalism",
    "microemotion_subtext",
    "precision_under_pressure",
    "repeat_take_identity_consistency",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit("FAIL_CAST_LOCK_COMPILER: " + msg)


def is_sha256(value: object) -> bool:
    s = str(value or "")
    return len(s) == 64 and all(c in "0123456789abcdefABCDEF" for c in s)


def audio_rows(receipt: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [r for r in receipt.get("audio_files") or [] if isinstance(r, dict)]
    for row in rows:
        require(is_sha256(row.get("sha256")), f"receipt contains invalid audio sha256 for {row.get('path')}")
    return rows


def has_audio(rows: list[dict[str, Any]], block_id: str, sha: str) -> bool:
    return any(str(r.get("sha256")) == sha and block_id in str(r.get("path") or "") for r in rows)


def candidate_map(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(c.get("voice_id")): c for c in snapshot.get("candidates") or [] if c.get("voice_id")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider-snapshot", type=Path, required=True)
    ap.add_argument("--bindings", type=Path, required=True)
    ap.add_argument("--s0-receipt", type=Path, required=True)
    ap.add_argument("--finalist-receipt", type=Path, required=True)
    ap.add_argument("--review", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    for p in (args.provider_snapshot, args.bindings, args.s0_receipt, args.finalist_receipt, args.review):
        require(p.exists(), f"missing required file: {p}")

    snapshot = load(args.provider_snapshot)
    bindings = load(args.bindings)
    s0 = load(args.s0_receipt)
    finalist = load(args.finalist_receipt)
    review = load(args.review)

    require(snapshot.get("status") == "PASS_CANDIDATES_FOUND", "provider snapshot must PASS_CANDIDATES_FOUND")
    require(snapshot.get("authenticated_request_used") is True, "provider snapshot must come from authenticated request")
    require(snapshot.get("paid_synthesis_calls") == 0, "provider discovery snapshot must remain zero-spend")
    require(bindings.get("status") == "PAID_S0_AUTHORIZED", "bindings must be sealed PAID_S0_AUTHORIZED")
    require(bindings.get("canary_binding_only") is True, "upstream bindings must be canary-only")
    require(bindings.get("cast_lock") is False, "upstream bindings cannot already claim CAST LOCK")
    require(s0.get("stage_semantics") == "S0_SCREENING_ONLY_NOT_CAST_LOCK", "S0 receipt semantics mismatch")
    require(s0.get("cast_locked") is False and s0.get("full_episode_rendered") is False, "S0 receipt cannot claim lock/full episode")
    require(finalist.get("cast_locked") is False and finalist.get("full_episode_rendered") is False, "finalist receipt cannot claim lock/full episode")
    require(finalist.get("human_listen_required") is True, "finalist receipt must require human listen")

    require(review.get("status") == "POST_CANARY_REVIEW_COMPLETE", "review status must be POST_CANARY_REVIEW_COMPLETE")
    require(review.get("acting_evidence_complete") is True, "review acting_evidence_complete must be true")
    require(review.get("cast_lock") is False and review.get("full_e01_render_allowed") is False, "review cannot pre-grant lock/full E01")
    require(review.get("provider_snapshot_sha256") == digest(args.provider_snapshot), "review/provider snapshot hash mismatch")
    require(review.get("pre_canary_bindings_sha256") == digest(args.bindings), "review/bindings hash mismatch")
    require(review.get("s0_canary_receipt_sha256") == digest(args.s0_receipt), "review/S0 receipt hash mismatch")
    require(review.get("finalist_verification_receipt_sha256") == digest(args.finalist_receipt), "review/finalist receipt hash mismatch")
    require(review.get("pronunciation_gate") == "PASS", "global pronunciation gate must PASS")
    require(review.get("all_selected_voice_ids_unique") == "PASS", "selected voice IDs uniqueness gate must PASS")

    s0_rows = audio_rows(s0)
    finalist_rows = audio_rows(finalist)
    all_hashes = {str(r["sha256"]) for r in s0_rows + finalist_rows}
    require(bool(s0_rows), "S0 receipt contains no audio evidence")
    require(bool(finalist_rows), "finalist receipt contains no audio evidence")

    pair_review = review.get("pair_tests") or {}
    pair_pass: dict[str, str] = {}
    for key, allowed in PAIR_ALLOWED_BLOCKS.items():
        row = pair_review.get(key) or {}
        require(isinstance(row, dict), f"pair {key} review row missing")
        require(row.get("status") == "PASS", f"pair {key} must PASS")
        block_id = str(row.get("block_id") or "")
        sha = str(row.get("audio_sha256") or "")
        stage = str(row.get("source_stage") or "")
        require(block_id in allowed, f"pair {key}: invalid evidence block {block_id}")
        require(is_sha256(sha), f"pair {key}: invalid/missing audio sha256")
        if stage == "S0":
            require(has_audio(s0_rows, block_id, sha), f"pair {key}: S0 audio evidence not found in S0 receipt")
        elif stage == "FINALIST":
            require(has_audio(finalist_rows, block_id, sha), f"pair {key}: finalist audio evidence not found in finalist receipt")
        else:
            require(False, f"pair {key}: source_stage must be S0 or FINALIST")
        pair_pass[key] = "PASS"

    candidates = candidate_map(snapshot)
    locked_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    provider_verified_at = str(snapshot.get("generated_at") or "")
    require(bool(provider_verified_at), "provider snapshot generated_at missing")

    role_rows = review.get("roles") or {}
    bind_rows = bindings.get("roles") or {}
    selected_voice_ids: list[str] = []
    out_roles: dict[str, Any] = {}

    for role in ROLES:
        rr = role_rows.get(role) or {}
        br = bind_rows.get(role) or {}
        voice_id = str(rr.get("selected_voice_id") or "")
        require(bool(voice_id), f"{role}: selected_voice_id missing")
        require(voice_id == str(br.get("voice_id") or ""), f"{role}: final selected voice differs from sealed audition binding")
        candidate = candidates.get(voice_id)
        require(candidate is not None, f"{role}: selected voice absent from provider snapshot")
        require(candidate.get("ru_verified") is True, f"{role}: provider candidate is not RU verified")
        require(str(candidate.get("category") or "").lower() == "professional", f"{role}: provider category is not professional")
        notice = candidate.get("notice_period")
        require(isinstance(notice, (int, float)) and not isinstance(notice, bool) and int(notice) >= 365, f"{role}: notice period <365/missing")
        require(candidate.get("disable_at_unix") in (None, 0, "", "0"), f"{role}: provider voice has active disable_at_unix")
        require(br.get("provider_identity_check") == "PASS", f"{role}: provider identity check not PASS")
        require(br.get("provider_durability_check") == "PASS", f"{role}: provider durability check not PASS")

        for field in QUAL_PASS:
            require(rr.get(field) == "PASS", f"{role}: {field} must PASS")
        require(rr.get("founder_credibility") == "YES", f"{role}: Founder final credibility must be YES")
        score = rr.get("score_0_30")
        naturalism = rr.get("naturalism_score_0_5")
        pronunciation = rr.get("pronunciation_score_0_5")
        require(isinstance(score, (int, float)) and not isinstance(score, bool) and float(score) >= 24, f"{role}: score below 24/30")
        require(isinstance(naturalism, (int, float)) and not isinstance(naturalism, bool) and float(naturalism) >= 4, f"{role}: naturalism below 4/5")
        require(isinstance(pronunciation, (int, float)) and not isinstance(pronunciation, bool) and float(pronunciation) >= 4, f"{role}: pronunciation below 4/5")
        flags = rr.get("hard_reject_flags") or []
        require(not flags, f"{role}: hard reject flags present")

        ids = rr.get("accepted_canary_ids") or []
        hashes = rr.get("accepted_canary_sha256") or []
        require(len(ids) == len(hashes) and len(ids) >= 2, f"{role}: at least two accepted take IDs/hashes required")
        expected_s0, expected_repeat = ROLE_TAKES[role]
        require(expected_s0 in ids, f"{role}: accepted S0 take {expected_s0} missing")
        require(expected_repeat in ids, f"{role}: accepted finalist repeat {expected_repeat} missing")
        for block_id, sha in zip(ids, hashes):
            require(is_sha256(sha), f"{role}: invalid accepted audio sha256 for {block_id}")
            require(sha in all_hashes, f"{role}: accepted hash not found in sealed receipts")
            if block_id.startswith("RU_S0_"):
                require(has_audio(s0_rows, str(block_id), str(sha)), f"{role}: S0 accepted take not found in S0 receipt")
            elif block_id.startswith("RU_FV_"):
                require(has_audio(finalist_rows, str(block_id), str(sha)), f"{role}: finalist accepted take not found in finalist receipt")
            else:
                require(False, f"{role}: unsupported accepted canary id {block_id}")

        selected_voice_ids.append(voice_id)
        role_pair_map = {receipt_key: pair_pass[source_key] for receipt_key, source_key in ROLE_PAIR_RECEIPT[role].items()}
        out_roles[role] = {
            "role": role,
            "provider": "ElevenLabs",
            "voice_id": voice_id,
            "provider_voice_name": candidate.get("name") or rr.get("provider_name"),
            "verified_language": "ru",
            "category": candidate.get("category"),
            "notice_period_days": int(notice),
            "disable_at": candidate.get("disable_at_unix"),
            "model_id": "eleven_v3",
            "accepted_canary_ids": list(ids),
            "accepted_canary_sha256": list(hashes),
            "individual_score_raw": float(score),
            "naturalism_score": float(naturalism),
            "pronunciation_score": float(pronunciation),
            "pair_tests": role_pair_map,
            "hard_reject_flags": [],
            "founder_credibility": "YES",
            "provider_identity_verified_at": provider_verified_at,
            "locked_at": locked_at,
        }

    require(len(set(selected_voice_ids)) == len(ROLES), "selected voice IDs are not unique")

    out = {
        "schema_version": "ivdivo.room917_ru_cast_lock_receipt/2.0",
        "date": locked_at,
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "status": "LOCKED",
        "evidence": {
            "provider_snapshot_path": str(args.provider_snapshot),
            "provider_snapshot_sha256": digest(args.provider_snapshot),
            "bindings_path": str(args.bindings),
            "bindings_sha256": digest(args.bindings),
            "s0_receipt_path": str(args.s0_receipt),
            "s0_receipt_sha256": digest(args.s0_receipt),
            "finalist_receipt_path": str(args.finalist_receipt),
            "finalist_receipt_sha256": digest(args.finalist_receipt),
            "post_canary_review_path": str(args.review),
            "post_canary_review_sha256": digest(args.review),
        },
        "roles": out_roles,
        "global_lock_gate": {
            "provider_snapshot_status": "PASS_CANDIDATES_FOUND",
            "all_four_roles_locked": True,
            "all_provider_ids_resolve": True,
            "all_required_pair_tests_pass": True,
            "all_founder_credibility_yes": True,
            "full_e01_dialogue_render_allowed": True,
        },
        "hard_rules": [
            "LOCK_APPLIES_TO_RU_CAST_AND_CONTROLLED_DIALOGUE_PRODUCTION_ONLY",
            "NO_STORY_EDIT",
            "NO_MIX_EDIT_FROM_CAST_LOCK",
            "SELECTIVE_RERENDER_ONLY_IF_LATER_QC_FAILS"
        ]
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status":"LOCKED","roles":selected_voice_ids,"full_e01_dialogue_render_allowed":True,"out":str(args.out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
