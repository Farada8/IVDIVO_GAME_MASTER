from __future__ import annotations
from hashlib import sha256
import io, json, wave
from typing import Any

CANARY_BLOCKS = {
    "CH01_S02_RB001": {"units": list(range(1,25)), "chars":1271, "voices":["NARRATOR","ETHAN","AOIFE"],
                       "hash":"4f41805b6aa5ed0506d8c64f43bf0351993fb6b9de113bbcfaad3c10d1fddf8c",
                       "pronunciation":["AOIFE","CONTACT"]},
    "CH01_S02_RB002": {"units": list(range(25,30)), "chars":203, "voices":["NARRATOR","ETHAN","AOIFE"],
                       "hash":"f991022b8c13cc7b5b071caa4f11ee8dc6bd1b5def11fdffc971a9fb18c0b572",
                       "pronunciation":[]},
    "CH01_S02_RB003": {"units": list(range(30,37)), "chars":689, "voices":["NARRATOR"],
                       "hash":"425bdf23b2a02cda5f71531ca48bb5e32dfe5de777fd5bbc92c8255a1504a464",
                       "pronunciation":["CONTACT"]},
}
VALID_PAUSE_FUNCTIONS = {
    "THOUGHT","HESITATION","RECOGNITION","STATUS","REFUSAL","ATTRACTION",
    "SHOCK","LISTENING","OBJECT_ACTION","AFTERMATH","COMIC_TIMING",
    "INTERRUPTION_WINDOW","NO_REPLY"
}
PERFORMANCE_HARD_FAILS = {
    "TRAILER_VOICE","MELODRAMATIC_EMPHASIS","IDENTICAL_ENDINGS","NO_LISTENING",
    "STATUS_FLATTENING","ROBOTIC_BREATH","ADULT_ON_YOUTH","FALSE_INTIMACY"
}

def canonical_hash(obj: Any) -> str:
    return sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode()).hexdigest()

def clean_dry_build():
    return {
        "project":"LESSON_ZERO_RU_AUDIO",
        "episode":"BOOK1_CH01",
        "live_calls":False,
        "dispatch_allowed":False,
        "spoken_units":sum(len(x["units"]) for x in CANARY_BLOCKS.values()),
        "blocks":CANARY_BLOCKS,
    }

def resume_request(request_hash: str, ledger: dict[str,str]) -> str:
    if request_hash in ledger:
        return "REUSED"
    ledger[request_hash] = "PLANNED"
    return "PLANNED"

def invalidate(changed: str) -> set[str]:
    if changed == "voice_binding_version":
        return set(CANARY_BLOCKS)
    if changed == "pronunciation_version":
        return {bid for bid,b in CANARY_BLOCKS.items() if b["pronunciation"]}
    return set()

def selective_rerender(failed_block: str) -> list[str]:
    if failed_block not in CANARY_BLOCKS:
        raise KeyError(failed_block)
    return [failed_block]

def normalize_error(status: int, code: str | None = None) -> dict[str,Any]:
    retryable = status in (408,429,500,502,503,504)
    category = "AUTH" if status in (401,403) else "RATE_LIMIT" if status == 429 else "PROVIDER"
    return {"status":status,"code":code,"category":category,"retryable":retryable}

def retry_policy(error: dict[str,Any], response_started: bool=False) -> str:
    if response_started:
        return "QUARANTINE_AMBIGUOUS"
    if error["category"] == "AUTH":
        return "FAIL_CLOSED"
    if error["retryable"]:
        return "BACKOFF_RETRY"
    return "FAIL_CLOSED"

def pcm_s16le_to_wav(pcm: bytes, sample_rate=48000, channels=1) -> bytes:
    out=io.BytesIO()
    with wave.open(out,'wb') as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm)
    return out.getvalue()

def normalize_ttd_alignment(raw: dict[str,Any], turn_ids:list[str]) -> list[dict[str,Any]]:
    segs=raw.get("voice_segments")
    if not isinstance(segs,list):
        raise ValueError("ALIGNMENT_SCHEMA_UNSUPPORTED")
    out=[]
    for s in segs:
        i=s.get("dialogue_input_index")
        if i is None or i<0 or i>=len(turn_ids):
            raise ValueError("ALIGNMENT_TURN_UNPROVEN")
        out.append({"turn_id":turn_ids[i],"start":s["start_time_seconds"],"end":s["end_time_seconds"],"source_schema":"voice_segments"})
    return out

def normalize_tts_alignment(raw: dict[str,Any], turn_id:str) -> dict[str,Any]:
    a=raw.get("alignment") or raw.get("normalized_alignment")
    if not a or not a.get("character_start_times_seconds") or not a.get("character_end_times_seconds"):
        raise ValueError("ALIGNMENT_MISSING")
    return {"turn_id":turn_id,"start":min(a["character_start_times_seconds"]),
            "end":max(a["character_end_times_seconds"]),"source_schema":"character_alignment"}

def voice_drift(expected:str, observed:str|None) -> str:
    return "PASS" if observed == expected else "FAIL_VOICE_BINDING_DRIFT"

def provider_neutral_compilation() -> dict[str,Any]:
    return {"render_block_id":"RB","mode":"TTD_BLOCK","source_turn_ids":["U1"],"playable_direction":"restrained",
            "text_protected":True,"pronunciation_refs":[]}

def normalized_provider_response(provider:str, request_hash:str) -> dict[str,Any]:
    return {"provider":provider,"request_hash":request_hash,"status":"CANDIDATE","alignment_schema":"NORMALIZED"}

def silent_reaction_anchor():
    return {"anchor_id":"SR_CH01_S02_024_025","character_id":"ETHAN","trigger":"CH01_S02_U024",
            "silent_action":"question lands; no immediate verbal answer","silence_policy":"PROTECTED",
            "spoken_unit_delta":0}

def reply_latency_plan():
    return {
        "U024->U026":"PROTECTED_WAIT",
        "U026":"FAST_DEFENSIVE",
        "U027":"WAIT_THEN_PUNCTURE",
        "U028":"FASTER_DEFLECTION",
        "U029":"PLAIN_NO_RUSH",
    }

def microphone_states():
    return {"CLOSE_INTIMATE","NORMAL","ACROSS_ROOM","MEDIA"}

def media_bus(kind:str)->str:
    return {"dialogue":"DIALOGUE","music":"MUSIC","sfx":"SFX"}[kind]
