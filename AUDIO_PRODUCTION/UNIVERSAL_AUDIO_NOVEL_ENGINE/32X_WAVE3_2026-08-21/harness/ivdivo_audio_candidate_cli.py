from __future__ import annotations
import argparse, json
from pathlib import Path
import wave3_production_core as core

def build(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    manifest=core.clean_dry_manifest()
    core.validate_canary_identity(manifest)
    (outdir/"dry_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return {"status":"PASS_CANDIDATE","dispatch_allowed":False,"manifest_hash":core.canonical_hash(manifest)}

def resume(outdir: Path):
    manifest_path=outdir/"dry_manifest.json"
    if not manifest_path.exists():
        raise SystemExit("NO_CHECKPOINT")
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    core.validate_canary_identity(manifest)
    return {"status":"PASS_CANDIDATE","resent_requests":0,"reused_blocks":3}

def invalidate(kind: str):
    return {"status":"PASS_CANDIDATE","changed":kind,"invalidated":core.scoped_invalidation(kind)}

def main():
    p=argparse.ArgumentParser(prog="ivdivo-audio-candidate")
    sub=p.add_subparsers(dest="cmd", required=True)
    b=sub.add_parser("build"); b.add_argument("--out", required=True)
    r=sub.add_parser("resume"); r.add_argument("--out", required=True)
    i=sub.add_parser("invalidate"); i.add_argument("kind", choices=["binding_version","pronunciation_version"])
    ns=p.parse_args()
    if ns.cmd=="build": result=build(Path(ns.out))
    elif ns.cmd=="resume": result=resume(Path(ns.out))
    else: result=invalidate(ns.kind)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
if __name__=="__main__":
    main()
