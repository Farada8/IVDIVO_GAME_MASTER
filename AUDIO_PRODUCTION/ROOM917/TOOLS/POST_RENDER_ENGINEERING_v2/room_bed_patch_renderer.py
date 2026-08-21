#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, wave
from pathlib import Path
import numpy as np

def read_pcm24_or16(path: Path):
    with wave.open(str(path),"rb") as w:
        ch=w.getnchannels(); sw=w.getsampwidth(); sr=w.getframerate(); nf=w.getnframes(); ct=w.getcomptype(); raw=w.readframes(nf)
    if ct!="NONE" or sw not in (2,3): raise ValueError("Only uncompressed 16/24-bit PCM WAV supported")
    if sw==2:
        a=np.frombuffer(raw,dtype="<i2").astype(np.int32); full=32768.0
    else:
        b=np.frombuffer(raw,dtype=np.uint8).reshape(-1,3); u=b[:,0].astype(np.int32)|(b[:,1].astype(np.int32)<<8)|(b[:,2].astype(np.int32)<<16); a=np.where(u&0x800000,u|~0xFFFFFF,u).astype(np.int32); full=8388608.0
    return {"channels":ch,"sample_width":sw,"sample_rate":sr,"frames":nf}, a.reshape(-1,ch).astype(np.float64)/full

def write_pcm(path: Path, meta, x):
    x=np.clip(x,-0.999999,0.999999); sw=meta["sample_width"]; ch=meta["channels"]; sr=meta["sample_rate"]; flat=x.reshape(-1)
    if sw==2: raw=np.round(flat*32767).astype("<i2").tobytes()
    else:
        ints=np.round(flat*8388607).astype(np.int32); u=(ints.astype(np.int64)&0xFFFFFF).astype(np.uint32); b=np.empty((u.size,3),dtype=np.uint8); b[:,0]=u&255; b[:,1]=(u>>8)&255; b[:,2]=(u>>16)&255; raw=b.tobytes()
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),"wb") as w: w.setnchannels(ch); w.setsampwidth(sw); w.setframerate(sr); w.writeframes(raw)

def adapt_channels(x,target_ch):
    if x.shape[1]==target_ch: return x
    if x.shape[1]==1 and target_ch==2: return np.repeat(x,2,axis=1)
    if x.shape[1]==2 and target_ch==1: return x.mean(axis=1,keepdims=True)
    raise ValueError("Unsupported channel adaptation")

def loop_to_length(x,n):
    if len(x)==0: raise ValueError("empty bed")
    return np.tile(x,((n+len(x)-1)//len(x),1))[:n]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--master",required=True); ap.add_argument("--patch-plan",required=True); ap.add_argument("--asset-bindings",required=True); ap.add_argument("--out",required=True); ap.add_argument("--report",required=True); args=ap.parse_args()
    meta,master=read_pcm24_or16(Path(args.master)); plan=json.loads(Path(args.patch_plan).read_text(encoding="utf-8")); bindings=json.loads(Path(args.asset_bindings).read_text(encoding="utf-8")); out=master.copy(); applied=[]; holds=[]
    for p in plan.get("patches",[]):
        asset=p["source_asset"]; bind=bindings.get(asset)
        if not bind or not bind.get("path") or "gain_db" not in bind: holds.append({"patch_id":p["patch_id"],"reason":"ASSET_BINDING_OR_GAIN_MISSING"}); continue
        bed_meta,bed=read_pcm24_or16(Path(bind["path"]))
        if bed_meta["sample_rate"]!=meta["sample_rate"]: holds.append({"patch_id":p["patch_id"],"reason":"BED_SAMPLE_RATE_MISMATCH"}); continue
        bed=adapt_channels(bed,meta["channels"]); s=max(0,int(round(float(p["interval_start_seconds"])*meta["sample_rate"]))); e=min(len(out),int(round(float(p["interval_end_seconds"])*meta["sample_rate"])))
        if e<=s: holds.append({"patch_id":p["patch_id"],"reason":"EMPTY_INTERVAL"}); continue
        seg=loop_to_length(bed,e-s)*(10.0**(float(bind["gain_db"])/20.0)); fi=min(e-s,int(round(float(p.get("fade_in_ms",150))*meta["sample_rate"]/1000))); fo=min(e-s,int(round(float(p.get("fade_out_ms",200))*meta["sample_rate"]/1000))); env=np.ones((e-s,1))
        if fi>0: env[:fi,0]=np.linspace(0,1,fi,endpoint=True)
        if fo>0: env[-fo:,0]=np.minimum(env[-fo:,0],np.linspace(1,0,fo,endpoint=True))
        out[s:e]+=seg*env; applied.append({"patch_id":p["patch_id"],"asset":asset,"gain_db":bind["gain_db"],"start_seconds":s/meta["sample_rate"],"end_seconds":e/meta["sample_rate"]})
    status="PASS" if applied and not holds else ("PASS_WITH_HOLDS" if applied else "HOLD"); write_pcm(Path(args.out),meta,out); report={"schema_version":"room917.room_bed_patch_render/1.0","status":status,"applied":applied,"holds":holds,"law":"Only planner-authorized ranges are modified. Gain must be explicitly bound; no inferred production gain."}; Path(args.report).write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print(f"{status} applied={len(applied)} holds={len(holds)}"); return 0 if applied else 4
if __name__=="__main__": raise SystemExit(main())
