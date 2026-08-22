from __future__ import annotations
import itertools, math, random, statistics
from collections import defaultdict

def make_commutative_table(n, upper_values):
    pairs=[(i,j) for i in range(n) for j in range(i,n)]
    if len(upper_values)!=len(pairs): raise ValueError("wrong table length")
    T=[[None]*n for _ in range(n)]
    for (i,j),v in zip(pairs,upper_values):
        T[i][j]=v;T[j][i]=v
    return T

def associative(T):
    n=len(T)
    for a,b,c in itertools.product(range(n),repeat=3):
        if T[T[a][b]][c] != T[a][T[b][c]]:
            return False
    return True

def commutative(T):
    n=len(T)
    return all(T[i][j]==T[j][i] for i in range(n) for j in range(n))

def diagonal_map(T):
    return tuple(T[i][i] for i in range(len(T)))

def orbit_signature(D,start):
    seen={};seq=[];x=start
    while x not in seen:
        seen[x]=len(seq);seq.append(x);x=D[x]
    mu=seen[x];lam=len(seq)-mu
    return {"start":start,"tail":mu,"period":lam,"orbit":seq,"cycle":seq[mu:]}

def diagonal_signature(T):
    D=diagonal_map(T)
    return {"D":D,"orbits":[orbit_signature(D,i) for i in range(len(T))]}

def enumerate_commutative_semigroups(n):
    pairs=n*(n+1)//2;out=[]
    for vals in itertools.product(range(n), repeat=pairs):
        T=make_commutative_table(n,vals)
        if associative(T): out.append(T)
    return out

def canonical_table(T):
    n=len(T);reps=[]
    for p in itertools.permutations(range(n)):
        inv=[0]*n
        for i,v in enumerate(p):inv[v]=i
        flat=[]
        for i in range(n):
            for j in range(n):flat.append(inv[T[p[i]][p[j]]])
        reps.append(tuple(flat))
    return min(reps)

def isomorphism_classes(tables):
    groups={}
    for T in tables:
        c=canonical_table(T);groups[c]=groups.get(c,0)+1
    return groups

def count_same_diagonal_nonidentifiability(n, require_associative=False):
    tables=enumerate_commutative_semigroups(n) if require_associative else [
        make_commutative_table(n,v) for v in itertools.product(range(n),repeat=n*(n+1)//2)]
    groups=defaultdict(list)
    for T in tables:groups[diagonal_map(T)].append(T)
    sizes=sorted((len(v) for v in groups.values()),reverse=True)
    return {"n":n,"table_count":len(tables),"distinct_diagonals":len(groups),
            "max_tables_same_diagonal":max(sizes) if sizes else 0,
            "ambiguous_diagonals":sum(1 for s in sizes if s>1),"group_sizes":sizes}

def power_orbit_prediction(index,period):
    if index<1 or period<1: raise ValueError
    a=0;p=period
    while p%2==0:a+=1;p//=2
    k_index=math.ceil(math.log2(index)) if index>1 else 0
    pre=max(a,k_index)
    if p==1:cyc=1
    else:
        r=2%p;cyc=1
        while r!=1:r=(r*2)%p;cyc+=1
    return {"preperiod_bound":pre,"odd_period_part":p,"eventual_cycle_period":cyc}

def group_squaring_signature(order_m):
    a=0;q=order_m
    while q%2==0:a+=1;q//=2
    if q==1:return {"tail":a,"period":1}
    r=2%q;p=1
    while r!=1:r=(r*2)%q;p+=1
    return {"tail":a,"period":p}

def off_diagonal_disagreement(T1,T2):
    n=len(T1)
    return [(i,j,T1[i][j],T2[i][j]) for i in range(n) for j in range(i+1,n) if T1[i][j]!=T2[i][j]]

def candidate_binary_ops():
    return {
      "ADD":lambda a,b:a+b,"MUL":lambda a,b:a*b,"MAX":lambda a,b:max(a,b),
      "MIN":lambda a,b:min(a,b),"MEAN":lambda a,b:(a+b)/2.0,
      "RMS":lambda a,b:math.sqrt((a*a+b*b)/2.0),
      "HARMONIC":lambda a,b:0.0 if a+b==0 else 2*a*b/(a+b),
      "PROB_OR":lambda a,b:a+b-a*b,"XOR_POLY":lambda a,b:a+b-2*a*b}

def operator_search(pairs,ys,allow_scale=False):
    rows=[]
    for name,op in candidate_binary_ops().items():
        pred=[];valid=True
        for a,b in pairs:
            try:
                v=op(a,b)
                if not math.isfinite(v):valid=False;break
                pred.append(v)
            except Exception:valid=False;break
        if not valid:continue
        scale=1.0
        if allow_scale:
            den=sum(p*p for p in pred);scale=sum(o*p for o,p in zip(ys,pred))/den if den>1e-15 else 0.0
        rmse=(sum((y-scale*p)**2 for y,p in zip(ys,pred))/len(ys))**.5
        rows.append({"operator":name,"scale":scale,"rmse":rmse})
    return sorted(rows,key=lambda r:r["rmse"])

def mixed_probe_requirement(n):
    return {"general_unknown_off_diagonal_entries":n*n-n,
            "commutative_unknown_off_diagonal_entries":n*(n-1)//2}

def fit_lambda_add_mul(pairs,ys):
    num=sum((y-a-b)*(a*b) for (a,b),y in zip(pairs,ys));den=sum((a*b)**2 for a,b in pairs)
    lam=num/den if den>1e-15 else 0.0
    pred=[a+b+lam*a*b for a,b in pairs]
    rmse=(sum((y-p)**2 for y,p in zip(ys,pred))/len(ys))**0.5
    return {"lambda":lam,"rmse":rmse}

def add_mul_op(lam):return lambda a,b:a+b+lam*a*b

def associativity_defect(op,triples):
    errs=[]
    for a,b,c in triples:
        try:errs.append(abs(op(op(a,b),c)-op(a,op(b,c))))
        except Exception:errs.append(float("inf"))
    finite=[e for e in errs if math.isfinite(e)]
    return {"max":max(finite) if finite else float("inf"),"mean":sum(finite)/len(finite) if finite else float("inf")}

def linearization_defect(op, transform, pairs):
    errs=[]
    for a,b in pairs:
        try:
            e=transform(op(a,b))-transform(a)-transform(b)
            if not math.isfinite(e):return float("inf")
            errs.append(e)
        except Exception:return float("inf")
    return (sum(e*e for e in errs)/len(errs))**0.5

def linearizer_candidates(lambda_hint=.37):
    return {"IDENTITY":lambda x:x,"LOG_POSITIVE":lambda x:math.log(x),
            "NEG_LOG1M":lambda x:-math.log(1-x),
            "LOG1P_LAMBDA":lambda x:math.log(1+lambda_hint*x),
            "ATANH":lambda x:.5*math.log((1+x)/(1-x))}

def search_linearizer(op,pairs,lambda_hint=.37):
    return sorted([{"transform":name,"defect":linearization_defect(op,f,pairs)}
                   for name,f in linearizer_candidates(lambda_hint).items()],key=lambda r:r["defect"])
