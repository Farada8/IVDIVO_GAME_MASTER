from dataclasses import dataclass, asdict
from typing import Any, Dict, List

PASS="PASS"; FAIL="FAIL"; UNKNOWN="UNKNOWN"; NOT_APPLICABLE="NOT_APPLICABLE"
ALLOWED_APPLICABILITY={"KNOWN_IN_SCOPE","KNOWN_NOT_YET_IN_SCOPE","UNKNOWN"}

@dataclass(frozen=True)
class Finding:
    rule_id: str
    plane: str
    status: str
    message: str
    chase_owner: str | None = None

def _finding(rule_id, plane, status, message, chase_owner=None):
    return Finding(rule_id, plane, status, message, chase_owner)

def _state(value: Any) -> str:
    if value is None: return "UNKNOWN"
    if isinstance(value, str): return "PRESENT" if value.strip() else "MISSING"
    if value is True: return "PRESENT"
    if value is False: return "MISSING"
    if isinstance(value, (list, dict)): return "PRESENT" if value else "MISSING"
    return "PRESENT"

def _required(case: Dict[str, Any], key: str, plane: str, rule_id: str, owner: str) -> Finding:
    s=_state(case.get(key))
    if s=="PRESENT": return _finding(rule_id, plane, PASS, f"{key} present")
    if s=="UNKNOWN": return _finding(rule_id, plane, UNKNOWN, f"{key} unresolved", owner)
    return _finding(rule_id, plane, FAIL, f"{key} missing", owner)

def validate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    case_id=case.get("case_id") or "UNNAMED"
    applicability=case.get("applicability_status", "UNKNOWN")
    if applicability not in ALLOWED_APPLICABILITY:
        raise ValueError("invalid applicability_status")

    findings: List[Finding]=[]
    findings.append(_required(case,"applicable_legal_basis","APPLICABILITY","DPP-A01","LEGAL_SCOPE_OWNER"))
    findings.append(_required(case,"product_group","APPLICABILITY","DPP-A02","PRODUCT_OWNER"))
    findings.append(_required(case,"economic_operator_id","OPERATOR","DPP-O01","ECONOMIC_OPERATOR"))
    findings.append(_required(case,"economic_operator_role","OPERATOR","DPP-O02","ECONOMIC_OPERATOR"))
    findings.append(_required(case,"product_identifier","IDENTITY","DPP-I01","PRODUCT_OWNER"))

    imported=case.get("imported_to_eu")
    if imported is True:
        findings.append(_required(case,"commodity_code","IDENTITY","DPP-I02","TRADE_COMPLIANCE"))
    elif imported is None:
        findings.append(_finding("DPP-I02","IDENTITY",UNKNOWN,"import status unresolved; commodity-code requirement cannot be routed","TRADE_COMPLIANCE"))
    else:
        findings.append(_finding("DPP-I02","IDENTITY",NOT_APPLICABLE,"fixture is not imported"))

    findings.append(_required(case,"data_carrier_type","LINKAGE","DPP-L01","PRODUCT_OWNER"))
    findings.append(_required(case,"decentralised_dpp_location","LINKAGE","DPP-L02","DATA_OWNER"))

    records=case.get("supplier_records")
    if records is None:
        findings.append(_finding("DPP-S01","SUPPLIER_EVIDENCE",UNKNOWN,"supplier record set unresolved","SUPPLY_CHAIN"))
    elif not records:
        findings.append(_finding("DPP-S01","SUPPLIER_EVIDENCE",FAIL,"supplier record set empty","SUPPLY_CHAIN"))
    else:
        bad=[]
        for i, record in enumerate(records):
            if not isinstance(record, dict):
                bad.append(f"record_{i}:invalid")
                continue
            for key in ("supplier_id","data_point","value","source_evidence","freshness_date"):
                if _state(record.get(key)) != "PRESENT":
                    bad.append(f"record_{i}:{key}")
        if bad:
            findings.append(_finding("DPP-S01","SUPPLIER_EVIDENCE",FAIL,"supplier evidence incomplete: "+",".join(bad),"SUPPLY_CHAIN"))
        else:
            findings.append(_finding("DPP-S01","SUPPLIER_EVIDENCE",PASS,f"{len(records)} supplier evidence records complete"))

    expected=case.get("fixture_required_data_points")
    mapped=case.get("mapped_data_points")
    if expected is None:
        findings.append(_finding("DPP-D01","DATA_MAPPING",UNKNOWN,"fixture-required data points unresolved","LEGAL_SCOPE_OWNER"))
    elif mapped is None:
        findings.append(_finding("DPP-D01","DATA_MAPPING",UNKNOWN,"mapped data points unresolved","DATA_OWNER"))
    else:
        missing=sorted(set(expected)-set(mapped))
        if missing:
            findings.append(_finding("DPP-D01","DATA_MAPPING",FAIL,"unmapped fixture data points: "+",".join(missing),"DATA_OWNER"))
        else:
            findings.append(_finding("DPP-D01","DATA_MAPPING",PASS,"all fixture-required data points mapped"))

    if case.get("registry_generated_uri_before_registration"):
        findings.append(_finding("DPP-R01","REGISTRY_BOUNDARY",FAIL,"registry-generated identifier cannot be claimed before registration","IMPLEMENTATION_OWNER"))
    else:
        findings.append(_finding("DPP-R01","REGISTRY_BOUNDARY",PASS,"no pre-registration Registry URI fabricated"))

    if applicability=="UNKNOWN":
        disposition="HOLD_APPLICABILITY_UNKNOWN"
    elif applicability=="KNOWN_NOT_YET_IN_SCOPE":
        disposition="PREP_ONLY_NOT_CURRENT_LEGAL_REQUIREMENT"
    elif any(f.status==FAIL for f in findings):
        disposition="HOLD_DATA_GAPS"
    elif any(f.status==UNKNOWN for f in findings):
        disposition="HOLD_UNRESOLVED_EVIDENCE"
    else:
        disposition="READY_FOR_TEST_ENVIRONMENT_PREFLIGHT"

    chase=[{"rule_id":f.rule_id,"plane":f.plane,"owner":f.chase_owner,"message":f.message} for f in findings if f.status in {FAIL,UNKNOWN}]
    return {
        "schema":"ivdivo.dpp.preflight_result/0.1",
        "case_id":case_id,
        "applicability_status":applicability,
        "disposition":disposition,
        "findings":[asdict(f) for f in findings],
        "gap_count":len(chase),
        "chase_list":chase,
        "registry_submission_performed":False,
        "registry_registration_proven":False,
        "legal_applicability_proven_by_tool":False,
        "legal_compliance_proven":False,
        "buyer_demand_proven":False,
        "wtp_proven":False,
        "transaction_proven":False,
        "external_action_authorized":False
    }

def revalidate(before: Dict[str, Any], corrected: Dict[str, Any]) -> Dict[str, Any]:
    a=validate_case(before); b=validate_case(corrected)
    return {
        "before_case_id":a["case_id"],
        "after_case_id":b["case_id"],
        "before_gap_count":a["gap_count"],
        "after_gap_count":b["gap_count"],
        "gap_delta":a["gap_count"]-b["gap_count"],
        "before_disposition":a["disposition"],
        "after_disposition":b["disposition"],
        "implementation_delta_observed":b["gap_count"] < a["gap_count"],
        "market_proof_promotion":False
    }

def validate_many(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [validate_case(c) for c in cases]
