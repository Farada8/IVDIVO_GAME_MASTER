from __future__ import annotations

import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

NS = "https://www.doclang.ai/ns/v0"
TEXT_TAG = f"{{{NS}}}text"


def _norm(value: str) -> str:
    return " ".join(value.split())


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_source_truth(path: Path) -> tuple[list[str] | None, list[str]]:
    problems: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"SOURCE_TRUTH_UNREADABLE:{type(exc).__name__}"]

    blocks = data.get("expected_text_blocks")
    if not isinstance(blocks, list) or not blocks:
        return None, ["SOURCE_TRUTH_EXPECTED_TEXT_BLOCKS_MISSING"]
    if any(not isinstance(x, str) or not _norm(x) for x in blocks):
        problems.append("SOURCE_TRUTH_BLOCK_INVALID")
    if problems:
        return None, problems
    return [_norm(x) for x in blocks], []


def extract_doclang_text_blocks(path: Path) -> tuple[list[str] | None, list[str]]:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        return None, [f"DOCLANG_XML_UNREADABLE:{type(exc).__name__}"]

    if root.tag != f"{{{NS}}}doclang":
        return None, ["DOCLANG_NAMESPACE_OR_ROOT_MISMATCH"]

    blocks: list[str] = []
    for elem in root.iter(TEXT_TAG):
        logical = _norm("".join(elem.itertext()))
        blocks.append(logical)
    return blocks, []


def check(source_truth_path: Path, doclang_path: Path) -> dict[str, Any]:
    expected, truth_problems = load_source_truth(source_truth_path)
    observed, doc_problems = extract_doclang_text_blocks(doclang_path)

    base = {
        "schema": "ivdivo.general_business.doclang_fidelity_result/1.0",
        "source_truth_sha256": _sha256(source_truth_path) if source_truth_path.exists() else None,
        "doclang_sha256": _sha256(doclang_path) if doclang_path.exists() else None,
        "official_structural_validation_proven_by_this_checker": False,
        "buyer_demand_proven": False,
        "wtp_proven": False,
        "transaction_proven": False,
        "profitability_proven": False,
        "external_action_authorized": False,
    }

    if truth_problems or doc_problems or expected is None or observed is None:
        return {
            **base,
            "status": "HOLD_INPUT_UNRESOLVED",
            "problems": truth_problems + doc_problems,
            "expected_text_blocks": expected,
            "observed_text_blocks": observed,
            "mismatches": [],
        }

    mismatches: list[dict[str, Any]] = []
    max_len = max(len(expected), len(observed))
    for index in range(max_len):
        exp = expected[index] if index < len(expected) else None
        obs = observed[index] if index < len(observed) else None
        if exp != obs:
            mismatches.append({
                "index": index,
                "expected": exp,
                "observed": obs,
                "kind": "TEXT_MISMATCH" if exp is not None and obs is not None else "BLOCK_COUNT_MISMATCH",
            })

    return {
        **base,
        "status": "PASS_FIDELITY" if not mismatches else "FAIL_FIDELITY",
        "problems": [],
        "expected_text_blocks": expected,
        "observed_text_blocks": observed,
        "mismatches": mismatches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare source-truth text blocks with DocLang logical text.")
    parser.add_argument("source_truth", type=Path)
    parser.add_argument("doclang", type=Path)
    args = parser.parse_args()
    result = check(args.source_truth, args.doclang)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS_FIDELITY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
