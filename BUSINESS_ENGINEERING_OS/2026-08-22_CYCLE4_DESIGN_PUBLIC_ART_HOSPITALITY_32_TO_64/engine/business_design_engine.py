from typing import Any, Dict, List

UNKNOWN = {None, "", "UNKNOWN", "TBD"}

def _is_unknown(v):
    if isinstance(v, (list, tuple, set, dict)):
        return len(v) == 0
    return v in UNKNOWN

def source_state(raw_confirmed: bool, derived_confirmed: bool=False, corrupt: bool=False):
    if corrupt: return "QUARANTINED"
    if raw_confirmed: return "CONFIRMED_RAW"
    if derived_confirmed: return "CONFIRMED_DERIVED"
    return "PLANNED_NOT_CONFIRMED_UPLOADED"

def source_adequacy(required: List[str], payload: Dict[str, Any], source_role: str):
    missing=[x for x in required if _is_unknown(payload.get(x))]
    if not missing: return {"status":"ADEQUATE","missing":[]}
    if source_role in {"ROUTING_SUMMARY","CONCEPT_NOTE","EARLY_BRIEF"}:
        return {"status":"INSUFFICIENT_SOURCE_NOT_PROJECT_DEFECT","missing":missing}
    return {"status":"MISSING_REQUIRED_PROJECT_DATA","missing":missing}

def site_context_gate(p):
    req=["site_id","location","site_type","dimensions_state","ownership_or_access_state","climate_exposure","heritage_state","public_access","stakeholders"]
    q=source_adequacy(req,p,p.get("source_role","EARLY_BRIEF"))
    if q["status"]!="ADEQUATE": return q
    if p["ownership_or_access_state"] not in {"CONFIRMED","PERMISSION_PENDING"}:
        return {"status":"SITE_AUTHORITY_HOLD"}
    return {"status":"SITE_CONTEXT_READY"}

def design_brief_gate(p):
    req=["objective","users","site_ref","programme","constraints","deliverables","exclusions"]
    q=source_adequacy(req,p,p.get("source_role","DESIGN_BRIEF"))
    if q["status"]!="ADEQUATE": return q
    if "unknowns" not in p:
        return {"status":"MISSING_REQUIRED_PROJECT_DATA","missing":["unknowns"],"source_role":p.get("source_role","DESIGN_BRIEF")}
    return {"status":"BRIEF_READY"}

def composition_gate(p):
    req=["dominant","subordinate","focal_path","value_structure","distance"]
    q=source_adequacy(req,p,p.get("source_role","COMPOSITION_STUDY"))
    if q["status"]!="ADEQUATE": return q
    if p["dominant"] == p["subordinate"]: return {"status":"FLAT_HIERARCHY_RISK"}
    return {"status":"COMPOSITION_READY"}

def distance_readability(p):
    if p.get("distance_m") in UNKNOWN or p.get("critical_feature_size_mm") in UNKNOWN:
        return {"status":"DISTANCE_DATA_REQUIRED"}
    if p["distance_m"] <= 0 or p["critical_feature_size_mm"] <= 0:
        return {"status":"INVALID_GEOMETRY"}
    ratio=p["critical_feature_size_mm"]/(p["distance_m"]*1000)
    return {"status":"READABILITY_PROXY_PASS" if ratio>=0.002 else "READABILITY_PROXY_RISK",
            "proxy_ratio":round(ratio,6),"evidence_ceiling":"ENGINEERING_PROXY_NOT_HUMAN_VIEWING"}

def prompt_compile(p):
    protected=p.get("protected_unknowns",[])
    text=" | ".join([
        f"objective:{p.get('objective','')}", f"site:{p.get('site','')}", f"users:{p.get('users','')}",
        f"composition:{p.get('composition','')}", f"materials:{p.get('materials','TBD')}",
        f"constraints:{p.get('constraints','')}", f"DO_NOT_INVENT:{','.join(protected)}"])
    return {"status":"PROMPT_COMPILED","prompt":text}

def mural_surface_gate(p):
    req=["substrate","moisture_state","uv_exposure","wind_exposure","prep_system","access_method","coating_system","maintenance_plan"]
    q=source_adequacy(req,p,p.get("source_role","TECHNICAL_SURVEY"))
    if q["status"]!="ADEQUATE": return q
    if p["moisture_state"]=="UNRESOLVED": return {"status":"MURAL_TECHNICAL_HOLD","reason":"MOISTURE_UNRESOLVED"}
    return {"status":"MURAL_TECHNICAL_READY_FOR_SPECIALIST_REVIEW"}

def sculpture_gate(p):
    req=["material","height_or_mass_state","foundation_state","structural_review_state","public_contact","maintenance_plan"]
    q=source_adequacy(req,p,p.get("source_role","TECHNICAL_SURVEY"))
    if q["status"]!="ADEQUATE": return q
    if p["structural_review_state"]!="CONFIRMED": return {"status":"STRUCTURAL_REVIEW_REQUIRED"}
    return {"status":"SCULPTURE_TECHNICAL_READY"}

def hospitality_flow(p):
    req=["guest_path","service_path","delivery_path","waste_path","accessible_path","capacity_state"]
    q=source_adequacy(req,p,p.get("source_role","FLOW_PLAN"))
    if q["status"]!="ADEQUATE": return q
    collisions=set(p["guest_path"]) & set(p["service_path"])
    bad=[x for x in collisions if x not in set(p.get("shared_allowed",[]))]
    return {"status":"FLOW_CONFLICT" if bad else "FLOW_READY","conflicts":sorted(bad)}

def material_lifecycle(p):
    req=["material","environment","maintenance_interval","replacement_method","failure_modes"]
    q=source_adequacy(req,p,p.get("source_role","MATERIAL_SCHEDULE"))
    if q["status"]!="ADEQUATE": return q
    return {"status":"LIFECYCLE_REGISTERED"}

def buildability_gate(p):
    req=["fabrication","transport","site_access","installation","inspection","maintenance_access"]
    q=source_adequacy(req,p,p.get("source_role","TECHNICAL_PACKAGE"))
    if q["status"]!="ADEQUATE": return q
    return {"status":"BUILDABILITY_READY_FOR_SPECIALIST_REVIEW"}

def cost_band(p):
    required=["quantity_basis","unit_cost_low","unit_cost_high","contingency_pct"]
    q=source_adequacy(required,p,p.get("source_role","COST_ASSUMPTIONS"))
    if q["status"]!="ADEQUATE": return q
    qty=float(p["quantity_basis"]); lo=float(p["unit_cost_low"])*qty; hi=float(p["unit_cost_high"])*qty
    cont=float(p["contingency_pct"])/100.0
    return {"status":"ASSUMPTION_BANDED_COST","low":round(lo*(1+cont),2),"high":round(hi*(1+cont),2),"evidence_ceiling":"ASSUMPTION_RANGE_NOT_QUOTE"}

def commission_route(p):
    req=["buyer_class","procurement_route","approval_chain","required_evidence"]
    q=source_adequacy(req,p,p.get("source_role","MARKET_ROUTE"))
    if q["status"]!="ADEQUATE": return q
    return {"status":"COMMISSION_ROUTE_MAPPED","buyer_intent_claimed":False}

def public_signal_gate(p):
    grade=p.get("e_grade","E0")
    if grade in {"E3","E4","E5","E6","E7"} and not p.get("direct_buyer_or_money_evidence"):
        return {"status":"EVIDENCE_LAUNDERING_BLOCKED"}
    return {"status":"PUBLIC_SIGNAL_ACCEPTED","market_ceiling":grade}

def offer_package(p):
    req=["scope","deliverables","assumptions","exclusions","price_basis_state","evidence_state"]
    q=source_adequacy(req,p,p.get("source_role","OFFER"))
    if q["status"]!="ADEQUATE": return q
    return {"status":"OFFER_READY_FOR_REVIEW"}

def red_team(p):
    fatal=[]; major=[]; medium=[]
    if not p.get("site_authority"): fatal.append("SITE_AUTHORITY_UNKNOWN")
    if p.get("technical_maturity_claimed") and not p.get("technical_review"): fatal.append("TECHNICAL_PROOF_MISSING")
    if p.get("buyer_demand_claimed") and not p.get("buyer_evidence"): major.append("BUYER_EVIDENCE_MISSING")
    if p.get("cost_point_estimate") and not p.get("cost_assumptions"): major.append("FAKE_COST_PRECISION")
    if not p.get("maintenance_path"): medium.append("MAINTENANCE_UNBOUND")
    return {"status":"NO_GO" if fatal or major else "PASS_WITH_WATCHES","fatal":fatal,"major":major,"medium":medium}

def self_improvement_observation(p):
    req=["project_id","defect_or_success","root_cause","evidence_ref","repeat_count","proposed_mechanism"]
    q=source_adequacy(req,p,"LEARNING_RECORD")
    if q["status"]!="ADEQUATE": return q
    if p["repeat_count"] < 2: return {"status":"CAPTURE_ONLY_NOT_ENGINE_CANDIDATE"}
    return {"status":"CANDIDATE_FOR_SELF_IMPROVEMENT_REVIEW","auto_promote":False}
