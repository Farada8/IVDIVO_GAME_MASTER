from __future__ import annotations
import hashlib, json

def evidence_id(payload): return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def add_evidence(graph:dict,item:dict)->dict:
    g={"nodes":list(graph.get("nodes",[])),"edges":list(graph.get("edges",[]))}
    iid=item.get("evidence_id") or evidence_id({k:v for k,v in item.items() if k!="evidence_id"})
    node={**item,"evidence_id":iid}
    if any(n["evidence_id"]==iid for n in g["nodes"]): return g
    g["nodes"].append(node)
    parent=item.get("derived_from")
    if parent: g["edges"].append({"from":parent,"to":iid,"relation":"DERIVED_FROM"})
    return g

def independent_families(graph:dict)->dict:
    parent={e["to"]:e["from"] for e in graph.get("edges",[]) if e.get("relation")=="DERIVED_FROM"}
    def root(x):
        seen=set()
        while x in parent and x not in seen: seen.add(x); x=parent[x]
        return x
    fam={}
    for n in graph.get("nodes",[]): fam.setdefault(root(n["evidence_id"]),[]).append(n["evidence_id"])
    return {"family_count":len(fam),"families":fam}

def reconcile_reports(reports:list[dict],graph:dict)->dict:
    fam=independent_families(graph)
    roots={eid:root for root,eids in fam["families"].items() for eid in eids}
    claims={}
    for r in reports:
        rid=r["evidence_id"]; key=(r["claim"],r["verdict"])
        claims.setdefault(key,set()).add(roots.get(rid,rid))
    return {"claim_family_counts":{f"{k[0]}::{k[1]}":len(v) for k,v in claims.items()},"agreement_is_validation":False}
