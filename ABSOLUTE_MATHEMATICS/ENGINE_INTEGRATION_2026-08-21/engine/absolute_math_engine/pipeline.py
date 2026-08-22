from __future__ import annotations
from .context import context_no_go
from .partition import learn_min_partition
from .models import GateResult, PromotionDecision

def run_finite_markov(problem,contexts,P,labels):
    no_go=context_no_go(problem.micro_states,contexts)
    gates=[GateResult("NO_GO",no_go["verdict"]!="NO_NONTRIVIAL_EXACT_COMPRESSION",
                      reason=no_go["verdict"],evidence=no_go)]
    if not gates[-1].passed:
        return PromotionDecision("NO_PROMOTION",None,gates,len(problem.micro_states),
            ["Point-separating context family forbids nontrivial exact compression."])
    learned=learn_min_partition(P,labels,problem.tolerance)
    if learned is None:
        gates.append(GateResult("PARTITION_SEARCH",False,reason="NO_FEASIBLE_PARTITION"))
        return PromotionDecision("INCONCLUSIVE",None,gates,None)
    exact=learned["defect"]<=1e-12
    gates.append(GateResult("LUMPABILITY",True,metric=learned["defect"],threshold=problem.tolerance,evidence=learned))
    return PromotionDecision("EXACT" if exact else "APPROXIMATE",f"{problem.problem_id}:P",gates,learned["state_count"])
