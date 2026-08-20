#!/usr/bin/env python3
"""IVDIVO ElevenLabs provider preflight v1.0.

Read-only preflight: secret presence, /v1/models reachability/auth, model capability,
known voice resolution. Never logs or persists API key. No synthesis call.
"""
from __future__ import annotations
import argparse, json, os, socket, ssl, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_URL = "https://api.elevenlabs.io"
KEY_ENV = "ELEVENLABS_API_KEY"

def utc_now(): return datetime.now(timezone.utc).isoformat()

def _get_json(path: str, api_key: str, timeout: float = 15.0):
    req = urllib.request.Request(BASE_URL+path, headers={"Accept":"application/json","xi-api-key":api_key}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            data=json.loads(r.read().decode("utf-8")); meta={"http_status":int(r.status)}
            for name in ("request-id","x-request-id"):
                v=r.headers.get(name)
                if v: meta["provider_request_id"]=v; break
            return data, meta
    except urllib.error.HTTPError as e:
        failure="FAIL_PROVIDER_CREDENTIAL" if e.code in (401,403) else ("FAIL_PROVIDER_REQUEST" if 400<=e.code<500 else "FAIL_PROVIDER_CONNECTIVITY")
        raise RuntimeError(json.dumps({"failure":failure,"http_status":int(e.code)}))
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as e:
        raise RuntimeError(json.dumps({"failure":"FAIL_PROVIDER_CONNECTIVITY","error_type":type(e).__name__}))

def preflight(model_ids: list[str], voice_ids: list[str], timeout: float = 15.0) -> dict[str,Any]:
    key=os.environ.get(KEY_ENV)
    report={"schema_version":"1.0","provider":"elevenlabs","checked_at":utc_now(),"secret_env_present":bool(key),"connectivity":"NOT_RUN","credential":"NOT_RUN","models":{},"voices":{},"status":"FAIL","failures":[]}
    if not key:
        report["credential"]="FAIL_MISSING_SECRET"; report["failures"].append("FAIL_PROVIDER_CREDENTIAL"); return report
    try:
        models,meta=_get_json("/v1/models",key,timeout); report["connectivity"]="PASS"; report["credential"]="PASS"; report["models_request_meta"]=meta
    except RuntimeError as exc:
        info=json.loads(str(exc)); f=info.get("failure","FAIL_PROVIDER_CONNECTIVITY"); report["failures"].append(f); report["connectivity"]="FAIL" if f=="FAIL_PROVIDER_CONNECTIVITY" else "REACHED_PROVIDER"; report["credential"]="FAIL" if f=="FAIL_PROVIDER_CREDENTIAL" else "UNKNOWN"; report["http_status"]=info.get("http_status"); return report
    model_map={m.get("model_id"):m for m in models if isinstance(m,dict) and m.get("model_id")}
    for mid in model_ids:
        m=model_map.get(mid)
        if not m:
            report["models"][mid]={"status":"FAIL_NOT_FOUND"}; report["failures"].append("FAIL_PROVIDER_CAPABILITY")
        elif not bool(m.get("can_do_text_to_speech")):
            report["models"][mid]={"status":"FAIL_NO_TTS_CAPABILITY"}; report["failures"].append("FAIL_PROVIDER_CAPABILITY")
        else:
            report["models"][mid]={"status":"PASS","name":m.get("name"),"can_do_text_to_speech":True,"maximum_text_length_per_request":m.get("maximum_text_length_per_request"),"concurrency_group":m.get("concurrency_group")}
    for vid in voice_ids:
        try:
            voice,meta=_get_json(f"/v1/voices/{urllib.parse.quote(vid,safe='')}",key,timeout)
            if voice.get("voice_id")!=vid:
                report["voices"][vid]={"status":"FAIL_ID_MISMATCH"}; report["failures"].append("FAIL_PROVIDER_CAPABILITY")
            else:
                report["voices"][vid]={"status":"PASS","name":voice.get("name"),"category":voice.get("category"),"is_legacy":voice.get("is_legacy"),"request_meta":meta}
        except RuntimeError as exc:
            info=json.loads(str(exc)); report["voices"][vid]={"status":"FAIL","failure":info.get("failure"),"http_status":info.get("http_status")}; report["failures"].append(info.get("failure","FAIL_PROVIDER_CAPABILITY"))
    report["failures"]=sorted(set(report["failures"])); report["status"]="PASS" if not report["failures"] else "FAIL"; return report

def main():
    p=argparse.ArgumentParser(description="Read-only ElevenLabs preflight; never prints/stores API key."); p.add_argument("--model-id",action="append",default=[]); p.add_argument("--voice-id",action="append",default=[]); p.add_argument("--timeout",type=float,default=15.0); p.add_argument("--output",required=True); a=p.parse_args()
    report=preflight(a.model_id,a.voice_id,a.timeout); Path(a.output).write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print(f"{report['status']} provider preflight; report={a.output}")
    if report["status"]!="PASS": raise SystemExit(2)

if __name__=="__main__": main()
