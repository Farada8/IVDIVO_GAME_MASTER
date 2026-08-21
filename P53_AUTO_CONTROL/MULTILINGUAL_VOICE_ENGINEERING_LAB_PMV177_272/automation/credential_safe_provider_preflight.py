#!/usr/bin/env python3
import argparse, json, os
from pathlib import Path
import httpx

BASE="https://api.elevenlabs.io"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--execute",action="store_true")
    ap.add_argument("--out",type=Path,default=Path("provider_preflight.json"))
    args=ap.parse_args()
    key=os.getenv("ELEVENLABS_API_KEY")
    result={"artifact":"BODYGUARD_ELEVENLABS_CREDENTIAL_SAFE_PREFLIGHT_v1","api_key_present":bool(key),"api_key_persisted":False,"execute":args.execute,"checks":{}}
    if not args.execute:
        result["status"]="DRY_RUN"
        result["checks"]={"GET_/v1/user":"PLANNED","GET_/v1/user/subscription":"PLANNED","GET_/v2/voices":"PLANNED","voice_design_endpoint":"DOCUMENTED","text_to_dialogue_timestamps_endpoint":"DOCUMENTED"}
        args.out.write_text(json.dumps(result,indent=2),encoding="utf-8")
        print("DRY RUN — no network")
        return
    if not key:
        raise SystemExit("FAIL-CLOSED: ELEVENLABS_API_KEY absent")
    headers={"xi-api-key":key}
    with httpx.Client(timeout=30.0) as c:
        for name,path in [("user","/v1/user"),("subscription","/v1/user/subscription"),("voices","/v2/voices")]:
            r=c.get(BASE+path,headers=headers)
            result["checks"][name]={"status_code":r.status_code,"ok":200<=r.status_code<300}
            if name=="subscription" and r.is_success:
                obj=r.json(); result["subscription"]={k:obj.get(k) for k in ["tier","character_count","character_limit","voice_slots_used","voice_limit","status","currency"]}
    result["status"]="PASS" if all(x["ok"] for x in result["checks"].values()) else "FAIL"
    args.out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(result["status"])

if __name__=="__main__": main()
