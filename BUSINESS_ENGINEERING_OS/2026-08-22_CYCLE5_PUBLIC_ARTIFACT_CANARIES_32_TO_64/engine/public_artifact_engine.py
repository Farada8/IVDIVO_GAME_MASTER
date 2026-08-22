from __future__ import annotations

import hashlib
import json
from typing import Any

PUBLIC_EVIDENCE_GRADES = {"E0", "E1", "E2", "E2+"}
FORBIDDEN_PUBLIC_PROOF_FIELDS = {
    "willingness_to_pay",
    "paid_amount_eur",
    "buyer_commitment",
    "repeat_purchase",
    "unit_economics",
    "gross_margin",
    "conversion_rate",
    "procurement_eligibility",
    "legal_clearance",
}


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def register_library_discovery(
    *,
    title: str,
    file_library_ref: str | None,
    raw_drive_id: str | None = None,
    byte_hash: str | None = None,
) -> dict[str, Any]:
    if not title.strip():
        raise ValueError("TITLE_REQUIRED")
    durable = bool(raw_drive_id and byte_hash)
    status = "RAW_DURABLE" if durable else "FILE_LIBRARY_REFERENCE_ONLY"
    row = {
        "schema": "ivdivo.business.library_discovery/1.0",
        "title": title.strip(),
        "file_library_ref": file_library_ref,
        "raw_drive_id": raw_drive_id,
        "byte_hash": byte_hash,
        "status": status,
        "raw_copyright_binary_public_git_allowed": False,
    }
    row["record_hash"] = canonical_hash(row)
    return row


def evidence_ceiling_guard(record: dict[str, Any]) -> dict[str, Any]:
    grade = record.get("evidence_grade")
    violations: list[str] = []
    if grade not in PUBLIC_EVIDENCE_GRADES:
        violations.append("EVIDENCE_GRADE_ABOVE_PUBLIC_CEILING")
    for field in sorted(FORBIDDEN_PUBLIC_PROOF_FIELDS):
        if record.get(field) is not None:
            violations.append(f"PUBLIC_SOURCE_CANNOT_PROVE:{field}")
    return {
        "status": "PASS" if not violations else "FAIL",
        "public_ceiling": "E2+",
        "violations": violations,
    }


def compile_public_artifact(
    opportunity: dict[str, Any],
    *,
    artifact_template_id: str,
    public_sources: list[dict[str, Any]],
    decision_checks: list[str],
    missing_data: list[str],
    target_candidate: str | None = None,
) -> dict[str, Any]:
    guard = evidence_ceiling_guard(opportunity)
    if guard["status"] != "PASS":
        return {
            "schema": "ivdivo.business.public_artifact/1.0",
            "status": "FAIL_EVIDENCE_CEILING",
            "guard": guard,
            "dispatch_allowed": False,
            "market_proof_claimed": False,
        }
    if not artifact_template_id.strip():
        raise ValueError("ARTIFACT_TEMPLATE_REQUIRED")
    if not public_sources:
        raise ValueError("PUBLIC_SOURCE_REQUIRED")
    for source in public_sources:
        if not source.get("source_ref") or not source.get("observed_at"):
            raise ValueError("SOURCE_REF_AND_DATE_REQUIRED")

    unique_sources = sorted(
        ({"source_ref": s["source_ref"], "observed_at": s["observed_at"], "authority": s.get("authority", "PUBLIC")} for s in public_sources),
        key=lambda x: (x["source_ref"], x["observed_at"]),
    )
    artifact = {
        "schema": "ivdivo.business.public_artifact/1.0",
        "status": "PUBLIC_SAMPLE_READY",
        "opportunity_id": opportunity.get("opportunity_id"),
        "opportunity_name": opportunity.get("name"),
        "artifact_template_id": artifact_template_id,
        "buyer_segment": opportunity.get("buyer_segment"),
        "buyer_workload_hypothesis": opportunity.get("buyer_workload"),
        "offer_hypothesis": opportunity.get("offer"),
        "target_candidate": target_candidate,
        "decision_checks": list(decision_checks),
        "missing_data": list(missing_data),
        "sources": unique_sources,
        "evidence_grade": opportunity.get("evidence_grade"),
        "evidence_ceiling": "E2+",
        "founder_cash_eur": 0,
        "requires_buyer_contact": False,
        "willingness_to_pay": None,
        "paid_amount_eur": None,
        "buyer_commitment": None,
        "repeat_purchase": None,
        "unit_economics": None,
        "gross_margin": None,
        "conversion_rate": None,
        "procurement_eligibility": None,
        "legal_clearance": None,
        "market_claim_status": "HYPOTHESIS_ONLY",
        "market_proof_claimed": False,
        "dispatch_allowed": False,
    }
    artifact["artifact_hash"] = canonical_hash(artifact)
    return artifact


def validate_buyer_interaction_receipt(receipt: dict[str, Any] | None, *, artifact_hash: str) -> dict[str, Any]:
    if not receipt:
        return {"status": "HOLD_NO_REAL_BUYER_INTERACTION", "evidence_grade": "E2+"}
    required = {"kind", "source_type", "artifact_hash", "observed_at", "buyer_role", "interaction_outcome"}
    missing = sorted(k for k in required if not receipt.get(k))
    if missing:
        return {"status": "FAIL_BUYER_RECEIPT_INCOMPLETE", "missing": missing, "evidence_grade": "E2+"}
    if receipt.get("kind") != "BUYER_INTERACTION" or receipt.get("source_type") != "REAL_HUMAN":
        return {"status": "FAIL_SYNTHETIC_OR_WRONG_CLASS", "evidence_grade": "E2+"}
    if receipt.get("artifact_hash") != artifact_hash:
        return {"status": "FAIL_ARTIFACT_LINEAGE", "evidence_grade": "E2+"}
    return {"status": "PASS_E3_OBSERVED", "evidence_grade": "E3", "receipt_hash": canonical_hash(receipt)}


def validate_money_receipt(receipt: dict[str, Any] | None, *, artifact_hash: str) -> dict[str, Any]:
    if not receipt:
        return {"status": "HOLD_NO_REAL_MONEY_OR_PO", "evidence_grade": "E3_OR_LOWER"}
    required = {"kind", "source_type", "artifact_hash", "observed_at", "transaction_or_po_id", "amount_eur"}
    missing = sorted(k for k in required if receipt.get(k) in (None, ""))
    if missing:
        return {"status": "FAIL_MONEY_RECEIPT_INCOMPLETE", "missing": missing, "evidence_grade": "E3_OR_LOWER"}
    if receipt.get("kind") not in {"PAYMENT", "PURCHASE_ORDER", "DEPOSIT"} or receipt.get("source_type") != "REAL_TRANSACTION":
        return {"status": "FAIL_SYNTHETIC_OR_WRONG_CLASS", "evidence_grade": "E3_OR_LOWER"}
    if receipt.get("artifact_hash") != artifact_hash:
        return {"status": "FAIL_ARTIFACT_LINEAGE", "evidence_grade": "E3_OR_LOWER"}
    if float(receipt.get("amount_eur", 0)) <= 0:
        return {"status": "FAIL_NONPOSITIVE_AMOUNT", "evidence_grade": "E3_OR_LOWER"}
    return {"status": "PASS_E4_MONEY_OBSERVED", "evidence_grade": "E4", "receipt_hash": canonical_hash(receipt)}


def route_market_experiment(
    artifact: dict[str, Any] | None,
    *,
    buyer_receipt: dict[str, Any] | None = None,
    money_receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not artifact or artifact.get("status") != "PUBLIC_SAMPLE_READY":
        return {"status": "HOLD_PUBLIC_SAMPLE_REQUIRED", "next_action": "COMPILE_PUBLIC_SAMPLE", "send_allowed": False}
    buyer = validate_buyer_interaction_receipt(buyer_receipt, artifact_hash=artifact["artifact_hash"])
    if buyer["status"] != "PASS_E3_OBSERVED":
        return {
            "status": "BUYER_REVIEW_REQUIRED",
            "next_action": "REAL_VOLUNTARY_BUYER_INTERACTION",
            "current_evidence_grade": "E2+",
            "send_allowed": False,
            "buyer_gate": buyer,
        }
    money = validate_money_receipt(money_receipt, artifact_hash=artifact["artifact_hash"])
    if money["status"] != "PASS_E4_MONEY_OBSERVED":
        return {
            "status": "E3_OBSERVED_MONEY_REQUIRED",
            "next_action": "BOUNDED_PAID_PILOT_OR_PO",
            "current_evidence_grade": "E3",
            "send_allowed": False,
            "buyer_gate": buyer,
            "money_gate": money,
        }
    return {
        "status": "E4_OBSERVED",
        "next_action": "MEASURE_DELIVERY_AND_UNIT_ECONOMICS",
        "current_evidence_grade": "E4",
        "send_allowed": False,
        "buyer_gate": buyer,
        "money_gate": money,
    }


def wip_guard(primary: str | None, pilots: list[str]) -> dict[str, Any]:
    active = ([primary] if primary else []) + list(pilots)
    violations: list[str] = []
    if len(active) > 3:
        violations.append("WIP_LIMIT_EXCEEDED")
    if len(active) != len(set(active)):
        violations.append("DUPLICATE_WIP_ID")
    return {"status": "PASS" if not violations else "FAIL", "active": active, "limit": 3, "violations": violations}


def price_hypothesis(low_eur: float, high_eur: float) -> dict[str, Any]:
    if low_eur < 0 or high_eur <= 0 or low_eur > high_eur:
        raise ValueError("INVALID_PRICE_RANGE")
    return {"low_eur": low_eur, "high_eur": high_eur, "validated": False, "evidence_grade": "HYPOTHESIS_ONLY"}


def self_improvement_candidate(
    *,
    defect: str,
    root_cause: str,
    repair: str,
    retest_result: str,
    evidence_hashes: list[str],
) -> dict[str, Any]:
    if not all([defect, root_cause, repair, retest_result]) or not evidence_hashes:
        raise ValueError("COMPLETE_LEARNING_RECORD_REQUIRED")
    row = {
        "schema": "ivdivo.business.self_improvement_candidate/1.0",
        "defect": defect,
        "root_cause": root_cause,
        "repair": repair,
        "retest_result": retest_result,
        "evidence_hashes": sorted(set(evidence_hashes)),
        "authority": "CANDIDATE_ONLY",
        "auto_promote": False,
    }
    row["candidate_hash"] = canonical_hash(row)
    return row
