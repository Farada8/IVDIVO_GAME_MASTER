#!/usr/bin/env python3
import json,hashlib,sys
from pathlib import Path
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def compile_manifest(text_authority,cap,contract):
    if text_authority.get("status")!="LOCKED_FOR_VOICE_AUDITION": raise SystemExit("FAIL-CLOSED text not locked")
    if cap.get("status")!="PASS" or not cap.get("auth_ok"): raise SystemExit("FAIL-CLOSED provider not authenticated")
    by={x["source_speech_index"]:x for x in text_authority["anchors"]}
    jobs=[]
    for x in contract["baseline"]:
        a=by[x["source_index"]]
        jobs.append({"role":x["role"],"candidate_id":x["candidate_id"],"source_index":x["source_index"],
          "exact_text":a.get("text_ru_candidate") or a.get("text_ru"),"exact_text_sha256":sha(a.get("text_ru_candidate") or a.get("text_ru")),
          "purpose":"BASELINE_TECHNICAL_AND_CHARACTER_PROBE","casting_decision_allowed":False})
    return {"artifact":"BODYGUARD_RU_BASELINE_PREVIEW_MANIFEST_v1","status":"READY_FOR_LIVE_PROVIDER","jobs":jobs}
if __name__=="__main__":
    a,c,k=map(lambda p:json.loads(Path(p).read_text()),sys.argv[1:4])
    Path(sys.argv[4]).write_text(json.dumps(compile_manifest(a,c,k),ensure_ascii=False,indent=2),encoding="utf-8")
