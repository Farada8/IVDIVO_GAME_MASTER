#!/usr/bin/env python3
"""Compile a non-binding ROOM917 RU cast shortlist from a provider snapshot.

This tool never generates audio and never creates paid S0 bindings. It converts
an authenticated provider discovery snapshot into a review artifact containing
up to N candidates per role, while preserving the evidence required for later
human preview listening.

Fail-closed behavior:
- HOLD provider snapshot -> HOLD shortlist, zero candidates.
- Provider policy weaker than ROOM917 requirements -> HOLD.
- Candidate missing RU verification/professional category/durability evidence ->
  exclude candidate and record the rejection.

Promotion to ROOM917_RU_S0_NATIVE_BINDINGS.json remains a separate human gate.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
MIN_NOTICE_DAYS = 365
DIAGNOSTIC_IDS = {
    "21m00Tcm4TlvDq8ikWAM",
    "pNInz6obpgDQGcFmaJgB",
    "XrExE9yKIg1WjnnlVkGX",
    "EXAVITQu4vr4xnSDxMaL",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value: object) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def int_or_none(value: object) -> int | None:
    if value in (None, "") or isinstance(value, bool):
        return None
    try:
        return int(float(str(value)))
    except ValueError:
        return None


def validate_snapshot_policy(snapshot: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    query = snapshot.get("query_policy") or {}
    if norm(query.get("language")) != "ru":
        errors.append("snapshot query_policy.language must be ru")
    if norm(query.get("category")) != "professional":
        errors.append("snapshot query_policy.category must be professional")
    notice = int_or_none(query.get("min_notice_period_days")) or 0
    if notice < MIN_NOTICE_DAYS:
        errors.append(f"snapshot minimum notice policy {notice} < {MIN_NOTICE_DAYS}")
    if query.get("include_live_moderated") is not False:
        errors.append("snapshot must exclude live-moderated voices")
    if query.get("include_custom_rates") is not False:
        errors.append("snapshot must exclude custom-rate voices")
    if snapshot.get("paid_synthesis_calls") != 0:
        errors.append("discovery snapshot must report paid_synthesis_calls=0")
    return errors


def candidate_by_id(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("voice_id")): row
        for row in snapshot.get("candidates") or []
        if row.get("voice_id")
    }


def candidate_gate(candidate: dict[str, Any]) -> tuple[bool, list[str]]:
    failures: list[str] = []
    voice_id = str(candidate.get("voice_id") or "")
    if not voice_id:
        failures.append("missing_voice_id")
    if voice_id in DIAGNOSTIC_IDS:
        failures.append("historical_diagnostic_voice_id_forbidden")
    if candidate.get("ru_verified") is not True:
        failures.append("ru_verified_not_true")
    if norm(candidate.get("category")) != "professional":
        failures.append("category_not_professional")

    notice = int_or_none(candidate.get("notice_period"))
    if notice is None:
        failures.append("notice_period_missing_or_non_numeric")
    elif notice < MIN_NOTICE_DAYS:
        failures.append(f"notice_period_{notice}_below_{MIN_NOTICE_DAYS}")

    disable = candidate.get("disable_at_unix")
    if disable not in (None, 0, "", "0"):
        failures.append(f"disable_at_unix_active:{disable}")
    if candidate.get("live_moderation_enabled") is True:
        failures.append("live_moderation_enabled")

    rate = candidate.get("rate")
    if rate not in (None, ""):
        try:
            if float(rate) != 1.0:
                failures.append(f"custom_rate:{rate}")
        except (TypeError, ValueError):
            failures.append(f"unparseable_rate:{rate}")

    return not failures, failures


def ranked_rows(snapshot: dict[str, Any], role: str) -> list[dict[str, Any]]:
    rows = (snapshot.get("ranked_role_candidates") or {}).get(role) or []
    return [row for row in rows if isinstance(row, dict)]


def compile_shortlist(snapshot_path: Path, max_per_role: int) -> dict[str, Any]:
    snapshot = load(snapshot_path)
    snapshot_status = str(snapshot.get("status") or "UNKNOWN")
    output: dict[str, Any] = {
        "schema_version": "ivdivo.room917_ru_cast_shortlist_proposal/1.0",
        "generated_at": utc_now(),
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "classification": "WORKING_PROPOSAL_NOT_BINDINGS",
        "provider": "ElevenLabs",
        "provider_snapshot": {
            "path": str(snapshot_path),
            "sha256": sha256(snapshot_path),
            "status": snapshot_status,
        },
        "paid_synthesis_calls": 0,
        "auto_cast": False,
        "cast_lock": False,
        "paid_s0_authorized": False,
        "full_e01_render_allowed": False,
        "max_candidates_per_role": max_per_role,
        "roles": {role: [] for role in ROLES},
        "rejected_candidates": [],
        "collisions": [],
        "next": None,
    }

    if snapshot_status == "HOLD_PROVIDER_AUTH_REQUIRED":
        output["status"] = "HOLD_PROVIDER_AUTH_REQUIRED"
        output["next"] = "CONFIGURE_PROVIDER_AUTH_AND_RERUN_ZERO_SPEND_DISCOVERY"
        return output
    if snapshot_status == "HOLD_NO_NATIVE_DURABLE_CANDIDATES":
        output["status"] = "HOLD_NO_NATIVE_DURABLE_CANDIDATES"
        output["next"] = "REVIEW_PROVIDER_FILTERS_OR_VOICE_LIBRARY_WITHOUT_LOWERING_DURABILITY_GATE_SILENTLY"
        return output
    if snapshot_status != "PASS_CANDIDATES_FOUND":
        output["status"] = "HOLD_UNSUPPORTED_PROVIDER_SNAPSHOT_STATUS"
        output["next"] = "REVIEW_PROVIDER_SNAPSHOT"
        return output

    policy_errors = validate_snapshot_policy(snapshot)
    if policy_errors:
        output["status"] = "HOLD_PROVIDER_POLICY_MISMATCH"
        output["policy_errors"] = policy_errors
        output["next"] = "REGENERATE_PROVIDER_SNAPSHOT_WITH_ROOM917_POLICY"
        return output

    candidates = candidate_by_id(snapshot)
    selected_ids_by_role: dict[str, list[str]] = {role: [] for role in ROLES}

    for role in ROLES:
        for rank_row in ranked_rows(snapshot, role):
            if len(output["roles"][role]) >= max_per_role:
                break
            voice_id = str(rank_row.get("voice_id") or "")
            candidate = candidates.get(voice_id)
            if candidate is None:
                output["rejected_candidates"].append({
                    "role": role,
                    "voice_id": voice_id or None,
                    "provider_name": rank_row.get("name"),
                    "failures": ["ranked_voice_absent_from_candidate_snapshot"],
                })
                continue
            passed, failures = candidate_gate(candidate)
            if not passed:
                output["rejected_candidates"].append({
                    "role": role,
                    "voice_id": voice_id,
                    "provider_name": candidate.get("name"),
                    "failures": failures,
                })
                continue

            output["roles"][role].append({
                "rank_within_role": len(output["roles"][role]) + 1,
                "voice_id": voice_id,
                "provider_name": candidate.get("name"),
                "provider_score": rank_row.get("score"),
                "gender": candidate.get("gender"),
                "age": candidate.get("age"),
                "accent": candidate.get("accent"),
                "descriptive": candidate.get("descriptive"),
                "use_case": candidate.get("use_case"),
                "preview_url": rank_row.get("preview_url") or candidate.get("preview_url"),
                "notice_period": candidate.get("notice_period"),
                "disable_at_unix": candidate.get("disable_at_unix"),
                "ru_verified": True,
                "provider_identity_check": "PENDING_HUMAN_REVIEW",
                "preview_listen": "PENDING",
                "founder_credibility": "PENDING",
                "binding_eligible": False,
                "ranking_reasons": rank_row.get("reasons") or [],
            })
            selected_ids_by_role[role].append(voice_id)

    reverse: dict[str, list[str]] = {}
    for role, ids in selected_ids_by_role.items():
        for voice_id in ids:
            reverse.setdefault(voice_id, []).append(role)
    output["collisions"] = [
        {"voice_id": voice_id, "roles": roles, "rule": "REVIEW_BEFORE_BINDING; SAME_VOICE_FOR_MULTIPLE_CHARACTERS_NOT_AUTO_ALLOWED"}
        for voice_id, roles in sorted(reverse.items())
        if len(roles) > 1
    ]

    missing_roles = [role for role in ROLES if not output["roles"][role]]
    if missing_roles:
        output["status"] = "HOLD_INCOMPLETE_ROLE_SHORTLIST"
        output["missing_roles"] = missing_roles
        output["next"] = "REVIEW_REJECTED_CANDIDATES_OR_DISCOVER_MORE_PROVIDER_VOICES"
    else:
        output["status"] = "READY_FOR_PREVIEW_LISTEN_NOT_BINDINGS"
        output["next"] = "PREVIEW_CANDIDATES__MARK_IDENTITY_AND_CREDIBILITY__THEN_CREATE_BINDINGS_SEPARATELY"
    return output


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--max-per-role", type=int, default=3)
    args = ap.parse_args()
    if not args.snapshot.exists():
        ap.error(f"snapshot does not exist: {args.snapshot}")
    if not 1 <= args.max_per_role <= 5:
        ap.error("--max-per-role must be between 1 and 5")

    result = compile_shortlist(args.snapshot, args.max_per_role)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "out": str(args.out),
        "role_counts": {role: len(result["roles"][role]) for role in ROLES},
        "rejected": len(result.get("rejected_candidates") or []),
        "collisions": len(result.get("collisions") or []),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
