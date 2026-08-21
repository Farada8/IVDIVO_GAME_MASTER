from __future__ import annotations

def _parts(seq):
    seq=list(seq)
    if not seq:
        yield []
        return
    first=seq[0]
    for rest in _parts(seq[1:]):
        yield [{first}] + [set(b) for b in rest]
        for i in range(len(rest)):
            out=[set(b) for b in rest]
            out[i].add(first)
            yield out

def canonical(part):
    return tuple(sorted(tuple(sorted(b)) for b in part))

def all_partitions(n:int):
    seen=set()
    for p in _parts(range(n)):
        c=canonical(p)
        if c not in seen:
            seen.add(c)
            yield [set(b) for b in c]

def output_consistent(part, labels):
    return all(len({labels[i] for i in block})==1 for block in part)

def markov_lumpability_defect(P, part):
    defect=0.0
    for block in part:
        for i in block:
            for j in block:
                for target in part:
                    pi=sum(P[i][k] for k in target)
                    pj=sum(P[j][k] for k in target)
                    defect=max(defect,abs(pi-pj))
    return float(defect)

def learn_min_partition(P, labels, epsilon:float=0.0):
    n=len(P); candidates=[]
    for p in all_partitions(n):
        if not output_consistent(p,labels): continue
        d=markov_lumpability_defect(P,p)
        if d <= epsilon + 1e-12:
            candidates.append((len(p),d,canonical(p)))
    if not candidates: return None
    candidates.sort(key=lambda x:(x[0],x[1],x[2]))
    k,d,c=candidates[0]
    return {"state_count":k,"defect":d,"blocks":[list(x) for x in c]}
