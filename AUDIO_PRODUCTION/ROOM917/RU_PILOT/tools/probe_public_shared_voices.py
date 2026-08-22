#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import urllib.parse
import urllib.request

API = "https://api.elevenlabs.io/v1/shared-voices"


def norm(x: object) -> str:
    return str(x or "").strip().lower().replace("-", "_")


def is_ru(v: dict) -> bool:
    if norm(v.get("language")) == "ru":
        return True
    for row in v.get("verified_languages") or []:
        if norm(row.get("language")) == "ru" or norm(row.get("locale")).startswith("ru_"):
            return True
    return False


def notice(v: dict) -> int:
    try:
        return int(float(v.get("notice_period") or 0))
    except (TypeError, ValueError):
        return 0


def standard_rate(v: dict) -> bool:
    try:
        return float(v.get("rate")) == 1.0
    except (TypeError, ValueError):
        return False


def fetch(page: int) -> dict:
    q = urllib.parse.urlencode({"page": page, "page_size": 3})
    req = urllib.request.Request(API + "?" + q, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--pages", type=int, default=100)
    ap.add_argument("--min-notice-days", type=int, default=365)
    args = ap.parse_args()

    rows: list[dict] = []
    has_more = True
    total = None
    pages_scanned = 0
    for page in range(args.pages):
        data = fetch(page)
        pages_scanned += 1
        if total is None:
            total = data.get("total_count")
        rows.extend(data.get("voices") or [])
        has_more = bool(data.get("has_more"))
        if not has_more:
            break

    ru_any = [v for v in rows if is_ru(v)]
    production = [
        v for v in ru_any
        if norm(v.get("category")) == "professional"
        and notice(v) >= args.min_notice_days
        and v.get("live_moderation_enabled") is not True
        and standard_rate(v)
    ]

    def compact(v: dict) -> dict:
        return {
            "voice_id": v.get("voice_id"),
            "public_owner_id": v.get("public_owner_id"),
            "name": v.get("name"),
            "gender": v.get("gender"),
            "age": v.get("age"),
            "accent": v.get("accent"),
            "descriptive": v.get("descriptive"),
            "use_case": v.get("use_case"),
            "category": v.get("category"),
            "language": v.get("language"),
            "notice_period": v.get("notice_period"),
            "rate": v.get("rate"),
            "live_moderation_enabled": v.get("live_moderation_enabled"),
            "disable_at_unix": v.get("disable_at_unix"),
            "preview_url": v.get("preview_url"),
            "verified_languages": v.get("verified_languages") or [],
        }

    out = {
        "schema_version": "ivdivo.room917_public_shared_voice_probe/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider": "ElevenLabs",
        "authentication": "NONE",
        "tts_calls": 0,
        "page_size": 3,
        "pages_scanned": pages_scanned,
        "voice_rows_scanned": len(rows),
        "provider_total_count": total,
        "provider_has_more_after_probe": has_more,
        "ru_voice_count_in_probe": len(ru_any),
        "production_candidate_count_in_probe": len(production),
        "ru_voices": [compact(v) for v in ru_any],
        "production_candidates": [compact(v) for v in production],
        "production_filter": {
            "category": "professional",
            "ru_verified": True,
            "min_notice_period_days": args.min_notice_days,
            "live_moderation_enabled": False,
            "standard_rate_only": True,
        },
        "complete_catalog_claim": not has_more,
        "cast_lock": False,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS_PROBE",
        "pages_scanned": pages_scanned,
        "voice_rows_scanned": len(rows),
        "ru_voice_count": len(ru_any),
        "production_candidate_count": len(production),
        "has_more": has_more,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
