#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, re, shutil, subprocess, wave
from pathlib import Path
import numpy as np

SOURCE_SHA="231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8"
REQ_REG={"FORMAT_DURATION_STABILITY","SCENE3_BYTES_UNCHANGED","UNAUTHORIZED_RANGES_UNCHANGED","AUTHORIZED_PATCH_RANGE_CHANGED"}

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""): h.update(b)
    return h.hexdigest()
def ref_ok(ref,label,errs):
    if not isinstance(ref,dict) or not ref.get("path") or not ref.get("sha256"): errs.append(label+"_REF_MISSING"); return None
    p=Path(ref["path"])
    if not p.is_file(): errs.append(label+"_FILE_NOT_FOUND"); return None
    if sha(p)!=str(ref["sha256"]).lower(): errs.append(label+"_SHA_MISMATCH"); return None
    return p
def read_pcm(p):
    with wave.open(str(p),"rb") as w:
        ch,sw,sr,nf,ct=w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes(),w.getcomptype(); raw=w.readframes(nf)
    if ct!="NONE" or sw not in (2,3,4): raise ValueError("Only uncompressed PCM WAV supported")
    if sw==2: a=np.frombuffer(raw,dtype="<i2").astype(np.int32); full=32768.0
    elif sw==3:
        b=np.frombuffer(raw,dtype=np.uint8).reshape(-1,3); u=b[:,0].astype(np.int32)|(b[:,1].astype(np.int32)<<8)|(b[:,2].astype(np.int32)<<16); a=np.where(u&0x800000,u|~0xFFFFFF,u).astype(np.int32); full=8388608.0
    else: a=np.frombuffer(raw,dtype="<i4").astype(np.int64); full=2147483648.0
    return {"channels":ch,"bit_depth":sw*8,"sample_rate":sr,"frames":nf,"duration_seconds":nf/sr},a.reshape(-1,ch).astype(np.float64)/full
def db(v): return None if v<=0 else 20*math.log10(v)
def stereo(x):
    if x.shape[1]!=2:return {"status":"NOT_STEREO"}
    l,r=x[:,0],x[:,1]; mid=.5*(l+r); side=.5*(l-r); mr=float(np.sqrt(np.mean(mid*mid))); sr=float(np.sqrt(np.mean(side*side))); corr=None if np.std(l)==0 or np.std(r)==0 else float(np.corrcoef(l,r)[0,1])
    return {"status":"DIAGNOSTIC_ONLY_COMPARE_TO_STEREO_INTENT","correlation":corr if corr is None or math.isfinite(corr) else None,"side_relative_to_mid_db":None if sr<=0 or mr<=0 else 20*math.log10(sr/mr),"mono_fold_peak_dbfs":db(float(np.max(np.abs(mid))))}
def loudnorm(ff,p,tech):
    filt=f"loudnorm=I={tech['integrated_lufs_target']}:TP={tech['true_peak_ceiling_dbtp']}:LRA={tech['lra_ceiling_lu']}:print_format=json"; q=subprocess.run([ff,"-hide_banner","-nostats","-i",str(p),"-af",filt,"-f","null","-"],capture_output=True,text=True)
    if q.returncode: raise RuntimeError(q.stderr[-1000:])
    m=re.findall(r'\{\s*"input_i".*?\}',q.stderr,re.S)
    if not m: raise RuntimeError("loudnorm JSON missing")
    r=json.loads(m[-1]); return {"integrated_lufs":float(r["input_i"]),"true_peak_dbtp":float(r["input_tp"]),"lra_lu":float(r["input_lra"]),"threshold_lufs":float(r["input_thresh"])}
def proxy(ff,src,dst,phone):
    c=[ff,"-y","-hide_banner","-loglevel","error","-i",str(src)]; c += ["-af","highpass=f=250,lowpass=f=5000","-ac","1"] if phone else ["-ac","1"]; c += ["-ar","48000","-c:a","pcm_s24le",str(dst)]; subprocess.run(c,check=True)
def verify_prov(p,candidate_sha,errs):
    prov=load(p)
    if prov.get("schema_version")!="room917.derived_master_provenance/1.1": errs.append("PROVENANCE_SCHEMA_INVALID")
    if prov.get("candidate_sha256")!=candidate_sha: errs.append("PROVENANCE_CANDIDATE_SHA_MISMATCH")
    if prov.get("parent_source_sha256")!=SOURCE_SHA: errs.append("PROVENANCE_PARENT_SHA_MISMATCH")
    src=ref_ok(prov.get("source_master"),"SOURCE_MASTER",errs)
    if src and sha(src)!=SOURCE_SHA: errs.append("SOURCE_MASTER_NOT_IMMUTABLE_SOURCE")
    for k in ("patch_plan","render_report","regression_report"): ref_ok(prov.get(k),k.upper(),errs)
    direct={c.get("id"):c.get("pass") for c in prov.get("direct_byte_regression",[])}
    for cid in REQ_REG:
        if direct.get(cid) is not True: errs.append("DIRECT_BYTE_REGRESSION_NOT_PASS:"+cid)
    return {"path":str(Path(p).resolve()),"sha256":sha(p),"build_id":prov.get("build_id"),"parent_source_sha256":prov.get("parent_source_sha256")}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--master",required=True,type=Path); ap.add_argument("--profile",required=True,type=Path); ap.add_argument("--outdir",required=True,type=Path); ap.add_argument("--derived-provenance",type=Path); ap.add_argument("--ffmpeg",default="ffmpeg"); a=ap.parse_args()
    profile=load(a.profile); exp=profile["expected_master_identity"]; tech=profile["technical_profile"]; a.outdir.mkdir(parents=True,exist_ok=True); errs=[]; holds=[]
    if not a.master.is_file(): raise SystemExit("master bytes not found")
    h=sha(a.master); meta,x=read_pcm(a.master); mode="DERIVED_CANDIDATE" if a.derived_provenance else "IMMUTABLE_SOURCE_MASTER"; prov=None
    if a.derived_provenance: prov=verify_prov(a.derived_provenance,h,errs)
    elif h!=SOURCE_SHA: errs.append("MASTER_SHA256_MISMATCH")
    if abs(meta["duration_seconds"]-float(exp["duration_seconds"]))>1/meta["sample_rate"]: errs.append("MASTER_DURATION_MISMATCH")
    if meta["sample_rate"]!=exp["sample_rate_hz"]: errs.append("MASTER_SAMPLE_RATE_MISMATCH")
    if meta["bit_depth"]!=exp["bit_depth"]: errs.append("MASTER_BIT_DEPTH_MISMATCH")
    if meta["channels"]!=exp["channels"]: errs.append("MASTER_CHANNEL_COUNT_MISMATCH")
    peaks=np.max(np.abs(x),axis=0); clipping=bool(np.any(peaks>=1.0))
    if clipping: errs.append("CLIPPING_DETECTED")
    ff=shutil.which(a.ffmpeg); l=None
    if not ff: holds.append("FFMPEG_NOT_AVAILABLE")
    else:
        try:
            l=loudnorm(ff,a.master,tech)
            if abs(l["integrated_lufs"]-tech["integrated_lufs_target"])>tech["integrated_lufs_tolerance_lu"]: errs.append("INTEGRATED_LUFS_OUT_OF_PROFILE")
            if l["true_peak_dbtp"]>tech["true_peak_ceiling_dbtp"]: errs.append("TRUE_PEAK_EXCEEDS_CEILING")
            if l["lra_lu"]>tech["lra_ceiling_lu"]: errs.append("LRA_EXCEEDS_CEILING")
        except Exception as e: holds.append("LOUDNORM_FAILED:"+str(e))
    proxies={}
    if ff and not errs:
        try:
            m=a.outdir/"ROOM917_E01_MONO_FOLDDOWN_QC_PROXY.wav"; p=a.outdir/"ROOM917_E01_PHONE_BAND_MONO_QC_PROXY.wav"; proxy(ff,a.master,m,False); proxy(ff,a.master,p,True); proxies={"mono_folddown":str(m),"phone_band_mono":str(p),"phone_proxy_warning":"Bandwidth/mono stress proxy only; not a physical-device loudspeaker model."}
        except Exception as e: holds.append("PROXY_BUILD_FAILED:"+str(e))
    status="FAIL" if errs else ("HOLD" if holds else "PASS"); report={"schema_version":"room917.release_translation_machine_qc/1.3","status":status,"master":str(a.master),"identity":{"mode":mode,"sha256":h,"size_bytes":a.master.stat().st_size,**meta},"identity_expected_source":exp,"derived_provenance":prov,"sample_peaks_dbfs":[db(float(v)) for v in peaks],"clipping_detected":clipping,"loudness":l,"stereo":stereo(x),"translation_proxies":proxies,"failures":errs,"holds":holds,"human_translation_checks":"REQUIRED_NOT_EXECUTED_BY_MACHINE_QC","human_checklist":profile.get("room917_critical_translation_checks",[]),"law":"Source requires exact SHA. Derived requires provenance/1.1 with accessible exact source and PASS direct byte regression. High correlation is diagnostic only. Human P003B remains mandatory."}
    (a.outdir/"ROOM917_E01_RELEASE_TRANSLATION_MACHINE_QC.json").write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8"); print(status); return 0 if status=="PASS" else 4
if __name__=="__main__": raise SystemExit(main())
