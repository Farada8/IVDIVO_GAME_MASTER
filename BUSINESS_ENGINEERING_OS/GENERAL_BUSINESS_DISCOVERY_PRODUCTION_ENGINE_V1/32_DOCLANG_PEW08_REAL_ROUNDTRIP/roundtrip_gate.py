from __future__ import annotations

import argparse
import importlib.metadata
import json
import re
import subprocess
import traceback
from pathlib import Path
from typing import Any, Dict, List

from docling.document_converter import DocumentConverter
from docling_core.transforms.serializer.doclang import DocLangDocSerializer, DocLangParams


def _norm(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _enum(value: Any) -> Any:
    return getattr(value, "value", value)


def semantic_signature(doc: Any) -> List[Dict[str, Any]]:
    """Extract bounded downstream-relevant semantics, excluding volatile provenance."""
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
            cells: List[Dict[str, Any]] = []
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
            cells.sort(
                key=lambda x: (
                    x["start_row"], x["start_col"], x["end_row"],
                    x["end_col"], x["text"]
                )
            )
            entry["table"] = {
                "num_rows": int(getattr(data, "num_rows", 0)),
                "num_cols": int(getattr(data, "num_cols", 0)),
                "cells": cells,
            }
        out.append(entry)
    return out


def diff_signatures(before: List[Dict[str, Any]], after: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    mismatches: List[Dict[str, Any]] = []
    for idx in range(max(len(before), len(after))):
        b = before[idx] if idx < len(before) else None
        a = after[idx] if idx < len(after) else None
        if b != a:
            mismatches.append({"index": idx, "before": b, "after": a})
    return mismatches


def _validate_xsd(path: Path) -> Dict[str, Any]:
    proc = subprocess.run(
        ["doclang", "validate", str(path), "--xsd-only", "--quiet"],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
    }


def base_result(source: Path) -> Dict[str, Any]:
    return {
        "schema": "ivdivo.general_business.doclang_pew08_real_roundtrip/1.1",
        "source": source.name,
        "runtime": {
            "docling": importlib.metadata.version("docling"),
            "doclang": importlib.metadata.version("doclang"),
        },
        "path": "HTML_SOURCE_TO_DOCLING_DOCUMENT_TO_DOCLANG_TO_DOCLING_DOCUMENT",
        "baseline_contract": "DOCLING_JSON_LOSSLESS_BASELINE",
        "buyer_demand": "UNPROVEN",
        "wtp": "UNKNOWN",
        "price": None,
        "transactions": 0,
        "profitability": "UNPROVEN",
        "wip_promotion": False,
        "external_action_authorized": False,
        "market_winner": False,
    }


def write_result(out_dir: Path, result: Dict[str, Any]) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "roundtrip_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return result


def run(source: Path, out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    result = base_result(source)

    try:
        converter = DocumentConverter()
        source_doc = converter.convert(source).document
        source_doc.save_as_json(out_dir / "baseline_docling.json")
        before = semantic_signature(source_doc)
        (out_dir / "before_signature.json").write_text(
            json.dumps(before, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )

        # Production/default convenience API path under test.
        default_doclang_path = out_dir / "generated_default.dclg.xml"
        default_doclang_path.write_text(source_doc.export_to_doclang(), encoding="utf-8")

        # Same serializer/content with only the namespace switch changed.
        namespace_doclang_path = out_dir / "generated_with_namespace.dclg.xml"
        namespace_serializer = DocLangDocSerializer(
            doc=source_doc,
            params=DocLangParams(include_namespace=True),
        )
        namespace_doclang_path.write_text(namespace_serializer.serialize().text, encoding="utf-8")
    except Exception as exc:
        result.update({
            "technical_route": "HOLD_TEST_INFRASTRUCTURE_FAILURE",
            "stage": "SOURCE_CONVERT_OR_DOCLANG_EXPORT",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        })
        return write_result(out_dir, result)

    default_xsd = _validate_xsd(default_doclang_path)
    namespace_xsd = _validate_xsd(namespace_doclang_path)
    result["official_xsd"] = {
        "default_export": default_xsd,
        "explicit_namespace_control": namespace_xsd,
    }
    result["serializer_defaults"] = {
        "export_to_doclang_uses_DocLangParams_defaults": True,
        "DocLangParams.include_namespace_default": False,
        "namespace_control_value": True,
    }

    if default_xsd["returncode"] != 0:
        if namespace_xsd["returncode"] == 0:
            result.update({
                "technical_route": "PASS_REAL_DEFAULT_NAMESPACE_COMPATIBILITY_GAP_TECHNICAL_ONLY",
                "real_converter_generated_gap": True,
                "gap_plane": "DEFAULT_PRODUCER_NAMESPACE_VS_OFFICIAL_XSD",
                "minimal_control_fix": "DocLangParams(include_namespace=True)",
            })
        else:
            result.update({
                "technical_route": "PASS_REAL_STRUCTURAL_COMPATIBILITY_GAP_TECHNICAL_ONLY",
                "real_converter_generated_gap": True,
                "gap_plane": "PRODUCER_OUTPUT_VS_OFFICIAL_XSD_BEYOND_NAMESPACE_CONTROL",
            })
        return write_result(out_dir, result)

    # If the default producer becomes XSD-valid, continue into the real round-trip.
    try:
        reloaded_doc = DocumentConverter().convert(default_doclang_path).document
        reloaded_doc.save_as_json(out_dir / "reloaded_docling.json")
        after = semantic_signature(reloaded_doc)
        (out_dir / "after_signature.json").write_text(
            json.dumps(after, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )
    except Exception as exc:
        result.update({
            "technical_route": "PASS_REAL_STRUCTURAL_COMPATIBILITY_GAP_TECHNICAL_ONLY",
            "real_converter_generated_gap": True,
            "gap_plane": "DOCLANG_REIMPORT_FAILURE",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        })
        return write_result(out_dir, result)

    mismatches = diff_signatures(before, after)
    result.update({
        "before_item_count": len(before),
        "after_item_count": len(after),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
    })
    if mismatches:
        result.update({
            "technical_route": "PASS_REAL_FIDELITY_GAP_TECHNICAL_ONLY",
            "real_converter_generated_gap": True,
            "gap_plane": "SCHEMA_VALID_ROUNDTRIP_SEMANTICS",
        })
    else:
        result.update({
            "technical_route": "HOLD_NO_REAL_GAP_IN_BOUNDED_FIXTURES",
            "real_converter_generated_gap": False,
            "gap_plane": None,
        })
    return write_result(out_dir, result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    run(Path(args.source), Path(args.out))


if __name__ == "__main__":
    main()
