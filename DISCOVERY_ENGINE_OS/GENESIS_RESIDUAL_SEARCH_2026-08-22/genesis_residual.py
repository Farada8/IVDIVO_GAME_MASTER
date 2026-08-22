from __future__ import annotations
import itertools, math, random

def peer_genesis(xs, steps=1):
    xs=list(map(float,xs))
    history=[]
    for _ in range(steps):
        S=sum(xs)
        new=S
        xs.append(new)
        history.append({"created":new,"next_sum":sum(xs),"size":len(xs)})
    return {"elements":xs,"history":history}

def elementary_symmetric(xs,k):
    if k==0:
        return 1.0
    return sum(math.prod(c) for c in itertools.combinations(xs,k))

def symmetric_ladder(xs):
    xs=list(map(float,xs))
    return [elementary_symmetric(xs,k) for k in range(1,len(xs)+1)]

def subset_monomials(x,max_order=None):
    x=list(map(float,x))
    n=len(x)
    max_order=max_order or n
    feats=[]
    labels=[]
    for k in range(1,max_order+1):
        for idx in itertools.combinations(range(n),k):
            feats.append(math.prod(x[i] for i in idx))
            labels.append(idx)
    return feats,labels

def symmetric_features(x,max_order=None):
    n=len(x)
    max_order=max_order or n
    return [elementary_symmetric(x,k) for k in range(1,max_order+1)]

def _solve_linear(X,y,l2=1e-10):
    p=len(X[0])
    A=[[sum(row[i]*row[j] for row in X)+(l2 if i==j else 0.0) for j in range(p)] for i in range(p)]
    b=[sum(row[i]*yy for row,yy in zip(X,y)) for i in range(p)]
    M=[A[i]+[b[i]] for i in range(p)]
    for c in range(p):
        piv=max(range(c,p),key=lambda r:abs(M[r][c]))
        if abs(M[piv][c])<1e-14:
            continue
        M[c],M[piv]=M[piv],M[c]
        d=M[c][c]
        for j in range(c,p+1):
            M[c][j]/=d
        for r in range(p):
            if r==c: continue
            f=M[r][c]
            for j in range(c,p+1):
                M[r][j]-=f*M[c][j]
    return [M[i][p] for i in range(p)]

def fit_linear(features,y,l2=1e-10):
    X=[[1.0]+list(f) for f in features]
    w=_solve_linear(X,list(map(float,y)),l2=l2)
    pred=[sum(a*b for a,b in zip(w,row)) for row in X]
    mse=sum((a-b)**2 for a,b in zip(pred,y))/len(y)
    return {"weights":w,"mse":mse,"rmse":mse**0.5}

def _split(data,frac=.7):
    k=max(1,int(len(data)*frac))
    return data[:k],data[k:]

def residual_order_search(samples, mode="subset", max_order=None, train_fraction=.7):
    samples=list(samples)
    train,test=_split(samples,train_fraction)
    n=len(samples[0][0])
    max_order=max_order or n
    rows=[]
    prev=None
    for k in range(1,max_order+1):
        def phi(x):
            if mode=="symmetric":
                return symmetric_features(x,k)
            f,_=subset_monomials(x,k)
            return f
        fit=fit_linear([phi(x) for x,y in train],[y for x,y in train])
        w=fit["weights"]
        def pred(x):
            row=[1.0]+phi(x)
            return sum(a*b for a,b in zip(w,row))
        tr=fit["rmse"]
        te=(sum((pred(x)-y)**2 for x,y in test)/len(test))**0.5 if test else tr
        delta=None if prev is None else prev-te
        rows.append({"order":k,"train_rmse":tr,"test_rmse":te,"delta_test":delta,"weights":w})
        prev=te
    return rows

def first_effective_order(rows, relative_threshold=.2, absolute_threshold=1e-6):
    for r in rows[1:]:
        prev_rmse=r["test_rmse"] + (r["delta_test"] or 0)
        d=r["delta_test"] or 0
        if d>absolute_threshold and d/max(prev_rmse,1e-15)>=relative_threshold:
            return r["order"]
    return None

def make_dataset(kind,n=400,dim=4,seed=0,noise=0.0):
    rng=random.Random(seed)
    out=[]
    for _ in range(n):
        x=[rng.uniform(-1,1) for _ in range(dim)]
        if kind=="sum":
            y=sum(x)
        elif kind=="symmetric_pair":
            y=sum(a*b for a,b in itertools.combinations(x,2))
        elif kind=="symmetric_triple":
            y=sum(a*b*c for a,b,c in itertools.combinations(x,3))
        elif kind=="full_product":
            y=math.prod(x)
        elif kind=="specific_pair":
            y=x[0]*x[1]
        elif kind=="mixed":
            y=0.7*sum(x)+1.8*x[0]*x[1]-1.2*x[2]*x[3]+0.9*x[0]*x[1]*x[2]
        else:
            raise ValueError(kind)
        y += rng.gauss(0,noise)
        out.append((x,y))
    return out

def genesis_status(*,new_element_in_old_closure, expands_observable_structure=False):
    if new_element_in_old_closure and not expands_observable_structure:
        return "REPRESENTATIONAL_GENESIS_ONLY"
    if expands_observable_structure:
        return "STRUCTURAL_GENESIS_RELATIVE_TO_DECLARED_OBSERVABLES"
    return "UNRESOLVED"
