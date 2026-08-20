#!/usr/bin/env python3
"""IVDIVO source-vs-stem stereo integrity QC v1.0.

Diagnoses unintended mixer collapse versus intentionally mono/narrow source material.
Uses declared stereo intent; correlation=1.0 is not automatically a failure.
"""
from __future__ import annotations
import argparse, json, math, wave
from pathlib import Path
import numpy as np

INTENTS = {"MONO_INTENTIONAL", "NARROW", "NATURAL_STEREO", "WIDE", "BINAURAL_OR_POSITIONAL", "SOURCE_DEPENDENT"}


def _read_pcm_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as w:
        ch = w.getnchannels(); sr = w.getframerate(); sw = w.getsampwidth(); n = w.getnframes(); raw = w.readframes(n)
    if ch < 2:
        raise ValueError(f"Need stereo WAV: {path}")
    if sw == 1:
        x = (np.frombuffer(raw, dtype=np.uint8).astype(np.float64)-128.0)/128.0
    elif sw == 2:
        x = np.frombuffer(raw, dtype='<i2').astype(np.float64)/32768.0
    elif sw == 3:
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1,3)
        vals = b[:,0].astype(np.int32) | (b[:,1].astype(np.int32)<<8) | (b[:,2].astype(np.int32)<<16)
        vals = np.where(vals & 0x800000, vals | ~0xFFFFFF, vals)
        x = vals.astype(np.float64)/8388608.0
    elif sw == 4:
        x = np.frombuffer(raw, dtype='<i4').astype(np.float64)/2147483648.0
    else:
        raise ValueError(f"Unsupported PCM sample width {sw}")
    return x.reshape(-1,ch)[:, :2], sr


def metrics(path: Path) -> dict:
    x, sr = _read_pcm_wav(path)
    L,R = x[:,0],x[:,1]
    mask = (np.maximum(np.abs(L), np.abs(R)) > 1e-7)
    if mask.sum() < 32:
        return {"path":str(path),"sample_rate":sr,"frames":len(x),"lr_correlation":None,"side_mid_db":None,"silent":True}
    L,R=L[mask],R[mask]
    if np.std(L)<1e-12 or np.std(R)<1e-12:
        corr = 1.0 if np.allclose(L,R,atol=1e-12) else 0.0
    else:
        corr=float(np.corrcoef(L,R)[0,1])
    mid=(L+R)*0.5; side=(L-R)*0.5
    mr=math.sqrt(float(np.mean(mid*mid))+1e-30); srms=math.sqrt(float(np.mean(side*side))+1e-30)
    side_mid_db=20*math.log10(srms/mr+1e-30)
    return {"path":str(path),"sample_rate":sr,"frames":len(x),"lr_correlation":corr,"side_mid_db":side_mid_db,"silent":False}


def diagnose(source: dict, stem: dict, intent: str,
             collapse_corr: float=0.9999, wide_source_corr: float=0.995,
             side_loss_db: float=12.0) -> dict:
    if intent not in INTENTS: raise ValueError(f"Unknown stereo intent {intent}")
    if stem["silent"]:
        diagnosis="MANUAL_REVIEW"; status="MANUAL_REVIEW"; reason="stem is silent/too low for stereo diagnosis"
    elif intent=="MONO_INTENTIONAL":
        diagnosis="INTENTIONAL_MONO"; status="PASS"; reason="mono collapse is declared intent"
    elif source["silent"]:
        diagnosis="MANUAL_REVIEW"; status="MANUAL_REVIEW"; reason="source is silent/too low for source-vs-stem comparison"
    else:
        sc, tc = source["lr_correlation"], stem["lr_correlation"]
        sside, tside = source["side_mid_db"], stem["side_mid_db"]
        loss = sside - tside if sside is not None and tside is not None else 0.0
        if sc is not None and tc is not None and sc < wide_source_corr and tc >= collapse_corr and loss >= side_loss_db:
            diagnosis="MIXER_COLLAPSE"; status="FAIL"; reason=f"source had stereo width; stem collapsed (side loss {loss:.1f} dB)"
        elif sc is not None and sc >= wide_source_corr and tc is not None and tc >= wide_source_corr:
            diagnosis="SOURCE_NARROWNESS"; status="PASS_WITH_WARNING"; reason="source itself is narrow/mono; not proven mixer collapse"
        else:
            diagnosis="PASS"; status="PASS"; reason="stem width is compatible with source/intent"
    return {"status":status,"diagnosis":diagnosis,"reason":reason,"intent":intent,"source":source,"stem":stem}


def main():
    p=argparse.ArgumentParser(); p.add_argument("source_wav"); p.add_argument("stem_wav"); p.add_argument("--intent",required=True,choices=sorted(INTENTS)); p.add_argument("--output")
    a=p.parse_args(); result=diagnose(metrics(Path(a.source_wav)),metrics(Path(a.stem_wav)),a.intent)
    s=json.dumps(result,indent=2)
    if a.output: Path(a.output).write_text(s+"\n",encoding="utf-8")
    print(s)
    if result["status"]=="FAIL": raise SystemExit(2)

if __name__=="__main__": main()
