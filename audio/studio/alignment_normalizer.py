#!/usr/bin/env python3
"""IVDIVO provider-neutral alignment normalizer v1.0.

Normalizes known provider timestamp response families into a stable internal record.
No downstream module should consume raw provider alignment directly.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any, Dict, List


def _record(provider: str, endpoint_profile: str, source_schema: str,
            block_id: str, unit_id: str, unit_index: int,
            start: float, end: float, text_ref: str | None,
            raw_ref: str | None) -> Dict[str, Any]:
    if start is None or end is None or end < start:
        raise ValueError(f"Invalid alignment bounds for {block_id}/{unit_id}: {start}..{end}")
    return {
        "provider": provider,
        "endpoint_profile": endpoint_profile,
        "source_schema": source_schema,
        "block_id": block_id,
        "unit_id": unit_id,
        "unit_index": unit_index,
        "start_seconds": float(start),
        "end_seconds": float(end),
        "text_ref": text_ref,
        "confidence_or_quality": None,
        "raw_evidence_ref": raw_ref,
    }


def detect_schema(payload: Dict[str, Any]) -> str:
    if isinstance(payload.get("voice_segments"), list):
        return "voice_segments"
    al = payload.get("alignment")
    if isinstance(al, dict) and isinstance(al.get("character_start_times_seconds"), list):
        return "character_alignment"
    if isinstance(payload.get("character_start_times_seconds"), list):
        return "character_alignment_top_level"
    raise ValueError("FAIL_ALIGNMENT_SCHEMA_UNSUPPORTED")


def normalize_voice_segments(payload: Dict[str, Any], block_id: str,
                             unit_ids: List[str] | None,
                             text_refs: List[str] | None,
                             provider: str, endpoint_profile: str,
                             raw_ref: str | None) -> List[Dict[str, Any]]:
    out = []
    for i, seg in enumerate(payload["voice_segments"]):
        idx = int(seg.get("dialogue_input_index", i))
        unit_id = unit_ids[idx] if unit_ids and idx < len(unit_ids) else f"{block_id}:unit:{idx}"
        text_ref = text_refs[idx] if text_refs and idx < len(text_refs) else None
        out.append(_record(provider, endpoint_profile, "voice_segments", block_id,
                           unit_id, idx, seg.get("start_time_seconds"),
                           seg.get("end_time_seconds"), text_ref, raw_ref))
    out.sort(key=lambda r: (r["start_seconds"], r["unit_index"]))
    return out


def normalize_character_alignment(payload: Dict[str, Any], block_id: str,
                                  unit_ids: List[str] | None,
                                  text_refs: List[str] | None,
                                  provider: str, endpoint_profile: str,
                                  raw_ref: str | None) -> List[Dict[str, Any]]:
    al = payload.get("alignment") if isinstance(payload.get("alignment"), dict) else payload
    starts = al.get("character_start_times_seconds") or []
    ends = al.get("character_end_times_seconds") or []
    chars = al.get("characters") or []
    if not starts or len(starts) != len(ends):
        raise ValueError("FAIL_ALIGNMENT_NORMALIZATION: missing/mismatched character boundaries")
    unit_id = unit_ids[0] if unit_ids else f"{block_id}:unit:0"
    text_ref = text_refs[0] if text_refs else None
    rec = _record(provider, endpoint_profile, "character_alignment", block_id,
                  unit_id, 0, starts[0], ends[-1], text_ref, raw_ref)
    rec["character_count"] = len(chars) if chars else len(starts)
    return [rec]


def validate(records: List[Dict[str, Any]]) -> None:
    if not records:
        raise ValueError("FAIL_ALIGNMENT_NORMALIZATION: zero normalized records")
    prev = -1.0
    for r in records:
        if r["start_seconds"] < 0 or r["end_seconds"] < r["start_seconds"]:
            raise ValueError("FAIL_ALIGNMENT_NORMALIZATION: invalid bounds")
        if r["start_seconds"] < prev:
            raise ValueError("FAIL_ALIGNMENT_NORMALIZATION: records not sorted")
        prev = r["start_seconds"]


def normalize(payload: Dict[str, Any], block_id: str,
              unit_ids: List[str] | None = None,
              text_refs: List[str] | None = None,
              provider: str = "elevenlabs",
              endpoint_profile: str = "unknown",
              raw_ref: str | None = None) -> Dict[str, Any]:
    schema = detect_schema(payload)
    if schema == "voice_segments":
        records = normalize_voice_segments(payload, block_id, unit_ids, text_refs,
                                           provider, endpoint_profile, raw_ref)
    else:
        records = normalize_character_alignment(payload, block_id, unit_ids, text_refs,
                                                provider, endpoint_profile, raw_ref)
    validate(records)
    return {"schema_version":"1.0","provider":provider,"source_schema":schema,"block_id":block_id,"records":records}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input_json")
    p.add_argument("output_json")
    p.add_argument("--block-id", required=True)
    p.add_argument("--provider", default="elevenlabs")
    p.add_argument("--endpoint-profile", default="unknown")
    p.add_argument("--unit-id", action="append", dest="unit_ids")
    p.add_argument("--text-ref", action="append", dest="text_refs")
    args = p.parse_args()
    inp = Path(args.input_json)
    payload = json.loads(inp.read_text(encoding="utf-8"))
    result = normalize(payload, args.block_id, args.unit_ids, args.text_refs,
                       args.provider, args.endpoint_profile, str(inp))
    Path(args.output_json).write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(f"PASS normalized {len(result['records'])} records from {result['source_schema']}")

if __name__ == "__main__":
    main()
