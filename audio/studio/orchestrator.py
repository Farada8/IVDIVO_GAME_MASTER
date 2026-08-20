#!/usr/bin/env python3
"""IVDIVO Audio Studio Orchestrator v1.0

Fail-closed local orchestrator for stage/artifact control.
It does NOT call external providers. Provider adapters are separate.
"""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

STAGES = [
    ("S00_AUTHORITY", ["00_AUTHORITY/AUTHORITY_MANIFEST.json"], "AUTHORITY_PASS"),
    ("S01_DRAMATURGY", ["01_DRAMATURGY/LISTENER_CONTRACT.json", "01_DRAMATURGY/AUDIO_DRAMATURGY.json"], "DRAMATURGY_PASS"),
    ("S02_STAGING", ["02_STAGING/AUDIO_STAGING_SCRIPT.json"], "STAGING_PASS"),
    ("S03_PERFORMANCE", ["03_PERFORMANCE/ACTOR_DIRECTOR_SCORE.json", "03_PERFORMANCE/CAST_MAP.json"], "PERFORMANCE_PLAN_PASS"),
    ("S04_SOUND_WORLD", ["05_FOLEY_MICROTEXTURE/FOLEY_CAUSALITY_GRAPH.json", "06_SFX_SOUND_DESIGN/SFX_CUE_SHEET.json", "07_AMBIENCE_SPATIAL/ACOUSTIC_PASSPORT.json"], "SOUND_PLAN_PASS"),
    ("S05_MUSIC", ["08_MUSIC/MUSIC_DRAMATURGY.json"], "MUSIC_PLAN_PASS"),
    ("S06_PROVIDER_DRY_RUN", ["04_DIALOGUE_RENDER/RENDER_BLOCK_PLAN.json", "04_DIALOGUE_RENDER/PROVIDER_REQUESTS_DRY_RUN.json"], "DRY_RUN_PASS"),
    ("S07_DIALOGUE_RENDER", ["04_DIALOGUE_RENDER/TAKE_REGISTRY.json"], "DIALOGUE_LOCK"),
    ("S08_ASSET_RENDER", ["06_SFX_SOUND_DESIGN/ASSET_REGISTRY.json"], "ASSET_LOCK"),
    ("S09_EDIT_ALIGNMENT", ["09_EDIT_ALIGNMENT/RESOLVED_TIMELINE.json"], "TIMELINE_LOCK"),
    ("S10_MIX", ["10_MIX/MIX_ACTION_SCORE.json", "10_MIX/AUTOMIX_MANIFEST.json"], "MIX_PASS"),
    ("S11_MASTER", ["11_MASTER/MASTER_REPORT.json"], "MASTER_TECH_PASS"),
    ("S12_QC_RELEASE", ["12_QC/QC_REPORT.json", "13_RELEASE/RELEASE_GATE.json"], "RELEASE_GO"),
]

FOLDERS = [
    "00_AUTHORITY", "01_DRAMATURGY", "02_STAGING", "03_PERFORMANCE",
    "04_DIALOGUE_RENDER", "05_FOLEY_MICROTEXTURE", "06_SFX_SOUND_DESIGN",
    "07_AMBIENCE_SPATIAL", "08_MUSIC", "09_EDIT_ALIGNMENT", "10_MIX",
    "11_MASTER", "12_QC", "13_RELEASE", "99_ARCHIVE_SUPERSEDED"
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_init(args):
    root = Path(args.project).resolve()
    root.mkdir(parents=True, exist_ok=True)
    for folder in FOLDERS:
        (root / folder).mkdir(exist_ok=True)

    source = Path(args.source).resolve()
    if not source.exists():
        raise SystemExit(f"Source not found: {source}")

    manifest = {
        "project_id": args.project_id,
        "source_path": str(source),
        "source_version": args.source_version,
        "source_hash_sha256": sha256_file(source),
        "delivery_mode": args.delivery_mode,
        "authority_versions": args.authority,
        "project_overlay_version": args.overlay,
        "status": "WORKING",
        "created_at": utc_now(),
        "gates": {gate: "NOT_STARTED" for _, _, gate in STAGES},
    }
    write_json(root / "00_AUTHORITY/AUTHORITY_MANIFEST.json", manifest)
    print(f"Initialized: {root}")
    print(f"Source SHA256: {manifest['source_hash_sha256']}")


def artifact_status(root: Path):
    rows = []
    for stage, files, gate in STAGES:
        missing = [f for f in files if not (root / f).exists()]
        rows.append((stage, gate, missing))
    return rows


def cmd_status(args):
    root = Path(args.project).resolve()
    manifest_path = root / "00_AUTHORITY/AUTHORITY_MANIFEST.json"
    if not manifest_path.exists():
        raise SystemExit("No AUTHORITY_MANIFEST.json. Run init first.")
    manifest = read_json(manifest_path)
    print(f"Project: {manifest.get('project_id')}")
    print(f"Mode: {manifest.get('delivery_mode')}")
    print(f"Source hash: {manifest.get('source_hash_sha256')}")
    for stage, gate, missing in artifact_status(root):
        gate_state = manifest.get("gates", {}).get(gate, "NOT_STARTED")
        print(f"{stage:24} {gate:22} {gate_state:12} missing={len(missing)}")
        for item in missing:
            print(f"  - {item}")


def ensure_previous_gates(manifest: dict, target_gate: str):
    gate_names = [g for _, _, g in STAGES]
    idx = gate_names.index(target_gate)
    for prior in gate_names[:idx]:
        if manifest.get("gates", {}).get(prior) not in ("PASS", "LOCKED"):
            raise SystemExit(f"Fail closed: previous gate {prior} is not PASS/LOCKED")


def cmd_gate(args):
    root = Path(args.project).resolve()
    manifest_path = root / "00_AUTHORITY/AUTHORITY_MANIFEST.json"
    manifest = read_json(manifest_path)
    gate_names = [g for _, _, g in STAGES]
    if args.gate not in gate_names:
        raise SystemExit(f"Unknown gate: {args.gate}")

    stage, required_files, _ = next(row for row in STAGES if row[2] == args.gate)
    if args.state in ("PASS", "LOCKED"):
        ensure_previous_gates(manifest, args.gate)
        missing = [f for f in required_files if not (root / f).exists()]
        if missing:
            raise SystemExit("Fail closed: required artifacts missing:\n" + "\n".join(missing))

    manifest.setdefault("gates", {})[args.gate] = args.state
    manifest["updated_at"] = utc_now()
    write_json(manifest_path, manifest)
    print(f"{args.gate} -> {args.state}")


def cmd_verify_source(args):
    root = Path(args.project).resolve()
    manifest = read_json(root / "00_AUTHORITY/AUTHORITY_MANIFEST.json")
    source = Path(manifest["source_path"])
    current = sha256_file(source)
    expected = manifest["source_hash_sha256"]
    if current != expected:
        raise SystemExit(f"FAIL source hash mismatch\nexpected={expected}\ncurrent ={current}")
    print("PASS source hash unchanged")


def cmd_release_check(args):
    root = Path(args.project).resolve()
    manifest = read_json(root / "00_AUTHORITY/AUTHORITY_MANIFEST.json")
    required = [g for _, _, g in STAGES]
    failed = [g for g in required if manifest.get("gates", {}).get(g) not in ("PASS", "LOCKED")]
    if failed:
        print("NO_GO")
        for g in failed:
            print(f"- {g}: {manifest.get('gates', {}).get(g, 'NOT_STARTED')}")
        raise SystemExit(2)
    print("GO — all required studio gates are PASS/LOCKED")


def build_parser():
    p = argparse.ArgumentParser(description="IVDIVO Audio Studio fail-closed orchestrator")
    sub = p.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init")
    i.add_argument("project")
    i.add_argument("source")
    i.add_argument("--project-id", required=True)
    i.add_argument("--source-version", required=True)
    i.add_argument("--delivery-mode", choices=["NARRATED", "MULTI_VOICE", "DRAMATIZED", "FULL_AUDIO_DRAMA"], required=True)
    i.add_argument("--authority", action="append", default=[])
    i.add_argument("--overlay", default=None)
    i.set_defaults(func=cmd_init)

    s = sub.add_parser("status")
    s.add_argument("project")
    s.set_defaults(func=cmd_status)

    g = sub.add_parser("gate")
    g.add_argument("project")
    g.add_argument("gate")
    g.add_argument("state", choices=["NOT_STARTED", "WORKING", "REVIEW_PENDING", "PASS", "FAIL", "LOCKED", "SUPERSEDED"])
    g.set_defaults(func=cmd_gate)

    v = sub.add_parser("verify-source")
    v.add_argument("project")
    v.set_defaults(func=cmd_verify_source)

    r = sub.add_parser("release-check")
    r.add_argument("project")
    r.set_defaults(func=cmd_release_check)
    return p


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
