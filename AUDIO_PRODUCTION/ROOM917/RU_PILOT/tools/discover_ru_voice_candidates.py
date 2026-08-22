#!/usr/bin/env python3
"""Discover durable native-Russian ElevenLabs Voice Library candidates for ROOM917.

Production discovery requires an authenticated filtered Voice Library request.
Live provider probes on 2026-08-22 showed that unauthenticated requests cannot
use filters and cannot be relied on for pagination. Therefore, when
ELEVENLABS_API_KEY is absent, this script writes a zero-spend HOLD receipt and
exits successfully instead of attempting misleading public discovery.

No TTS synthesis endpoint is called. No API key is persisted or printed.
Metadata ranking is pre-audition only; preview listening, bounded canary, pair
tests and Founder credibility listen remain mandatory before CAST LOCK.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://api.elevenlabs.io/v1/shared-voices"
KEY_ENV = "ELEVENLABS_API_KEY"
ROLES = ("ELENA", "JULIAN", "MINA", "CATE")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def norm(value: object) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def is_ru_voice(voice: dict) -> bool:
    if norm(voice.get("language")) == "ru":
        return True
    for item in voice.get("verified_languages") or []:
        if norm(item.get("language")) == "ru" or norm(item.get("locale")).startswith("ru_"):
            return True
    return False


def sanitized_voice(voice: dict) -> dict:
    return {
        "voice_id": voice.get("voice_id"),
        "public_owner_id": voice.get("public_owner_id"),
        "name": voice.get("name"),
        "category": voice.get("category"),
        "language": voice.get("language"),
        "accent": voice.get("accent"),
        "gender": voice.get("gender"),
        "age": voice.get("age"),
        "descriptive": voice.get("descriptive"),
        "use_case": voice.get("use_case"),
        "description": voice.get("description"),
        "preview_url": voice.get("preview_url"),
        "verified_languages": voice.get("verified_languages") or [],
        "notice_period": voice.get("notice_period"),
        "disable_at_unix": voice.get("disable_at_unix"),
        "live_moderation_enabled": voice.get("live_moderation_enabled"),
        "rate": voice.get("rate"),
        "cloned_by_count": voice.get("cloned_by_count"),
        "usage_character_count_1y": voice.get("usage_character_count_1y"),
        "ru_verified": is_ru_voice(voice),
    }


def searchable_text(voice: dict) -> str:
    return " ".join(
        norm(x)
        for x in [
            voice.get("name"), voice.get("accent"), voice.get("gender"), voice.get("age"),
            voice.get("descriptive"), voice.get("use_case"), voice.get("description"),
        ]
        if x
    )


def role_score(voice: dict, role: str) -> tuple[int, list[str]]:
    text = searchable_text(voice)
    gender = norm(voice.get("gender"))
    age = norm(voice.get("age"))
    score = 0
    reasons: list[str] = []

    if voice.get("ru_verified"):
        score += 40; reasons.append("verified_ru:+40")

    expected_gender = "male" if role == "JULIAN" else "female"
    if gender == expected_gender:
        score += 20; reasons.append("gender_match:+20")
    elif gender and gender not in {"neutral", "unknown"}:
        score -= 60; reasons.append("gender_mismatch:-60")

    if age in {"young", "middle_aged", "middle-aged", "adult"}:
        score += 5; reasons.append("age_band_fit:+5")
    if voice.get("preview_url"):
        score += 2; reasons.append("preview_available:+2")

    weights = {
        "ELENA": {"grounded":10,"calm":8,"conversational":8,"professional":6,"natural":4,"narration":-4,"dramatic":-5,"seductive":-10},
        "JULIAN": {"grounded":7,"calm":7,"professional":7,"conversational":6,"confident":5,"authoritative":4,"deep":2,"dramatic":-4,"seductive":-8},
        "MINA": {"conversational":10,"warm":7,"friendly":6,"natural":5,"expressive":4,"energetic":2,"narration":-4,"dramatic":-4},
        "CATE": {"warm":10,"gentle":8,"calm":7,"conversational":6,"soft":5,"natural":4,"narration":-3,"dramatic":-5,"ethereal":-10},
    }[role]
    for keyword, weight in weights.items():
        if norm(keyword) in text:
            score += weight
            reasons.append(f"keyword:{keyword}:{weight:+d}")
    return score, reasons


def rank_for_role(candidates: list[dict], role: str, limit: int = 12) -> list[dict]:
    rows = []
    for voice in candidates:
        score, reasons = role_score(voice, role)
        rows.append({
            "voice_id": voice.get("voice_id"), "name": voice.get("name"), "score": score,
            "gender": voice.get("gender"), "age": voice.get("age"), "accent": voice.get("accent"),
            "descriptive": voice.get("descriptive"), "use_case": voice.get("use_case"),
            "preview_url": voice.get("preview_url"), "notice_period": voice.get("notice_period"),
            "disable_at_unix": voice.get("disable_at_unix"), "reasons": reasons,
        })
    rows.sort(key=lambda row: (int(row["score"]), str(row.get("name") or "").lower()), reverse=True)
    return rows[:limit]


def write_hold(out_path: Path, min_notice_days: int) -> int:
    hold = {
        "schema_version": "ivdivo.room917_ru_voice_discovery_snapshot/1.3",
        "generated_at": utc_now(),
        "provider": "ElevenLabs",
        "endpoint": "/v1/shared-voices",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "status": "HOLD_PROVIDER_AUTH_REQUIRED",
        "paid_synthesis_calls": 0,
        "candidate_count": 0,
        "candidates": [],
        "ranked_role_candidates": {role: [] for role in ROLES},
        "query_policy": {
            "category": "professional",
            "language": "ru",
            "min_notice_period_days": min_notice_days,
            "include_custom_rates": False,
            "include_live_moderated": False,
            "sort": "trending",
        },
        "provider_access_evidence": {
            "date": "2026-08-22",
            "live_probe_filtered_without_auth": "401_YOU_MUST_BE_LOGGED_IN_TO_USE_FILTERS",
            "live_probe_unfiltered_over_three": "401_YOU_MUST_BE_LOGGED_IN_TO_FETCH_MORE_THAN_3_VOICES",
            "live_probe_page_size_three_pagination": "401_UNAUTHORIZED",
            "conclusion": "AUTHENTICATED_PROVIDER_ACCESS_REQUIRED_FOR_RELIABLE_PRODUCTION_DISCOVERY",
        },
        "selection_policy": {
            "auto_cast": False,
            "metadata_ranking_is_cast_evidence": False,
            "preview_listen_required_before_paid_canary": True,
            "paid_canary_required_before_cast_lock": True,
            "founder_credibility_listen_required": True,
            "full_e01_render_allowed": False,
            "next": "CONFIGURE_ELEVENLABS_API_KEY_OR_OBTAIN_AUTHENTICATED_PROVIDER_EXPORT",
        },
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(hold, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": hold["status"], "candidate_count": 0, "out": str(out_path)}))
    return 0


def fetch_page(page: int, page_size: int, min_notice_days: int, api_key: str) -> dict:
    query = urllib.parse.urlencode({
        "page": page,
        "page_size": page_size,
        "category": "professional",
        "language": "ru",
        "min_notice_period_days": min_notice_days,
        "include_custom_rates": "false",
        "include_live_moderated": "false",
        "sort": "trending",
    })
    req = urllib.request.Request(API_URL + "?" + query, headers={"Accept": "application/json", "xi-api-key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ElevenLabs shared-voices HTTP {exc.code}: {detail}") from exc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--page-size", type=int, default=100)
    ap.add_argument("--max-pages", type=int, default=3)
    ap.add_argument("--min-notice-days", type=int, default=365)
    args = ap.parse_args()

    if not 1 <= args.page_size <= 100:
        ap.error("--page-size must be 1..100")
    if args.max_pages < 1:
        ap.error("--max-pages must be >=1")
    if not 90 <= args.min_notice_days <= 730:
        ap.error("--min-notice-days must be 90..730")

    api_key = os.getenv(KEY_ENV)
    if not api_key:
        return write_hold(args.out, args.min_notice_days)

    collected: list[dict] = []
    provider_total = None
    for page in range(args.max_pages):
        payload = fetch_page(page, args.page_size, args.min_notice_days, api_key)
        if provider_total is None:
            provider_total = payload.get("total_count")
        for voice in payload.get("voices") or []:
            if is_ru_voice(voice):
                collected.append(sanitized_voice(voice))
        if not payload.get("has_more"):
            break

    seen: set[str] = set(); candidates = []
    for voice in collected:
        voice_id = str(voice.get("voice_id") or "")
        if voice_id and voice_id not in seen:
            seen.add(voice_id); candidates.append(voice)

    status = "PASS_CANDIDATES_FOUND" if candidates else "HOLD_NO_NATIVE_DURABLE_CANDIDATES"
    snapshot = {
        "schema_version": "ivdivo.room917_ru_voice_discovery_snapshot/1.3",
        "generated_at": utc_now(),
        "provider": "ElevenLabs",
        "endpoint": "/v1/shared-voices",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "status": status,
        "authenticated_request_used": True,
        "paid_synthesis_calls": 0,
        "provider_total_count": provider_total,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "ranked_role_candidates": {role: rank_for_role(candidates, role) for role in ROLES},
        "query_policy": {
            "category": "professional", "language": "ru", "min_notice_period_days": args.min_notice_days,
            "include_custom_rates": False, "include_live_moderated": False, "sort": "trending",
        },
        "selection_policy": {
            "auto_cast": False,
            "metadata_ranking_is_cast_evidence": False,
            "preview_listen_required_before_paid_canary": True,
            "paid_canary_required_before_cast_lock": True,
            "founder_credibility_listen_required": True,
            "next": "PREVIEW_TOP_ROLE_CANDIDATES_THEN_BIND_UP_TO_3_PER_ROLE",
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "candidate_count": len(candidates), "out": str(args.out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
