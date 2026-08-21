"""Project-neutral learning bridge with independent replication and leakage firewall."""
from __future__ import annotations
import re
PROJECT_TERMS=re.compile(r"\b(?:NINETY MISSING MINUTES|NMM|Isla|Leo|Vivian|Mercer|Calder|C-?17|harbour|copper|lantern)\b",re.I)
def sanitize_text(s:str)->str: return PROJECT_TERMS.sub("[PROJECT_SPECIFIC]",s)
def sanitize_record(rec:dict)->dict:
    out={}
    for k,v in rec.items():
        if isinstance(v,str): out[k]=sanitize_text(v)
        elif isinstance(v,list): out[k]=[sanitize_text(x) if isinstance(x,str) else x for x in v]
        else: out[k]=v
    out.pop("exact_text",None); out.pop("asset_id",None); return out

def classify_replication(records:list[dict])->dict:
    projects={r.get("project_id") for r in records if r.get("result") in {"PASS","IMPROVED"} and r.get("project_id")}
    human=sum(1 for r in records if r.get("human_evidence") is True and r.get("result") in {"PASS","IMPROVED"})
    if len(projects)<2: status="DISCOVERY_ONLY"
    elif human<1: status="CANDIDATE_FOR_REVIEW_TECHNICAL_ONLY"
    else: status="CANDIDATE_FOR_REVIEW"
    return {"status":status,"distinct_projects":len(projects),"human_evidence_records":human,"auto_promote":False}
