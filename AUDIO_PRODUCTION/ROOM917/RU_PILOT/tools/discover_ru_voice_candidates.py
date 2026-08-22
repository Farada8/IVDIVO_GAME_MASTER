#!/usr/bin/env python3
"""Discover durable native-Russian ElevenLabs Voice Library candidates for ROOM917.

No TTS generation and no credit-bearing speech request. The script queries the
shared Voice Library only, filters for Russian professional voices and a durable
notice period, and writes a sanitized snapshot for later audition selection.

Optional environment variable:
  ELEVENLABS_API_KEY

No secret value is persisted or printed.
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
        verified.append({
            "language": item.get("language"),
            "locale": item.get("locale"),
            "accent": item.get("accent"),
            "model_id": item.get("model_id"),
            "preview_url": item.get("preview_url"),
        })
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

    snapshot = {
        "schema_version": "ivdivo.room917_ru_voice_discovery_snapshot/1.0",
        "generated_at": utc_now(),
        "provider": "ElevenLabs",
        "endpoint": "/v1/shared-voices",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "query_policy": {
            "category": "professional",
            "language": "ru",
            "min_notice_period_days": args.min_notice_days,
            "include_custom_rates": False,
            "include_live_moderated": False,
            "sort": "trending"
        },
        "authenticated": bool(api_key),
        "provider_total_count": provider_total,
        "candidate_count": len(unique),
        "candidates": unique,
        "selection_policy": {
            "auto_cast": False,
            "next": "LISTEN_TO_PREVIEWS_THEN_RUN_ROOM917_RU_CAST_AUDITION_GATE_v1.0",
            "production_lock_requires_paid_canary_and_founder_listen": True
        }
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "candidate_count": len(unique), "out": str(args.out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
