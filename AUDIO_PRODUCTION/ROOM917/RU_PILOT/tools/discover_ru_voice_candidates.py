#!/usr/bin/env python3
"""Discover durable native-Russian ElevenLabs Voice Library candidates for ROOM917.

No TTS endpoint is called. Preferred mode uses authenticated server-side filters.
If no API key is available and ElevenLabs rejects filtered requests with 401, the
script falls back to the public unfiltered shared-voices listing and applies the
same production filters locally.

Metadata ranking is pre-audition only. Human Russian listening and pair tests are
mandatory before CAST LOCK.
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


def notice_days(voice: dict) -> int:
    value = voice.get("notice_period")
    if isinstance(value, bool) or value is None:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    try:
        return int(float(text))
    except ValueError:
        return 0


def is_standard_rate(voice: dict) -> bool:
    value = voice.get("rate")
    try:
        return float(value) == 1.0
    except (TypeError, ValueError):
        return False


def passes_local_production_filter(voice: dict, min_notice_days: int) -> bool:
    return all(
        [
            norm(voice.get("category")) == "professional",
            is_ru_voice(voice),
            notice_days(voice) >= min_notice_days,
            voice.get("live_moderation_enabled") is not True,
            is_standard_rate(voice),
        ]
    )


def sanitized_voice(voice: dict) -> dict:
    verified = []
    for item in voice.get("verified_languages") or []:
        verified.append(
            {
                "language": item.get("language"),
                "locale": item.get("locale"),
                "accent": item.get("accent"),
                "model_id": item.get("model_id"),
                "preview_url": item.get("preview_url"),
            }
        )
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
        "verified_languages": verified,
        "notice_period": voice.get("notice_period"),
        "notice_period_days_normalized": notice_days(voice),
        "disable_at_unix": voice.get("disable_at_unix"),
        "live_moderation_enabled": voice.get("live_moderation_enabled"),
        "rate": voice.get("rate"),
        "standard_rate_candidate": is_standard_rate(voice),
        "cloned_by_count": voice.get("cloned_by_count"),
        "usage_character_count_1y": voice.get("usage_character_count_1y"),
        "ru_verified": is_ru_voice(voice),
    }


def request_page(query: dict[str, object], api_key: str | None) -> dict:
    req = urllib.request.Request(
        API_URL + "?" + urllib.parse.urlencode(query),
        headers={"Accept": "application/json", **({"xi-api-key": api_key} if api_key else {})},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict):
                raise RuntimeError("Unexpected shared-voices response shape")
            return payload
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        error = RuntimeError(f"ElevenLabs shared-voices HTTP {exc.code}: {detail}")
        error.http_code = exc.code  # type: ignore[attr-defined]
        error.detail = detail  # type: ignore[attr-defined]
        raise error from exc


def filtered_query(page: int, page_size: int, min_notice_days: int) -> dict[str, object]:
    return {
        "page": page,
        "page_size": page_size,
        "category": "professional",
        "language": "ru",
        "min_notice_period_days": min_notice_days,
        "include_custom_rates": "false",
        "include_live_moderated": "false",
        "sort": "trending",
    }


def public_query(page: int, page_size: int) -> dict[str, object]:
    # ElevenLabs live behavior on 2026-08-22: unauthenticated requests may list
    # shared voices but return 401 when filter query parameters are supplied.
    return {"page": page, "page_size": page_size}


def searchable_text(voice: dict) -> str:
    parts = [
        voice.get("name"), voice.get("accent"), voice.get("gender"), voice.get("age"),
        voice.get("descriptive"), voice.get("use_case"), voice.get("description"),
    ]
    return " ".join(norm(part) for part in parts if part)


def role_score(voice: dict, role: str) -> tuple[int, list[str]]:
    text = searchable_text(voice)
    gender = norm(voice.get("gender"))
    age = norm(voice.get("age"))
    score = 40 if voice.get("ru_verified") else 0
    reasons = ["verified_ru:+40"] if voice.get("ru_verified") else []

    expected_gender = "male" if role == "JULIAN" else "female"
    if gender == expected_gender:
        score += 20
        reasons.append("gender_match:+20")
    elif gender and gender not in {"neutral", "unknown"}:
        score -= 60
        reasons.append("gender_mismatch:-60")

    if age in {"young", "middle_aged", "adult"}:
        score += 5
        reasons.append("age_band_fit:+5")
    if voice.get("preview_url"):
        score += 2
        reasons.append("preview_available:+2")

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
        rows.append(
            {
                "voice_id": voice.get("voice_id"), "name": voice.get("name"), "score": score,
                "gender": voice.get("gender"), "age": voice.get("age"), "accent": voice.get("accent"),
                "descriptive": voice.get("descriptive"), "use_case": voice.get("use_case"),
                "preview_url": voice.get("preview_url"), "notice_period": voice.get("notice_period"),
                "disable_at_unix": voice.get("disable_at_unix"), "rate": voice.get("rate"), "reasons": reasons,
            }
        )
    rows.sort(key=lambda row: (int(row["score"]), str(row.get("name") or "").lower()), reverse=True)
    return rows[:limit]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--page-size", type=int, default=100)
    ap.add_argument("--max-pages", type=int, default=3, help="Authenticated filtered crawl page cap")
    ap.add_argument("--public-max-pages", type=int, default=100, help="Unauthenticated fallback crawl cap")
    ap.add_argument("--min-notice-days", type=int, default=365)
    args = ap.parse_args()

    if not 1 <= args.page_size <= 100:
        ap.error("--page-size must be between 1 and 100")
    if args.max_pages < 1 or args.public_max_pages < 1:
        ap.error("page caps must be >=1")
    if not 90 <= args.min_notice_days <= 730:
        ap.error("--min-notice-days must be between 90 and 730")

    api_key = os.getenv(KEY_ENV) or None
    discovery_mode = "AUTH_FILTERED"
    raw_voices: list[dict] = []
    provider_total = None
    scanned_pages = 0

    try:
        for page in range(args.max_pages):
            payload = request_page(filtered_query(page, args.page_size, args.min_notice_days), api_key)
            scanned_pages += 1
            if provider_total is None:
                provider_total = payload.get("total_count")
            raw_voices.extend(payload.get("voices") or [])
            if not payload.get("has_more"):
                break
    except RuntimeError as exc:
        detail = str(getattr(exc, "detail", ""))
        if api_key or getattr(exc, "http_code", None) != 401 or "use filters" not in detail.lower():
            raise
        discovery_mode = "PUBLIC_UNFILTERED_LOCAL_FILTER"
        raw_voices = []
        provider_total = None
        scanned_pages = 0
        for page in range(args.public_max_pages):
            payload = request_page(public_query(page, args.page_size), None)
            scanned_pages += 1
            if provider_total is None:
                provider_total = payload.get("total_count")
            raw_voices.extend(payload.get("voices") or [])
            if not payload.get("has_more"):
                break
        if scanned_pages >= args.public_max_pages and payload.get("has_more"):
            raise RuntimeError("Public Voice Library crawl hit safety page cap before completion")

    filtered = [voice for voice in raw_voices if passes_local_production_filter(voice, args.min_notice_days)]
    seen: set[str] = set()
    candidates = []
    for voice in filtered:
        voice_id = str(voice.get("voice_id") or "")
        if voice_id and voice_id not in seen:
            seen.add(voice_id)
            candidates.append(sanitized_voice(voice))

    rankings = {role: rank_for_role(candidates, role) for role in ROLES}
    status = "PASS_CANDIDATES_FOUND" if candidates else "HOLD_NO_NATIVE_DURABLE_CANDIDATES"
    snapshot = {
        "schema_version": "ivdivo.room917_ru_voice_discovery_snapshot/1.2",
        "generated_at": utc_now(),
        "provider": "ElevenLabs",
        "endpoint": "/v1/shared-voices",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "status": status,
        "discovery_mode": discovery_mode,
        "live_provider_behavior": "UNAUTHENTICATED_FILTERS_RETURNED_401_ON_2026_08_22" if discovery_mode.startswith("PUBLIC_") else "AUTHENTICATED_FILTERS_ACCEPTED",
        "query_policy": {
            "category": "professional", "language": "ru", "min_notice_period_days": args.min_notice_days,
            "include_custom_rates": False, "include_live_moderated": False,
        },
        "local_filter_policy": {
            "category_professional": True, "ru_verified": True, "minimum_notice_days": args.min_notice_days,
            "live_moderation_disabled": True, "standard_rate_only": True,
        },
        "api_key_present": bool(api_key),
        "paid_synthesis_calls": 0,
        "provider_total_count": provider_total,
        "scanned_pages": scanned_pages,
        "scanned_voice_rows": len(raw_voices),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "ranked_role_candidates": rankings,
        "selection_policy": {
            "auto_cast": False,
            "metadata_ranking_is_cast_evidence": False,
            "preview_listen_required_before_paid_canary": True,
            "paid_canary_required_before_cast_lock": True,
            "founder_credibility_listen_required": True,
            "next": "PREVIEW_TOP_ROLE_CANDIDATES_THEN_BIND_3_PER_ROLE_TO_ROOM917_RU_CAST_AUDITION_GATE_v1.0",
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "mode": discovery_mode, "candidate_count": len(candidates), "scanned_voice_rows": len(raw_voices), "out": str(args.out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
