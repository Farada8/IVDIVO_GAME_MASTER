#!/usr/bin/env python3
"""IVDIVO Story Mechanism Intelligence v0.1 candidate.

Additive story-domain layer above Book Intelligence. Consumes normalized mechanism
cards; it does not ingest/redistribute raw books, decide canon, reopen locked text,
or claim literary quality from predicted routing vectors.
"""
from __future__ import annotations
import copy, hashlib, itertools, json, re
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

ALLOWED_STAGES={"DISCOVERY","ARCHITECTURE","CHAPTER_MAP","SCENE","DRAFT","DEVELOPMENT","RED_TEAM","REVISION","LOCKED_SHADOW"}
EVIDENCE_RANK={"CURRENT":6,"PROMOTABLE":5,"PILOT_READY":4,"LOCAL_TEST":3,"REFERENCE_ONLY":2,"HOLD":1,"REJECT":0}
SEVERITIES={"POLISH","MEDIUM","MAJOR","FATAL"}

def _norm_token(v:Any)->str:
    t=re.sub(r"\s+","_",str(v).strip().upper())
    return re.sub(r"[^A-Z0-9А-ЯЁ_-]+","",t)

def _norm_set(values:Iterable[Any])->List[str]:
    return sorted({t for t in (_norm_token(v) for v in values or []) if t})

def normalize_problem_signature(s:Mapping[str,Any])->Dict[str,Any]:
    out={"project_id":str(s.get("project_id","")).strip(),"stage":str(s.get("stage","")).strip().upper(),"genre_tags":_norm_set(s.get("genre_tags",[])),"problem_tags":_norm_set(s.get("problem_tags",[])),"desired_effects":_norm_set(s.get("desired_effects",[])),"hard_constraints":_norm_set(s.get("hard_constraints",[])),"available_conditions":_norm_set(s.get("available_conditions",[])),"protected_facts":sorted({str(x).strip() for x in s.get("protected_facts",[]) if str(x).strip()}),"forbidden_moves":_norm_set(s.get("forbidden_moves",[])),"max_mechanisms":int(s.get("max_mechanisms",3)),"locked":bool(s.get("locked",False))}
    if out["locked"]: out["stage"]="LOCKED_SHADOW"
    return out

def validate_problem_signature(s:Mapping[str,Any])->List[str]:
    e=[]
    for k in ("project_id","stage","problem_tags","desired_effects","hard_constraints"):
        if k not in s: e.append(f"missing:{k}")
    if s.get("stage") not in ALLOWED_STAGES: e.append("invalid:stage")
    m=s.get("max_mechanisms",3)
    if not isinstance(m,int) or m<1 or m>3: e.append("invalid:max_mechanisms")
    if not s.get("problem_tags"): e.append("empty:problem_tags")
    if not s.get("desired_effects"): e.append("empty:desired_effects")
    return e

def problem_signature_hash(s:Mapping[str,Any])->str:
    p=json.dumps(normalize_problem_signature(s),ensure_ascii=False,sort_keys=True,separators=(",",":"))
    return hashlib.sha256(p.encode()).hexdigest()[:20]

def _state(c:Mapping[str,Any])->str:
    return str(c.get("disposition") or c.get("evidence_state") or "REFERENCE_ONLY").upper()

def _reject(s:Mapping[str,Any],c:Mapping[str,Any])->List[str]:
    s=normalize_problem_signature(s); r=[]; state=_state(c)
    if state in {"HOLD","REJECT"}: r.append(f"mechanism_state:{state}")
    if not c.get("project_specific_expression_removed",False): r.append("distinctive_expression_not_confirmed_removed")
    if str(c.get("portability","PROJECT_NEUTRAL")).upper()=="PROJECT_ONLY" and str(c.get("project_id",""))!=s["project_id"]: r.append("project_only_cross_project_transfer")
    missing=sorted(set(_norm_set(c.get("prerequisites",[])))-set(s["available_conditions"]))
    if missing: r.append("missing_prerequisites:"+",".join(missing))
    env=set(s["problem_tags"])|set(s["hard_constraints"])|set(s["forbidden_moves"])
    hit=sorted(set(_norm_set(c.get("contraindications",[])))&env)
    if hit: r.append("contraindication:"+",".join(hit))
    moves=sorted(set(_norm_set(c.get("required_moves",[])))&set(s["forbidden_moves"]))
    if moves: r.append("forbidden_move_required:"+",".join(moves))
    if s["stage"]=="LOCKED_SHADOW" and c.get("requires_text_mutation",False): r.append("locked_text_mutation_forbidden")
    return r

def mechanism_match_vector(s:Mapping[str,Any],c:Mapping[str,Any])->Dict[str,Any]:
    s=normalize_problem_signature(s); reject=_reject(s,c)
    pt=set(s["problem_tags"]); de=set(s["desired_effects"]); gt=set(s["genre_tags"])
    ct=set(_norm_set(c.get("problem_tags",[]))); ce=set(_norm_set(c.get("effect_vector",[]))); cg=set(_norm_set(c.get("genre_tags",["GENERAL"])))
    return {"mechanism_id":str(c.get("mechanism_id","")),"eligible":not reject,"rejection_reasons":reject,"problem_tag_hits":sorted(pt&ct),"problem_tag_fit":len(pt&ct),"desired_effect_hits":sorted(de&ce),"desired_effect_fit":len(de&ce),"genre_fit":2 if gt and gt&cg else 1 if "GENERAL" in cg or not gt else 0,"evidence_rank":EVIDENCE_RANK.get(_state(c),0),"evidence_state":_state(c),"source_group_count":len(set(c.get("independent_source_groups",[]))),"failure_mode_count":len(set(c.get("failure_modes",[])))}

def _rank_key(v:Mapping[str,Any],c:Mapping[str,Any])->Tuple[Any,...]:
    return (v["desired_effect_fit"],v["problem_tag_fit"],v["evidence_rank"],v["genre_fit"],min(v["source_group_count"],2),-int(v["failure_mode_count"]==0),str(c.get("mechanism_id","")))

def rank_mechanisms(s:Mapping[str,Any],cards:Sequence[Mapping[str,Any]])->List[Dict[str,Any]]:
    out=[]
    for c in cards:
        v=mechanism_match_vector(s,c)
        if v["eligible"]: out.append({"card":copy.deepcopy(dict(c)),"match":v})
    out.sort(key=lambda x:_rank_key(x["match"],x["card"]),reverse=True)
    return out

def pair_compatibility(a:Mapping[str,Any],b:Mapping[str,Any])->Dict[str,Any]:
    aid,bid=str(a.get("mechanism_id","")),str(b.get("mechanism_id","")); reasons=[]
    if bid in set(map(str,a.get("incompatible_with",[]))) or aid in set(map(str,b.get("incompatible_with",[]))): reasons.append("explicit_incompatibility")
    af=set(_norm_set(a.get("forbids_effects",[]))); bf=set(_norm_set(b.get("forbids_effects",[])))
    ae=set(_norm_set(a.get("effect_vector",[]))); be=set(_norm_set(b.get("effect_vector",[])))
    if af&be or bf&ae: reasons.append("effect_conflict")
    return {"compatible":not reasons,"reasons":reasons}

def _combo_vector(s:Mapping[str,Any],cards:Sequence[Mapping[str,Any]])->Tuple[Any,...]:
    s=normalize_problem_signature(s); desired=set(s["desired_effects"]); problem=set(s["problem_tags"])
    effects=set().union(*(set(_norm_set(c.get("effect_vector",[]))) for c in cards)); tags=set().union(*(set(_norm_set(c.get("problem_tags",[]))) for c in cards))
    evidence=[EVIDENCE_RANK.get(_state(c),0) for c in cards]; groups=set().union(*(set(c.get("independent_source_groups",[])) for c in cards))
    return (len(desired&effects),len(problem&tags),min(evidence) if evidence else 0,min(len(groups),3),-len(cards),tuple(sorted(str(c.get("mechanism_id","")) for c in cards)))

def compose_mechanism_set(s:Mapping[str,Any],cards:Sequence[Mapping[str,Any]])->Dict[str,Any]:
    errors=validate_problem_signature(s)
    if errors: return {"status":"HOLD","errors":errors,"selected":[],"rejected_pairs":[]}
    s=normalize_problem_signature(s); eligible=[x["card"] for x in rank_mechanisms(s,cards)]; valid=[]; rejected=[]
    for size in range(1,min(s["max_mechanisms"],len(eligible))+1):
        for combo in itertools.combinations(eligible,size):
            bad=[]
            for a,b in itertools.combinations(combo,2):
                pc=pair_compatibility(a,b)
                if not pc["compatible"]: bad.append((a.get("mechanism_id"),b.get("mechanism_id"),pc["reasons"]))
            if bad: rejected.extend(bad)
            else: valid.append(combo)
    if not valid: return {"status":"HOLD","errors":["no_compatible_eligible_mechanism_set"],"selected":[],"rejected_pairs":rejected}
    valid.sort(key=lambda x:_combo_vector(s,x),reverse=True); selected=list(valid[0]); v=_combo_vector(s,selected)
    return {"status":"SELECTED","selected":selected,"selection_vector":{"desired_effect_coverage":v[0],"problem_tag_coverage":v[1],"weakest_evidence_rank":v[2],"independent_source_group_coverage":v[3],"mechanism_count":len(selected)},"rejected_pairs":rejected}

def _constraints(s:Mapping[str,Any])->List[str]:
    x=["MATCH_VECTOR_IS_NOT_STORY_QUALITY_PROOF","PREDICTED_EFFECT_IS_NOT_OBSERVED_EFFECT","REFERENCE_MECHANISM_IS_NOT_CANON","DUPLICATE_SOURCE_IS_NOT_INDEPENDENT_SUPPORT","MECHANISM_COMPOSITION_IS_NOT_PLOT_COPY","MORE_MECHANISMS_IS_NOT_BETTER","RETRIEVAL_PASS_IS_NOT_DRAFT_PASS","BASELINE_COMPARISON_REQUIRED_FOR_GAIN_CLAIM","NO_DISTINCTIVE_EXPRESSION_COPY","PROTECTED_FACTS_AND_CURRENT_PROJECT_AUTHORITY_WIN"]
    if s.get("stage")=="LOCKED_SHADOW": x.append("LOCKED_TEXT_SHADOW_EVALUATION_ONLY_NO_MUTATION")
    return x

def build_story_mechanism_packet(s:Mapping[str,Any],cards:Sequence[Mapping[str,Any]])->Dict[str,Any]:
    s=normalize_problem_signature(s); result=compose_mechanism_set(s,cards)
    if result["status"]!="SELECTED": return {"status":"HOLD","problem_signature":s,"problem_signature_hash":problem_signature_hash(s),"errors":result.get("errors",[]),"constraints":_constraints(s)}
    selected=result["selected"]; desired=set(s["desired_effects"]); fx=set().union(*(set(_norm_set(c.get("effect_vector",[]))) for c in selected))
    return {"status":"SHADOW_ONLY" if s["stage"]=="LOCKED_SHADOW" else "CANDIDATE_PACKET","problem_signature":s,"problem_signature_hash":problem_signature_hash(s),"mechanisms":[{"mechanism_id":c.get("mechanism_id"),"statement":c.get("statement"),"evidence_state":_state(c),"source_ids":list(c.get("source_ids",[])),"independent_source_groups":list(c.get("independent_source_groups",[])),"evidence_locators":list(c.get("evidence_locators",[])),"failure_modes":list(c.get("failure_modes",[])),"match":mechanism_match_vector(s,c)} for c in selected],"selection_vector":result["selection_vector"],"predicted_effects":sorted(desired&fx),"prediction_status":"PREDICTION_ONLY_NOT_OBSERVED_RESULT","constraints":_constraints(s),"acceptance":{"baseline_required_for_gain_claim":True,"fatal_major_regression_allowed":False,"observed_result_required_for_learning":True}}

def evaluate_baseline_candidate(*,baseline:Mapping[str,float],candidate:Mapping[str,float],directions:Mapping[str,str],protected_dimensions:Sequence[str]=(),severity_by_dimension:Mapping[str,str]|None=None)->Dict[str,Any]:
    severity_by_dimension=severity_by_dimension or {}; dims=sorted(set(baseline)|set(candidate))
    if not dims or set(baseline)!=set(candidate): return {"status":"EVIDENCE_HOLD","reason":"baseline_candidate_dimensions_missing_or_mismatched"}
    changes={}; blocking=[]; improved=[]; protected=set(protected_dimensions)
    for d in dims:
        direction=str(directions.get(d,"HIGHER")).upper(); b=float(baseline[d]); c=float(candidate[d]); delta=c-b if direction=="HIGHER" else b-c
        cls="IMPROVED" if delta>0 else "REGRESSED" if delta<0 else "SAME"; sev=str(severity_by_dimension.get(d,"MEDIUM")).upper(); sev=sev if sev in SEVERITIES else "MEDIUM"
        changes[d]={"baseline":b,"candidate":c,"direction":direction,"classification":cls,"severity":sev,"protected":d in protected}
        if cls=="IMPROVED": improved.append(d)
        if cls=="REGRESSED" and (d in protected or sev in {"FATAL","MAJOR"}): blocking.append(d)
    if blocking: return {"status":"REGRESSION","reason":"protected_or_fatal_major_regression","dimensions":changes,"blocking_dimensions":blocking}
    if improved: return {"status":"OBSERVED_NET_GAIN","dimensions":changes,"improved_dimensions":improved}
    return {"status":"NO_OBSERVED_GAIN","dimensions":changes}

def record_outcome_feedback(card:Mapping[str,Any],*,project_id:str,packet_hash:str,result:str,measurable_gain:bool,severity:str="MEDIUM",evidence_locator:str)->Dict[str,Any]:
    out=copy.deepcopy(dict(card)); rec={"project_id":project_id,"packet_hash":packet_hash,"result":str(result).upper(),"measurable_gain":bool(measurable_gain),"severity":str(severity).upper(),"evidence_locator":evidence_locator}; hist=list(out.get("application_evidence",[]))+[rec]; out["application_evidence"]=hist
    passes=[x for x in hist if x.get("result")=="PASS" and x.get("measurable_gain")]; projects={x.get("project_id") for x in passes if x.get("project_id")}; regress=[x for x in hist if x.get("result")=="REGRESSION" and x.get("severity") in {"FATAL","MAJOR"}]
    out["application_readiness"]="HOLD_APPLICATION" if regress else "PROMOTION_REVIEW_READY" if len(projects)>=2 else "SECOND_PROJECT_REQUIRED" if len(projects)==1 else "LOCAL_TEST_REQUIRED"
    return out

def main()->None:
    import argparse
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True); q=sub.add_parser("build-packet"); q.add_argument("problem_json"); q.add_argument("mechanisms_json"); a=p.parse_args()
    if a.cmd=="build-packet":
        with open(a.problem_json,encoding="utf-8") as f: s=json.load(f)
        with open(a.mechanisms_json,encoding="utf-8") as f: c=json.load(f)
        print(json.dumps(build_story_mechanism_packet(s,c),ensure_ascii=False,indent=2))
if __name__=="__main__": main()
