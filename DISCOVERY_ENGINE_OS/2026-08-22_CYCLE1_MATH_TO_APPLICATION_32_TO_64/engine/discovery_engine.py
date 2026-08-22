from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, Sequence, Mapping, Any
import itertools, math, hashlib, json

NOVELTY_STATUSES={
    "KNOWN","REDISCOVERY","DERIVED","COUNTEREXAMPLE","NOVELTY_UNVERIFIED",
    "ENGINEERING_SYNTHESIS","APPLICATION_CANDIDATE","PATENT_TRIAGE_HOLD",
    "FAILED","INCONCLUSIVE"
}
PLANES=("MATHEMATICAL_TRUTH","SCIENTIFIC_NOVELTY","PATENT_NOVELTY",
        "ENGINEERING_NOVELTY","APPLICATION_VALUE","MARKET_PROOF")

def atomize_claim(text:str)->list[str]:
    chunks=[x.strip(" .;") for x in text.replace(" and ",";").split(";") if x.strip(" .;")]
    return chunks or [text.strip()]

def novelty_planes()->dict[str,str]:
    return {p:"UNASSESSED" for p in PLANES}

def bounded_absence_gate(matches:int, searched_sources:int)->str:
    if matches>0: return "PRIOR_ART_FOUND"
    return "NOVELTY_UNVERIFIED"

def feature_matrix(candidate_features:set[str], references:Mapping[str,set[str]])->dict[str,Any]:
    single=[]; overlaps={}
    for rid,fs in references.items():
        cov=candidate_features & fs; overlaps[rid]=sorted(cov)
        if candidate_features <= fs: single.append(rid)
    return {"candidate":sorted(candidate_features),"overlap":overlaps,
        "single_reference_full_disclosure":sorted(single),
        "novelty_triage":"NOT_NOVEL_SINGLE_REFERENCE" if single else "SINGLE_REFERENCE_NOVELTY_NOT_DESTROYED",
        "inventive_step":"UNRESOLVED"}

def novelty_status(*,formal_truth=False, prior_art_full=False, prior_art_partial=False,
                   generated_from_known=False, new_combination=False, app_transfer=False)->str:
    if prior_art_full or generated_from_known: return "REDISCOVERY" if formal_truth else "KNOWN"
    if app_transfer and not new_combination: return "APPLICATION_CANDIDATE"
    if new_combination and prior_art_partial: return "ENGINEERING_SYNTHESIS"
    return "NOVELTY_UNVERIFIED"

def polynomial_fit_quadratic(xs,ys):
    X=[[1.0,float(x),float(x)*float(x)] for x in xs]
    A=[[sum(row[i]*row[j] for row in X) for j in range(3)] for i in range(3)]
    b=[sum(row[i]*float(y) for row,y in zip(X,ys)) for i in range(3)]
    M=[A[i]+[b[i]] for i in range(3)]
    for c in range(3):
        piv=max(range(c,3),key=lambda r:abs(M[r][c])); M[c],M[piv]=M[piv],M[c]
        d=M[c][c]
        for j in range(c,4): M[c][j]/=d
        for r in range(3):
            if r==c: continue
            f=M[r][c]
            for j in range(c,4): M[r][j]-=f*M[c][j]
    return [M[i][3] for i in range(3)]

def sequence_discovery(values):
    xs=list(range(len(values))); coef=polynomial_fit_quadratic(xs,values)
    pred=[coef[0]+coef[1]*x+coef[2]*x*x for x in xs]
    rmse=(sum((a-b)**2 for a,b in zip(values,pred))/len(values))**0.5
    return {"coefficients":coef,"rmse":rmse}

def graph_components(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    seen=set();c=0
    for s in range(n):
        if s in seen:continue
        c+=1;stack=[s];seen.add(s)
        while stack:
            u=stack.pop()
            for v in adj[u]:
                if v not in seen:seen.add(v);stack.append(v)
    return c

def graph_triangles(n,edges):
    E={tuple(sorted(e)) for e in edges}; t=0
    for a,b,c in itertools.combinations(range(n),3):
        if (a,b) in E and (a,c) in E and (b,c) in E:t+=1
    return t

def cyclomatic(n,edges): return len(edges)-n+graph_components(n,edges)

def exhaustive_graph_counterexample(candidate, max_n=5):
    checked=0
    for n in range(1,max_n+1):
        pairs=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            edges=[pairs[i] for i in range(len(pairs)) if (mask>>i)&1]; checked+=1
            if not candidate(n,edges): return {"found":True,"n":n,"edges":edges,"checked":checked}
    return {"found":False,"checked":checked}

def logistic_symbolic_regression(r=3.2,n=150,x0=.17):
    xs=[];ys=[];x=x0
    for _ in range(n):
        y=r*x*(1-x); xs.append(x);ys.append(y);x=y
    c=polynomial_fit_quadratic(xs,ys)
    rmse=(sum((y-(c[0]+c[1]*x+c[2]*x*x))**2 for x,y in zip(xs,ys))/n)**0.5
    return {"coefficients":c,"rmse":rmse,"expected":[0.0,r,-r]}

def binpack(items,policy,cap=1.0):
    bins=[]
    for item in items:
        fits=[i for i,b in enumerate(bins) if b+item<=cap+1e-12]
        if not fits: bins.append(item); continue
        if policy=="FIRST_FIT":i=fits[0]
        elif policy=="BEST_FIT":i=max(fits,key=lambda j:bins[j])
        elif policy=="WORST_FIT":i=min(fits,key=lambda j:bins[j])
        elif policy=="TIGHT_OR_SPREAD":
            tight=[j for j in fits if cap-(bins[j]+item)<.08]
            i=max(tight,key=lambda j:bins[j]) if tight else min(fits,key=lambda j:bins[j])
        else: raise ValueError(policy)
        bins[i]+=item
    return len(bins)

def statistics_mean(v): return sum(v)/len(v)

def binpack_policy_benchmark():
    train=[
        [.19,.43,.53,.23,.25,.57,.23,.73,.63,.40,.25,.31],
        [.64,.60,.15,.45,.15,.58,.41,.25,.33,.33,.72,.18],
        [.72,.48,.16,.37,.35,.28,.43,.41,.20,.57,.46,.67],]
    hidden=[
        [.62,.46,.22,.45,.72,.18,.62,.67,.46,.42,.73,.19],
        [.66,.30,.50,.46,.39,.34,.35,.35,.25,.46,.22,.46],
        [.42,.22,.69,.51,.16,.46,.30,.24,.41,.52,.29,.40],]
    policies=["FIRST_FIT","BEST_FIT","WORST_FIT","TIGHT_OR_SPREAD"]
    def score(ds,p): return statistics_mean([binpack(x,p) for x in ds])
    rows=[{"policy":p,"train_bins":score(train,p),"hidden_bins":score(hidden,p)} for p in policies]
    selected=min(rows,key=lambda r:(r["train_bins"],r["policy"])); hidden_best=min(rows,key=lambda r:(r["hidden_bins"],r["policy"]))
    return {"rows":rows,"train_selected":selected,"hidden_best":hidden_best,
            "generalizes":selected["hidden_bins"]<=hidden_best["hidden_bins"]+1e-12,
            "control":"PLANTED_DISTRIBUTION_SHIFT"}

def context_partition(states,contexts):
    groups={}
    for s in states: groups.setdefault(tuple(c(s) for c in contexts),[]).append(s)
    return sorted([sorted(v) for v in groups.values()])

def context_refinement_fixture():
    states=[(0,0),(0,1),(1,0),(1,1)]; c1=lambda s:s[0]; c2=lambda s:s[1]
    p1=context_partition(states,[c1]); p2=context_partition(states,[c2]); p12=context_partition(states,[c1,c2])
    return {"c1_classes":len(p1),"c2_classes":len(p2),"combined_classes":len(p12),"c1":p1,"c2":p2,"combined":p12}

def transfer_certificate(mechanism,source_domain,target_domain,positive_fixture,negative_fixture):
    return {"mechanism":mechanism,"source_domain":source_domain,"target_domain":target_domain,
            "positive_fixture":positive_fixture,"negative_fixture":negative_fixture,
            "status":"APPLICATION_CANDIDATE" if positive_fixture and negative_fixture else "INCONCLUSIVE",
            "theorem_novelty":"NOT_INFERRED"}

def causal_claim_gate(evidence_type):
    return "CAUSAL_CLAIM_POSSIBLE_WITH_ASSUMPTIONS" if evidence_type in {"RANDOMIZED_INTERVENTION","VALID_CAUSAL_IDENTIFICATION"} else "ASSOCIATIONAL_ONLY"

def patent_triage(candidate_features,references):
    fm=feature_matrix(set(candidate_features),{k:set(v) for k,v in references.items()})
    status="PATENT_TRIAGE_NOT_NOVEL" if fm["single_reference_full_disclosure"] else "PATENT_TRIAGE_HOLD"
    return {**fm,"status":status,"legal_opinion":False}

def trl_gate(proof,prototype,real_environment):
    if not proof:return "TRL0_CONCEPT"
    if proof and not prototype:return "TRL1_2_PRINCIPLE"
    if prototype and not real_environment:return "TRL3_4_LAB_PROTOTYPE"
    return "TRL5_PLUS_REQUIRES_DOMAIN_REVIEW"

def ordinal_voi(kill_power,uncertainty,cash_cost,irreversibility):
    levels={"LOW":0,"MEDIUM":1,"HIGH":2}
    return (levels[kill_power]+levels[uncertainty],-cash_cost,-levels[irreversibility])

def discovery_portfolio(candidates,cap=3):
    eligible=[c for c in candidates if c.get("status") not in {"KNOWN","REDISCOVERY","COUNTEREXAMPLE","FAILED"}]
    return sorted(eligible,key=lambda c:(-c.get("falsifiability",0),-c.get("application_breadth",0),c["id"]))[:cap]

def naive_novelty_policy(case):
    return "NEW" if case["lexical_novelty"]>.6 and case["internal_score"]>.6 else "NOT_NEW"

def evidence_novelty_policy(case):
    if case.get("known_prior_art"): return "REDISCOVERY"
    if case.get("counterexample"): return "COUNTEREXAMPLE"
    return "NOVELTY_UNVERIFIED"

def self_improvement_fixture():
    cases=[
      {"id":"SI1_REWORD_KNOWN","lexical_novelty":.95,"internal_score":.9,"known_prior_art":True,"counterexample":False,"hidden_fail":False,"independent_prior_art_search":True,"proof_or_reproducible_evidence":True,"expected_not_new":True},
      {"id":"SI2_OVERFIT_ALGO","lexical_novelty":.8,"internal_score":.95,"known_prior_art":False,"counterexample":False,"hidden_fail":True,"independent_prior_art_search":False,"proof_or_reproducible_evidence":True,"expected_not_new":True},
      {"id":"SI3_FALSE_CONJECTURE","lexical_novelty":.75,"internal_score":.8,"known_prior_art":False,"counterexample":True,"hidden_fail":False,"independent_prior_art_search":False,"proof_or_reproducible_evidence":False,"expected_not_new":True},
      {"id":"SI4_NEW_COMBINATION","lexical_novelty":.9,"internal_score":.85,"known_prior_art":False,"counterexample":False,"hidden_fail":False,"independent_prior_art_search":False,"proof_or_reproducible_evidence":True,"expected_not_new":True},
      {"id":"SI5_LOW_WORDING_REAL","lexical_novelty":.2,"internal_score":.7,"known_prior_art":False,"counterexample":False,"hidden_fail":False,"independent_prior_art_search":True,"proof_or_reproducible_evidence":True,"expected_not_new":True},
      {"id":"SI6_NO_PROOF","lexical_novelty":.9,"internal_score":.9,"known_prior_art":False,"counterexample":False,"hidden_fail":False,"independent_prior_art_search":True,"proof_or_reproducible_evidence":False,"expected_not_new":True},]
    rows=[]; naive_errors=0; evidence_errors=0
    for c in cases:
        n=naive_novelty_policy(c); e=evidence_novelty_policy(c)
        nb=(n=="NEW" and c["expected_not_new"]); eb=(e=="NEW" and c["expected_not_new"])
        naive_errors+=int(nb); evidence_errors+=int(eb)
        rows.append({"id":c["id"],"naive":n,"evidence":e,"naive_error":nb,"evidence_error":eb})
    return {"rows":rows,"naive_false_new":naive_errors,"evidence_false_new":evidence_errors,
            "candidate":"EVIDENCE_FIRST_NOVELTY_GATE","candidate_status":"LOCAL_KEEP" if evidence_errors<naive_errors else "HOLD",
            "global_authority_promotion":False}

def close_discovery(records):
    bad=[r for r in records if r.get("status")=="NEW"]
    return {"can_close":not bad,"forbidden_unverified_new_count":len(bad)}
