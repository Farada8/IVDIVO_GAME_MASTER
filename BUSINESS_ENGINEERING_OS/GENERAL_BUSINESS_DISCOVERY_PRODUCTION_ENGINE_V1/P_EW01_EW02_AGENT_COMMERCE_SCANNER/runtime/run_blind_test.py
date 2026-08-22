from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from agent_commerce_readiness import (
    scan_many,
    validate_issue_classes,
    validate_no_generic_advice,
)

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "02_FIXTURE_INPUTS.json"
KEY = ROOT / "02A_FIXTURE_KEY.json"


def run() -> dict:
    inputs = json.loads(INPUTS.read_text(encoding="utf-8"))
    key = json.loads(KEY.read_text(encoding="utf-8"))
    fixtures = inputs["fixtures"]
    if len(fixtures) != 10:
        raise AssertionError(f"expected 10 fixtures, got {len(fixtures)}")

    # Blind phase: scanner receives normalized observations only.
    results = scan_many(fixtures)
    validate_issue_classes(results)
    validate_no_generic_advice(results)

    issue_counts = Counter()
    disposition_counts = Counter()
    positive_signal_count = 0
    for result in results:
        disposition_counts[result["disposition"]] += 1
        positive_signal_count += len(result["positive_signals"])
        for finding in result["findings"]:
            issue_counts[finding["classification"]] += 1

    # Re-identification happens after routing; names never affect decisions.
    named_results = []
    for result in results:
        identity = key["fixtures"][result["fixture_id"]]
        named_results.append({**result, **identity})

    summary = {
        "schema": "ivdivo.agent_commerce.blind_test_result/1.0",
        "date": "2026-08-22",
        "fixture_count": len(results),
        "issue_counts": dict(sorted(issue_counts.items())),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "positive_signal_count": positive_signal_count,
        "generic_seo_advice_emitted": False,
        "public_only_actionable_gap_count": issue_counts.get("ACTIONABLE_GAP", 0),
        "proof_promotion": False,
        "external_action_authorized": False,
        "commercial_conclusion": "PUBLIC_ONLY_SCAN_IS_PREFLIGHT_NOT_MARKET_VALIDATION",
        "next_engineering_decision": "KEEP_OW01_BUT_NARROW_SCANNER_TO_PREFLIGHT_PLUS_AUTHORIZED_MERCHANT_PACKET_FOR_DEEP_CONFORMANCE",
        "results": named_results,
    }
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
