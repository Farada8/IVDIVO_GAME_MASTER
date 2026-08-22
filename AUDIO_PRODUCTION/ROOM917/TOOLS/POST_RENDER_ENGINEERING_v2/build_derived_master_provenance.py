#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

SOURCE_SHA = "231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8"
REQ_REG = {
    "FORMAT_DURATION_STABILITY",
    "SCENE3_BYTES_UNCHANGED",
    "UNAUTHORIZED_RANGES_UNCHANGED",
    "AUTHORIZED_PATCH_RANGE_CHANGED",
}

def sha256_file(p: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(block_size), b""):
            h.update(b)
    return h.hexdigest()

def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def main() -> int:
    ap = argparse.ArgumentParser(description="Build fail-closed ROOM917 P004A derived-master provenance")
    ap.add_argument("--candidate", required=True, type=Path)
    ap.add_argument("--patch-plan", required=True, type=Path)
    ap.add_argument("--render-report", required=True, type=Path)
    ap.add_argument("--regression-report", required=True, type=Path)
    ap.add_argument("--build-id", required=True)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()

    for p in (a.candidate, a.patch_plan, a.render_report, a.regression_report):
        if not p.is_file():
            raise SystemExit(f"missing required file: {p}")

    patch = load(a.patch_plan)
    render = load(a.render_report)
    reg = load(a.regression_report)
    errors = []

    patches = patch.get("patches", [])
    if not patches:
        errors.append("PATCH_PLAN_HAS_NO_PATCHES")
    for p in patches:
        if p.get("source_master_sha256") != SOURCE_SHA:
            errors.append("PATCH_SOURCE_MASTER_SHA_MISMATCH")
            break

    if render.get("status") not in ("PASS", "PASS_WITH_HOLDS"):
        errors.append("RENDER_NOT_PASS")
    if not render.get("applied", []):
        errors.append("RENDER_HAS_NO_APPLIED_PATCHES")

    if reg.get("status") != "PASS":
        errors.append("REGRESSION_NOT_PASS")
    checks = {c.get("id"): c.get("pass") for c in reg.get("checks", [])}
    for cid in REQ_REG:
        if checks.get(cid) is not True:
            errors.append("REGRESSION_REQUIRED_CHECK_NOT_PASS:" + cid)

    if errors:
        print("HOLD " + ";".join(errors))
        return 4

    out = {
        "schema_version": "room917.derived_master_provenance/1.0",
        "build_id": a.build_id,
        "candidate_sha256": sha256_file(a.candidate),
        "parent_source_sha256": SOURCE_SHA,
        "repair_stage": "P004A_SELECTIVE_REPAIR",
        "patch_plan": {"path": str(a.patch_plan.resolve()), "sha256": sha256_file(a.patch_plan)},
        "render_report": {"path": str(a.render_report.resolve()), "sha256": sha256_file(a.render_report)},
        "regression_report": {"path": str(a.regression_report.resolve()), "sha256": sha256_file(a.regression_report)},
        "notes": "Machine provenance only. P003B human listening and final release gate remain mandatory."
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS " + out["candidate_sha256"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
