#!/usr/bin/env python3
"""Discover durable native-Russian ElevenLabs Voice Library candidates for ROOM917.

No TTS generation and no credit-bearing speech request. The script queries the
shared Voice Library, filters for Russian professional voices and a durable
notice period, then writes a secret-free discovery snapshot with metadata-only
role rankings for Elena, Julian, Mina and Cate.

The shared-voices endpoint documents xi-api-key as optional. If an API key is
present it may be sent, but native discovery must not depend on it.

No ranking result is a cast lock. Human Russian listening and pair tests remain
mandatory before production use.
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


def _norm(value: object) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def is_ru_voice(voice: dict) -> bool:
    if _norm(voice.get("language")) == "ru":
        return True
    for item in voice.get("verified_languages") or []:
        if _norm(item.get("language")) == "ru" or _norm(item.get("locale")).startswith("ru_"):
            return True
    return False


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
        "disable_at_unix": voice.get("disable_at_unix"),
        "live_moderation_enabled": voice.get("live_moderation_enabled"),
        "rate": voice.get("rate"),
        "cloned_by_count": voice.get("cloned_by_count"),
        "usage_character_count_1y": voice.get("usage_character_count_1y"),
        "ru_verified": is_ru_voice(voice),
    }


def fetch_page(page: int, page_size: int, min_notice_days: int, api_key: str | None) -> dict:
    query = urllib.parse.urlencode(
        {
            "page": page,
            "page_size": page_size,
            "category": "professional",
            "language": "ru",
            "min_notice_period_days": min_notice_days,
            "include_custom_rates": "false",
            "include_live_moderated": "false",
            "sort": "trending",
        }
    )
    req = urllib.request.Request(
        API_URL + "?" + query,
        headers={"Accept": "application/json", **({"xi-api-key": api_key} if api_key else {})},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ElevenLabs shared-voices HTTP {exc.code}: {detail}") from exc


def searchable_text(voice: dict) -> str:
    parts = [
        voice.get("name"),
        voice.get("accent"),
        voice.get("gender"),
        voice.get("age"),
        voice.get("descriptive"),
        voice.get("use_case"),
        voice.get("description"),
    ]
    return " ".join(_norm(part) for part in parts if part)


def _apply_keywords(text: str, weights: dict[str, int], reasons: list[str]) -> int:
    score = 0
    for keyword, weight in weights.items():
        token = _norm(keyword)
        if token and token in text:
            score += weight
            reasons.append(f"keyword:{token}:{weight:+d}")
    return score


def role_score(voice: dict, role: str) -> tuple[int, list[str]]:
    text = searchable_text(voice)
    gender = _norm(voice.get("gender"))
    age = _norm(voice.get("age"))
    score = 0
    reasons: list[str] = []

    if voice.get("ru_verified"):
        score += 40
        reasons.append("verified_ru:+40")

    expected_gender = "male" if role == "JULIAN" else "female"
    if gender == expected_gender:
        score += 20
        reasons.append("gender_match:+20")
    elif gender and gender not in {"neutral", "unknown"}:
        score -= 60
        reasons.append("gender_mismatch:-60")

    if role in {"ELENA", "JULIAN", "MINA"} and age in {"young", "middle_aged", "middle-aged", "adult"}:
        score += 5
        reasons.append("age_band_fit:+5")
    if role == "CATE" and age in {"middle_aged", "middle-aged", "adult", "young"}:
        score += 4
        reasons.append("age_band_fit:+4")

    if voice.get("preview_url"):
        score += 2
        reasons.append("preview_available:+2")

    if role == "ELENA":
        weights = {
            "grounded": 10,
            "calm": 8,
            "conversational": 8,
            "professional": 6,
            "confident": 3,
            "natural": 4,
            "character": 2,
            "narration": -4,
            "storyteller": -3,
            "dramatic": -5,
            "seductive": -10,
        }
    elif role == "JULIAN":
        weights = {
            "calm": 7,
            "professional": 7,
            "conversational": 6,
            "confident": 5,
            "authoritative": 4,
            "grounded": 6,
            "natural": 3,
            "deep": 2,
            "character": 2,
            "dramatic": -4,
            "seductive": -8,
        }
    elif role == "MINA":
        weights = {
            "conversational": 10,
            "warm": 7,
            "friendly": 6,
            "natural": 5,
            "expressive": 4,
            "energetic": 2,
            "character": 3,
            "narration": -4,
            "dramatic": -4,
        }
    else:
        weights = {
            "warm": 10,
            "gentle": 8,
            "calm": 7,
            "conversational": 6,
            "soft": 5,
            "natural": 4,
            "character": 2,
            "narration": -3,
            "dramatic": -5,
            "ethereal": -10,
        }

    score += _apply_keywords(text, weights, reasons)
    return score, reasons


def rank_for_role(candidates: list[dict], role: str, limit: int = 12) -> list[dict]:
    rows = []
    for voice in candidates:
        score, reasons = role_score(voice, role)
        rows.append(
            {
                "voice_id": voice.get("voice_id"),
                "name": voice.get("name"),
                "score": score,
                "gender": voice.get("gender"),
                "age": voice.get("age"),
                "accent": voice.get("accent"),
                "descriptive": voice.get("descriptive"),
                "use_case": voice.get("use_case"),
                "preview_url": voice.get("preview_url"),
                "notice_period": voice.get("notice_period"),
                "disable_at_unix": voice.get("disable_at_unix"),
                "reasons": reasons,
            }
        )
    rows.sort(key=lambda row: (int(row["score"]), str(row.get("name") or "").lower()), reverse=True)
    return rows[:limit]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--page-size", type=int, default=100)
    ap.add_argument("--max-pages", type=int, default=3)
    ap.add_argument("--min-notice-days", type=int, default=365)
    args = ap.parse_args()

    if not 1 <= args.page_size <= 100:
        ap.error("--page-size must be between 1 and 100")
    if args.max_pages < 1:
        ap.error("--max-pages must be >= 1")
    if not 90 <= args.min_notice_days <= 730:
        ap.error("--min-notice-days must be between 90 and 730")

    api_key = os.getenv(KEY_ENV)
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

    seen: set[str] = set()
    unique = []
    for voice in collected:
        voice_id = str(voice.get("voice_id") or "")
        if not voice_id or voice_id in seen:
            continue
        seen.add(voice_id)
        unique.append(voice)

    rankings = {role: rank_for_role(unique, role) for role in ROLES}
    status = "PASS_CANDIDATES_FOUND" if unique else "HOLD_NO_NATIVE_DURABLE_CANDIDATES"

    snapshot = {
        "schema_version": "ivdivo.room917_ru_voice_discovery_snapshot/1.1",
        "generated_at": utc_now(),
        "provider": "ElevenLabs",
        "endpoint": "/v1/shared-voices",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "status": status,
        "query_policy": {
            "category": "professional",
            "language": "ru",
            "min_notice_period_days": args.min_notice_days,
            "include_custom_rates": False,
            "include_live_moderated": False,
            "sort": "trending",
        },
        "api_key_optional_for_endpoint": True,
        "authenticated_request_used": bool(api_key),
        "paid_synthesis_calls": 0,
        "provider_total_count": provider_total,
        "candidate_count": len(unique),
        "candidates": unique,
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
    print(json.dumps({"status": status, "candidate_count": len(unique), "out": str(args.out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
