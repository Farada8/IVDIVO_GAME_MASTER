"""NMM policy wrapper around the current universal authenticated provider snapshot contract.

NMM does not reimplement provider authentication/hash/freshness rules. Those are
owned by audio/studio/provider_snapshot_contract.py. This module only adds NMM
voice-selection policy after the universal contract passes.
"""
from __future__ import annotations
from datetime import datetime

UNIVERSAL_MAX_AGE_SECONDS = 6 * 60 * 60

try:
    from provider_snapshot_contract import validate_provider_snapshot as _UNIVERSAL_VALIDATOR
except ImportError:
    _UNIVERSAL_VALIDATOR = None


def _parse_now(value: str | None):
    if value is None:
        return None
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def validate_snapshot(snapshot: dict, *, now_iso: str | None = None, approved_voice_ids: list[str] | None = None, universal_validator=None) -> dict:
    validator = universal_validator or _UNIVERSAL_VALIDATOR
    if validator is None:
        return {"gate": "FAIL_CLOSED", "reason": "UNIVERSAL_PROVIDER_CONTRACT_UNAVAILABLE", "delegated": False}
    universal = validator(snapshot, expected_provider="elevenlabs", max_age_seconds=UNIVERSAL_MAX_AGE_SECONDS, now=_parse_now(now_iso))
    if universal.get("status") != "PASS" or universal.get("verified") is not True:
        return {"gate": "FAIL_CLOSED", "reason": "UNIVERSAL_PROVIDER_CONTRACT_FAIL", "universal_status": universal.get("status"), "delegated": True}
    voice_ids = list(approved_voice_ids or [])
    if not voice_ids:
        return {"gate": "METADATA_ONLY", "reason": "NO_NMM_APPROVED_VOICE_IDS", "snapshot_hash": universal.get("snapshot_hash"), "delegated": True}
    inventory = snapshot.get("voices") if isinstance(snapshot, dict) else None
    if not isinstance(inventory, dict):
        return {"gate": "FAIL_CLOSED", "reason": "VOICE_INVENTORY_SHAPE", "delegated": True}
    missing = [voice_id for voice_id in voice_ids if voice_id not in inventory]
    if missing:
        return {"gate": "FAIL_CLOSED", "reason": "NMM_VOICE_ID_NOT_IN_VERIFIED_SNAPSHOT", "missing_voice_ids": missing, "delegated": True}
    return {"gate": "ELIGIBLE_FOR_UNIVERSAL_PRESPEND_GATE", "snapshot_hash": universal.get("snapshot_hash"), "approved_voice_ids": voice_ids, "delegated": True, "voice_lock": False, "take_lock": False, "law": "Universal provider PASS authorizes capability evidence only; NMM availability never implies voice/take lock."}


def credential_environment_state(env: dict) -> dict:
    present = bool(env.get("ELEVENLABS_API_KEY"))
    return {"credential_present": present, "gate": "CAN_ATTEMPT_UNIVERSAL_SNAPSHOT_ACQUIRER" if present else "HOLD_NO_CREDENTIAL", "secret_value_persisted": False}
