from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

from docling.document_converter import DocumentConverter


def _norm(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _enum(value: Any) -> Any:
    return getattr(value, "value", value)


def semantic_signature(doc: Any) -> List[Dict[str, Any]]:
    """Return bounded semantic/structural invariants for fidelity comparison.

    We intentionally do not compare volatile provenance hashes or source-specific
    geometry. The contract measures reading-order item type/label/level, logical
    text, and table cell text/span coordinates because those are user-visible or
    downstream-structural semantics that DocLang is expected to preserve.
    """
    out: List[Dict[str, Any]] = []
    for item, level in doc.iterate_items(with_groups=True):
        entry: Dict[str, Any] = {
            "type": type(item).__name__,
            "level": int(level),
            "label": _enum(getattr(item, "label", None)),
        }
        if hasattr(item, "text"):
            entry["text"] = _norm(getattr(item, "text", ""))
        if hasattr(item, "name") and getattr(item, "name", None):
            entry["name"] = _norm(getattr(item, "name"))

        data = getattr(item, "data", None)
        if data is not None and hasattr(data, "table_cells"):
            cells = []
            for cell in data.table_cells:
                cells.append(
                    {
                        "text": _norm(getattr(cell, "text", "")),
                        "row_span": int(getattr(cell, "row_span", 1)),
                        "col_span": int(getattr(cell, "col_span", 1)),
                        "start_row": int(getattr(cell, "start_row_offset_idx", 0)),
                        "end_row": int(getattr(cell, "end_row_offset_idx", 0)),
                        "start_col": int(getattr(cell, "start_col_offset_idx", 0)),
                        "end_col": int(getattr(cell, "end_col_offset_idx", 0)),
                    }
                )
            cells.sort(key=lambda x: (x["start_row"], x["start_col"], x["end_row"], x["end_col"], x["text"]))
            entry["table"] = {
                "num_rows": int(getattr(data, "num_rows", 0)),
                "num_cols": int(getattr(data, "num_cols", 0)),
                "cells": cells,
            }
        out.append(entry)
    return out


def diff_signatures(before: List[Dict[str, Any]], after: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    mismatches: List[Dict[str, Any]] = []
    n = max(len(before), len(after))
    for i in range(n):
        b = before[i] if i < len(before) else None
        a = after[i] if i < len(after) else None
        if b != a:
            mismatches.append({"index": i, "before": b, "after": a})
    return mismatches


def run(source: Path, out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    converter = DocumentConverter()

    source_result = converter.convert(source)
    source_doc = source_result.document
    baseline_json = out_dir / "baseline_docling.json"
    source_doc.save_as_json(baseline_json)

    doclang_path = out_dir / "generated_roundtrip.dclg.xml"
    doclang_path.write_text(source_doc.export_to_doclang(), encoding="utf-8")

    reloaded_result = converter.convert(doclang_path)
    reloaded_doc = reloaded_result.document
    reloaded_json = out_dir / "reloaded_docling.json"
    reloaded_doc.save_as_json(reloaded_json)

    before = semantic_signature(source_doc)
    after = semantic_signature(reloaded_doc)
    mismatches = diff_signatures(before, after)

    real_gap = len(mismatches) > 0
    route = "PASS_REAL_FIDELITY_GAP_TECHNICAL_ONLY" if real_gap else "HOLD_NO_REAL_GAP_IN_BOUNDED_FIXTURES"
    result = {
        "schema": "ivdivo.general_business.doclang_pew07_roundtrip/1.0",
        "source": source.name,
        "docling_version_pin": "2.121.0",
        "baseline_contract": "DOCLING_JSON_LOSSLESS_BASELINE",
        "path": "SOURCE_TO_DOCLING_DOCUMENT_TO_DOCLANG_TO_DOCLING_DOCUMENT",
        "before_item_count": len(before),
        "after_item_count": len(after),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "real_converter_generated_gap": real_gap,
        "technical_route": route,
        "buyer_demand": "UNPROVEN",
        "wtp": "UNKNOWN",
        "price": None,
        "transactions": 0,
        "profitability": "UNPROVEN",
        "wip_promotion": False,
        "external_action_authorized": False,
    }
    (out_dir / "roundtrip_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )
    (out_dir / "before_signature.json").write_text(
        json.dumps(before, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )
    (out_dir / "after_signature.json").write_text(
        json.dumps(after, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = run(Path(args.source), Path(args.out))
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
