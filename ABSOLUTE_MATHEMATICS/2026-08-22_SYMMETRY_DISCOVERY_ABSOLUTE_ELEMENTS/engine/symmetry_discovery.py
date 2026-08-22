from __future__ import annotations
import itertools, math, random

def all_perms(n):
    return list(itertools.permutations(range(n)))

def apply_perm(x,p):
    return [x[p[i]] for i in range(len(p))]

def compose(p,q):
    return tuple(p[q[i]] for i in range(len(p)))

def identity(n):
    return tuple(range(n))

def closure(gens,n):
    G={identity(n)}
    changed=True
    while changed:
        changed=False
        current=list(G)
        for a in current:
            for b in gens+current:
                for c in (compose(a,b),compose(b,a)):
                    if c not in G:
                        G.add(c); changed=True
    return sorted(G)

def discover_exact_symmetry(task,n=4,trials=400,seed=0,tol=1e-9):
    rng=random.Random(seed)
    samples=[[rng.uniform(-1.3,1.3) for _ in range(n)] for _ in range(trials)]
    good=[]; violations={}
    for p in all_perms(n):
        worst=0.0
        for x in samples:
            d=abs(task(x)-task(apply_perm(x,p)))
            worst=max(worst,d)
        violations["".join(map(str,p))]=worst
        if worst<=tol: good.append(p)
    return {"group":good,"size":len(good),"violations":violations}

def subset_action(S,p):
    return tuple(sorted(p[i] for i in S))

def nonempty_subsets(n):
    return [s for k in range(1,n+1) for s in itertools.combinations(range(n),k)]

def subset_orbits(n,G):
    unseen=set(nonempty_subsets(n)); orbits=[]
    while unseen:
        S=min(unseen)
        orb={subset_action(S,p) for p in G}
        orbits.append(sorted(orb))
        unseen-=orb
    return sorted(orbits,key=lambda O:(len(O[0]),O[0]))

def burnside_subset_orbit_count(n,G):
    total=0
    for p in G:
        total += sum(1 for S in nonempty_subsets(n) if subset_action(S,p)==S)
    return total//len(G)

def orbit_sum_features(x,G):
    feats=[]
    for O in subset_orbits(len(x),G):
        feats.append(sum(math.prod(x[i] for i in S) for S in O))
    return feats

def task_symmetric(x):
    return sum(x)+0.7*sum(x[i]*x[j] for i,j in itertools.combinations(range(4),2))

def task_block(x):
    return (x[0]+x[1])-1.5*(x[2]+x[3])+0.25*x[0]*x[1]-0.4*x[2]*x[3]

def task_role(x):
    return x[0]-2*x[1]+0.5*x[2]-x[3]

def task_cycle(x):
    return x[0]*x[1]+x[1]*x[2]+x[2]*x[3]+x[3]*x[0]

def _solve_linear(X,y,l2=1e-10):
    p=len(X[0]); A=[]; b=[]
    for i in range(p):
        A.append([sum(r[i]*r[j] for r in X)+(l2 if i==j else 0.0) for j in range(p)])
        b.append(sum(r[i]*yy for r,yy in zip(X,y)))
    M=[A[i]+[b[i]] for i in range(p)]
    for c in range(p):
        piv=max(range(c,p),key=lambda r:abs(M[r][c]))
        if abs(M[piv][c])<1e-14:
            continue
        M[c],M[piv]=M[piv],M[c]
        d=M[c][c]
        for j in range(c,p+1): M[c][j]/=d
        for r in range(p):
            if r==c: continue
            f=M[r][c]
            for j in range(c,p+1): M[r][j]-=f*M[c][j]
    return [M[i][p] for i in range(p)]

def benchmark_task(task,G,n=4,seed=0):
    rng=random.Random(seed)
    data=[]
    for _ in range(1000):
        x=[rng.uniform(-1.2,1.2) for _ in range(n)]
        data.append((x,task(x)))
    tr,te=data[:700],data[700:]
    phi=lambda x:orbit_sum_features(x,G)
    X=[[1.0]+phi(x) for x,y in tr]; y=[y for x,y in tr]
    w=_solve_linear(X,y)
    def pred(x):
        row=[1.0]+phi(x)
        return sum(a*b for a,b in zip(w,row))
    tr_rmse=(sum((pred(x)-y)**2 for x,y in tr)/len(tr))**0.5
    te_rmse=(sum((pred(x)-y)**2 for x,y in te)/len(te))**0.5
    return {"feature_dim":len(phi(tr[0][0])),"train_rmse":tr_rmse,"hidden_rmse":te_rmse}

def jacobian_rank_squarefree(x):
    n=len(x); subs=nonempty_subsets(n)
    J=[]
    for S in subs:
        row=[]
        for j in range(n):
            if j not in S:
                row.append(0.0)
            else:
                prod=1.0
                for i in S:
                    if i!=j: prod*=x[i]
                row.append(prod)
        J.append(row)
    A=[r[:] for r in J]; rank=0; col=0
    while rank<len(A) and col<n:
        piv=max(range(rank,len(A)),key=lambda r:abs(A[r][col]))
        if abs(A[piv][col])<1e-10:
            col+=1; continue
        A[rank],A[piv]=A[piv],A[rank]
        d=A[rank][col]
        for j in range(col,n): A[rank][j]/=d
        for r in range(len(A)):
            if r==rank: continue
            f=A[r][col]
            if abs(f)>1e-12:
                for j in range(col,n): A[r][j]-=f*A[rank][j]
        rank+=1; col+=1
    return rank

def relation_type_count(n,G):
    return len(subset_orbits(n,G))

def fit_feature_indices(task,G,indices,n=4,seed=0,samples_n=1000):
    rng=random.Random(seed)
    data=[]
    for _ in range(samples_n):
        x=[rng.uniform(-1.2,1.2) for _ in range(n)]
        data.append((x,task(x)))
    tr,te=data[:700],data[700:]
    def phi(x):
        allf=orbit_sum_features(x,G)
        return [allf[i] for i in indices]
    X=[[1.0]+phi(x) for x,y in tr]
    y=[y for x,y in tr]
    w=_solve_linear(X,y)
    def pred(x):
        row=[1.0]+phi(x)
        return sum(a*b for a,b in zip(w,row))
    tr_rmse=(sum((pred(x)-y)**2 for x,y in tr)/len(tr))**0.5
    te_rmse=(sum((pred(x)-y)**2 for x,y in te)/len(te))**0.5
    return {"indices":list(indices),"dim":len(indices),"train_rmse":tr_rmse,"hidden_rmse":te_rmse,"weights":w}

def minimal_task_sufficient_orbit_features(task,G,n=4,tol=1e-7,seed=0):
    m=len(subset_orbits(n,G))
    winners=[]
    for k in range(0,m+1):
        for inds in itertools.combinations(range(m),k):
            r=fit_feature_indices(task,G,inds,n=n,seed=seed)
            if r["hidden_rmse"]<=tol:
                winners.append(r)
        if winners:
            winners.sort(key=lambda r:(r["hidden_rmse"],r["indices"]))
            return {"min_dim":k,"best":winners[0],"all_minimal":[r["indices"] for r in winners]}
    return {"min_dim":None,"best":None,"all_minimal":[]}

def singleton_feature_indices(n,G):
    orbs=subset_orbits(n,G)
    return [i for i,O in enumerate(orbs) if len(O[0])==1]

def state_reconstruction_generator_hint(group_name):
    if group_name=="S4":
        return {"count":4,"generators":["e1","e2","e3","e4"],"status":"KNOWN_INVARIANT_RING_GENERATORS"}
    if group_name=="S2xS2":
        return {"count":4,"generators":["sA=x1+x2","pA=x1*x2","sB=x3+x4","pB=x3*x4"],"status":"KNOWN_BLOCK_GENERATORS"}
    if group_name=="IDENTITY":
        return {"count":4,"generators":["x1","x2","x3","x4"],"status":"TRIVIAL_LABELED_COORDINATES"}
    return {"count":None,"generators":[],"status":"NOT_DERIVED_HERE"}
