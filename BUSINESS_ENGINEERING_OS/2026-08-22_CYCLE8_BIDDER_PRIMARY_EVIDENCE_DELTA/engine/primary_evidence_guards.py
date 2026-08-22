from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class RegistryScreenResult:
    registration_number_proven: bool
    screen_status: str | None
    current_status_authorized: bool
    freshness: str


def classify_registry_screen(
    *,
    registration_number: str | None,
    screen_status: str | None,
    capture_timestamp: str | None,
    embedded_latest_event_date: str | None,
) -> RegistryScreenResult:
    """An official-interface screen may bind displayed fields, but current status needs freshness."""
    number_proven = bool(registration_number)
    current_status_authorized = bool(screen_status and capture_timestamp)
    if capture_timestamp:
        freshness = "TIMESTAMPED_SCREEN_EVIDENCE"
    elif embedded_latest_event_date:
        freshness = "LOWER_BOUND_ONLY_CURRENTNESS_UNVERIFIED"
    else:
        freshness = "CURRENTNESS_UNVERIFIED"
    return RegistryScreenResult(
        registration_number_proven=number_proven,
        screen_status=screen_status,
        current_status_authorized=current_status_authorized,
        freshness=freshness,
    )


@dataclass(frozen=True)
class TaxEvidenceResult:
    registration_evidence_present: bool
    historical_account_state_present: bool
    tax_clearance_proven: bool
    current_balance_authorized: bool


def classify_tax_evidence(
    *,
    registration_evidence_present: bool,
    statement_timestamp: str | None,
    historical_balance_observed: bool,
    tax_clearance_certificate_present: bool,
) -> TaxEvidenceResult:
    return TaxEvidenceResult(
        registration_evidence_present=registration_evidence_present,
        historical_account_state_present=bool(statement_timestamp and historical_balance_observed),
        tax_clearance_proven=tax_clearance_certificate_present,
        current_balance_authorized=False,
    )


@dataclass(frozen=True)
class DeliveryRecordResult:
    delivery_record_present: bool
    payment_proven: bool
    third_party_completion_proven: bool
    evidence_class: str


def classify_seller_invoice(
    *,
    invoice_number: str | None,
    work_scope_present: bool,
    independent_payment_receipt: bool = False,
    client_completion_corroboration: bool = False,
) -> DeliveryRecordResult:
    present = bool(invoice_number and work_scope_present)
    return DeliveryRecordResult(
        delivery_record_present=present,
        payment_proven=bool(present and independent_payment_receipt),
        third_party_completion_proven=bool(present and client_completion_corroboration),
        evidence_class=(
            "THIRD_PARTY_CORROBORATED_DELIVERY"
            if present and client_completion_corroboration
            else "SELF_ISSUED_DELIVERY_RECORD"
            if present
            else "NO_DELIVERY_RECORD"
        ),
    )


def dedupe_invoice_families(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Same invoice number is one evidence family; conflicting periods are a version conflict."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        invoice_number = row.get("invoice_number")
        if not invoice_number:
            continue
        grouped.setdefault(str(invoice_number), []).append(row)

    conflicts: list[str] = []
    for invoice_number, versions in grouped.items():
        periods = {v.get("work_period") for v in versions if v.get("work_period")}
        if len(periods) > 1:
            conflicts.append(invoice_number)
    return {
        "family_count": len(grouped),
        "version_conflicts": sorted(conflicts),
        "double_count_allowed": False,
    }


def bidder_designation_authorized(*, explicit_case_designation: bool) -> bool:
    return bool(explicit_case_designation)


def public_derivative_redaction_ok(payload: dict[str, Any]) -> bool:
    """Reject public derivatives that expose common private fields."""
    forbidden = {
        "iban",
        "bic",
        "swift",
        "client_email",
        "client_phone",
        "client_pps",
        "tax_registration_number",
        "exact_site_address",
    }
    keys = {str(k).lower() for k in payload.keys()}
    return not bool(keys & forbidden)


def target_bid_decision_authorized(
    *,
    target_pack_complete: bool,
    explicit_bidder_designation: bool,
    supplier_packet_complete: bool,
) -> bool:
    return bool(target_pack_complete and explicit_bidder_designation and supplier_packet_complete)
