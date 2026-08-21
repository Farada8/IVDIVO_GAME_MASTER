"""Validate authenticated provider-preflight evidence before any NMM spend/voice binding."""
from __future__ import annotations
from datetime import datetime

def _dt(s): return datetime.fromisoformat(str(s).replace('Z','+00:00'))
def validate_snapshot(snapshot:dict, *, now_iso:str, max_age_hours:int=24)->dict:
    required=["provider","provider_model","output_format","captured_at","authenticated","preflight_artifact_sha256","capabilities"]
    missing=[k for k in required if snapshot.get(k) in (None,"",[]) ]
    if missing: return {"gate":"FAIL_CLOSED","reason":"MISSING_REQUIRED","missing":missing}
    if snapshot.get("authenticated") is not True: return {"gate":"FAIL_CLOSED","reason":"NOT_AUTHENTICATED"}
    age=(_dt(now_iso)-_dt(snapshot["captured_at"])).total_seconds()/3600
    if age < 0: return {"gate":"FAIL_CLOSED","reason":"FUTURE_TIMESTAMP"}
    if age > max_age_hours: return {"gate":"STALE_REVALIDATE","reason":"SNAPSHOT_TOO_OLD","age_hours":age}
    if not snapshot.get("approved_voice_ids"):
        return {"gate":"METADATA_ONLY","reason":"NO_APPROVED_VOICE_IDS","age_hours":age}
    return {"gate":"ELIGIBLE_FOR_PRESPEND_GATE","age_hours":age,"law":"Provider availability never implies voice/take lock."}

def credential_environment_state(env:dict)->dict:
    present=bool(env.get("ELEVENLABS_API_KEY"))
    return {"credential_present":present,"gate":"CAN_ATTEMPT_AUTHENTICATED_PREFLIGHT" if present else "HOLD_NO_CREDENTIAL",
            "secret_value_persisted":False}
