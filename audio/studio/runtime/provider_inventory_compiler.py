#!/usr/bin/env python3
"""IVDIVO Audio Studio — compile a validated provider capability inventory.

The compiler consumes an authenticated secret-free ProviderSnapshot and emits a
provider-neutral inventory for downstream casting. It does not contact a
provider, does not guess missing capabilities and cannot voice-lock or select an
artistic winner.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from provider_snapshot_contract import canonical_hash, validate_provider_snapshot


def compile_provider_inventory(
    snapshot: dict[str, Any],
    *,
    expected_provider: str = "elevenlabs",
    max_age_seconds: float = 21600,
    now: datetime | None = None,
) -> dict[str, Any]:
    validation = validate_provider_snapshot(
        snapshot,
        expected_provider=expected_provider,
        max_age_seconds=max_age_seconds,
        now=now,
    )
    if not validation.get("verified"):
        return {
            "status": "HOLD_PROVIDER_SNAPSHOT",
            "verified": False,
            "provider_validation": validation,
            "voice_lock": False,
            "auto_substitution": False,
        }

    models = snapshot.get("models", {})
    voices = snapshot.get("voices", {})
    compiled_models: list[dict[str, Any]] = []
    for model_id, metadata in sorted(models.items()):
        metadata = metadata if isinstance(metadata, dict) else {}
        compiled_models.append({
            "model_id": model_id,
            "name": metadata.get("name"),
            "can_do_text_to_speech": metadata.get("can_do_text_to_speech"),
            "can_use_style": metadata.get("can_use_style"),
            "can_use_speaker_boost": metadata.get("can_use_speaker_boost"),
            "maximum_text_length_per_request": metadata.get("maximum_text_length_per_request"),
            "metadata_hash": canonical_hash(metadata),
        })

    compiled_voices: list[dict[str, Any]] = []
    for voice_id, metadata in sorted(voices.items()):
        metadata = metadata if isinstance(metadata, dict) else {}
        compiled_voices.append({
            "voice_id": voice_id,
            "name": metadata.get("name"),
            "category": metadata.get("category"),
            "labels": metadata.get("labels") if isinstance(metadata.get("labels"), dict) else {},
            "recording_quality": metadata.get("recording_quality"),
            "available_for_tiers": metadata.get("available_for_tiers"),
            "metadata_hash": canonical_hash(metadata),
        })

    tts_model_ids = sorted(
        row["model_id"] for row in compiled_models if row.get("can_do_text_to_speech") is True
    )
    status = "PASS" if compiled_voices and tts_model_ids else "HOLD_CAPABILITY_INCOMPLETE"
    return {
        "schema": "ivdivo.provider_inventory/1.0",
        "status": status,
        "verified": status == "PASS",
        "provider": expected_provider,
        "source_snapshot_hash": validation["snapshot_hash"],
        "captured_at": validation["captured_at"],
        "account_fingerprint_sha256": snapshot.get("account", {}).get("fingerprint_sha256"),
        "models": compiled_models,
        "voices": compiled_voices,
        "tts_model_ids": tts_model_ids,
        "voice_count": len(compiled_voices),
        "model_count": len(compiled_models),
        "selection_authority": "HUMAN_OR_EXPLICIT_CAST_RULES",
        "voice_lock": False,
        "auto_substitution": False,
        "provider_calls_performed": 0,
    }
