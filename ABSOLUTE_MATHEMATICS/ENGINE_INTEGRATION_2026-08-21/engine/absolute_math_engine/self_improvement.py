from __future__ import annotations
from dataclasses import asdict
from .models import ImprovementProposal

def improvement_score(metrics,weights):
    return sum(metrics.get(k,0.0)*w for k,w in weights.items())

class ImprovementArchive:
    def __init__(self): self.nodes={}
    def add(self,proposal:ImprovementProposal,parent_id=None,metrics=None,verdict="HOLD"):
        if proposal.proposal_id in self.nodes: raise ValueError("DUPLICATE_PROPOSAL_ID")
        self.nodes[proposal.proposal_id]={"proposal":asdict(proposal),"parent_id":parent_id,
            "metrics":dict(metrics or {}),"verdict":verdict,"children":[]}
        if parent_id:
            if parent_id not in self.nodes: raise ValueError("UNKNOWN_PARENT")
            self.nodes[parent_id]["children"].append(proposal.proposal_id)
    def candidates(self):
        return [n for n in self.nodes.values() if n["verdict"] in {"PASS","CANDIDATE"}]

def promotion_gate(*,baseline,candidate,regression_floor=0.0,min_primary_gain=0.0):
    primary_gain=candidate.get("primary",0)-baseline.get("primary",0)
    regression=min((candidate.get(k,0)-baseline.get(k,0) for k in baseline if k!="primary"),default=0.0)
    passed=primary_gain>=min_primary_gain and regression>=-regression_floor
    return {"passed":passed,"primary_gain":primary_gain,"worst_regression":regression,
            "reason":"PASS" if passed else "HOLD_OR_REJECT"}

def lineage_potential(node,archive,depth=2):
    seen=set(); frontier=[(node,0)]; vals=[]
    while frontier:
        nid,d=frontier.pop()
        if nid in seen or nid not in archive.nodes or d>depth: continue
        seen.add(nid); n=archive.nodes[nid]
        if n["metrics"]: vals.append(n["metrics"].get("primary",0.0))
        for c in n["children"]: frontier.append((c,d+1))
    return sum(vals)/len(vals) if vals else 0.0

def parent_priority(node_id,archive,novelty=0.0,descendant_weight=0.25,novelty_weight=0.15):
    current=archive.nodes[node_id]["metrics"].get("primary",0.0)
    return current+descendant_weight*lineage_potential(node_id,archive)+novelty_weight*novelty
