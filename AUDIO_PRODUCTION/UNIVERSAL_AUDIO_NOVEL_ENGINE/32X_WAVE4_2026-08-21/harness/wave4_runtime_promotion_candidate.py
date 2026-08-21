from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable
from hashlib import sha256
import json, io, wave

CANARY_BLOCKS = {
    "CH01_S02_RB001": {"units": list(range(1,25)), "chars":1271, "voices":["NARRATOR","ETHAN","AOIFE"], "hash":"4f41805b6aa5ed0506d8c64f43bf0351993fb6b9de113bbcfaad3c10d1fddf8c", "pronunciation":["AOIFE","CONTACT"]},
    "CH01_S02_RB002": {"units": list(range(25,30)), "chars":203, "voices":["NARRATOR","ETHAN","AOIFE"], "hash":"f991022b8c13cc7b5b071caa4f11ee8dc6bd1b5def11fdffc971a9fb18c0b572", "pronunciation":[]},
    "CH01_S02_RB003": {"units": list(range(30,37)), "chars":689, "voices":["NARRATOR"], "hash":"425bdf23b2a02cda5f71531ca48bb5e32dfe5de777fd5bbc92c8255a1504a464", "pronunciation":["CONTACT"]},
}
LEDGER_STATES={"PLANNED","SENT","AMBIGUOUS","ACCEPTED","REJECTED"}

def canonical_hash(obj:Any)->str:
    return sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def canary_manifest()->dict[str,Any]:
    return {"project":"LESSON_ZERO_RU_AUDIO","episode":"BOOK1_CH01","dispatch_allowed":False,"request_count":3,"spoken_units":36,"provider_characters":2163,"blocks":CANARY_BLOCKS,"voice_bindings":{"NARRATOR":None,"ETHAN":None,"AOIFE":None},"pronunciation_version":"UNLOCKED","binding_version":"UNCAST"}

def validate_canary_identity(m:dict[str,Any])->dict[str,Any]:
    if m.get("request_count")!=3: raise ValueError("CANARY_REQUEST_COUNT_DRIFT")
    if m.get("spoken_units")!=36: raise ValueError("CANARY_UNIT_COUNT_DRIFT")
    if m.get("provider_characters")!=2163: raise ValueError("CANARY_CHARACTER_COUNT_DRIFT")
    blocks=m.get("blocks")
    if not isinstance(blocks,dict) or set(blocks)!=set(CANARY_BLOCKS): raise ValueError("CANARY_BLOCK_SET_DRIFT")
    seen=[]
    for bid,exp in CANARY_BLOCKS.items():
        got=blocks[bid]
        for k in ("units","chars","voices","hash"):
            if got.get(k)!=exp[k]: raise ValueError(f"CANARY_{bid}_{k.upper()}_DRIFT")
        seen.extend(got["units"])
    if seen!=list(range(1,37)): raise ValueError("CANARY_UNIT_COVERAGE_DRIFT")
    return {"status":"PASS","requests":3,"units":36,"chars":2163}

def pronunciation_audition_manifest()->dict[str,Any]:
    return {"status":"READY_DRY_NOT_HEARD","exact_text_mutation_allowed":False,"pronunciation_lock":False,"targets":[{"block_id":"CH01_S02_RB001","source_hash":CANARY_BLOCKS["CH01_S02_RB001"]["hash"],"tokens":["AOIFE","CONTACT"]},{"block_id":"CH01_S02_RB003","source_hash":CANARY_BLOCKS["CH01_S02_RB003"]["hash"],"tokens":["CONTACT"]}]}

@dataclass
class Attempt:
    request_hash:str
    block_id:str
    state:str="PLANNED"
    provider_request_id:str|None=None
    response_hash:str|None=None
    charge:float|None=None

class SpendLedger:
    def __init__(self,path:str|Path):
        self.path=Path(path); self.attempts={}
        if self.path.exists():
            raw=json.loads(self.path.read_text(encoding="utf-8")); self.attempts={k:Attempt(**v) for k,v in raw.items()}
    def _save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.path.write_text(json.dumps({k:asdict(v) for k,v in self.attempts.items()},ensure_ascii=False,indent=2,sort_keys=True),encoding="utf-8")
    def plan(self,request_hash:str,block_id:str)->str:
        old=self.attempts.get(request_hash)
        if old:
            if old.state=="ACCEPTED": return "REUSED_ACCEPTED"
            if old.state=="AMBIGUOUS": return "RECONCILE_REQUIRED"
            return f"EXISTS_{old.state}"
        self.attempts[request_hash]=Attempt(request_hash,block_id); self._save(); return "PLANNED"
    def transition(self,request_hash:str,state:str,provider_request_id=None,response_hash=None,charge=None):
        if state not in LEDGER_STATES: raise ValueError("INVALID_LEDGER_STATE")
        if request_hash not in self.attempts: raise KeyError(request_hash)
        a=self.attempts[request_hash]
        if a.state=="ACCEPTED" and state!="ACCEPTED": raise ValueError("ACCEPTED_ATTEMPT_IMMUTABLE")
        if a.state=="AMBIGUOUS" and state=="SENT": raise ValueError("AMBIGUOUS_REQUIRES_RECONCILIATION")
        a.state=state
        if provider_request_id is not None: a.provider_request_id=provider_request_id
        if response_hash is not None: a.response_hash=response_hash
        if charge is not None: a.charge=float(charge)
        self._save()

def reconcile_ambiguous(attempt:Attempt, provider_lookup:Callable[[str],dict[str,Any]|None])->dict[str,Any]:
    if attempt.state!="AMBIGUOUS": return {"status":"NOT_REQUIRED","action":"NONE"}
    if not attempt.provider_request_id: return {"status":"HOLD","action":"NO_RETRY","reason":"NO_PROVIDER_REQUEST_ID"}
    found=provider_lookup(attempt.provider_request_id)
    if found is None: return {"status":"HOLD","action":"NO_RETRY","reason":"PROVIDER_STATE_UNRESOLVED"}
    if found.get("accepted") and found.get("response_hash"): return {"status":"RECONCILED_ACCEPTED","action":"REUSE","response_hash":found["response_hash"]}
    if found.get("definitive_failure"): return {"status":"RECONCILED_FAILED","action":"RETRY_ALLOWED"}
    return {"status":"HOLD","action":"NO_RETRY","reason":"AMBIGUOUS_PROVIDER_STATE"}

def normalize_provider_error(status:int|None=None,code:str|None=None,message:str="")->dict[str,Any]:
    c=(code or "").upper(); m=message.upper()
    if status in (401,403) or "AUTH" in c: cat,retry="AUTH",False
    elif "VOICE" in c: cat,retry="VOICE",False
    elif "MODEL" in c: cat,retry="MODEL",False
    elif "ALIGN" in c: cat,retry="ALIGNMENT",False
    elif "FORMAT" in c or "AUDIO_FORMAT" in c: cat,retry="FORMAT",False
    elif "QUOTA" in c or "CREDIT" in m: cat,retry="QUOTA",False
    elif status==429 or "RATE" in c: cat,retry="RATE_LIMIT",True
    elif status in (408,504) or "TIMEOUT" in c: cat,retry="TIMEOUT",True
    elif status in (400,404,422) or "INVALID" in c: cat,retry="INVALID_REQUEST",False
    else: cat,retry="PROVIDER",status in (500,502,503)
    return {"category":cat,"retryable":retry,"status":status,"code":code}

def pcm_s16le_to_wav(pcm:bytes,sample_rate:int=48000,channels:int=1)->bytes:
    if sample_rate!=48000: raise ValueError("UNSUPPORTED_SAMPLE_RATE")
    if channels not in (1,2): raise ValueError("UNSUPPORTED_CHANNEL_COUNT")
    if len(pcm)%(2*channels): raise ValueError("MALFORMED_PCM_LENGTH")
    out=io.BytesIO()
    with wave.open(out,"wb") as w:
        w.setnchannels(channels); w.setsampwidth(2); w.setframerate(sample_rate); w.writeframes(pcm)
    return out.getvalue()

def asset_fingerprint(data:bytes)->dict[str,Any]: return {"sha256":sha256(data).hexdigest(),"bytes":len(data)}

def normalize_ttd_alignment(raw:dict[str,Any],turn_ids:list[str])->list[dict[str,Any]]:
    segs=raw.get("voice_segments")
    if not isinstance(segs,list) or not segs: raise ValueError("ALIGNMENT_SCHEMA_UNSUPPORTED")
    out=[]
    for s in segs:
        i=s.get("dialogue_input_index")
        if not isinstance(i,int) or not 0<=i<len(turn_ids): raise ValueError("ALIGNMENT_TURN_UNPROVEN")
        st,en=s.get("start_time_seconds"),s.get("end_time_seconds")
        if not isinstance(st,(int,float)) or not isinstance(en,(int,float)) or en<st: raise ValueError("ALIGNMENT_INTERVAL_INVALID")
        out.append({"turn_id":turn_ids[i],"start":float(st),"end":float(en),"source_schema":"voice_segments"})
    return out

def normalize_tts_alignment(raw:dict[str,Any],turn_id:str)->dict[str,Any]:
    a=raw.get("alignment") or raw.get("normalized_alignment")
    if not isinstance(a,dict): raise ValueError("ALIGNMENT_MISSING")
    starts=a.get("character_start_times_seconds"); ends=a.get("character_end_times_seconds")
    if not starts or not ends or len(starts)!=len(ends): raise ValueError("ALIGNMENT_MISSING")
    if any(e<s for s,e in zip(starts,ends)): raise ValueError("ALIGNMENT_INTERVAL_INVALID")
    return {"turn_id":turn_id,"start":float(min(starts)),"end":float(max(ends)),"source_schema":"character_alignment"}

def normalize_alignment(raw:dict[str,Any],turn_ids:list[str]|None=None,turn_id:str|None=None):
    if "voice_segments" in raw:
        if not turn_ids: raise ValueError("TURN_IDS_REQUIRED")
        return normalize_ttd_alignment(raw,turn_ids)
    if "alignment" in raw or "normalized_alignment" in raw:
        if not turn_id: raise ValueError("TURN_ID_REQUIRED")
        return normalize_tts_alignment(raw,turn_id)
    raise ValueError("ALIGNMENT_SCHEMA_UNSUPPORTED")

def capability_drift(expected:dict[str,Any],snapshot:dict[str,Any])->dict[str,Any]:
    voices=snapshot.get("voices",{})
    if isinstance(voices,list): voices={x.get("voice_id"):x for x in voices if isinstance(x,dict) and x.get("voice_id")}
    missing_voices=[x for x in expected.get("voice_ids",[]) if x not in voices]
    missing_models=[x for x in expected.get("model_ids",[]) if x not in snapshot.get("models",[])]
    return {"status":"PASS" if not missing_voices and not missing_models else "FAIL_DRIFT","missing_voices":missing_voices,"missing_models":missing_models,"auto_substitution":False}

def role_binding_invalidation(role:str)->list[str]:
    if role not in {"NARRATOR","ETHAN","AOIFE"}: return []
    return sorted([bid for bid,b in CANARY_BLOCKS.items() if role in b["voices"]])

def pronunciation_invalidation()->list[str]: return sorted([bid for bid,b in CANARY_BLOCKS.items() if b["pronunciation"]])

def live_provenance_gate(records:list[dict[str,Any]])->dict[str,Any]:
    if len(records)!=3: return {"status":"HOLD","reason":"REQUIRES_EXACTLY_3_ACCEPTED_RESPONSES"}
    req={"request_hash","provider_request_id","audio_sha256","alignment_raw","binding_version"}
    missing=[i for i,r in enumerate(records) if not req.issubset(r)]
    return {"status":"PASS" if not missing else "HOLD","missing_record_indexes":missing}

def unit_alignment_coverage(unit_ids:list[str], mapped:list[str])->dict[str,Any]:
    missing=[u for u in unit_ids if mapped.count(u)==0]; dup=[u for u in unit_ids if mapped.count(u)>1]; extra=sorted(set(mapped)-set(unit_ids))
    return {"status":"PASS" if not missing and not dup and not extra else "FAIL","missing":missing,"duplicate":dup,"extra":extra}

def synthetic_timing_firewall(source_kind:str)->dict[str,Any]:
    if source_kind!="LIVE_PROVIDER_ALIGNMENT": return {"status":"FAIL_CLOSED","timeline_allowed":False}
    return {"status":"PASS","timeline_allowed":True}
