#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

from authority_hygiene_guard import PASS, evaluate_authority


def exists(path):
    return bool(path and Path(path).exists())


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def resolve_authority(explicit, lineage, rules_path):
    if exists(explicit):
        return load(explicit)
    if exists(lineage):
        rules = load(rules_path)
        data = load(lineage)
        return evaluate_authority(data.get("source_authority", {}), rules)
    return {
        "status": "HOLD_UNVERIFIED_AUTHORITY",
        "reasons": ["no_lineage_or_explicit_authority_preflight"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", required=True)
    ap.add_argument("--master-path")
    ap.add_argument("--lineage-compiled")
    ap.add_argument("--timing-map")
    ap.add_argument("--authority-hygiene")
    ap.add_argument("--authority-rules")
    ap.add_argument("--interval-analysis")
    ap.add_argument("--classified")
    ap.add_argument("--patch-plan")
    ap.add_argument("--patched-master")
    ap.add_argument("--regression")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    state = load(args.state)
    here = Path(__file__).resolve().parent
    rules_path = (
        Path(args.authority_rules)
        if args.authority_rules
        else here / "AUTHORITY_HYGIENE_RULES_v1.json"
    )

    authority = resolve_authority(
        args.authority_hygiene,
        args.lineage_compiled,
        rules_path,
    )
    authority_ok = authority.get("status") == PASS

    master_ok = exists(args.master_path)
    lineage_exists = exists(args.lineage_compiled)
    lineage_ok = lineage_exists and authority_ok
    timing_ok = exists(args.timing_map)
    analysis_ok = exists(args.interval_analysis)
    class_ok = exists(args.classified)
    plan_ok = exists(args.patch_plan)
    patched_ok = exists(args.patched_master)
    reg_ok = False

    if exists(args.regression):
        try:
            reg_ok = load(args.regression).get("status") == "PASS"
        except Exception:
            pass

    missing_for_classification = []
    if not authority_ok:
        missing_for_classification.append("AUTHORITY_HYGIENE")
    if not lineage_ok:
        missing_for_classification.append("SEMANTIC_CUE_LINEAGE")
    if not timing_ok:
        missing_for_classification.append("LIVE_ACCEPTED_TIMING")
    if not analysis_ok:
        missing_for_classification.append("P003A2_INTERVAL_ANALYSIS")

    stages = [
        {
            "stage": "AUTHORITY_HYGIENE",
            "status": "PASS" if authority_ok else authority.get("status", "HOLD_UNVERIFIED_AUTHORITY"),
            "details": authority,
        },
        {
            "stage": "MASTER_BYTE_ESCROW",
            "status": "PASS_LOCAL_BYTES_PRESENT" if master_ok else "BLOCKED",
            "next": "Provide exact immutable full-master bytes" if not master_ok else None,
        },
        {
            "stage": "SEMANTIC_CUE_LINEAGE",
            "status": (
                "PASS"
                if lineage_ok
                else ("HOLD_AUTHORITY_PREFLIGHT" if lineage_exists else "READY")
            ),
            "next": (
                None
                if lineage_ok
                else ("Resolve authority hygiene" if lineage_exists else "Compile semantic lineage")
            ),
        },
        {
            "stage": "LIVE_ACCEPTED_TIMING",
            "status": "PASS" if timing_ok else "BLOCKED",
            "next": (
                "Provide ACCEPTED_ALIGNMENT or LIVE_TIMELINE timing map"
                if not timing_ok
                else None
            ),
        },
        {
            "stage": "P003A2_INTERVAL_ANALYSIS",
            "status": (
                "PASS"
                if analysis_ok
                else ("READY" if master_ok else "BLOCKED_MASTER_BYTES")
            ),
        },
        {
            "stage": "INTERVAL_CLASSIFICATION",
            "status": (
                "PASS"
                if class_ok
                else (
                    "READY"
                    if authority_ok and lineage_ok and timing_ok and analysis_ok
                    else "BLOCKED"
                )
            ),
            "missing_prerequisites": [] if class_ok else missing_for_classification,
        },
        {
            "stage": "P004A_SELECTIVE_REPAIR_PLAN",
            "status": "PASS" if plan_ok else ("READY" if class_ok else "BLOCKED"),
        },
        {
            "stage": "PATCH_RENDER",
            "status": (
                "PASS"
                if patched_ok
                else ("READY_EXTERNAL_MIX_ACTION" if plan_ok else "BLOCKED")
            ),
        },
        {
            "stage": "REGRESSION_GATE",
            "status": "PASS" if reg_ok else ("READY" if patched_ok else "BLOCKED"),
        },
        {"stage": "P003B_HUMAN_LISTEN", "status": "REQUIRED_NOT_SIMULATED"},
        {
            "stage": "COMMERCIAL_ABC",
            "status": "BLOCKED_UNTIL_TECHNICAL_REPAIR_AND_HUMAN_GATE",
        },
    ]

    out = {
        "schema_version": "room917.post_render_router/1.1",
        "project": "ROOM917",
        "episode": "E01",
        "state_status": state.get("status"),
        "authority_hygiene": authority,
        "stages": stages,
    }
    Path(args.out).write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("ROUTED authority=" + authority.get("status", "UNKNOWN"))


if __name__ == "__main__":
    main()
