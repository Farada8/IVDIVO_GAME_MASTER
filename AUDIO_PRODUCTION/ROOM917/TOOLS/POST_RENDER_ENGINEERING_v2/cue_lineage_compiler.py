#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

from authority_hygiene_guard import PASS, evaluate_authority

ALLOWED_GRADES = {
    "SCRIPT_SOUND_MASTER_EXPLICIT", "ROOM_CONTRACT_REQUIRED",
    "ACCEPTED_ALIGNMENT", "LIVE_TIMELINE", "DIRECTORIAL_INFERENCE"
}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def compile_lineage(data, rules=None):
    errors = []
    authority_result = None
    if rules is not None:
        authority_result = evaluate_authority(data.get("source_authority", {}), rules)
        if authority_result.get("status") != PASS:
            errors.append(
                "source_authority rejected: "
                + authority_result.get("status", "UNKNOWN")
            )

    blocks = data.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        errors.append("blocks[] required")
        return None, errors

    seen = set()
    normalized = []
    for i, b in enumerate(blocks):
        bid = b.get("block_id")
        if not bid or bid in seen:
            errors.append(f"block[{i}] missing/duplicate block_id")
            continue
        seen.add(bid)
        for f in (
            "scene_id", "room_id", "required_bed", "required_cues",
            "prohibited", "evidence_grade"
        ):
            if f not in b:
                errors.append(f"{bid}: missing {f}")
        grade = b.get("evidence_grade")
        if grade not in ALLOWED_GRADES:
            errors.append(f"{bid}: invalid evidence_grade {grade}")
        has_time = ("start_s" in b or "end_s" in b)
        if has_time:
            if not ("start_s" in b and "end_s" in b):
                errors.append(f"{bid}: start_s/end_s must appear together")
            elif grade not in {"ACCEPTED_ALIGNMENT", "LIVE_TIMELINE"}:
                errors.append(f"{bid}: absolute timing forbidden at grade {grade}")
            elif float(b["end_s"]) <= float(b["start_s"]):
                errors.append(f"{bid}: invalid interval")
        n = dict(b)
        n["required_cues"] = list(b.get("required_cues") or [])
        n["prohibited"] = list(b.get("prohibited") or [])
        normalized.append(n)

    out = {
        "schema_version": "room917.compiled_cue_lineage/1.1",
        "source_schema": data.get("schema_version"),
        "status": "PASS" if not errors else "FAIL",
        "authority_hygiene": authority_result,
        "timing_state": (
            "RESOLVED"
            if normalized and all("start_s" in b for b in normalized)
            else "SEMANTIC_ONLY"
        ),
        "block_count": len(normalized),
        "blocks": normalized,
        "protected_global": data.get("protected_global", []),
        "rooms": data.get("rooms", {}),
        "source_authority": data.get("source_authority", {}),
        "segment": data.get("segment", {}),
    }
    return out, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    ap.add_argument("--authority-rules")
    args = ap.parse_args()

    data = load(args.input)
    rules_path = (
        Path(args.authority_rules)
        if args.authority_rules
        else Path(__file__).resolve().parent / "AUTHORITY_HYGIENE_RULES_v1.json"
    )
    rules = load(rules_path)
    out, errors = compile_lineage(data, rules)
    if out is not None:
        Path(args.out).write_text(
            json.dumps(out, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 2
    print(
        f"PASS authority={out['authority_hygiene']['status']} "
        f"blocks={out['block_count']} timing={out['timing_state']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
