from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from hashlib import sha256
import json, io, wave, statistics, re

CANARY_BLOCKS = {
    "CH01_S02_RB001": {
        "units": list(range(1,25)), "chars":1271, "voices":["NARRATOR","ETHAN","AOIFE"],
        "hash":"4f41805b6aa5ed0506d8c64f43bf0351993fb6b9de113bbcfaad3c10d1fddf8c",
        "pronunciation":["AOIFE","CONTACT"]
    },
    "CH01_S02_RB002": {
        "units": list(range(25,30)), "chars":203, "voices":["NARRATOR","ETHAN","AOIFE"],
        "hash":"f991022b8c13cc7b5b071caa4f11ee8dc6bd1b5def11fdffc971a9fb18c0b572",
        "pronunciation":[]
    },
    "CH01_S02_RB003": {
        "units": list(range(30,37)), "chars":689, "voices":["NARRATOR"],
        "hash":"425bdf23b2a02cda5f71531ca48bb5e32dfe5de777fd5bbc92c8255a1504a464",
        "pronunciation":["CONTACT"]
    },
}

VALID_PAUSE_FUNCTIONS = {
    "THOUGHT","HESITATION","RECOGNITION","STATUS","REFUSAL","ATTRACTION",
    "SHOCK","LISTENING","OBJECT_ACTION","AFTERMATH","COMIC_TIMING",
    "INTERRUPTION_WINDOW","NO_REPLY"
}
MIC_PERSPECTIVES = {"CLOSE","NORMAL","ACROSS_ROOM","MEDIA"}
LEDGER_STATES = {"PLANNED","SENT","AMBIGUOUS","ACCEPTED","REJECTED"}
ERROR_CATEGORIES = {
    "AUTH","RATE_LIMIT","QUOTA","INVALID_REQUEST","FORMAT","TIMEOUT",
    "ALIGNMENT","MODEL","VOICE","PROVIDER"
}

def canonical_hash(obj: Any) -> str:
    return sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode()).hexdigest()

def clean_dry_manifest() -> dict[str, Any]:
    return {
        "project":"LESSON_ZERO_RU_AUDIO",
        "episode":"BOOK1_CH01",
        "dispatch_allowed":False,
        "spoken_units":36,
        "characters":2163,
        "blocks":CANARY_BLOCKS,
        "voice_bindings":{"NARRATOR":None,"ETHAN":None,"AOIFE":None},
        "pronunciation_version":"UNLOCKED",
        "binding_version":"UNCAST",
    }

def validate_canary_identity(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest.get("spoken_units") != 36:
        raise ValueError("CANARY_UNIT_COUNT_DRIFT")
    if manifest.get("characters") != 2163:
        raise ValueError("CANARY_CHARACTER_COUNT_DRIFT")
    blocks = manifest.get("blocks")
    if not isinstance(blocks, dict) or set(blocks) != set(CANARY_BLOCKS):
        raise ValueError("CANARY_BLOCK_SET_DRIFT")
    units = []
    for bid, exp in CANARY_BLOCKS.items():
        got = blocks[bid]
        for k in ("chars","hash","voices","units"):
            if got.get(k) != exp[k]:
                raise ValueError(f"CANARY_{bid}_{k.upper()}_DRIFT")
        units.extend(got["units"])
    if units != list(range(1,37)):
        raise ValueError("CANARY_UNIT_COVERAGE_DRIFT")
    return {"status":"PASS","blocks":3,"spoken_units":36,"characters":2163}

@dataclass
class Attempt:
    request_hash: str
    block_id: str
    state: str
    provider_request_id: str | None = None
    response_hash: str | None = None

class SpendLedger:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.attempts: dict[str, Attempt] = {}
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.attempts = {k: Attempt(**v) for k,v in raw.items()}

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({k:asdict(v) for k,v in self.attempts.items()}, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8"
        )

    def plan(self, request_hash: str, block_id: str) -> str:
        old = self.attempts.get(request_hash)
        if old:
            if old.state == "ACCEPTED":
                return "REUSED_ACCEPTED"
            if old.state == "AMBIGUOUS":
                return "RECONCILE_REQUIRED"
            return f"EXISTS_{old.state}"
        self.attempts[request_hash] = Attempt(request_hash, block_id, "PLANNED")
        self._save()
        return "PLANNED"

    def transition(self, request_hash: str, state: str, provider_request_id: str|None=None, response_hash: str|None=None):
        if state not in LEDGER_STATES:
            raise ValueError("INVALID_LEDGER_STATE")
        if request_hash not in self.attempts:
            raise KeyError(request_hash)
        current = self.attempts[request_hash]
        if current.state == "ACCEPTED" and state != "ACCEPTED":
            raise ValueError("ACCEPTED_ATTEMPT_IMMUTABLE")
        if current.state == "AMBIGUOUS" and state == "SENT":
            raise ValueError("AMBIGUOUS_REQUIRES_RECONCILIATION")
        current.state = state
        if provider_request_id is not None:
            current.provider_request_id = provider_request_id
        if response_hash is not None:
            current.response_hash = response_hash
        self._save()

def normalize_provider_error(status: int|None=None, code: str|None=None, message: str="") -> dict[str, Any]:
    c = (code or "").upper()
    m = message.upper()
    if status in (401,403) or "AUTH" in c:
        cat="AUTH"; retry=False
    elif "VOICE" in c:
        cat="VOICE"; retry=False
    elif "MODEL" in c:
        cat="MODEL"; retry=False
    elif "ALIGN" in c:
        cat="ALIGNMENT"; retry=False
    elif "FORMAT" in c or "AUDIO_FORMAT" in c:
        cat="FORMAT"; retry=False
    elif "QUOTA" in c or "CREDIT" in m:
        cat="QUOTA"; retry=False
    elif status == 429 or "RATE" in c:
        cat="RATE_LIMIT"; retry=True
    elif status in (408,504) or "TIMEOUT" in c:
        cat="TIMEOUT"; retry=True
    elif status in (400,404,422) or "INVALID" in c:
        cat="INVALID_REQUEST"; retry=False
    else:
        cat="PROVIDER"; retry=bool(status in (500,502,503))
    return {"category":cat,"retryable":retry,"status":status,"code":code}

def retry_decision(error: dict[str,Any], response_started: bool=False) -> str:
    if response_started:
        return "QUARANTINE_AMBIGUOUS"
    return "BACKOFF_RETRY" if error["retryable"] else "FAIL_CLOSED"

def pcm_s16le_to_wav(pcm: bytes, sample_rate: int=48000, channels: int=1) -> bytes:
    if sample_rate != 48000:
        raise ValueError("UNSUPPORTED_SAMPLE_RATE")
    if channels not in (1,2):
        raise ValueError("UNSUPPORTED_CHANNEL_COUNT")
    frame_bytes = 2 * channels
    if len(pcm) % frame_bytes:
        raise ValueError("MALFORMED_PCM_LENGTH")
    out=io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm)
    return out.getvalue()

def audio_hash(data: bytes) -> str:
    return sha256(data).hexdigest()

def normalize_ttd_alignment(raw: dict[str,Any], turn_ids:list[str]) -> list[dict[str,Any]]:
    segs=raw.get("voice_segments")
    if not isinstance(segs,list) or not segs:
        raise ValueError("ALIGNMENT_SCHEMA_UNSUPPORTED")
    out=[]
    for s in segs:
        i=s.get("dialogue_input_index")
        if not isinstance(i,int) or i<0 or i>=len(turn_ids):
            raise ValueError("ALIGNMENT_TURN_UNPROVEN")
        start=s.get("start_time_seconds"); end=s.get("end_time_seconds")
        if not isinstance(start,(int,float)) or not isinstance(end,(int,float)) or end < start:
            raise ValueError("ALIGNMENT_INTERVAL_INVALID")
        out.append({"turn_id":turn_ids[i],"start":float(start),"end":float(end),"source_schema":"voice_segments"})
    return out

def normalize_tts_alignment(raw: dict[str,Any], turn_id:str) -> dict[str,Any]:
    a=raw.get("alignment") or raw.get("normalized_alignment")
    if not isinstance(a,dict):
        raise ValueError("ALIGNMENT_MISSING")
    starts=a.get("character_start_times_seconds"); ends=a.get("character_end_times_seconds")
    if not starts or not ends or len(starts)!=len(ends):
        raise ValueError("ALIGNMENT_MISSING")
    if any(e < s for s,e in zip(starts,ends)):
        raise ValueError("ALIGNMENT_INTERVAL_INVALID")
    return {"turn_id":turn_id,"start":float(min(starts)),"end":float(max(ends)),"source_schema":"character_alignment"}

def normalize_alignment(raw: dict[str,Any], *, turn_ids:list[str]|None=None, turn_id:str|None=None):
    if "voice_segments" in raw:
        if not turn_ids: raise ValueError("TURN_IDS_REQUIRED")
        return normalize_ttd_alignment(raw, turn_ids)
    if "alignment" in raw or "normalized_alignment" in raw:
        if not turn_id: raise ValueError("TURN_ID_REQUIRED")
        return normalize_tts_alignment(raw, turn_id)
    raise ValueError("ALIGNMENT_SCHEMA_UNSUPPORTED")

def capability_drift(expected: dict[str,str], snapshot: dict[str,Any]) -> dict[str,Any]:
    missing_voices=[vid for vid in expected.get("voice_ids",[]) if vid not in snapshot.get("voices",{})]
    missing_models=[mid for mid in expected.get("model_ids",[]) if mid not in snapshot.get("models",[])]
    return {
        "status":"PASS" if not missing_voices and not missing_models else "FAIL_DRIFT",
        "missing_voices":missing_voices,
        "missing_models":missing_models,
        "auto_substitution":False,
    }

class ProviderAdapterMock2:
    name="mock2"
    def render(self, request: dict[str,Any]) -> dict[str,Any]:
        if "request_hash" not in request or "block_id" not in request:
            raise ValueError("INVALID_REQUEST")
        return {
            "provider":self.name,
            "request_hash":request["request_hash"],
            "block_id":request["block_id"],
            "status":"CANDIDATE",
            "raw_audio":b"\x00\x00"*480,
            "alignment":{"alignment":{"character_start_times_seconds":[0.0], "character_end_times_seconds":[0.01]}}
        }

def promote_silent_reaction(anchor: dict[str,Any]) -> dict[str,Any]:
    required={"anchor_id","character_id","trigger","silent_action","silence_policy"}
    if not required.issubset(anchor):
        raise ValueError("SILENT_REACTION_FIELDS_MISSING")
    out=dict(anchor); out["spoken_unit_delta"]=0
    return out

def compile_pause(functions: list[str], hypotheses_ms: list[int]|None=None) -> dict[str,Any]:
    bad=[x for x in functions if x not in VALID_PAUSE_FUNCTIONS]
    if bad:
        raise ValueError(f"UNSUPPORTED_PAUSE_FUNCTION:{','.join(bad)}")
    return {"functions":functions,"duration_hypotheses_ms":hypotheses_ms or [],"timing_status":"SEMANTIC_UNTIL_ALIGNMENT"}

def compile_reply_latency(trigger: str, response: str, state: str) -> dict[str,Any]:
    if state not in {"PROTECTED_WAIT","FAST_DEFENSIVE","WAIT_THEN_PUNCTURE","FASTER_DEFLECTION","PLAIN_NO_RUSH"}:
        raise ValueError("UNSUPPORTED_LATENCY_STATE")
    return {"trigger":trigger,"response":response,"state":state,"absolute_time":None}

def compile_microphone_choreography(role: str, perspective: str, movement_path:list[str]|None=None) -> dict[str,Any]:
    if perspective not in MIC_PERSPECTIVES:
        raise ValueError("UNSUPPORTED_MIC_PERSPECTIVE")
    return {"role":role,"perspective":perspective,"movement_path":movement_path or [],"mix_pan_required":False}

def ai_tell_flags(line_endings:list[str], pause_intervals:list[float], breath_intervals:list[float]) -> dict[str,Any]:
    flags=[]
    if len(line_endings)>=4:
        normalized=[re.sub(r"\W+","",x.lower()) for x in line_endings]
        if len(set(normalized)) <= max(1,len(normalized)//2):
            flags.append("REPEATED_ENDINGS")
    for label,vals in (("PAUSE_REGULARITY",pause_intervals),("BREATH_REGULARITY",breath_intervals)):
        if len(vals)>=4 and statistics.mean(vals)>0:
            cv=statistics.pstdev(vals)/statistics.mean(vals)
            if cv < 0.06:
                flags.append(label)
    return {"flags":flags,"authoritative":False,"auto_reject":False}

def performance_lock_gate(evidence: dict[str,bool], pair_required: bool=True) -> dict[str,Any]:
    required=["multi_state","pronunciation","fatigue","human_review"]
    if pair_required: required.append("pair")
    missing=[k for k in required if not evidence.get(k)]
    return {
        "status":"LOCKED" if not missing else "HOLD",
        "missing":missing,
        "machine_may_auto_lock":False
    }

def scoped_invalidation(changed: str) -> list[str]:
    if changed == "binding_version":
        return sorted(CANARY_BLOCKS)
    if changed == "pronunciation_version":
        return sorted([bid for bid,b in CANARY_BLOCKS.items() if b["pronunciation"]])
    return []

def orchestration_acceptance(results: dict[str,bool]) -> dict[str,Any]:
    required=["clean_build","resume","scoped_invalidation","selective_rerender","fail_closed"]
    missing=[k for k in required if not results.get(k)]
    return {"status":"PASS_CANDIDATE" if not missing else "HOLD","missing":missing,"promotion":"REQUIRES_MAIN_INTEGRATION_REVIEW"}
