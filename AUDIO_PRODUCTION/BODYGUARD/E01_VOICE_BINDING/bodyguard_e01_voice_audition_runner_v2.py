#!/usr/bin/env python3
"""BODYGUARD E01 — ElevenLabs staged voice audition runner v2.0.

- A/B/C public Voice Library source IDs are prebound.
- Live mode preflights GET /v1/voices/{voice_id}.
- If needed it adds a shared voice using POST /v1/voices/add/{public_user_id}/{voice_id}.
- S0 is technical only; S1 is fair same-line comparison.
- API key is environment-only. No voice lock is produced.
"""
from __future__ import annotations
import argparse, base64, hashlib, json, os, sys, time, wave
from pathlib import Path
from typing import Any
import httpx

EXPECTED_SPOKEN_SEQUENCE_SHA = "2af60ca3b58bc90a2863e8f6dbee2bf7541d6b1f2315e78704f12ca214da9149"
BASE_URL = "https://api.elevenlabs.io"
DEFAULT_OUTPUT_FORMAT = "pcm_48000"

class FailClosed(RuntimeError): pass

def load_json(path: Path) -> dict[str, Any]: return json.loads(path.read_text(encoding="utf-8"))
def sha256_text(text: str) -> str: return hashlib.sha256(text.encode("utf-8")).hexdigest()
def sha256_bytes(data: bytes) -> str: return hashlib.sha256(data).hexdigest()

def validate_authority(requests: dict[str, Any], cascade: dict[str, Any]) -> None:
    if requests["coverage_validation"]["source_spoken_sha256"] != EXPECTED_SPOKEN_SEQUENCE_SHA: raise FailClosed("Request manifest spoken-sequence SHA mismatch.")
    if cascade["authority"]["spoken_sequence_sha256"] != EXPECTED_SPOKEN_SEQUENCE_SHA: raise FailClosed("Cascade spoken-sequence SHA mismatch.")
    by_block = {r["block_id"]: r for r in requests["requests"]}
    for stage in ("S0", "S1"):
        for j in cascade[stage]["jobs"]:
            src = by_block.get(j["block_id"])
            if not src: raise FailClosed(f"{stage}: missing block {j['block_id']}")
            if j["exact_text"] != src["exact_text"]: raise FailClosed(f"{stage}: exact text mismatch {j['job_id']}")
            if j["exact_text_sha256"] != src["exact_text_sha256"]: raise FailClosed(f"{stage}: stored hash mismatch {j['job_id']}")
            if sha256_text(j["exact_text"]) != j["exact_text_sha256"]: raise FailClosed(f"{stage}: computed hash mismatch {j['job_id']}")
    if len(cascade["S0"]["jobs"]) != 5 or cascade["S0"]["job_count"] != 5: raise FailClosed("S0 must be exactly 5 jobs.")
    if len(cascade["S1"]["jobs"]) != 15 or cascade["S1"]["job_count"] != 15: raise FailClosed("S1 must be exactly 15 jobs.")
    grouped = {}
    for j in cascade["S1"]["jobs"]: grouped.setdefault(j["role"], []).append(j)
    for role, jobs in grouped.items():
        if sorted(j["candidate"] for j in jobs) != ["A", "B", "C"]: raise FailClosed(f"S1 {role}: candidates must be A/B/C.")
        if len({j["block_id"] for j in jobs}) != 1 or len({j["exact_text_sha256"] for j in jobs}) != 1: raise FailClosed(f"S1 {role}: unfair same-line comparison.")

def validate_bindings(bindings, acquisition, jobs):
    for j in jobs:
        role, cand = j["role"], j["candidate"]
        try:
            b = bindings["roles"][role][cand]; a = acquisition["roles"][role][cand]
        except KeyError as exc: raise FailClosed(f"Missing binding/acquisition slot {role}:{cand}") from exc
        if b.get("source_type") != "shared_library": raise FailClosed(f"{role}:{cand} is not shared_library.")
        if b.get("voice_id") != a.get("source_voice_id"): raise FailClosed(f"{role}:{cand} source ID mismatch.")
        if not b.get("public_user_id"): raise FailClosed(f"{role}:{cand} missing public_user_id.")
        if not (b.get("model_id") or bindings.get("model_default")): raise FailClosed(f"{role}:{cand} missing model_id.")

def write_pcm16_mono_wav(path: Path, pcm: bytes, sample_rate: int = 48000) -> None:
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sample_rate); wf.writeframes(pcm)

def ensure_voice_access(client, api_key, binding, base_url):
    source_voice_id = binding["voice_id"]
    headers = {"xi-api-key": api_key}
    get_url = f"{base_url.rstrip('/')}/v1/voices/{source_voice_id}"
    resp = client.get(get_url, headers=headers)
    if 200 <= resp.status_code < 300:
        return source_voice_id, {"method":"DIRECT_GET_ACCESS","source_voice_id":source_voice_id,"get_status":resp.status_code,"add_status":None}
    public_user_id = binding["public_user_id"]
    add_url = f"{base_url.rstrip('/')}/v1/voices/add/{public_user_id}/{source_voice_id}"
    add = client.post(add_url, headers={"xi-api-key":api_key,"content-type":"application/json"}, json={"new_name":f"BG_{binding['label']}","bookmarked":True})
    if 200 <= add.status_code < 300:
        obj = add.json(); resolved = obj.get("voice_id") or source_voice_id
        return resolved, {"method":"ADDED_SHARED_VOICE","source_voice_id":source_voice_id,"resolved_voice_id":resolved,"get_status":resp.status_code,"add_status":add.status_code}
    retry = client.get(get_url, headers=headers)
    if 200 <= retry.status_code < 300:
        return source_voice_id, {"method":"RETRY_GET_AFTER_ADD_RESPONSE","source_voice_id":source_voice_id,"get_status":resp.status_code,"add_status":add.status_code,"retry_get_status":retry.status_code}
    raise FailClosed(f"Shared voice access failed for {binding['label']}: GET={resp.status_code}, ADD={add.status_code}, RETRY_GET={retry.status_code}")

def call_tts(client, api_key, voice_id, model_id, text, output_format, base_url, max_attempts):
    url = f"{base_url.rstrip('/')}/v1/text-to-speech/{voice_id}/with-timestamps"
    headers = {"xi-api-key":api_key,"accept":"application/json","content-type":"application/json"}
    params = {"output_format":output_format}; payload = {"text":text,"model_id":model_id}; last = None
    for attempt in range(1, max_attempts + 1):
        try: resp = client.post(url, headers=headers, params=params, json=payload)
        except httpx.HTTPError as exc: last=f"network error: {exc}"; retry=True
        else:
            if 200 <= resp.status_code < 300:
                obj=resp.json(); audio_b64=obj.get("audio_base64")
                if not audio_b64: raise FailClosed("Provider response missing audio_base64.")
                pcm=base64.b64decode(audio_b64)
                return pcm, {"alignment":obj.get("alignment"),"normalized_alignment":obj.get("normalized_alignment")}, {"request_id":resp.headers.get("request-id") or resp.headers.get("x-request-id"),"character_cost":resp.headers.get("character-cost")}
            last=f"HTTP {resp.status_code}: {resp.text[:500]}"; retry=resp.status_code==429 or resp.status_code>=500
        if not retry or attempt==max_attempts: raise FailClosed(last or "TTS request failed.")
        time.sleep(min(2 ** (attempt - 1), 16))
    raise FailClosed(last or "TTS request failed.")

def gate(stage, records, expected):
    complete=len(records)==expected; nonempty=complete and all(r.get("audio_bytes",0)>0 for r in records); hashed=complete and all(r.get("audio_sha256") for r in records); ok=complete and nonempty and hashed
    return {"artifact":f"BODYGUARD_E01_{stage}_TECHNICAL_GATE_v2","stage":stage,"expected_jobs":expected,"completed_jobs":len(records),"checks":{"complete":complete,"nonempty_audio":nonempty,"audio_hashed":hashed},"verdict":"PASS_TO_S1" if stage=="S0" and ok else "S1_AUDIO_READY_FOR_HUMAN_COMPARISON" if stage=="S1" and ok else "FAIL","casting_decision":"NOT_ALLOWED_FROM_MACHINE_GATE","voice_lock":False}

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--stage",choices=["S0","S1"],required=True); ap.add_argument("--requests",type=Path,required=True); ap.add_argument("--cascade",type=Path,required=True); ap.add_argument("--bindings",type=Path,required=True); ap.add_argument("--acquisition",type=Path,required=True); ap.add_argument("--output-dir",type=Path,default=Path("renders/BODYGUARD_E01_AUDITIONS")); ap.add_argument("--execute",action="store_true"); ap.add_argument("--base-url",default=os.getenv("ELEVENLABS_BASE_URL",BASE_URL)); ap.add_argument("--output-format",default=os.getenv("ELEVENLABS_OUTPUT_FORMAT",DEFAULT_OUTPUT_FORMAT)); ap.add_argument("--timeout",type=float,default=90.0); ap.add_argument("--max-attempts",type=int,default=4); args=ap.parse_args()
    requests=load_json(args.requests); cascade=load_json(args.cascade); bindings=load_json(args.bindings); acquisition=load_json(args.acquisition); validate_authority(requests,cascade); jobs=cascade[args.stage]["jobs"]; validate_bindings(bindings,acquisition,jobs)
    print(f"AUTHORITY PASS — {args.stage}"); print(f"locked spoken SHA: {EXPECTED_SPOKEN_SEQUENCE_SHA}"); print(f"jobs: {len(jobs)}"); print("candidate source IDs: PREPARED / NOT AUDITIONED")
    if not args.execute:
        print("DRY RUN — 0 network calls.")
        for j in jobs:
            b=bindings["roles"][j["role"]][j["candidate"]]; print(f"{j['job_id']} | {b['source_name']} | source_voice_id={b['voice_id']} | model={b.get('model_id') or bindings['model_default']} | {j['exact_text']}")
        return 0
    api_key=os.getenv("ELEVENLABS_API_KEY")
    if not api_key: raise FailClosed("ELEVENLABS_API_KEY required for live --execute.")
    stage_dir=args.output_dir/args.stage; stage_dir.mkdir(parents=True,exist_ok=True); records=[]; resolved_cache={}
    with httpx.Client(timeout=args.timeout) as client:
        for n,j in enumerate(jobs,1):
            role,cand=j["role"],j["candidate"]; b=bindings["roles"][role][cand]; key=(role,cand)
            if key not in resolved_cache: resolved_cache[key]=ensure_voice_access(client,api_key,b,args.base_url)
            resolved_voice_id,access=resolved_cache[key]; model_id=b.get("model_id") or bindings["model_default"]
            pcm,alignment,provider=call_tts(client,api_key,resolved_voice_id,model_id,j["exact_text"],args.output_format,args.base_url,args.max_attempts); wav_name=f"{j['job_id']}.wav"; wav_path=stage_dir/wav_name; write_pcm16_mono_wav(wav_path,pcm,48000)
            record={"job_id":j["job_id"],"stage":args.stage,"role":role,"candidate":cand,"source_name":b["source_name"],"source_voice_id":b["voice_id"],"resolved_voice_id":resolved_voice_id,"voice_access":access,"model_id":model_id,"block_id":j["block_id"],"exact_text_sha256":j["exact_text_sha256"],"render_status":"RENDERED","wav_file":wav_name,"audio_bytes":len(pcm),"audio_sha256":sha256_bytes(pcm),"provider":provider,"alignment":alignment,"casting_decision":"NONE","voice_lock":False}; wav_path.with_suffix(".json").write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8"); records.append(record); print(f"[{n}/{len(jobs)}] {j['job_id']} -> {wav_path}")
    (stage_dir/f"BODYGUARD_E01_{args.stage}_EXECUTION_LOG_v2.json").write_text(json.dumps({"artifact":f"BODYGUARD_E01_{args.stage}_EXECUTION_LOG_v2","records":records,"api_key_persisted":False},ensure_ascii=False,indent=2),encoding="utf-8"); g=gate(args.stage,records,len(jobs)); gate_path=stage_dir/f"BODYGUARD_E01_{args.stage}_TECHNICAL_GATE_v2.json"; gate_path.write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding="utf-8"); print(f"GATE: {g['verdict']} -> {gate_path}"); return 0 if g["verdict"]!="FAIL" else 2

if __name__=="__main__":
    try: raise SystemExit(main())
    except FailClosed as exc: print(f"FAIL-CLOSED: {exc}",file=sys.stderr); raise SystemExit(2)
