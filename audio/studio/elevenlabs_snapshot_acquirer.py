#!/usr/bin/env python3
"""ElevenLabs authenticated provider-snapshot acquisition.

Reads ELEVENLABS_API_KEY only from the runtime environment, performs read-only
authenticated API calls, immediately discards the raw credential, and persists
only a redacted capability snapshot sealed by provider_snapshot_contract.

No paid synthesis request is issued here.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any
import argparse
import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request

from provider_snapshot_contract import SCHEMA_VERSION, seal_snapshot, validate_provider_snapshot

BASE_URL = "https://api.elevenlabs.io"
KEY_ENV = "ELEVENLABS_API_KEY"
CAPTURE_ENGINE = "ivdivo.elevenlabs_snapshot_acquirer/1.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get(path: str, key: str, *, query: dict[str, Any] | None = None, timeout: float = 30.0):
    query_string = urllib.parse.urlencode(query or {})
    url = BASE_URL + path + (("?" + query_string) if query_string else "")
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "xi-api-key": key},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
            payload = json.loads(response.read().decode("utf-8"))
            meta = {"http_status": int(response.status), "path": path}
            for name in ("request-id", "x-request-id"):
                value = response.headers.get(name)
                if value:
                    meta["provider_request_id"] = value
                    break
            return payload, meta
    except urllib.error.HTTPError as exc:
        failure = "FAIL_PROVIDER_CREDENTIAL" if exc.code in (401, 403) else (
            "FAIL_PROVIDER_REQUEST" if 400 <= exc.code < 500 else "FAIL_PROVIDER_CONNECTIVITY"
        )
        raise RuntimeError(json.dumps({"failure": failure, "http_status": int(exc.code), "path": path}))
    except Exception as exc:
        raise RuntimeError(json.dumps({
            "failure": "FAIL_PROVIDER_CONNECTIVITY",
            "error_type": type(exc).__name__,
            "path": path,
        }))


def _account_fingerprint(user_payload: dict[str, Any]) -> str:
    user_id = user_payload.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        raise ValueError("PROVIDER_SNAPSHOT_USER_ID_MISSING")
    return sha256(("elevenlabs:" + user_id).encode("utf-8")).hexdigest()


def _sanitize_model(model: dict[str, Any]) -> dict[str, Any]:
    allowed = (
        "name", "can_be_finetuned", "can_do_text_to_speech", "can_do_voice_conversion",
        "can_use_style", "can_use_speaker_boost", "serves_pro_voices",
        "token_cost_factor", "requires_alpha_access",
        "max_characters_request_free_user", "max_characters_request_subscribed_user",
        "maximum_text_length_per_request", "languages", "model_rates", "concurrency_group",
    )
    return {key: model.get(key) for key in allowed if key in model}


def _sanitize_voice(voice: dict[str, Any]) -> dict[str, Any]:
    allowed = (
        "name", "category", "labels", "description", "available_for_tiers",
        "is_owner", "is_legacy", "is_mixed", "recording_quality", "labelling_status",
    )
    return {key: voice.get(key) for key in allowed if key in voice}


def _subscription_summary(subscription: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    stable = {
        key: subscription.get(key)
        for key in (
            "tier", "status", "voice_limit", "professional_voice_limit",
            "can_use_instant_voice_cloning", "can_use_professional_voice_cloning",
            "currency", "billing_period", "character_refresh_period",
        )
        if key in subscription
    }
    volatile = {
        key: subscription.get(key)
        for key in (
            "character_count", "character_limit", "max_character_limit_extension",
            "max_credit_limit_extension", "voice_slots_used", "professional_voice_slots_used",
            "professional_voice_slots_used_in_workspace", "current_overage",
            "has_open_invoices", "next_character_count_reset_unix",
        )
        if key in subscription
    }
    return stable, volatile


def _list_all_voices(key: str, *, timeout: float) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    voices: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    next_token: str | None = None
    seen_tokens: set[str] = set()
    while True:
        query: dict[str, Any] = {"page_size": 100, "include_total_count": "false"}
        if next_token:
            if next_token in seen_tokens:
                raise RuntimeError(json.dumps({"failure": "FAIL_PROVIDER_PAGINATION_LOOP"}))
            seen_tokens.add(next_token)
            query["next_page_token"] = next_token
        payload, meta = _get("/v2/voices", key, query=query, timeout=timeout)
        page = payload.get("voices")
        if not isinstance(page, list):
            raise RuntimeError(json.dumps({"failure": "FAIL_PROVIDER_RESPONSE_SHAPE", "path": "/v2/voices"}))
        voices.extend(item for item in page if isinstance(item, dict))
        evidence.append(meta)
        if not payload.get("has_more"):
            break
        next_token = payload.get("next_page_token")
        if not isinstance(next_token, str) or not next_token:
            raise RuntimeError(json.dumps({"failure": "FAIL_PROVIDER_PAGINATION_TOKEN_MISSING"}))
    return voices, evidence


def acquire_snapshot(*, timeout: float = 30.0) -> dict[str, Any]:
    key = os.environ.get(KEY_ENV)
    if not key:
        raise RuntimeError(json.dumps({"failure": "FAIL_PROVIDER_CREDENTIAL", "reason": "missing runtime secret env"}))

    user, user_meta = _get("/v1/user", key, timeout=timeout)
    subscription, subscription_meta = _get("/v1/user/subscription", key, timeout=timeout)
    models_payload, models_meta = _get("/v1/models", key, timeout=timeout)
    voices_payload, voice_meta = _list_all_voices(key, timeout=timeout)

    account_fingerprint = _account_fingerprint(user)
    stable_subscription, volatile_subscription = _subscription_summary(subscription)

    if not isinstance(models_payload, list):
        raise RuntimeError(json.dumps({"failure": "FAIL_PROVIDER_RESPONSE_SHAPE", "path": "/v1/models"}))

    models: dict[str, Any] = {}
    for model in models_payload:
        if not isinstance(model, dict):
            continue
        model_id = model.get("model_id")
        if isinstance(model_id, str) and model_id:
            models[model_id] = _sanitize_model(model)

    voices: dict[str, Any] = {}
    for voice in voices_payload:
        voice_id = voice.get("voice_id")
        if isinstance(voice_id, str) and voice_id:
            voices[voice_id] = _sanitize_voice(voice)

    captured_at = utc_now()
    source_evidence = [user_meta, subscription_meta, models_meta, *voice_meta]
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "provider": "elevenlabs",
        "status": "PASS",
        "authentication": {
            "state": "AUTHENTICATED",
            "method": "XI_API_KEY_RUNTIME_ENV",
            "credential_persisted": False,
        },
        "provenance": {
            "captured_at": captured_at,
            "capture_method": "DIRECT_AUTHENTICATED_READ_ONLY_API",
            "capture_engine": CAPTURE_ENGINE,
            "source": source_evidence,
        },
        "account": {
            "fingerprint_sha256": account_fingerprint,
            **stable_subscription,
        },
        "models": models,
        "voices": voices,
        "volatile": {
            "captured_at": captured_at,
            **volatile_subscription,
        },
    }
    sealed = seal_snapshot(snapshot)
    verification = validate_provider_snapshot(sealed, expected_provider="elevenlabs")
    if verification.get("status") != "PASS":
        raise RuntimeError(json.dumps({"failure": "FAIL_PROVIDER_SNAPSHOT_SELF_VERIFY", "verification": verification}))
    return sealed


def main() -> None:
    parser = argparse.ArgumentParser(prog="ivdivo-elevenlabs-snapshot")
    parser.add_argument("--out", required=True)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    snapshot = acquire_snapshot(timeout=args.timeout)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "provider": snapshot["provider"],
        "snapshot_hash": snapshot["snapshot_hash"],
        "voice_count": len(snapshot["voices"]),
        "model_count": len(snapshot["models"]),
        "artifact": str(out),
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
