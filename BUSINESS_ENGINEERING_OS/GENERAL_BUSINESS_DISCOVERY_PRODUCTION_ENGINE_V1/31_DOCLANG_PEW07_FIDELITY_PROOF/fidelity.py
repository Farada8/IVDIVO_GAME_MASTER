from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent
NS = {"d": "https://www.doclang.ai/ns/v0"}


def _normalize_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_text_blocks(xml_path: Path) -> List[str]:
    """Extract logical text payloads from DocLang <text> elements.

    Child <location/> elements carry no semantic text. itertext() therefore
    reconstructs the human-readable payload while XML entity decoding happens
    in the parser (e.g. &amp; -> &).
    """
    root = ET.parse(xml_path).getroot()
    blocks: List[str] = []
    for elem in root.findall("d:text", NS):
        logical = _normalize_ws("".join(elem.itertext()))
        blocks.append(logical)
    return blocks


def compare(expected: List[str], actual: List[str]) -> Dict[str, Any]:
    max_len = max(len(expected), len(actual))
    mismatches = []
    for i in range(max_len):
        e = expected[i] if i < len(expected) else None
        a = actual[i] if i < len(actual) else None
        if e != a:
            mismatches.append({"block_index": i, "expected": e, "actual": a})
    return {
        "expected_block_count": len(expected),
        "actual_block_count": len(actual),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "fidelity_pass": len(mismatches) == 0,
    }


def evaluate(xml_path: Path, source_truth_path: Path | None = None) -> Dict[str, Any]:
    source_truth_path = source_truth_path or (ROOT / "01_SOURCE_TRUTH.json")
    truth = json.loads(source_truth_path.read_text(encoding="utf-8"))
    expected = truth["expected_text_blocks"]
    actual = extract_text_blocks(xml_path)
    result = compare(expected, actual)
    result.update(
        {
            "schema": "ivdivo.general_business.doclang_fidelity_result/1.0",
            "fixture": xml_path.name,
            "structural_validation_source": "OFFICIAL_DOCLANG_TOOLKIT_SEPARATE_CI_GATE",
            "buyer_demand": "UNPROVEN",
            "wtp": "UNKNOWN",
            "wip_promotion": False,
            "external_action_authorized": False,
        }
    )
    return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("xml")
    args = parser.parse_args()
    print(json.dumps(evaluate(Path(args.xml)), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
