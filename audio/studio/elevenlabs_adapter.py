#!/usr/bin/env python3
"""IVDIVO ElevenLabs adapter v1.0.

Supports TTD with timestamps and single-voice TTS with timestamps, sanitized request
hashing/evidence, audio decode, and provider-neutral alignment normalization.
No ambience/music/Foley mixing and no story decisions.
"""
from __future__ import annotations
import argparse, base64, hashlib, json, os, ssl, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from alignment_normalizer import normalize

BASE_URL="https://api.elevenlabs.io"; KEY_ENV="ELEVENLABS_API_KEY"
TTD_PATH="/v1/text-to-dialogue/with-timestamps"; TTS_PATH_TMPL="/v1/text-to-speech/{voice_id}/with-timestamps"
PROFILE_TTD="ELEVEN_TTD_TIMESTAMPS_V1"; PROFILE_TTS="ELEVEN_TTS_TIMESTAMPS_V1"

def utc_now(): return datetime.now(timezone.utc).isoformat()
def canonical_json_bytes(data): return json.dumps(data,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def sha256_obj(data): return hashlib.sha256(canonical_json_bytes(data)).hexdigest()

def _validate_pronunciation(locators):
    locators=locators or []
    if len(locators)>3: raise ValueError("FAIL_PROVIDER_REQUEST: pronunciation_dictionary_locators > 3")
    for x in locators:
        if not x.get("pronunciation_dictionary_id") and not x.get("id"): raise ValueError("FAIL_PROVIDER_REQUEST: pronunciation dictionary id missing")
        if not x.get("version_id"): raise ValueError("FAIL_PROVIDER_REQUEST: pronunciation dictionary version_id missing")
    return locators

def build_ttd_request(block:dict[str,Any]):
    turns=block.get("turns") or []
    if len(turns)<2: raise ValueError("TTD block requires at least two turns")
    inputs=[]; voices=set(); total=0; unit_ids=[]; text_refs=[]
    for i,t in enumerate(turns):
        text=t.get("exact_text") or t.get("performance_text"); voice=t.get("voice_id")
        if not text or not voice: raise ValueError(f"TTD turn {i} missing text/voice_id")
        inputs.append({"text":text,"voice_id":voice}); voices.add(voice); total+=len(text); unit_ids.append(t.get("unit_id") or f"{block['block_id']}:unit:{i}"); text_refs.append(t.get("text_ref") or t.get("unit_id"))
    if len(voices)>10: raise ValueError("FAIL_PROVIDER_REQUEST: >10 unique TTD voices")
    ceiling=int(block.get("provider_character_ceiling",2000))
    if total>ceiling: raise ValueError(f"FAIL_PROVIDER_REQUEST: TTD chars {total} > ceiling {ceiling}")
    loc=_validate_pronunciation(block.get("pronunciation_dictionary_locators")); body={"inputs":inputs,"model_id":block.get("model_id","eleven_v3")}
    for k in ("language_code","settings","seed","apply_text_normalization"):
        if block.get(k) is not None: body[k]=block[k]
    if loc: body["pronunciation_dictionary_locators"]=loc
    return {"endpoint_profile":PROFILE_TTD,"method":"POST","path":TTD_PATH,"query":{"output_format":block.get("output_format","mp3_44100_128")},"body":body,"unit_ids":unit_ids,"text_refs":text_refs}

def build_tts_request(block:dict[str,Any]):
    text=block.get("exact_text") or block.get("performance_text"); voice=block.get("voice_id")
    if not text or not voice: raise ValueError("TTS block missing text/voice_id")
    loc=_validate_pronunciation(block.get("pronunciation_dictionary_locators")); body={"text":text,"model_id":block.get("model_id","eleven_multilingual_v2")}
    for k in ("language_code","voice_settings","seed","apply_text_normalization"):
        if block.get(k) is not None: body[k]=block[k]
    if loc: body["pronunciation_dictionary_locators"]=loc
    return {"endpoint_profile":PROFILE_TTS,"method":"POST","path":TTS_PATH_TMPL.format(voice_id=urllib.parse.quote(voice,safe="")),"query":{"output_format":block.get("output_format","mp3_44100_128")},"body":body,"unit_ids":[block.get("unit_id") or f"{block['block_id']}:unit:0"],"text_refs":[block.get("text_ref") or block.get("unit_id")]}

def compile_block(block):
    bt=block.get("block_type")
    if bt=="TTD_BLOCK": req=build_ttd_request(block)
    elif bt in {"ISOLATED_TTS","NARRATION_BLOCK","VOCALIZATION_BLOCK"}: req=build_tts_request(block)
    else: raise ValueError(f"Unsupported dispatch block type: {bt}")
    hi={"provider":"elevenlabs","endpoint_profile":req["endpoint_profile"],"path":req["path"],"query":req["query"],"body":req["body"],"block_id":block["block_id"]}; req["block_id"]=block["block_id"]; req["request_hash"]=sha256_obj(hi); return req

def dispatch(compiled,timeout=60.0):
    key=os.environ.get(KEY_ENV)
    if not key: raise RuntimeError(json.dumps({"failure":"FAIL_PROVIDER_CREDENTIAL","reason":"missing secret env"}))
    q=urllib.parse.urlencode(compiled.get("query") or {}); url=BASE_URL+compiled["path"]+("?"+q if q else "")
    req=urllib.request.Request(url,data=json.dumps(compiled["body"],ensure_ascii=False).encode("utf-8"),headers={"Content-Type":"application/json","Accept":"application/json","xi-api-key":key},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=timeout,context=ssl.create_default_context()) as r:
            payload=json.loads(r.read().decode("utf-8")); meta={"http_status":int(r.status)}
            for name in ("request-id","x-request-id"):
                v=r.headers.get(name)
                if v: meta["provider_request_id"]=v; break
            return payload,meta
    except urllib.error.HTTPError as e:
        f="FAIL_PROVIDER_CREDENTIAL" if e.code in (401,403) else ("FAIL_PROVIDER_REQUEST" if 400<=e.code<500 else "FAIL_PROVIDER_CONNECTIVITY"); raise RuntimeError(json.dumps({"failure":f,"http_status":int(e.code)}))
    except Exception as e: raise RuntimeError(json.dumps({"failure":"FAIL_PROVIDER_CONNECTIVITY","error_type":type(e).__name__}))

def extension_from_format(fmt):
    if fmt.startswith("mp3_"): return ".mp3"
    if fmt.startswith("wav_"): return ".wav"
    if fmt.startswith("pcm_"): return ".pcm"
    if fmt.startswith("ulaw_") or fmt.startswith("mulaw_"): return ".ulaw"
    return ".audio"

def persist(compiled,raw,response_meta,out_dir:Path):
    out_dir.mkdir(parents=True,exist_ok=True); bid=compiled["block_id"]; reqp=out_dir/f"{bid}__request.json"; rawp=out_dir/f"{bid}__response.json"; alp=out_dir/f"{bid}__raw_alignment.json"; normp=out_dir/f"{bid}__normalized_alignment.json"
    re={k:v for k,v in compiled.items() if k not in ("unit_ids","text_refs")}; re["recorded_at"]=utc_now(); reqp.write_text(json.dumps(re,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    b64=raw.get("audio_base64")
    if not isinstance(b64,str): raise ValueError("FAIL_PROVIDER_REQUEST: response missing audio_base64")
    audio=base64.b64decode(b64,validate=True); fmt=compiled.get("query",{}).get("output_format","mp3_44100_128"); audiop=out_dir/f"{bid}__audio{extension_from_format(fmt)}"; audiop.write_bytes(audio)
    evidence=dict(raw); evidence["audio_base64"]={"removed_from_json_evidence":True,"decoded_audio_path":str(audiop),"decoded_bytes":len(audio),"sha256":hashlib.sha256(audio).hexdigest()}; evidence["_ivdivo_response_meta"]=response_meta; rawp.write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    ae={k:raw[k] for k in ("voice_segments","alignment","normalized_alignment") if k in raw}; alp.write_text(json.dumps(ae,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    norm=normalize(raw,bid,compiled.get("unit_ids"),compiled.get("text_refs"),provider="elevenlabs",endpoint_profile=compiled["endpoint_profile"],raw_ref=str(alp)); normp.write_text(json.dumps(norm,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return {"block_id":bid,"request_hash":compiled["request_hash"],"request_artifact":str(reqp),"response_artifact":str(rawp),"audio_artifact":str(audiop),"raw_alignment_artifact":str(alp),"normalized_alignment_artifact":str(normp),"audio_sha256":hashlib.sha256(audio).hexdigest(),"provider_response_meta":response_meta}

def main():
    p=argparse.ArgumentParser(); p.add_argument("block_json"); p.add_argument("--out-dir",required=True); p.add_argument("--dry-run",action="store_true"); p.add_argument("--timeout",type=float,default=60.0); a=p.parse_args(); block=json.loads(Path(a.block_json).read_text(encoding="utf-8")); c=compile_block(block); out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); dp=out/f"{c['block_id']}__compiled_request.json"; dp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    if a.dry_run: print(f"DRY_RUN PASS request_hash={c['request_hash']} artifact={dp}"); return
    raw,meta=dispatch(c,a.timeout); ev=persist(c,raw,meta,out); print(json.dumps({"status":"LIVE_PASS",**ev},indent=2))

if __name__=="__main__": main()
