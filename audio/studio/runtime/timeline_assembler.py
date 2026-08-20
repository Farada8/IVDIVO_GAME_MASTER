#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio — Resolved Timeline Assembler v0.1.

Consumes accepted provider-neutral normalized alignments plus an explicit block
assembly plan. Resolves semantic cue anchors only after real alignment exists.

No guessed absolute timestamps. Unknown blocks/units/anchors fail closed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

ALLOWED_EDGES = {"START", "END"}


def load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def index_alignments(alignment_docs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for doc in alignment_docs:
        bid = doc.get("block_id")
        records = doc.get("records")
        if not bid or not isinstance(records, list) or not records:
            raise ValueError("FAIL_ALIGNMENT_INPUT: normalized alignment missing block_id/records")
        if bid in out:
            raise ValueError(f"FAIL_DUPLICATE_ALIGNMENT_BLOCK: {bid}")
        for rec in records:
            if rec.get("block_id") != bid:
                raise ValueError(f"FAIL_ALIGNMENT_BLOCK_MISMATCH: {bid}")
            start = rec.get("start_seconds")
            end = rec.get("end_seconds")
            if start is None or end is None or float(end) < float(start):
                raise ValueError(f"FAIL_ALIGNMENT_BOUNDS: {bid}/{rec.get('unit_id')}")
        out[bid] = doc
    return out


def resolve_blocks(assembly: Dict[str, Any], alignment_index: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    blocks = assembly.get("blocks") or []
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("FAIL_ASSEMBLY_PLAN: no blocks")

    resolved_blocks: List[Dict[str, Any]] = []
    unit_index: Dict[str, Dict[str, Any]] = {}
    dialogue_events: List[Dict[str, Any]] = []
    cursor = 0.0
    seen = set()

    for i, b in enumerate(blocks):
        bid = b.get("block_id")
        if not bid:
            raise ValueError(f"FAIL_ASSEMBLY_PLAN: blocks[{i}] missing block_id")
        if bid in seen:
            raise ValueError(f"FAIL_DUPLICATE_ASSEMBLY_BLOCK: {bid}")
        seen.add(bid)
        if bid not in alignment_index:
            raise ValueError(f"FAIL_MISSING_ALIGNMENT_BLOCK: {bid}")

        gap_before_ms = float(b.get("gap_before_ms", 0) or 0)
        overlap_previous_ms = float(b.get("overlap_previous_ms", 0) or 0)
        if gap_before_ms < 0 or overlap_previous_ms < 0:
            raise ValueError(f"FAIL_ASSEMBLY_PLAN: negative gap/overlap for {bid}")
        if gap_before_ms and overlap_previous_ms:
            raise ValueError(f"FAIL_ASSEMBLY_PLAN: {bid} cannot define both gap_before_ms and overlap_previous_ms")

        block_start = cursor + gap_before_ms / 1000.0 - overlap_previous_ms / 1000.0
        if block_start < 0:
            raise ValueError(f"FAIL_ASSEMBLY_PLAN: negative block start for {bid}")

        records = alignment_index[bid]["records"]
        block_relative_end = max(float(r["end_seconds"]) for r in records)
        block_end = block_start + block_relative_end

        resolved_blocks.append({
            "block_id": bid,
            "sequence_index": i,
            "start_seconds": block_start,
            "end_seconds": block_end,
            "duration_seconds": block_relative_end,
            "gap_before_ms": gap_before_ms,
            "overlap_previous_ms": overlap_previous_ms,
            "alignment_source_schema": alignment_index[bid].get("source_schema"),
        })

        for rec in records:
            uid = rec.get("unit_id")
            if not uid:
                raise ValueError(f"FAIL_ALIGNMENT_INPUT: unit_id missing in {bid}")
            if uid in unit_index:
                raise ValueError(f"FAIL_DUPLICATE_TIMELINE_UNIT: {uid}")
            absolute = {
                "event_type": "DIALOGUE_UNIT",
                "block_id": bid,
                "unit_id": uid,
                "text_ref": rec.get("text_ref"),
                "start_seconds": block_start + float(rec["start_seconds"]),
                "end_seconds": block_start + float(rec["end_seconds"]),
                "source_relative_start_seconds": float(rec["start_seconds"]),
                "source_relative_end_seconds": float(rec["end_seconds"]),
                "provider": rec.get("provider"),
                "endpoint_profile": rec.get("endpoint_profile"),
                "raw_evidence_ref": rec.get("raw_evidence_ref"),
            }
            unit_index[uid] = absolute
            dialogue_events.append(absolute)

        cursor = max(cursor, block_end)

    unused_alignments = sorted(set(alignment_index) - seen)
    return {
        "resolved_blocks": resolved_blocks,
        "dialogue_events": sorted(dialogue_events, key=lambda x: (x["start_seconds"], x["end_seconds"])),
        "unit_index": unit_index,
        "scene_duration_seconds": cursor,
        "unused_alignment_blocks": unused_alignments,
    }


def resolve_cues(cue_plan: Dict[str, Any] | None, unit_index: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    if not cue_plan:
        return {"resolved": [], "unresolved": []}
    cues = cue_plan.get("cues") or []
    resolved: List[Dict[str, Any]] = []
    unresolved: List[Dict[str, Any]] = []

    for cue in cues:
        cid = cue.get("cue_id")
        anchor = cue.get("anchor") or {}
        uid = anchor.get("unit_id")
        edge = str(anchor.get("edge", "")).upper()
        offset_ms = float(anchor.get("offset_ms", 0) or 0)
        if not cid or not uid or edge not in ALLOWED_EDGES:
            unresolved.append({"cue_id": cid, "reason": "INVALID_SEMANTIC_ANCHOR", "anchor": anchor})
            continue
        unit = unit_index.get(uid)
        if not unit:
            unresolved.append({"cue_id": cid, "reason": "UNIT_NOT_FOUND", "anchor": anchor})
            continue
        base = unit["start_seconds"] if edge == "START" else unit["end_seconds"]
        start = base + offset_ms / 1000.0
        if start < 0:
            unresolved.append({"cue_id": cid, "reason": "NEGATIVE_RESOLVED_TIME", "anchor": anchor})
            continue
        duration_ms = cue.get("duration_ms")
        end = None if duration_ms is None else start + float(duration_ms) / 1000.0
        resolved.append({
            "event_type": cue.get("event_type", "CUE"),
            "cue_id": cid,
            "source_id": cue.get("source_id"),
            "story_function": cue.get("story_function"),
            "start_seconds": start,
            "end_seconds": end,
            "resolved_from": {"unit_id": uid, "edge": edge, "offset_ms": offset_ms},
            "stem": cue.get("stem"),
            "asset_id": cue.get("asset_id"),
            "mix_intent_ref": cue.get("mix_intent_ref"),
        })
    return {"resolved": sorted(resolved, key=lambda x: x["start_seconds"]), "unresolved": unresolved}


def assemble(assembly: Dict[str, Any], alignment_docs: List[Dict[str, Any]], cue_plan: Dict[str, Any] | None = None) -> Dict[str, Any]:
    idx = index_alignments(alignment_docs)
    base = resolve_blocks(assembly, idx)
    cues = resolve_cues(cue_plan, base["unit_index"])
    gate = "PASS" if not cues["unresolved"] else "FAIL"

    all_events = list(base["dialogue_events"]) + list(cues["resolved"])
    all_events.sort(key=lambda x: (x.get("start_seconds", 0), x.get("event_type", "")))
    duration = base["scene_duration_seconds"]
    for ev in cues["resolved"]:
        if ev.get("end_seconds") is not None:
            duration = max(duration, float(ev["end_seconds"]))
        else:
            duration = max(duration, float(ev["start_seconds"]))

    return {
        "schema": "IVDIVO_RESOLVED_TIMELINE_v1",
        "project_id": assembly.get("project_id"),
        "scene_id": assembly.get("scene_id"),
        "source_hash": assembly.get("source_hash"),
        "gate": gate,
        "timeline_origin_seconds": 0.0,
        "duration_seconds": duration,
        "blocks": base["resolved_blocks"],
        "events": all_events,
        "unresolved_anchors": cues["unresolved"],
        "unused_alignment_blocks": base["unused_alignment_blocks"],
        "law": "All absolute times derive from accepted normalized alignment + explicit assembly gaps/overlaps + semantic anchors; no guessed timestamps.",
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Assemble provider-neutral resolved scene timeline")
    p.add_argument("assembly_plan")
    p.add_argument("alignment", nargs="+")
    p.add_argument("--cue-plan")
    p.add_argument("--output", required=True)
    a = p.parse_args()

    try:
        result = assemble(
            load(Path(a.assembly_plan)),
            [load(Path(x)) for x in a.alignment],
            load(Path(a.cue_plan)) if a.cue_plan else None,
        )
    except ValueError as exc:
        raise SystemExit(str(exc))

    write(Path(a.output), result)
    print(json.dumps({
        "gate": result["gate"],
        "blocks": len(result["blocks"]),
        "events": len(result["events"]),
        "duration_seconds": result["duration_seconds"],
        "unresolved_anchors": len(result["unresolved_anchors"]),
    }, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["gate"] == "PASS" else 2)


if __name__ == "__main__":
    main()
