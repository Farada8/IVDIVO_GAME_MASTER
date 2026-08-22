from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

LEGAL_STATES = {"UNKNOWN", "IN_SCOPE_VERIFIED", "OUT_OF_SCOPE_VERIFIED"}
CORE_PREFLIGHT_FIELDS = {
    "unique_product_identifier",
    "product_name",
    "manufacturer_name",
    "dpp_data_location",
}
CANDIDATE_LEGAL_FIELDS = {
    "manufacturer_unique_operator_identifier",
    "gtin_or_equivalent",
    "commodity_code",
    "compliance_document_refs",
    "facility_identifier",
    "dpp_service_provider_ref",
}

@dataclass(frozen=True)
class Finding:
    field: str
    outcome: str
    data_state: str
    requiredness_state: str
    message: str

def _is_missing(value: Any) -> bool:
    if value is None or value == "" or value == [] or value == {}:
        return True
    if isinstance(value, dict):
        return any(v in (None, "", [], {}) for v in value.values())
    return False

def validate_record(record: dict[str, Any], legal_applicability: str) -> dict[str, Any]:
    if legal_applicability not in LEGAL_STATES:
        raise ValueError(f"unsupported legal_applicability={legal_applicability!r}")
    sources = {x.get("source_ref") for x in record.get("source_records", []) if x.get("source_ref")}
    fields = record.get("candidate_fields") or {}
    findings: list[Finding] = []
    for name, block in fields.items():
        block = block or {}
        value = block.get("value")
        source_ref = block.get("source_ref")
        synthetic = bool(block.get("synthetic"))
        missing = _is_missing(value)
        if missing:
            if name in CORE_PREFLIGHT_FIELDS:
                findings.append(Finding(name, "GAP", "MISSING_SUPPLIER_DATA", "TECHNICAL_PREFLIGHT_CORE", "Core preflight datum is missing."))
            elif name in CANDIDATE_LEGAL_FIELDS:
                findings.append(Finding(name, "HOLD", "MISSING_SUPPLIER_DATA", "LEGAL_REQUIREDNESS_UNKNOWN", "Datum is unavailable; whether it is legally required depends on applicable product rules."))
            else:
                findings.append(Finding(name, "GAP", "MISSING_SUPPLIER_DATA", "PRODUCT_DATA_READINESS", "Supplier/product datum is incomplete."))
            continue
        if not source_ref:
            findings.append(Finding(name, "ERROR", "PRESENT_WITHOUT_SOURCE", "UNVERIFIED", "Populated datum has no source_ref."))
            continue
        if source_ref not in sources:
            findings.append(Finding(name, "ERROR", "SOURCE_REF_NOT_FOUND", "UNVERIFIED", f"source_ref {source_ref!r} is not declared in source_records."))
            continue
        data_state = "PRESENT_SYNTHETIC_ONLY" if synthetic else "PRESENT_WITH_SOURCE"
        requiredness = "LEGAL_REQUIREDNESS_UNKNOWN" if name in CANDIDATE_LEGAL_FIELDS and legal_applicability == "UNKNOWN" else "TECHNICAL_DATA_AVAILABLE"
        findings.append(Finding(name, "PASS", data_state, requiredness, "Datum is traceable to a declared source; legal requiredness is evaluated separately."))
    for core in sorted(CORE_PREFLIGHT_FIELDS - fields.keys()):
        findings.append(Finding(core, "GAP", "MISSING_SUPPLIER_DATA", "TECHNICAL_PREFLIGHT_CORE", "Core preflight field absent from candidate_fields."))
    registry = record.get("registry_metadata") or {}
    if registry.get("full_dpp_payload") not in (None, {}, []):
        findings.append(Finding("registry_metadata.full_dpp_payload", "ERROR", "REGISTRY_OVERPACKED", "ARCHITECTURE", "Registry metadata must not embed the full decentralised DPP dataset."))
    else:
        findings.append(Finding("registry_metadata.full_dpp_payload", "PASS", "HIGH_LEVEL_METADATA_ONLY", "ARCHITECTURE", "Registry view remains separated from detailed decentralised DPP data."))
    if registry.get("unique_product_identifier") != (fields.get("unique_product_identifier") or {}).get("value"):
        findings.append(Finding("registry_metadata.unique_product_identifier", "ERROR", "IDENTIFIER_MISMATCH", "ARCHITECTURE", "Registry identifier does not match product preflight identifier."))
    errors = [f for f in findings if f.outcome == "ERROR"]
    gaps = [f for f in findings if f.outcome == "GAP"]
    holds = [f for f in findings if f.outcome == "HOLD"]
    if errors:
        disposition = "INVALID_PREFLIGHT"
    elif legal_applicability == "OUT_OF_SCOPE_VERIFIED":
        disposition = "TECHNICAL_DATA_MAP_ONLY_OUT_OF_SCOPE_VERIFIED"
    elif legal_applicability == "UNKNOWN":
        disposition = "TECHNICAL_PREFLIGHT_COMPLETE_LEGAL_SCOPE_UNKNOWN"
    elif holds:
        disposition = "IN_SCOPE_PRODUCT_RULE_REQUIREDNESS_UNRESOLVED"
    elif gaps:
        disposition = "IN_SCOPE_TECHNICAL_GAPS_REMAIN"
    else:
        disposition = "READY_FOR_REGISTRY_TEST_NOT_PRODUCTION"
    return {
        "schema": "ivdivo.dpp.supplier_data_preflight_result/0.1",
        "disposition": disposition,
        "legal_applicability": legal_applicability,
        "counts": {"PASS": sum(f.outcome == "PASS" for f in findings), "GAP": len(gaps), "HOLD": len(holds), "ERROR": len(errors)},
        "missing_supplier_data": sorted(f.field for f in findings if f.data_state == "MISSING_SUPPLIER_DATA"),
        "findings": [asdict(f) for f in findings],
        "proof_boundary": {"legal_dpp_applicability_proven": legal_applicability != "UNKNOWN", "registry_production_submission_proven": False, "conformity_proven": False, "buyer_demand_proven": False, "wtp_proven": False},
    }

def compare_correction(fixture: dict[str, Any]) -> dict[str, Any]:
    legal = fixture.get("legal_applicability", "UNKNOWN")
    initial = validate_record(fixture["initial"], legal)
    corrected = validate_record(fixture["corrected"], legal)
    before = set(initial["missing_supplier_data"])
    after = set(corrected["missing_supplier_data"])
    closed = sorted(before - after)
    introduced = sorted(after - before)
    return {
        "schema": "ivdivo.dpp.correction_loop/0.1",
        "fixture_id": fixture.get("fixture_id"),
        "initial": initial,
        "corrected": corrected,
        "closed_missing_data_gaps": closed,
        "new_missing_data_gaps": introduced,
        "closed_count": len(closed),
        "engineering_pass": len(closed) >= 2 and corrected["counts"]["ERROR"] == 0 and corrected["legal_applicability"] == "UNKNOWN" and corrected["disposition"] == "TECHNICAL_PREFLIGHT_COMPLETE_LEGAL_SCOPE_UNKNOWN",
        "proof_boundary": {"correction_loop_is_legal_compliance_proof": False, "correction_loop_is_registry_acceptance_proof": False, "technical_data_delta_proven_on_synthetic_fixture": len(closed) >= 2},
    }

def main(path: str) -> int:
    fixture = json.loads(Path(path).read_text())
    result = compare_correction(fixture)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["engineering_pass"] else 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validator.py FIXTURE.json")
    raise SystemExit(main(sys.argv[1]))
