from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "01_FIXTURES.json"


def compute(payload: Dict[str, Any]) -> Dict[str, Any]:
    records = payload["records"]
    ctx = payload["decision_context"]

    total_cost = sum(float(r["cost_eur"]) for r in records)
    work_cost = sum(float(r["cost_eur"]) for r in records if r.get("work_unit_id"))
    outcome_cost = sum(float(r["cost_eur"]) for r in records if r.get("outcome_id"))
    unattributed_outcome_cost = total_cost - outcome_cost

    target = ctx["segment"]
    observed_target_ai = sum(
        float(r["cost_eur"]) for r in records if r.get("observed_segment") == target
    )
    truth_target_ai = sum(
        float(r["cost_eur"])
        for r in records
        if r.get("fixture_ground_truth_segment") == target
    )

    revenue = float(ctx["revenue_eur"])
    non_ai = float(ctx["non_ai_variable_cost_eur"])
    reported_margin = revenue - non_ai - observed_target_ai
    corrected_margin = revenue - non_ai - truth_target_ai

    work_cov = 100.0 * work_cost / total_cost if total_cost else 0.0
    outcome_cov = 100.0 * outcome_cost / total_cost if total_cost else 0.0
    threshold = float(ctx["decision_ready_outcome_coverage_threshold_pct"])

    flip = (reported_margin >= 0 > corrected_margin) or (reported_margin < 0 <= corrected_margin)
    threshold_pass = outcome_cov >= threshold

    return {
        "schema": "ivdivo.general_business.tokenomics_proof_result/1.0",
        "synthetic": True,
        "total_cost_eur": round(total_cost, 2),
        "work_unit_cost_coverage_pct": round(work_cov, 1),
        "outcome_cost_coverage_pct": round(outcome_cov, 1),
        "unattributed_outcome_cost_eur": round(unattributed_outcome_cost, 2),
        "target_segment": target,
        "observed_target_ai_cost_eur": round(observed_target_ai, 2),
        "ground_truth_target_ai_cost_eur": round(truth_target_ai, 2),
        "reported_margin_eur": round(reported_margin, 2),
        "corrected_margin_eur": round(corrected_margin, 2),
        "decision_error_detected": flip,
        "outcome_coverage_threshold_pct": threshold,
        "decision_ready_by_threshold": threshold_pass,
        "technical_result": (
            "PASS_TECHNICAL_GAP_ONLY"
            if flip and not threshold_pass
            else "NO_DECISION_ERROR_DEMONSTRATED"
        ),
        "commercial_result": "HOLD_COMMERCIAL_DIFFERENTIATION_UNPROVEN",
        "wip_promotion": False,
        "buyer_demand": "UNPROVEN",
        "wtp": "UNKNOWN",
        "price": None,
        "transactions": 0,
        "profitability": "UNPROVEN",
        "external_action_authorized": False,
    }


def main() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    print(json.dumps(compute(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
