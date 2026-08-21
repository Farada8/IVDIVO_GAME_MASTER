#!/usr/bin/env python3
import argparse,csv,json
from pathlib import Path

FIELDS=["event_id","timestamp","locale","role","stage","provider","model","request_id","characters","character_cost","audio_seconds","accepted","regenerated","pickup_reason","cost_currency","cost_amount"]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sidecars",type=Path,nargs="*",default=[])
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args(); rows=[]
    for p in args.sidecars:
        d=json.loads(p.read_text(encoding="utf-8"))
        rows.append({"event_id":d.get("job_id",p.stem),"timestamp":d.get("timestamp",""),"locale":d.get("locale","ru-RU"),"role":d.get("role",""),"stage":d.get("stage",""),"provider":"ElevenLabs","model":d.get("model_id",""),"request_id":d.get("provider_request_id") or d.get("provider",{}).get("request_id",""),"characters":len(d.get("exact_text","")) if d.get("exact_text") else d.get("characters",""),"character_cost":d.get("provider",{}).get("character_cost",""),"audio_seconds":d.get("duration_seconds",""),"accepted":d.get("accepted",""),"regenerated":d.get("regenerated",""),"pickup_reason":d.get("pickup_reason",""),"cost_currency":d.get("cost_currency",""),"cost_amount":d.get("cost_amount","")})
    with args.out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print("rows",len(rows))

if __name__=="__main__": main()
