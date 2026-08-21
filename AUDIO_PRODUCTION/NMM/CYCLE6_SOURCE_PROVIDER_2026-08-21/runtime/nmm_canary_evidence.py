from __future__ import annotations
import hashlib, json

def ingest_canary(*, dispatch_status:str, audio_bytes:bytes|None, request_hash:str|None, spend_receipt:dict|None, metadata:dict|None) -> dict:
    if dispatch_status!="GO_ONE_BOUNDED_CANARY": return {"status":"HOLD_EXTERNAL","reason":"DISPATCH_GATE_NOT_GO"}
    if not audio_bytes: return {"status":"FAIL_CLOSED","reason":"AUDIO_BYTES_MISSING"}
    if not request_hash or not spend_receipt: return {"status":"FAIL_CLOSED","reason":"PROVENANCE_OR_SPEND_MISSING"}
    md=metadata or {}
    return {"status":"PASS","audio_sha256":hashlib.sha256(audio_bytes).hexdigest(),"request_hash":request_hash,"spend_receipt":spend_receipt,"metadata":md,"voice_lock":False}

def technical_compare(canaries:list[dict]) -> dict:
    passed=[c for c in canaries if c.get("status")=="PASS"]
    if not passed: return {"status":"HOLD_EXTERNAL","reason":"NO_LIVE_CANARIES","admissible":[]}
    admissible=[c for c in passed if c.get("metadata",{}).get("decodable",True) and c.get("metadata",{}).get("alignment_status") not in {"QUARANTINE","FAIL"}]
    return {"status":"PASS" if admissible else "FAIL_CLOSED","admissible":admissible}

def blinded_s1_map(candidate_ids:list[str]|None) -> dict:
    if not candidate_ids: return {"status":"HOLD_EXTERNAL","labels":{}}
    labels={cid:chr(65+i) for i,cid in enumerate(candidate_ids)}
    return {"status":"PASS","labels":labels,"identity_hidden":True}

def provisional_eligibility(canaries:list[dict]) -> dict:
    passed=[c for c in canaries if c.get("status")=="PASS"]
    return {"status":"EVIDENCE_PRESENT" if passed else "HOLD_EXTERNAL","eligible_count":len(passed),"voice_lock":False}

def reject_taxonomy(canaries:list[dict], spend_receipts:list[dict]|None=None) -> dict:
    cats={"AUTH":0,"SOURCE_DRIFT":0,"PROVIDER":0,"DECODE":0,"ALIGNMENT":0,"ARTIFACT":0,"PRONUNCIATION":0,"OTHER":0}
    for c in canaries:
        reason=str(c.get("reason","")).upper()
        key=next((k for k in cats if k in reason),"OTHER")
        if c.get("status")!="PASS": cats[key]+=1
    receipts=spend_receipts or []
    measured=None if not receipts else sum(float(r.get("amount",0)) for r in receipts if r.get("amount") is not None)
    return {"taxonomy":cats,"measured_spend":measured,"spend_is_measured":bool(receipts)}

def evidence_packet(*, source_bindings:list[dict], provider:dict, candidate_sets:list[dict], canaries:list[dict], spend:dict) -> dict:
    external_complete=provider.get("status")=="PASS" and bool(canaries) and all(c.get("status")=="PASS" for c in canaries)
    packet={"source_bindings":source_bindings,"provider":provider,"candidate_sets":candidate_sets,"canaries":canaries,"spend":spend,"voice_lock":False,"release_go":False}
    packet["status"]="PROVIDER_CAST_PACKET_COMPLETE_HUMAN_PENDING" if external_complete else "ENGINEERING_READY_EXTERNAL_HOLD"
    packet["packet_hash"]=hashlib.sha256(json.dumps(packet,sort_keys=True,default=str,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
    return packet
