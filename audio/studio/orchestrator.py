#!/usr/bin/env python3
"""IVDIVO Audio Studio Orchestrator v1.1 (audited).

Fail-closed local project/gate controller.
- dependency DAG, not blind linear sequencing
- explicit NOT_APPLICABLE with reason
- build LIVE/DRY_RUN/MIXED evidence tracking
- provider preflight gate
- unresolved MANUAL_REVIEW blocks release
- provider-independent; no secrets and no live provider calls
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from datetime import datetime, timezone

FOLDERS = [
    "00_AUTHORITY", "01_DRAMATURGY", "02_STAGING", "03_PERFORMANCE",
    "04_DIALOGUE_RENDER", "05_FOLEY_MICROTEXTURE", "06_SFX_SOUND_DESIGN",
    "07_AMBIENCE_SPATIAL", "08_MUSIC", "09_EDIT_ALIGNMENT", "10_MIX",
    "11_MASTER", "12_QC", "13_RELEASE", "99_ARCHIVE_SUPERSEDED"
]

GATE_REQUIRED_ARTIFACTS = {
    "AUTHORITY_PASS": ["00_AUTHORITY/AUTHORITY_MANIFEST.json", "00_AUTHORITY/BUILD_MANIFEST.json"],
    "DRAMATURGY_PASS": ["01_DRAMATURGY/LISTENER_CONTRACT.json", "01_DRAMATURGY/AUDIO_DRAMATURGY.json"],
    "STAGING_PASS": ["02_STAGING/AUDIO_STAGING_SCRIPT.json"],
    "PERFORMANCE_PLAN_PASS": ["03_PERFORMANCE/ACTOR_DIRECTOR_SCORE.json", "03_PERFORMANCE/CAST_MAP.json", "03_PERFORMANCE/VOICE_BINDING_LEDGER.json"],
    "SOUND_PLAN_PASS": ["07_AMBIENCE_SPATIAL/ACOUSTIC_PASSPORT.json"],
    "MUSIC_PLAN_PASS": ["08_MUSIC/MUSIC_DRAMATURGY.json"],
    "DRY_RUN_PASS": ["04_DIALOGUE_RENDER/RENDER_BLOCK_PLAN.json", "04_DIALOGUE_RENDER/PROVIDER_REQUESTS_DRY_RUN.json"],
    "PROVIDER_PREFLIGHT_PASS": ["04_DIALOGUE_RENDER/PROVIDER_PREFLIGHT.json"],
    "PILOT_SAMPLE_PASS": ["04_DIALOGUE_RENDER/PILOT_SAMPLE_REPORT.json"],
    "DIALOGUE_LOCK": ["04_DIALOGUE_RENDER/TAKE_REGISTRY.json"],
    "ASSET_LOCK": ["06_SFX_SOUND_DESIGN/ASSET_REGISTRY.json"],
    "TIMELINE_LOCK": ["09_EDIT_ALIGNMENT/NORMALIZED_ALIGNMENT.json", "09_EDIT_ALIGNMENT/RESOLVED_TIMELINE.json"],
    "MIX_PASS": ["10_MIX/MIX_ACTION_SCORE.json", "10_MIX/AUTOMIX_MANIFEST.json", "10_MIX/STEREO_INTEGRITY_REPORT.json"],
    "MASTER_TECH_PASS": ["11_MASTER/MASTER_REPORT.json"],
    "HUMAN_LISTEN_PASS": ["12_QC/HUMAN_LISTEN_REPORT.json"],
    "RELEASE_GO": ["12_QC/QC_REPORT.json", "13_RELEASE/RELEASE_GATE.json"],
}

GATE_DEPS = {
    "AUTHORITY_PASS": [],
    "DRAMATURGY_PASS": ["AUTHORITY_PASS"],
    "STAGING_PASS": ["DRAMATURGY_PASS"],
    "PERFORMANCE_PLAN_PASS": ["STAGING_PASS"],
    "SOUND_PLAN_PASS": ["STAGING_PASS"],
    "MUSIC_PLAN_PASS": ["DRAMATURGY_PASS"],
    "DRY_RUN_PASS": ["PERFORMANCE_PLAN_PASS"],
    "PROVIDER_PREFLIGHT_PASS": ["DRY_RUN_PASS"],
    "PILOT_SAMPLE_PASS": ["PROVIDER_PREFLIGHT_PASS"],
    "DIALOGUE_LOCK": ["PILOT_SAMPLE_PASS"],
    "ASSET_LOCK": ["SOUND_PLAN_PASS", "MUSIC_PLAN_PASS"],
    "TIMELINE_LOCK": ["DIALOGUE_LOCK", "ASSET_LOCK"],
    "MIX_PASS": ["TIMELINE_LOCK"],
    "MASTER_TECH_PASS": ["MIX_PASS"],
    "HUMAN_LISTEN_PASS": ["MASTER_TECH_PASS"],
    "RELEASE_GO": ["HUMAN_LISTEN_PASS"],
}

VALID_GATE_STATES = {"NOT_STARTED", "NOT_APPLICABLE", "WORKING", "REVIEW_PENDING", "PASS", "FAIL", "LOCKED", "SUPERSEDED"}
SATISFIED = {"PASS", "LOCKED", "NOT_APPLICABLE"}


def utc_now(): return datetime.now(timezone.utc).isoformat()

def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

def read_json(path: Path): return json.loads(path.read_text(encoding="utf-8"))

def sha256_file(path: Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def manifest_paths(root):
    return root/"00_AUTHORITY/AUTHORITY_MANIFEST.json", root/"00_AUTHORITY/BUILD_MANIFEST.json"

def load_manifests(root):
    ap,bp=manifest_paths(root)
    if not ap.exists() or not bp.exists(): raise SystemExit("Missing authority/build manifest; run init first")
    return read_json(ap), read_json(bp), ap, bp


def cmd_init(a):
    root=Path(a.project).resolve(); root.mkdir(parents=True,exist_ok=True)
    for f in FOLDERS:(root/f).mkdir(exist_ok=True)
    source=Path(a.source).resolve()
    if not source.exists(): raise SystemExit(f"Source not found: {source}")
    build_id=a.build_id or f"{a.project_id}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    gates={g:"NOT_STARTED" for g in GATE_DEPS}
    authority={
        "project_id":a.project_id,"source_path":str(source),"source_version":a.source_version,
        "source_hash_sha256":sha256_file(source),"delivery_mode":a.delivery_mode,
        "authority_versions":a.authority,"project_overlay_version":a.overlay,"build_id":build_id,
        "status":"WORKING","created_at":utc_now(),"gates":gates,"not_applicable_reasons":{}
    }
    build={
        "build_id":build_id,"project_id":a.project_id,"source_hash":authority["source_hash_sha256"],
        "authority_versions":a.authority,"live_render_status":"DRY_RUN",
        "required_render_blocks":[],"live_evidence_by_block":{},"reused_evidence_by_block":{},
        "placeholder_or_synthetic_blocks":[],"created_at":utc_now(),"status":"WORKING"
    }
    ap,bp=manifest_paths(root); write_json(ap,authority); write_json(bp,build)
    print(f"Initialized {root}\nBuild {build_id}\nSource SHA256 {authority['source_hash_sha256']}")


def ensure_deps(authority, gate):
    for dep in GATE_DEPS[gate]:
        st=authority.get("gates",{}).get(dep,"NOT_STARTED")
        if st not in SATISFIED: raise SystemExit(f"Fail closed: dependency {dep}={st}, required by {gate}")


def missing_artifacts(root, gate):
    return [x for x in GATE_REQUIRED_ARTIFACTS.get(gate,[]) if not (root/x).exists()]


def cmd_gate(a):
    root=Path(a.project).resolve(); authority,build,ap,bp=load_manifests(root)
    if a.gate not in GATE_DEPS: raise SystemExit(f"Unknown gate {a.gate}")
    if a.state not in VALID_GATE_STATES: raise SystemExit(f"Unknown state {a.state}")
    if a.state=="NOT_APPLICABLE":
        if not a.reason: raise SystemExit("NOT_APPLICABLE requires --reason")
        authority.setdefault("not_applicable_reasons",{})[a.gate]=a.reason
    elif a.state in {"PASS","LOCKED"}:
        ensure_deps(authority,a.gate)
        miss=missing_artifacts(root,a.gate)
        if miss: raise SystemExit("Fail closed: required artifacts missing:\n"+"\n".join(miss))
    authority.setdefault("gates",{})[a.gate]=a.state; authority["updated_at"]=utc_now(); write_json(ap,authority)
    print(f"{a.gate} -> {a.state}")


def cmd_status(a):
    root=Path(a.project).resolve(); authority,build,_,_=load_manifests(root)
    print(f"Project: {authority['project_id']}  Build: {build['build_id']}  Render: {build['live_render_status']}")
    for gate in GATE_DEPS:
        st=authority["gates"].get(gate,"NOT_STARTED"); miss=missing_artifacts(root,gate)
        print(f"{gate:26} {st:16} missing={len(miss)} deps={','.join(GATE_DEPS[gate]) or '-'}")


def cmd_verify_source(a):
    root=Path(a.project).resolve(); authority,_,_,_=load_manifests(root)
    cur=sha256_file(Path(authority["source_path"])); exp=authority["source_hash_sha256"]
    if cur!=exp: raise SystemExit(f"FAIL_SOURCE_HASH_MISMATCH\nexpected={exp}\ncurrent ={cur}")
    print("PASS source hash unchanged")


def cmd_render_status(a):
    root=Path(a.project).resolve(); _,build,_,bp=load_manifests(root)
    build["live_render_status"]=a.status; build["updated_at"]=utc_now(); write_json(bp,build)
    print(f"live_render_status -> {a.status}")


def cmd_set_blocks(a):
    root=Path(a.project).resolve(); _,build,_,bp=load_manifests(root)
    build["required_render_blocks"]=a.block or []; build["updated_at"]=utc_now(); write_json(bp,build)
    print(f"required_render_blocks={len(build['required_render_blocks'])}")


def cmd_evidence(a):
    root=Path(a.project).resolve(); _,build,_,bp=load_manifests(root)
    rec={"request":a.request,"response":a.response,"audio":a.audio,"raw_alignment":a.raw_alignment,"request_hash":a.request_hash,"recorded_at":utc_now()}
    target="reused_evidence_by_block" if a.reused_from_build else "live_evidence_by_block"
    if a.reused_from_build:
        rec.update({"reused_from_build_id":a.reused_from_build,"original_take_id":a.original_take_id,"compatibility_check":a.compatibility_check})
    build.setdefault(target,{})[a.block_id]=rec
    build["placeholder_or_synthetic_blocks"]=[x for x in build.get("placeholder_or_synthetic_blocks",[]) if x!=a.block_id]
    build["updated_at"]=utc_now(); write_json(bp,build); print(f"recorded {target}: {a.block_id}")


def live_evidence_errors(build):
    req=set(build.get("required_render_blocks",[])); live=set(build.get("live_evidence_by_block",{})); reused=set(build.get("reused_evidence_by_block",{})); ph=set(build.get("placeholder_or_synthetic_blocks",[]))
    missing=sorted(req-(live|reused)); bad=sorted(req & ph); errs=[]
    if build.get("live_render_status")=="DRY_RUN": errs.append("FAIL_MISSING_LIVE_EVIDENCE: build is DRY_RUN")
    if missing: errs.append("FAIL_MISSING_LIVE_EVIDENCE blocks="+",".join(missing))
    if bad: errs.append("FAIL_MISSING_LIVE_EVIDENCE placeholder_blocks="+",".join(bad))
    for bid,rec in build.get("reused_evidence_by_block",{}).items():
        if bid in req and (not rec.get("reused_from_build_id") or not rec.get("original_take_id") or not rec.get("compatibility_check")):
            errs.append(f"FAIL_INVALID_REUSE_PROVENANCE block={bid}")
    return errs


def unresolved_manual_reviews(root):
    q=root/"12_QC/QC_REPORT.json"
    if not q.exists(): return []
    data=read_json(q); issues=data.get("issues",[]) if isinstance(data,dict) else []
    return [i for i in issues if i.get("status")=="MANUAL_REVIEW"]


def cmd_release_check(a):
    root=Path(a.project).resolve(); authority,build,_,_=load_manifests(root); failed=[]
    for gate in GATE_DEPS:
        if gate=="RELEASE_GO": continue
        st=authority.get("gates",{}).get(gate,"NOT_STARTED")
        if st not in SATISFIED: failed.append(f"{gate}={st}")
    failed += live_evidence_errors(build)
    mr=unresolved_manual_reviews(root)
    if mr: failed.append(f"FAIL_UNRESOLVED_MANUAL_REVIEW count={len(mr)}")
    if failed:
        print("NO_GO")
        for x in failed: print("- "+x)
        raise SystemExit(2)
    print("GO — upstream gates satisfied, live evidence complete, no unresolved manual reviews")


def parser():
    p=argparse.ArgumentParser(description="IVDIVO Audio Studio fail-closed orchestrator v1.1"); sub=p.add_subparsers(dest="cmd",required=True)
    i=sub.add_parser("init"); i.add_argument("project"); i.add_argument("source"); i.add_argument("--project-id",required=True); i.add_argument("--source-version",required=True); i.add_argument("--delivery-mode",choices=["NARRATED","MULTI_VOICE","DRAMATIZED","FULL_AUDIO_DRAMA"],required=True); i.add_argument("--authority",action="append",default=[]); i.add_argument("--overlay"); i.add_argument("--build-id"); i.set_defaults(func=cmd_init)
    s=sub.add_parser("status"); s.add_argument("project"); s.set_defaults(func=cmd_status)
    g=sub.add_parser("gate"); g.add_argument("project"); g.add_argument("gate",choices=list(GATE_DEPS)); g.add_argument("state",choices=sorted(VALID_GATE_STATES)); g.add_argument("--reason"); g.set_defaults(func=cmd_gate)
    v=sub.add_parser("verify-source"); v.add_argument("project"); v.set_defaults(func=cmd_verify_source)
    rs=sub.add_parser("render-status"); rs.add_argument("project"); rs.add_argument("status",choices=["DRY_RUN","LIVE","MIXED"]); rs.set_defaults(func=cmd_render_status)
    b=sub.add_parser("set-render-blocks"); b.add_argument("project"); b.add_argument("--block",action="append"); b.set_defaults(func=cmd_set_blocks)
    e=sub.add_parser("record-evidence"); e.add_argument("project"); e.add_argument("--block-id",required=True); e.add_argument("--request"); e.add_argument("--response"); e.add_argument("--audio"); e.add_argument("--raw-alignment"); e.add_argument("--request-hash"); e.add_argument("--reused-from-build"); e.add_argument("--original-take-id"); e.add_argument("--compatibility-check"); e.set_defaults(func=cmd_evidence)
    r=sub.add_parser("release-check"); r.add_argument("project"); r.set_defaults(func=cmd_release_check)
    return p


def main():
    a=parser().parse_args(); a.func(a)

if __name__=="__main__": main()
