#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,wave
from pathlib import Path

def read_pcm(path):
    with wave.open(str(path),"rb") as w:
        meta=(w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes(),w.getcomptype()); raw=w.readframes(w.getnframes())
    return meta,raw

def ranges_to_frames(ranges,sr,frame_bytes):
    out=[]
    for r in ranges:
        a=max(0,int(round(float(r["start_s"])*sr))*frame_bytes); b=max(a,int(round(float(r["end_s"])*sr))*frame_bytes); out.append((a,b))
    return out

def diff_outside_allowed(a,b,allowed):
    if len(a)!=len(b): return True
    mask=bytearray(len(a))
    for s,e in allowed: mask[s:min(e,len(mask))]=b"\x01"*max(0,min(e,len(mask))-s)
    return any(x!=y and not mask[i] for i,(x,y) in enumerate(zip(a,b)))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--before",required=True); ap.add_argument("--after",required=True); ap.add_argument("--patch-plan",required=True); ap.add_argument("--out",required=True); ap.add_argument("--scene3-start",type=float,default=444.980); args=ap.parse_args()
    mb,rb=read_pcm(Path(args.before)); ma,ra=read_pcm(Path(args.after)); checks=[{"id":"FORMAT_DURATION_STABILITY","pass":mb==ma,"detail":{"before":mb,"after":ma}}]
    if mb!=ma:
        Path(args.out).write_text(json.dumps({"status":"FAIL","checks":checks},indent=2)+"\n"); print("FAIL format mismatch"); return 2
    ch,sw,sr,nf,ct=mb; fb=ch*sw; plan=json.loads(Path(args.patch_plan).read_text()); allowed=[{"start_s":p.get("interval_start_seconds",p.get("interval_start_s")),"end_s":p.get("interval_end_seconds",p.get("interval_end_s"))} for p in plan.get("patches",[])]; allowed_bytes=ranges_to_frames(allowed,sr,fb); s3=int(round(args.scene3_start*sr))*fb
    checks.append({"id":"SCENE3_BYTES_UNCHANGED","pass":rb[s3:]==ra[s3:]}); checks.append({"id":"UNAUTHORIZED_RANGES_UNCHANGED","pass":not diff_outside_allowed(rb[:s3],ra[:s3],allowed_bytes)}); any_patch_changed=any(rb[s:e]!=ra[s:e] for s,e in allowed_bytes); checks.append({"id":"AUTHORIZED_PATCH_RANGE_CHANGED","pass":any_patch_changed if allowed_bytes else True}); status="PASS" if all(c["pass"] for c in checks) else "FAIL"; Path(args.out).write_text(json.dumps({"schema_version":"room917.regression_gate/1.0","status":status,"checks":checks},indent=2)+"\n"); print(status); return 0 if status=="PASS" else 3
if __name__=="__main__": raise SystemExit(main())
