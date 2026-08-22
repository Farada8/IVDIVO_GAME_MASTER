"""Business Engineering OS — class-specific real-market evidence lineage.

Extends the controlling Cycle5 PA0–PA5 public-artifact engine. It does not
acquire buyers, send outreach, authorize pricing, or manufacture market proof.
Its only job is to bind future real target-user decision use (PA5/E3) and real
money/deposit/PO evidence (E4) to the exact artifact that was actually tested.
"""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
import hashlib
import json
from typing import Any

from public_artifact_engine import PA_ORDER, Artifact, validate_artifact

BUYER_SCHEMA = "ivdivo.business.buyer_decision_receipt/1.0"
MONEY_SCHEMA = "ivdivo.business.money_receipt/1.0"

FORBIDDEN_CALLER_TRUTH_FIELDS = {
    "verified",
    "buyer_confirmed",
    "market_validated",
    "willingness_to_pay_proven",
    "payment_verified",
    "profitability_proven",
    "winner",
}


def canonical_hash(value: Any) -> str:
    if is_dataclass(value):
        value = asdict(value)
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def artifact_fingerprint(artifact: Artifact) -> str:
    """Stable hash of the exact artifact object used in an external test."""
    errors = validate_artifact(artifact)
    if errors:
        raise ValueError(f"ARTIFACT_INVALID:{','.join(errors)}")
    return canonical_hash(artifact)


def _valid_iso_time(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _caller_truth_hits(receipt: dict[str, Any]) -> list[str]:
    return sorted(field for field in FORBIDDEN_CALLER_TRUTH_FIELDS if receipt.get(field) is not None)


def validate_buyer_decision_receipt(
    receipt: dict[str, Any] | None,
    *,
    artifact_hash: str,
    artifact_id: str,
) -> dict[str, Any]:
    """Validate real target-user decision use. PASS is PA5/E3 evidence, not E4."""
    if receipt is None:
        return {
            "status": "HOLD_NO_REAL_TARGET_USER_DECISION_USE",
            "verified": False,
            "pa_grade": "PA4_OR_LOWER",
            "market_grade": "E2+_OR_LOWER",
        }

    caller_truth = _caller_truth_hits(receipt)
    if caller_truth:
        return {
            "status": "FAIL_CALLER_BOOLEAN_OR_LABEL_AS_EVIDENCE",
            "verified": False,
            "forbidden_fields": caller_truth,
        }

    required = (
        "schema",
        "evidence_class",
        "source_type",
        "receipt_id",
        "artifact_hash",
        "artifact_id",
        "observed_at",
        "buyer_role",
        "decision_use",
        "interaction_outcome",
    )
    missing = sorted(field for field in required if receipt.get(field) in (None, ""))
    if missing:
        return {"status": "FAIL_BUYER_RECEIPT_INCOMPLETE", "verified": False, "missing": missing}

    if receipt.get("schema") != BUYER_SCHEMA:
        return {"status": "FAIL_BUYER_RECEIPT_SCHEMA", "verified": False}
    if receipt.get("evidence_class") != "BUYER_DECISION_USE" or receipt.get("source_type") != "REAL_HUMAN":
        return {"status": "FAIL_WRONG_OR_SYNTHETIC_BUYER_EVIDENCE_CLASS", "verified": False}
    if receipt.get("artifact_hash") != artifact_hash or receipt.get("artifact_id") != artifact_id:
        return {"status": "FAIL_BUYER_ARTIFACT_LINEAGE", "verified": False}
    if not _valid_iso_time(receipt.get("observed_at")):
        return {"status": "FAIL_BUYER_OBSERVED_AT", "verified": False}
    if receipt.get("decision_use") not in {"USED", "CHANGED", "REJECTED"}:
        return {"status": "FAIL_BUYER_DECISION_USE_CLASS", "verified": False}

    sealed = dict(receipt)
    sealed["receipt_hash"] = canonical_hash(receipt)
    return {
        "status": "PASS_PA5_E3_REAL_DECISION_USE",
        "verified": True,
        "pa_grade": "PA5",
        "market_grade": "E3",
        "artifact_hash": artifact_hash,
        "artifact_id": artifact_id,
        "receipt_hash": sealed["receipt_hash"],
        "willingness_to_pay_proven": False,
        "payment_proven": False,
        "profitability_proven": False,
    }


def validate_money_receipt(
    receipt: dict[str, Any] | None,
    *,
    artifact_hash: str,
    artifact_id: str,
    buyer_receipt_hash: str,
) -> dict[str, Any]:
    """Validate real money/deposit/PO evidence bound to artifact and buyer lineage."""
    if receipt is None:
        return {"status": "HOLD_NO_REAL_MONEY_DEPOSIT_OR_PO", "verified": False, "market_grade": "E3_OR_LOWER"}

    caller_truth = _caller_truth_hits(receipt)
    if caller_truth:
        return {
            "status": "FAIL_CALLER_BOOLEAN_OR_LABEL_AS_EVIDENCE",
            "verified": False,
            "forbidden_fields": caller_truth,
        }

    required = (
        "schema",
        "evidence_class",
        "source_type",
        "receipt_id",
        "artifact_hash",
        "artifact_id",
        "buyer_receipt_hash",
        "observed_at",
        "transaction_or_po_id",
        "amount",
        "currency",
    )
    missing = sorted(field for field in required if receipt.get(field) in (None, ""))
    if missing:
        return {"status": "FAIL_MONEY_RECEIPT_INCOMPLETE", "verified": False, "missing": missing}

    if receipt.get("schema") != MONEY_SCHEMA:
        return {"status": "FAIL_MONEY_RECEIPT_SCHEMA", "verified": False}
    if receipt.get("evidence_class") not in {"PAYMENT", "DEPOSIT", "PURCHASE_ORDER"} or receipt.get("source_type") != "REAL_TRANSACTION":
        return {"status": "FAIL_WRONG_OR_SYNTHETIC_MONEY_EVIDENCE_CLASS", "verified": False}
    if receipt.get("artifact_hash") != artifact_hash or receipt.get("artifact_id") != artifact_id:
        return {"status": "FAIL_MONEY_ARTIFACT_LINEAGE", "verified": False}
    if receipt.get("buyer_receipt_hash") != buyer_receipt_hash:
        return {"status": "FAIL_MONEY_BUYER_LINEAGE", "verified": False}
    if not _valid_iso_time(receipt.get("observed_at")):
        return {"status": "FAIL_MONEY_OBSERVED_AT", "verified": False}
    try:
        amount = float(receipt.get("amount"))
    except (TypeError, ValueError):
        return {"status": "FAIL_MONEY_AMOUNT", "verified": False}
    if amount <= 0:
        return {"status": "FAIL_MONEY_AMOUNT", "verified": False}
    currency = str(receipt.get("currency", "")).upper()
    if len(currency) != 3 or not currency.isalpha():
        return {"status": "FAIL_MONEY_CURRENCY", "verified": False}

    return {
        "status": "PASS_E4_REAL_MONEY_OBSERVED",
        "verified": True,
        "market_grade": "E4",
        "artifact_hash": artifact_hash,
        "artifact_id": artifact_id,
        "buyer_receipt_hash": buyer_receipt_hash,
        "receipt_hash": canonical_hash(receipt),
        "amount": amount,
        "currency": currency,
        "repeatability_proven": False,
        "unit_economics_proven": False,
        "profitability_proven": False,
    }


def route_market_evidence(
    artifact: Artifact,
    *,
    buyer_receipt: dict[str, Any] | None = None,
    money_receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Route only; never sends outreach or authorizes an external action."""
    errors = validate_artifact(artifact)
    if errors:
        return {"status": "HOLD_ARTIFACT_INVALID", "errors": errors, "external_action_authorized": False}

    artifact_hash = artifact_fingerprint(artifact)
    if PA_ORDER.get(artifact.pa_grade, -1) < PA_ORDER["PA4"]:
        return {
            "status": "PA4_INDEPENDENT_VALIDATION_REQUIRED",
            "artifact_id": artifact.artifact_id,
            "artifact_hash": artifact_hash,
            "current_pa_grade": artifact.pa_grade,
            "current_market_grade": artifact.market_claim_grade,
            "external_action_authorized": False,
        }

    buyer = validate_buyer_decision_receipt(
        buyer_receipt,
        artifact_hash=artifact_hash,
        artifact_id=artifact.artifact_id,
    )
    if buyer.get("verified") is not True:
        return {
            "status": "REAL_TARGET_USER_DECISION_USE_REQUIRED",
            "artifact_id": artifact.artifact_id,
            "artifact_hash": artifact_hash,
            "current_pa_grade": artifact.pa_grade,
            "current_market_grade": artifact.market_claim_grade,
            "buyer_gate": buyer,
            "external_action_authorized": False,
        }

    money = validate_money_receipt(
        money_receipt,
        artifact_hash=artifact_hash,
        artifact_id=artifact.artifact_id,
        buyer_receipt_hash=buyer["receipt_hash"],
    )
    if money.get("verified") is not True:
        return {
            "status": "PA5_E3_OBSERVED_E4_NOT_PROVEN",
            "artifact_id": artifact.artifact_id,
            "artifact_hash": artifact_hash,
            "current_pa_grade": "PA5",
            "current_market_grade": "E3",
            "buyer_gate": buyer,
            "money_gate": money,
            "external_action_authorized": False,
        }

    return {
        "status": "E4_REAL_MONEY_OBSERVED_MEASUREMENT_REQUIRED",
        "artifact_id": artifact.artifact_id,
        "artifact_hash": artifact_hash,
        "current_pa_grade": "PA5",
        "current_market_grade": "E4",
        "buyer_gate": buyer,
        "money_gate": money,
        "next_internal_action": "MEASURE_DELIVERY_COST_TIME_ACCEPTANCE_AND_UNIT_ECONOMICS",
        "external_action_authorized": False,
    }
