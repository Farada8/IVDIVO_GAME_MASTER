#!/usr/bin/env python3
"""BODYGUARD E01 staged ElevenLabs voice-audition runner v1.0.
S0 = five technical canary jobs. S1 = fifteen fair A/B/C anchors.
Default is dry-run. Live execution requires --execute, environment ELEVENLABS_API_KEY, and bound candidate voice/model IDs.
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

def validate_authority(requests, cascade):
    if requests["coverage_validation"]["source_spoken_sha256"] != EXPECTED_SPOKEN_SEQUENCE_SHA: raise FailClosed("Request manifest authority SHA mismatch.")
    if cascade["authority"]["spoken_sequence_sha256"] != EXPECTED_SPOKEN_SEQUENCE_SHA: raise FailClosed("Cascade authority SHA mismatch.")
    by_block = {r["block_id"]: r for r in requests["requests"]}
    for stage in ("S0","S1"):
        for job in cascade[stage]["jobs"]:
            src = by_block.get(job["block_id"])
            if not src: raise FailClosed(f"{stage}: missing block {job['block_id']}")
            if job["exact_text"] != src["exact_text"] or job["exact_text_sha256"] != src["exact_text_sha256"]: raise FailClosed(f"{stage}: exact-text mismatch {job['job_id']}")
            if sha256_text(job["exact_text"]) != job["exact_text_sha256"]: raise FailClosed(f"{stage}: computed hash mismatch {job['job_id']}")
    if len(cascade["S0"]["jobs"]) != 5 or cascade["S0"]["job_count"] != 5: raise FailClosed("S0 must be exactly 5 jobs.")
    if len(cascade["S1"]["jobs"]) != 15 or cascade["S1"]["job_count"] != 15: raise FailClosed("S1 must be exactly 15 jobs.")
    grouped = {}
    for j in cascade["S1"]["jobs"]: grouped.setdefault(j["role"], []).append(j)
    if len(grouped) != 5: raise FailClosed("S1 must cover exactly five roles.")
    for role,jobs in grouped.items():
        if sorted(j["candidate"] for j in jobs) != ["A","B","C"]: raise FailClosed(f"S1 {role}: candidates not A/B/C.")
        if len({j["block_id"] for j in jobs}) != 1 or len({j["exact_text_sha256"] for j in jobs}) != 1: raise FailClosed(f"S1 {role}: unfair anchor comparison.")

def validate_bindings(bindings, jobs, execute):
    missing=[]
    for j in jobs:
        try: b=bindings["roles"][j["role"]][j["candidate"]]
        except KeyError: missing.append(f"{j['role']}:{j['candidate']}:missing-slot"); continue
        if execute and (not b.get("voice_id") or not (b.get("model_id") or bindings.get("model_default"))): missing.append(f"{j['role']}:{j['candidate']}:unbound")
    if missing: raise FailClosed("Candidate binding incomplete: "+", ".join(sorted(set(missing))))

def selected_jobs(cascade,stage):
    if stage in ("S0","S1"): return cascade[stage]["jobs"]
    raise FailClosed(f"Unsupported stage {stage}")

def write_pcm16_mono_wav(path,pcm,sample_rate=48000):
    with wave.open(str(path),"wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sample_rate); wf.writeframes(pcm)

def call_with_timestamps(client,api_key,voice_id,model_id,text,output_format,base_url,max_attempts):
    url=f"{base_url.rstrip('/')}/v1/text-to-speech/{voice_id}/with-timestamps"
    headers={"xi-api-key":api_key,"accept":"application/json","content-type":"application/json"}
    payload={"text":text,"model_id":model_id}; params={"output_format":output_format}; last=None
    for attempt in range(1,max_attempts+1):
        try: resp=client.post(url,params=params,headers=headers,json=payload)
        except httpx.HTTPError as exc: last=f"network error: {exc}"; retry=True
        else:
            if 200 <= resp.status_code < 300:
                obj=resp.json(); audio_b64=obj.get("audio_base64")
                if not audio_b64: raise FailClosed("Provider response missing audio_base64.")
                pcm=base64.b64decode(audio_b64)
                alignment={"alignment":obj.get("alignment"),"normalized_alignment":obj.get("normalized_alignment")}
                meta={"request_id":resp.headers.get("request-id") or resp.headers.get("x-request-id") or ""}
                return pcm,alignment,meta
            last=f"HTTP {resp.status_code}: {resp.text[:500]}"; retry=resp.status_code==429 or resp.status_code>=500
        if not retry or attempt==max_attempts: raise FailClosed(last or "Provider request failed.")
        time.sleep(min(2**(attempt-1),16))
    raise FailClosed(last or "Provider request failed.")

def machine_gate(stage,records,expected):
    ok=len(records)==expected and all(r["render_status"]=="RENDERED" and r.get("audio_bytes",0)>0 and r.get("audio_sha256") for r in records)
    return {"artifact":f"BODYGUARD_{stage}_TECHNICAL_GATE_v1","stage":stage,"expected_jobs":expected,"completed_jobs":len(records),"verdict":"PASS_TO_S1" if stage=="S0" and ok else "S1_AUDIO_READY_FOR_HUMAN_COMPARISON" if stage=="S1" and ok else "FAIL","casting_decision":"NOT_ALLOWED_FROM_MACHINE_GATE"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--stage",choices=["S0","S1"],required=True); ap.add_argument("--requests",type=Path,required=True); ap.add_argument("--cascade",type=Path,required=True); ap.add_argument("--bindings",type=Path,required=True); ap.add_argument("--output-dir",type=Path,default=Path("renders/BODYGUARD_E01_AUDITIONS")); ap.add_argument("--execute",action="store_true"); ap.add_argument("--base-url",default=os.getenv("ELEVENLABS_BASE_URL",BASE_URL)); ap.add_argument("--output-format",default=os.getenv("ELEVENLABS_OUTPUT_FORMAT",DEFAULT_OUTPUT_FORMAT)); ap.add_argument("--timeout",type=float,default=90.0); ap.add_argument("--max-attempts",type=int,default=4); args=ap.parse_args()
    requests=load_json(args.requests); cascade=load_json(args.cascade); bindings=load_json(args.bindings); validate_authority(requests,cascade); jobs=selected_jobs(cascade,args.stage); validate_bindings(bindings,jobs,args.execute)
    print(f"AUTHORITY PASS — {args.stage}"); print(f"locked spoken SHA: {EXPECTED_SPOKEN_SEQUENCE_SHA}"); print(f"jobs: {len(jobs)}")
    if not args.execute:
        print("DRY RUN — 0 network calls.")
        for j in jobs:
            b=bindings["roles"][j["role"]][j["candidate"]]; model=b.get("model_id") or bindings.get("model_default"); print(f"{j['job_id']} | {j['role']} {j['candidate']} | {j['block_id']} | voice_id={b.get('voice_id')!r} | model_id={model!r} | {j['exact_text']}")
        return 0
    api_key=os.getenv("ELEVENLABS_API_KEY")
    if not api_key: raise FailClosed("ELEVENLABS_API_KEY required for live --execute.")
    stage_dir=args.output_dir/args.stage; stage_dir.mkdir(parents=True,exist_ok=True); records=[]
    with httpx.Client(timeout=args.timeout) as client:
        for n,j in enumerate(jobs,1):
            b=bindings["roles"][j["role"]][j["candidate"]]; model=b.get("model_id") or bindings.get("model_default"); pcm,alignment,provider=call_with_timestamps(client,api_key,b["voice_id"],model,j["exact_text"],args.output_format,args.base_url,args.max_attempts); wav_name=f"{j['job_id']}.wav"; wav_path=stage_dir/wav_name; write_pcm16_mono_wav(wav_path,pcm)
            record={"job_id":j["job_id"],"stage":args.stage,"role":j["role"],"candidate":j["candidate"],"block_id":j["block_id"],"exact_text_sha256":j["exact_text_sha256"],"voice_id":b["voice_id"],"model_id":model,"output_format":args.output_format,"render_status":"RENDERED","wav_file":wav_name,"audio_bytes":len(pcm),"audio_sha256":sha256_bytes(pcm),"provider_request_id":provider.get("request_id") or None,"alignment":alignment}; wav_path.with_suffix(".json").write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8"); records.append(record); print(f"[{n}/{len(jobs)}] {j['job_id']} -> {wav_path}")
    (stage_dir/f"BODYGUARD_E01_{args.stage}_EXECUTION_LOG_v1.json").write_text(json.dumps({"artifact":f"BODYGUARD_E01_{args.stage}_EXECUTION_LOG_v1","stage":args.stage,"records":records},ensure_ascii=False,indent=2),encoding="utf-8"); gate=machine_gate(args.stage,records,len(jobs)); gate_path=stage_dir/f"BODYGUARD_E01_{args.stage}_TECHNICAL_GATE_v1.json"; gate_path.write_text(json.dumps(gate,ensure_ascii=False,indent=2),encoding="utf-8"); print(f"GATE: {gate['verdict']} -> {gate_path}"); return 0 if gate["verdict"]!="FAIL" else 2

if __name__=="__main__":
    try: raise SystemExit(main())
    except FailClosed as exc: print(f"FAIL-CLOSED: {exc}",file=sys.stderr); raise SystemExit(2)
