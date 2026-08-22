#!/usr/bin/env python3
"""Write a secret-free ROOM917 ElevenLabs account voice/model inventory.

If ELEVENLABS_API_KEY is absent this helper writes an explicit SKIPPED receipt
and exits successfully. Reliable production native-RU Voice Library discovery
also requires authenticated provider access; discover_ru_voice_candidates.py
writes HOLD_PROVIDER_AUTH_REQUIRED when the secret is absent.

No synthesis endpoint is called. No API key is persisted or printed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request

KEY_ENV = "ELEVENLABS_API_KEY"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def get_json(url: str, key: str) -> object:
    req = urllib.request.Request(url, headers={"xi-api-key": key, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    key = os.getenv(KEY_ENV)
    if not key:
        out = {
            "schema_version": "ivdivo.room917_ru_account_voice_inventory/1.3",
            "generated_at": utc_now(),
            "provider": "ElevenLabs",
            "status": "SKIPPED_NO_REPOSITORY_SECRET",
            "secret_persisted": False,
            "paid_synthesis_calls": 0,
            "voice_count": None,
            "voices": [],
            "models": [],
            "note": "Account inventory skipped. Native RU production discovery is also fail-closed until authenticated provider access exists.",
        }
        args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": out["status"], "out": str(args.out)}))
        return 0

    voices: list[dict] = []
    token: str | None = None
    while True:
        query = {"page_size": 100, "include_total_count": "false", "sort": "name", "sort_direction": "asc"}
        if token:
            query["next_page_token"] = token
        data = get_json("https://api.elevenlabs.io/v2/voices?" + urllib.parse.urlencode(query), key)
        if not isinstance(data, dict):
            raise RuntimeError("Unexpected /v2/voices response shape")
        for voice in data.get("voices") or []:
            labels = voice.get("labels") or {}
            voices.append(
                {
                    "voice_id": voice.get("voice_id"),
                    "name": voice.get("name"),
                    "category": voice.get("category"),
                    "description": voice.get("description"),
                    "labels": labels,
                }
            )
        if not data.get("has_more"):
            break
        token = data.get("next_page_token")
        if not token:
            break

    raw_models = get_json("https://api.elevenlabs.io/v1/models", key)
    if not isinstance(raw_models, list):
        raise RuntimeError("Unexpected /v1/models response shape")
    models = []
    for model in raw_models:
        languages = [row.get("language_id") for row in (model.get("languages") or []) if row.get("language_id")]
        models.append(
            {
                "model_id": model.get("model_id"),
                "name": model.get("name"),
                "can_do_text_to_speech": model.get("can_do_text_to_speech"),
                "maximum_text_length_per_request": model.get("maximum_text_length_per_request"),
                "languages": languages,
            }
        )

    out = {
        "schema_version": "ivdivo.room917_ru_account_voice_inventory/1.3",
        "generated_at": utc_now(),
        "provider": "ElevenLabs",
        "status": "PASS_AUTHENTICATED_ACCOUNT_INVENTORY",
        "secret_persisted": False,
        "paid_synthesis_calls": 0,
        "voice_count": len(voices),
        "voices": voices,
        "models": models,
        "note": "Authenticated account inventory is secondary metadata; authenticated native-RU shared-voice discovery remains the production casting authority.",
    }
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": out["status"], "voice_count": len(voices), "models": len(models), "out": str(args.out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
