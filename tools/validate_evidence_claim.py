#!/usr/bin/env python3
"""Fail-closed validator for IVDIVO evidence-category claims.

It prevents common category collapses such as automated tests being presented as
literary quality, model review as Human Signal, dry-run/static inspection as live
provider evidence, and predictions as market behavior.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

MIN_CLASS_FOR_CLAIM = {
    "LITERARY_QUALITY_HUMAN_BELIEVABILITY": {"HUMAN_EXPERT_REVIEW", "HUMAN_TARGET_AUDIENCE_SIGNAL"},
    "HUMAN_SIGNAL": {"HUMAN_TARGET_AUDIENCE_SIGNAL"},
    "LIVE_PROVIDER_RENDER_EXISTS": {"PROVIDER_LIVE_OUTPUT"},
    "RUNTIME_BEHAVIOR_EXECUTED": {"RUNTIME_EXECUTION", "PROVIDER_LIVE_OUTPUT"},
    "AUDIO_PERCEPTUAL_QUALITY": {"HUMAN_EXPERT_REVIEW", "HUMAN_TARGET_AUDIENCE_SIGNAL"},
    "MARKET_DEMAND_OR_CONVERSION": {"MARKET_BEHAVIOR"},
    "SOURCE_TEXT_CONTAINS_FACT": {"SOURCE_TEXT_FACT"},
    "AUTHORITY_STATUS": {"AUTHORITY_FACT"},
    "OBJECTIVE_AUDIO_LEVEL_OR_TIMING": {"OBJECTIVE_MEDIA_MEASUREMENT", "RUNTIME_EXECUTION"}
}

FORBIDDEN_COLLAPSES = {
    ("AUTOMATED_TEST", "LITERARY_QUALITY_HUMAN_BELIEVABILITY"),
    ("MODEL_REVIEW", "HUMAN_SIGNAL"),
    ("STATIC_INSPECTION", "LIVE_PROVIDER_RENDER_EXISTS"),
    ("AUTOMATED_TEST", "LIVE_PROVIDER_RENDER_EXISTS"),
    ("INFERENCE", "MARKET_DEMAND_OR_CONVERSION"),
    ("HYPOTHESIS", "MARKET_DEMAND_OR_CONVERSION"),
    ("MODEL_REVIEW", "MARKET_DEMAND_OR_CONVERSION"),
    ("STATIC_INSPECTION", "RUNTIME_BEHAVIOR_EXECUTED"),
}


def validate(claim: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    for field in ["claim_id", "claim", "result", "evidence_class", "evidence_source", "verification_method", "what_this_evidence_can_prove", "what_this_evidence_cannot_prove"]:
        if claim.get(field) in (None, "", []):
            errors.append(f"MISSING:{field}")

    evidence_class = str(claim.get("evidence_class", ""))
    claim_type = claim.get("claim_type") or claim.get("required_evidence_class_for_claim")
    if claim_type:
        if (evidence_class, claim_type) in FORBIDDEN_COLLAPSES:
            errors.append(f"FORBIDDEN_EVIDENCE_COLLAPSE:{evidence_class}->{claim_type}")
        allowed = MIN_CLASS_FOR_CLAIM.get(str(claim_type))
        if allowed and evidence_class not in allowed:
            errors.append(f"INSUFFICIENT_EVIDENCE_CLASS:{evidence_class}->{claim_type};allowed={sorted(allowed)}")

    if claim.get("result") == "PASS" and claim.get("promotion_allowed") is True:
        if not claim_type:
            errors.append("PROMOTION_WITHOUT_CLAIM_TYPE")
        if evidence_class in {"INFERENCE", "HYPOTHESIS"}:
            errors.append("PROMOTION_FROM_NON_VERIFICATION_EVIDENCE")

    return {
        "status": "PASS" if not errors else "FAIL",
        "claim_id": claim.get("claim_id"),
        "errors": errors,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("claim", type=Path)
    args = p.parse_args()
    try:
        obj = json.loads(args.claim.read_text(encoding="utf-8"))
        result = validate(obj)
    except Exception as exc:
        result = {"status":"FAIL","errors":[f"READ_OR_PARSE:{exc}"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
