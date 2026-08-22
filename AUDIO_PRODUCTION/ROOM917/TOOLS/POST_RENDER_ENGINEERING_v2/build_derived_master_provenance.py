#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, wave
from pathlib import Path

SOURCE_SHA = "231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8"
SCENE3_START = 444.980
REQ_REG = {"FORMAT_DURATION_STABILITY","SCENE3_BYTES_UNCHANGED","UNAUTHORIZED_RANGES_UNCHANGED","AUTHORIZED_PATCH_RANGE_CHANGED"}

def sha256_file(p: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(block_size), b""): h.update(b)
    return h.hexdigest()

def load(p: Path): return json.loads(p.read_text(encoding="utf-8"))

def read_raw_pcm(p: Path):
    with wave.open(str(p), "rb") as w:
        meta={"channels":w.getnchannels(),"sample_width":w.getsampwidth(),"sample_rate":w.getframerate(),"frames":w.getnframes(),"compression":w.getcomptype()}
        raw=w.readframes(w.getnframes())
    return meta,raw

def frame_ranges(patches,sr,frame_bytes):
    out=[]
    for p in patches:
        s=float(p.get("interval_start_seconds",p.get("interval_start_s"))); e=float(p.get("interval_end_seconds",p.get("interval_end_s")))
        a=max(0,int(round(s*sr))*frame_bytes); b=max(a,int(round(e*sr))*frame_bytes); out.append((a,b,p.get("patch_id")))
    return out

def direct_byte_regression(source: Path,candidate: Path,patches):
    ms,rs=read_raw_pcm(source); mc,rc=read_raw_pcm(candidate); checks=[{"id":"FORMAT_DURATION_STABILITY","pass":ms==mc,"detail":{"source":ms,"candidate":mc}}]
    if ms!=mc: return checks
    sr=ms["sample_rate"]; fb=ms["channels"]*ms["sample_width"]; allowed=frame_ranges(patches,sr,fb); s3=int(round(SCENE3_START*sr))*fb
    checks.append({"id":"SCENE3_BYTES_UNCHANGED","pass":rs[s3:]==rc[s3:]})
    mask=bytearray(s3)
    for a,b,_ in allowed:
        a=min(max(0,a),s3); b=min(max(a,b),s3)
        if b>a: mask[a:b]=b"\x01"*(b-a)
    unauthorized_changed=any(x!=y and not mask[i] for i,(x,y) in enumerate(zip(rs[:s3],rc[:s3])))
    checks.append({"id":"UNAUTHORIZED_RANGES_UNCHANGED","pass":not unauthorized_changed})
    authorized_changed=any(rs[a:min(b,len(rs))]!=rc[a:min(b,len(rc))] for a,b,_ in allowed)
    checks.append({"id":"AUTHORIZED_PATCH_RANGE_CHANGED","pass":authorized_changed if allowed else True})
    return checks

def main() -> int:
    ap=argparse.ArgumentParser(description="Build evidence-backed ROOM917 P004A derived-master provenance")
    ap.add_argument("--source",required=True,type=Path); ap.add_argument("--candidate",required=True,type=Path); ap.add_argument("--patch-plan",required=True,type=Path); ap.add_argument("--render-report",required=True,type=Path); ap.add_argument("--regression-report",required=True,type=Path); ap.add_argument("--build-id",required=True); ap.add_argument("--out",required=True,type=Path); a=ap.parse_args()
    for p in (a.source,a.candidate,a.patch_plan,a.render_report,a.regression_report):
        if not p.is_file(): raise SystemExit(f"missing required file: {p}")
    errors=[]; source_sha=sha256_file(a.source)
    if source_sha!=SOURCE_SHA: errors.append("SOURCE_MASTER_SHA256_MISMATCH")
    patch=load(a.patch_plan); render=load(a.render_report); reg=load(a.regression_report); patches=patch.get("patches",[])
    if not patches: errors.append("PATCH_PLAN_HAS_NO_PATCHES")
    for p in patches:
        if p.get("source_master_sha256")!=SOURCE_SHA: errors.append("PATCH_SOURCE_MASTER_SHA_MISMATCH"); break
    planned_ids={p.get("patch_id") for p in patches if p.get("patch_id")}; applied_ids={p.get("patch_id") for p in render.get("applied",[]) if p.get("patch_id")}
    if render.get("status") not in ("PASS","PASS_WITH_HOLDS"): errors.append("RENDER_NOT_PASS")
    if not applied_ids: errors.append("RENDER_HAS_NO_APPLIED_PATCHES")
    if not applied_ids.issubset(planned_ids): errors.append("RENDER_APPLIED_PATCH_NOT_IN_PLAN")
    if planned_ids and applied_ids!=planned_ids: errors.append("RENDER_DID_NOT_APPLY_ALL_PLANNED_PATCHES")
    if reg.get("status")!="PASS": errors.append("REGRESSION_NOT_PASS")
    reported={c.get("id"):c.get("pass") for c in reg.get("checks",[])}
    for cid in REQ_REG:
        if reported.get(cid) is not True: errors.append("REGRESSION_REQUIRED_CHECK_NOT_PASS:"+cid)
    direct=direct_byte_regression(a.source,a.candidate,patches); direct_map={c.get("id"):c.get("pass") for c in direct}
    for cid in REQ_REG:
        if direct_map.get(cid) is not True: errors.append("DIRECT_BYTE_REGRESSION_NOT_PASS:"+cid)
    if errors: print("HOLD "+";".join(errors)); return 4
    out={"schema_version":"room917.derived_master_provenance/1.1","build_id":a.build_id,"candidate_sha256":sha256_file(a.candidate),"parent_source_sha256":SOURCE_SHA,"repair_stage":"P004A_SELECTIVE_REPAIR","source_master":{"path":str(a.source.resolve()),"sha256":source_sha},"patch_plan":{"path":str(a.patch_plan.resolve()),"sha256":sha256_file(a.patch_plan)},"render_report":{"path":str(a.render_report.resolve()),"sha256":sha256_file(a.render_report)},"regression_report":{"path":str(a.regression_report.resolve()),"sha256":sha256_file(a.regression_report)},"direct_byte_regression":direct,"notes":"Evidence-backed machine provenance. P003B human listening and final release gate remain mandatory."}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print("PASS "+out["candidate_sha256"]); return 0
if __name__=="__main__": raise SystemExit(main())
