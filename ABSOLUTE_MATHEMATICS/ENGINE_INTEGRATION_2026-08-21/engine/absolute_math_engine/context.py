from __future__ import annotations
from itertools import combinations
from collections import defaultdict
from typing import Callable, Hashable, Any

def behavioral_partition(states:list[Any], contexts:list[Callable[[Any],Hashable]]) -> list[list[int]]:
    groups=defaultdict(list)
    for i,s in enumerate(states):
        sig=tuple(c(s) for c in contexts)
        groups[sig].append(i)
    return sorted((sorted(v) for v in groups.values()), key=lambda x:(len(x),x))

def is_point_separating(states:list[Any], contexts:list[Callable[[Any],Hashable]]) -> bool:
    sigs=[tuple(c(s) for c in contexts) for s in states]
    return len(set(sigs)) == len(states)

def minimal_context_bases(states:list[Any], named_contexts:dict[str,Callable[[Any],Hashable]]):
    names=list(named_contexts)
    full=behavioral_partition(states,[named_contexts[n] for n in names])
    target={frozenset(x) for x in full}
    for k in range(len(names)+1):
        out=[]
        for sub in combinations(names,k):
            p=behavioral_partition(states,[named_contexts[n] for n in sub])
            if {frozenset(x) for x in p}==target:
                out.append(sub)
        if out:
            return out
    return [tuple(names)]

def context_no_go(states, contexts):
    point=is_point_separating(states,contexts)
    return {"point_separating":point,
            "verdict":"NO_NONTRIVIAL_EXACT_COMPRESSION" if point else "SEARCH_ALLOWED",
            "lower_bound_state_count":len(states) if point else None}
