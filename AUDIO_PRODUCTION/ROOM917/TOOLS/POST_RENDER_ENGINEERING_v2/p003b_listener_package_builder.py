#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, wave
from pathlib import Path

SOURCE_SHA="231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8"
REQ_DIRECT={"FORMAT_DURATION_STABILITY","SCENE3_BYTES_UNCHANGED","UNAUTHORIZED_RANGES_UNCHANGED","AUTHORIZED_PATCH_RANGE_CHANGED"}
IDENTITY_FAILURE_PREFIXES=("MASTER_SHA256_","MASTER_DURATION_","MASTER_SAMPLE_RATE_","MASTER_BIT_DEPTH_","MASTER_CHANNEL_COUNT_","DERIVED_","PATCH_","RENDER_","REGRESSION_")

def load(p: Path): return json.loads(p.read_text(encoding="utf-8"))
def sha256_file(p: Path,block_size:int=8*1024*1024)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(block_size),b""): h.update(b)
    return h.hexdigest()
def wav_meta(p: Path):
    with wave.open(str(p),"rb") as w:
        return {"sample_rate_hz":w.getframerate(),"bit_depth":w.getsampwidth()*8,"channels":w.getnchannels(),"duration_seconds":w.getnframes()/w.getframerate(),"compression":w.getcomptype()}
def verify_ref(ref,label,errors):
    if not isinstance(ref,dict) or not ref.get("path") or not ref.get("sha256"):
        errors.append(label+"_REF_MISSING"); return None
    p=Path(ref["path"])
    if not p.is_file(): errors.append(label+"_FILE_NOT_FOUND"); return None
    if sha256_file(p)!=str(ref["sha256"]).lower(): errors.append(label+"_SHA_MISMATCH"); return None
    return p

def main()->int:
    ap=argparse.ArgumentParser(description="Build blind P003B listener package only from identity-verified ROOM917 E01 audio")
    ap.add_argument("--audio",required=True,type=Path); ap.add_argument("--machine-qc",required=True,type=Path); ap.add_argument("--outdir",required=True,type=Path); ap.add_argument("--derived-provenance",type=Path); ap.add_argument("--package-id",default="R917_E01_LISTEN_001"); a=ap.parse_args()
    errors=[]
    if not a.audio.is_file() or not a.machine_qc.is_file(): raise SystemExit("audio or machine-qc file missing")
    audio_sha=sha256_file(a.audio); meta=wav_meta(a.audio); qc=load(a.machine_qc)
    if qc.get("identity",{}).get("sha256")!=audio_sha: errors.append("MACHINE_QC_TARGET_SHA_MISMATCH")
    identity_failures=[f for f in qc.get("failures",[]) if str(f).startswith(IDENTITY_FAILURE_PREFIXES)]
    if identity_failures: errors.extend(["MACHINE_QC_IDENTITY_FAILURE:"+str(f) for f in identity_failures])

    mode="IMMUTABLE_SOURCE_MASTER"; provenance_summary=None
    if a.derived_provenance:
        mode="PROVENANCE_VERIFIED_DERIVED_CANDIDATE"; prov=load(a.derived_provenance)
        if prov.get("schema_version")!="room917.derived_master_provenance/1.1": errors.append("PROVENANCE_SCHEMA_NOT_1_1")
        if prov.get("candidate_sha256")!=audio_sha: errors.append("PROVENANCE_CANDIDATE_SHA_MISMATCH")
        if prov.get("parent_source_sha256")!=SOURCE_SHA: errors.append("PROVENANCE_PARENT_SHA_MISMATCH")
        source=verify_ref(prov.get("source_master"),"SOURCE_MASTER",errors)
        if source and sha256_file(source)!=SOURCE_SHA: errors.append("SOURCE_MASTER_NOT_IMMUTABLE_SOURCE")
        for label in ("patch_plan","render_report","regression_report"): verify_ref(prov.get(label),label.upper(),errors)
        direct={c.get("id"):c.get("pass") for c in prov.get("direct_byte_regression",[])}
        for cid in REQ_DIRECT:
            if direct.get(cid) is not True: errors.append("DIRECT_BYTE_REGRESSION_NOT_PASS:"+cid)
        provenance_summary={"path":str(a.derived_provenance.resolve()),"sha256":sha256_file(a.derived_provenance),"build_id":prov.get("build_id"),"parent_source_sha256":prov.get("parent_source_sha256")}
    elif audio_sha!=SOURCE_SHA:
        errors.append("SOURCE_MODE_AUDIO_SHA_NOT_IMMUTABLE_MASTER")

    if errors:
        print("HOLD "+";".join(errors)); return 4

    a.outdir.mkdir(parents=True,exist_ok=True)
    blind=a.outdir/"R917_BLIND_E01_TARGET.wav"; shutil.copy2(a.audio,blind)
    files={"stereo_target":{"file":blind.name,"sha256":sha256_file(blind),"playback":"PASS_A_FIRST"}}
    proxies=qc.get("translation_proxies",{})
    for key,outname in (("mono_folddown","R917_BLIND_E01_MONO.wav"),("phone_band_mono","R917_BLIND_E01_PHONE_PROXY.wav")):
        src=proxies.get(key)
        if src and Path(src).is_file():
            dst=a.outdir/outname; shutil.copy2(src,dst); files[key]={"file":dst.name,"sha256":sha256_file(dst),"playback":"PASS_C_ONLY_AFTER_PASS_A_NOTES_FROZEN"}

    public_manifest={"schema_version":"room917.p003b_blind_listener_package/1.0","package_id":a.package_id,"status":"READY_FOR_PASS_A","listener_rules":["LISTEN_ONCE_WITHOUT_STORY_NOTES","DO_NOT_OPEN_INTERNAL_IDENTITY_KEY","FREEZE_PASS_A_NOTES_BEFORE_TARGETED_PASS_B","TRANSLATION_FILES_ARE_PASS_C_ONLY"],"files":files,"questions":["Does any acting sound synthetic or performed rather than lived?","Where does the scene feel dead or physically empty?","Can you always tell where people and important sounds are?","Which sound moments are unclear or mask speech?","Does the mystery read without explanation?","At what exact time do you want to stop listening, if anywhere?"],"machine_qc_status":qc.get("status"),"warning":"Machine QC status is not a human listening verdict."}
    (a.outdir/"LISTENER_MANIFEST.json").write_text(json.dumps(public_manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    internal={"schema_version":"room917.p003b_internal_identity_key/1.0","package_id":a.package_id,"identity_mode":mode,"target_original_path":str(a.audio.resolve()),"target_sha256":audio_sha,"target_wav_meta":meta,"machine_qc":{"path":str(a.machine_qc.resolve()),"sha256":sha256_file(a.machine_qc),"status":qc.get("status")},"derived_provenance":provenance_summary,"law":"Keep sealed from Pass A listener until notes are frozen."}
    (a.outdir/"INTERNAL_IDENTITY_KEY_SEALED.json").write_text(json.dumps(internal,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("PASS package="+a.package_id+" mode="+mode); return 0
if __name__=="__main__": raise SystemExit(main())
