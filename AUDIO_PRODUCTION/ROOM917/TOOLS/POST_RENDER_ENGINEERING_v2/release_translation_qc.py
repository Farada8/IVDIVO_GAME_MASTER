#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, re, shutil, subprocess, wave
from pathlib import Path
import numpy as np


def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def finite(v): return float(v) if v is not None and math.isfinite(float(v)) else None

def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(block_size),b""): h.update(b)
    return h.hexdigest()

def read_pcm(path: Path):
    with wave.open(str(path),"rb") as w:
        ch=w.getnchannels(); sw=w.getsampwidth(); sr=w.getframerate(); nf=w.getnframes(); ct=w.getcomptype(); raw=w.readframes(nf)
    if ct!="NONE" or sw not in (2,3,4): raise ValueError("Only uncompressed 16/24/32-bit PCM WAV supported")
    if sw==2: a=np.frombuffer(raw,dtype="<i2").astype(np.int32); full=32768.0
    elif sw==3:
        b=np.frombuffer(raw,dtype=np.uint8).reshape(-1,3); u=b[:,0].astype(np.int32)|(b[:,1].astype(np.int32)<<8)|(b[:,2].astype(np.int32)<<16); a=np.where(u&0x800000,u|~0xFFFFFF,u).astype(np.int32); full=8388608.0
    else: a=np.frombuffer(raw,dtype="<i4").astype(np.int64); full=2147483648.0
    x=a.reshape(-1,ch).astype(np.float64)/full
    return {"channels":ch,"sample_width":sw,"bit_depth":sw*8,"sample_rate":sr,"frames":nf,"duration_seconds":nf/sr},x

def dbfs(v: float): return None if v<=0 else 20.0*math.log10(v)
def stereo_metrics(x):
    if x.shape[1]!=2: return {"status":"NOT_STEREO"}
    l,r=x[:,0],x[:,1]; ls,rs=float(np.std(l)),float(np.std(r)); corr=None if ls==0 or rs==0 else finite(np.corrcoef(l,r)[0,1]); mid=.5*(l+r); side=.5*(l-r); mr=float(np.sqrt(np.mean(mid*mid))) if len(mid) else 0.0; sr=float(np.sqrt(np.mean(side*side))) if len(side) else 0.0
    return {"status":"DIAGNOSTIC_ONLY_COMPARE_TO_STEREO_INTENT","correlation":corr,"mid_rms_dbfs":dbfs(mr),"side_rms_dbfs":dbfs(sr),"side_relative_to_mid_db":None if sr<=0 or mr<=0 else finite(20*math.log10(sr/mr)),"mono_fold_peak_dbfs":dbfs(float(np.max(np.abs(mid))) if len(mid) else 0.0),"left_peak_dbfs":dbfs(float(np.max(np.abs(l))) if len(l) else 0.0),"right_peak_dbfs":dbfs(float(np.max(np.abs(r))) if len(r) else 0.0)}
def ffmpeg_loudnorm(ffmpeg,master,profile):
    t=profile["technical_profile"]; filt=f"loudnorm=I={t['integrated_lufs_target']}:TP={t['true_peak_ceiling_dbtp']}:LRA={t['lra_ceiling_lu']}:print_format=json"; p=subprocess.run([ffmpeg,"-hide_banner","-nostats","-i",str(master),"-af",filt,"-f","null","-"],capture_output=True,text=True)
    if p.returncode!=0: raise RuntimeError("ffmpeg loudnorm failed: "+p.stderr[-1200:])
    m=re.findall(r"\{\s*\"input_i\".*?\}",p.stderr,flags=re.S)
    if not m: raise RuntimeError("ffmpeg loudnorm JSON not found")
    raw=json.loads(m[-1]); return {"integrated_lufs":float(raw["input_i"]),"true_peak_dbtp":float(raw["input_tp"]),"lra_lu":float(raw["input_lra"]),"threshold_lufs":float(raw["input_thresh"]),"ffmpeg_raw":raw}
def make_proxy(ffmpeg,master,out,phone):
    cmd=[ffmpeg,"-y","-hide_banner","-loglevel","error","-i",str(master)]
    if phone: cmd += ["-af","highpass=f=250,lowpass=f=5000","-ac","1"]
    else: cmd += ["-ac","1"]
    cmd += ["-ar","48000","-c:a","pcm_s24le",str(out)]; subprocess.run(cmd,check=True)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--master",required=True,type=Path); ap.add_argument("--profile",required=True,type=Path); ap.add_argument("--outdir",required=True,type=Path); ap.add_argument("--ffmpeg",default="ffmpeg"); a=ap.parse_args(); profile=load(a.profile); expected=profile["expected_master_identity"]; tech=profile["technical_profile"]; a.outdir.mkdir(parents=True,exist_ok=True); failures=[]; holds=[]
    if not a.master.is_file(): raise SystemExit("master bytes not found")
    observed_sha=sha256_file(a.master); meta,x=read_pcm(a.master); identity={"sha256":observed_sha,"size_bytes":a.master.stat().st_size,"duration_seconds":meta["duration_seconds"],"sample_rate_hz":meta["sample_rate"],"bit_depth":meta["bit_depth"],"channels":meta["channels"]}
    if observed_sha!=expected["sha256"]: failures.append("MASTER_SHA256_MISMATCH")
    if abs(meta["duration_seconds"]-float(expected["duration_seconds"]))>(1.0/meta["sample_rate"]): failures.append("MASTER_DURATION_MISMATCH")
    if meta["sample_rate"]!=expected["sample_rate_hz"]: failures.append("MASTER_SAMPLE_RATE_MISMATCH")
    if meta["bit_depth"]!=expected["bit_depth"]: failures.append("MASTER_BIT_DEPTH_MISMATCH")
    if meta["channels"]!=expected["channels"]: failures.append("MASTER_CHANNEL_COUNT_MISMATCH")
    peaks=np.max(np.abs(x),axis=0) if len(x) else np.zeros(meta["channels"]); clipping=bool(np.any(peaks>=1.0))
    if clipping: failures.append("CLIPPING_DETECTED")
    ff=shutil.which(a.ffmpeg); loud=None
    if not ff: holds.append("FFMPEG_NOT_AVAILABLE_LOUDNESS_TRUEPEAK_LRA_UNVERIFIED")
    else:
        try:
            loud=ffmpeg_loudnorm(ff,a.master,profile)
            if abs(loud["integrated_lufs"]-tech["integrated_lufs_target"])>tech["integrated_lufs_tolerance_lu"]: failures.append("INTEGRATED_LUFS_OUT_OF_PROFILE")
            if loud["true_peak_dbtp"]>tech["true_peak_ceiling_dbtp"]: failures.append("TRUE_PEAK_EXCEEDS_CEILING")
            if loud["lra_lu"]>tech["lra_ceiling_lu"]: failures.append("LRA_EXCEEDS_CEILING")
        except Exception as e: holds.append("LOUDNORM_ANALYSIS_FAILED:"+str(e))
    proxies={}
    if ff and not failures:
        try:
            mono=a.outdir/"ROOM917_E01_MONO_FOLDDOWN_QC_PROXY.wav"; phone=a.outdir/"ROOM917_E01_PHONE_BAND_MONO_QC_PROXY.wav"; make_proxy(ff,a.master,mono,False); make_proxy(ff,a.master,phone,True); proxies={"mono_folddown":str(mono),"phone_band_mono":str(phone),"phone_proxy_warning":"Bandwidth/mono stress proxy only; not a physical-device loudspeaker model."}
        except Exception as e: holds.append("TRANSLATION_PROXY_BUILD_FAILED:"+str(e))
    status="FAIL" if failures else ("HOLD" if holds else "PASS"); report={"schema_version":"room917.release_translation_machine_qc/1.1","status":status,"master":str(a.master),"identity":identity,"identity_expected":expected,"sample_peaks_dbfs":[dbfs(float(p)) for p in peaks],"clipping_detected":clipping,"loudness":loud,"stereo":stereo_metrics(x),"translation_proxies":proxies,"failures":failures,"holds":holds,"human_translation_checks":"REQUIRED_NOT_EXECUTED_BY_MACHINE_QC","human_checklist":profile.get("room917_critical_translation_checks",[]),"law":"High stereo correlation is diagnostic, not an automatic defect. Machine QC never substitutes for P003B human listening."}; (a.outdir/"ROOM917_E01_RELEASE_TRANSLATION_MACHINE_QC.json").write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8"); print(status); return 0 if status=="PASS" else 4
if __name__=="__main__": raise SystemExit(main())
