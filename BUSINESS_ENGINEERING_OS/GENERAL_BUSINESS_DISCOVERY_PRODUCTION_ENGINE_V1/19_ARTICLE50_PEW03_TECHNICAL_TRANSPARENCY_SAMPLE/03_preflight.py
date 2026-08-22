#!/usr/bin/env python3
"""Deterministic non-legal Article 50 technical transparency preflight.

This module evaluates only declared fixture facts. It does not decide legal
applicability and never certifies compliance or market proof.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ALLOWED_ROLES = {"provider", "deployer", "provider_and_deployer"}
GEN_CONTENT_TYPES = {"audio", "image", "video", "text"}
FORBIDDEN_CLAIMS = {
    "COMPLIANT",
    "CERTIFIED",
    "LEGAL_PASS",
    "LEGAL_FAIL",
    "APPROVED",
    "BUYER_DEMAND_PROVEN",
    "WTP_PROVEN",
}


def _finding(control: str, state: str, reason: str) -> Dict[str, str]:
    return {"control": control, "state": state, "reason": reason}


def evaluate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    facts = case.get("facts", {})
    role = facts.get("role")
    findings: List[Dict[str, str]] = []

    if role not in ALLOWED_ROLES:
        findings.append(_finding(
            "ROLE-00",
            "UNKNOWN",
            "Provider/deployer role is not established; legal applicability cannot be inferred.",
        ))

    # Article 50(1): direct AI-human interaction disclosure.
    if facts.get("direct_human_interaction") is True:
        if role in {"provider", "provider_and_deployer"}:
            disclosure_ok = (
                facts.get("interaction_disclosure_present") is True
                and facts.get("interaction_disclosure_first_interaction") is True
            )
            findings.append(_finding(
                "A50-1-DISCLOSURE",
                "PASS" if disclosure_ok else "FAIL_CONTROL",
                "AI-interaction disclosure is present from first interaction."
                if disclosure_ok
                else "Direct human interaction is declared but first-interaction disclosure is missing or late.",
            ))
            accessibility = facts.get("disclosure_accessible")
            if accessibility is True:
                state, reason = "PASS", "Disclosure accessibility control is declared present."
            elif accessibility is False:
                state, reason = "FAIL_CONTROL", "Disclosure is declared inaccessible."
            else:
                state, reason = "UNKNOWN", "Accessibility of the disclosure is unverified."
            findings.append(_finding("A50-5-ACCESSIBILITY", state, reason))
        else:
            findings.append(_finding(
                "A50-1-DISCLOSURE",
                "UNKNOWN",
                "Direct interaction is declared but provider role is not established.",
            ))

    # Article 50(2): provider-side machine-readable marking.
    generates = facts.get("generates_synthetic_content") is True
    content_type = facts.get("content_type")
    if generates and content_type in GEN_CONTENT_TYPES:
        if facts.get("final_output") is False and facts.get("human_exposed") is False:
            findings.append(_finding(
                "A50-2-MACHINE-MARK",
                "NOT_APPLICABLE_TECHNICAL_SCOPE",
                "Fixture is a non-final closed-loop/machine-only output; technical preflight records the Commission-described scope carve-out without a legal conclusion.",
            ))
        elif role in {"provider", "provider_and_deployer"}:
            if (
                facts.get("placed_on_market_before_2026_08_02") is True
                and facts.get("machine_readable_mark") is not True
            ):
                findings.append(_finding(
                    "A50-2-MACHINE-MARK",
                    "REVIEW_REQUIRED",
                    "Legacy-system transition may apply to Article 50(2); dated legal/applicability review is required rather than an automated PASS/FAIL.",
                ))
            elif facts.get("standard_editing_exception") is True:
                findings.append(_finding(
                    "A50-2-MACHINE-MARK",
                    "REVIEW_REQUIRED",
                    "A standard-editing/non-substantial-alteration exception is asserted; the engine does not certify that exception.",
                ))
            elif facts.get("machine_readable_mark") is True:
                findings.append(_finding(
                    "A50-2-MACHINE-MARK",
                    "PASS",
                    "Machine-readable AI-origin/manipulation marking control is declared present.",
                ))
            elif facts.get("human_exposed") is True or facts.get("final_output") is True:
                findings.append(_finding(
                    "A50-2-MACHINE-MARK",
                    "FAIL_CONTROL",
                    "Provider-side final/human-exposed generative output is declared but no machine-readable mark is present.",
                ))
            else:
                findings.append(_finding(
                    "A50-2-MACHINE-MARK",
                    "UNKNOWN",
                    "Final-output/human-exposure state is insufficiently known.",
                ))
        else:
            findings.append(_finding(
                "A50-2-MACHINE-MARK",
                "UNKNOWN",
                "Generative output exists but provider role is not established from declared facts.",
            ))

    # Article 50(3): emotion recognition / biometric categorisation notice.
    if facts.get("emotion_recognition_or_biometric_categorisation") is True:
        if role in {"deployer", "provider_and_deployer"}:
            notice = facts.get("exposure_notice_present") is True
            findings.append(_finding(
                "A50-3-EXPOSURE-NOTICE",
                "PASS" if notice else "FAIL_CONTROL",
                "Exposure notice control is declared present."
                if notice
                else "Emotion-recognition/biometric-categorisation exposure is declared without notice.",
            ))
        else:
            findings.append(_finding(
                "A50-3-EXPOSURE-NOTICE",
                "UNKNOWN",
                "System function is declared but deployer role is not established.",
            ))

    # Article 50(4): deepfake disclosure for deployers.
    if facts.get("deepfake") is True:
        if role in {"deployer", "provider_and_deployer"}:
            label = facts.get("visible_or_audible_label_first_exposure") is True
            findings.append(_finding(
                "A50-4-DEEPFAKE-LABEL",
                "PASS" if label else "FAIL_CONTROL",
                "Human-perceivable disclosure is present at first exposure."
                if label
                else "Deepfake is declared but first-exposure human-perceivable disclosure is missing; machine-readable marking alone is insufficient.",
            ))
        else:
            findings.append(_finding(
                "A50-4-DEEPFAKE-LABEL",
                "UNKNOWN",
                "Deepfake is declared but deployer role is not established.",
            ))

    # Article 50(4): public-interest text disclosure / declared editorial exception.
    public_interest_text = (
        content_type == "text"
        and facts.get("published_to_inform_public") is True
        and facts.get("matter_of_public_interest") is True
    )
    if public_interest_text:
        if role in {"deployer", "provider_and_deployer"}:
            review = facts.get("substantive_human_review")
            editorial_control = facts.get("editorial_control")
            editorial_responsibility = facts.get("editorial_responsibility")
            if review is True and editorial_control is True and editorial_responsibility is True:
                findings.append(_finding(
                    "A50-4-PUBLIC-INTEREST-TEXT",
                    "NOT_APPLICABLE_DECLARED_EXCEPTION",
                    "Fixture declares substantive human review, editorial control and editorial responsibility; exception routing is recorded but not legally certified.",
                ))
            elif facts.get("visible_label_first_exposure") is True:
                findings.append(_finding(
                    "A50-4-PUBLIC-INTEREST-TEXT",
                    "PASS",
                    "Human-perceivable disclosure label is declared present.",
                ))
            elif review is False or editorial_control is False or editorial_responsibility is False:
                findings.append(_finding(
                    "A50-4-PUBLIC-INTEREST-TEXT",
                    "FAIL_CONTROL",
                    "Public-interest text lacks the declared review/editorial-responsibility exception and no disclosure label is present.",
                ))
            else:
                findings.append(_finding(
                    "A50-4-PUBLIC-INTEREST-TEXT",
                    "UNKNOWN",
                    "Human-review/editorial facts are incomplete; applicability cannot be collapsed to PASS or FAIL.",
                ))
        else:
            findings.append(_finding(
                "A50-4-PUBLIC-INTEREST-TEXT",
                "UNKNOWN",
                "Public-interest text facts exist but deployer role is not established.",
            ))

    if any(item["state"] == "FAIL_CONTROL" for item in findings):
        overall = "CONTROL_GAPS_FOUND"
    elif any(item["state"] in {"UNKNOWN", "REVIEW_REQUIRED"} for item in findings):
        overall = "REVIEW_REQUIRED"
    else:
        overall = "PASS_TECHNICAL_SAMPLE"

    result = {
        "case_id": case["case_id"],
        "overall": overall,
        "findings": findings,
        "legal_compliance_certified": False,
        "market_proof_promoted": False,
    }
    _assert_no_forbidden_claims(result)
    return result


def _assert_no_forbidden_claims(result: Dict[str, Any]) -> None:
    text = json.dumps(result, sort_keys=True).upper()
    for claim in FORBIDDEN_CLAIMS:
        if f'"{claim}"' in text:
            raise AssertionError(f"Forbidden promotion claim emitted: {claim}")


def evaluate_fixture(payload: Dict[str, Any]) -> Dict[str, Any]:
    results = [evaluate_case(case) for case in payload.get("cases", [])]
    return {
        "schema": "ivdivo.article50.preflight_results/0.1",
        "authority_cut": payload.get("authority_cut"),
        "results": results,
        "legal_compliance_certified": False,
        "market_proof_promoted": False,
    }


def main() -> int:
    here = Path(__file__).resolve().parent
    fixture = json.loads((here / "02_SYNTHETIC_FIXTURE.json").read_text(encoding="utf-8"))
    output = evaluate_fixture(fixture)
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
