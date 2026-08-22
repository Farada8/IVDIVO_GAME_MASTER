import math, itertools, random

def exact_monogenic_squaring(index, period):
    a=0; q=period
    while q%2==0:
        a+=1; q//=2
    k=0
    while (1<<k)<index: k+=1
    tail=max(a,k)
    if q==1: cycle=1
    else:
        r=2%q; cycle=1
        while r!=1:
            r=(2*r)%q; cycle+=1
    return tail,cycle

def candidate_ops():
    return {
      'ADD':lambda a,b:a+b,
      'MUL':lambda a,b:a*b,
      'MAX':lambda a,b:max(a,b),
      'MIN':lambda a,b:min(a,b),
      'MEAN':lambda a,b:(a+b)/2,
      'RMS':lambda a,b:math.sqrt((a*a+b*b)/2),
      'HARMONIC':lambda a,b:2*a*b/(a+b),
      'PROB_OR':lambda a,b:a+b-a*b,
      'XOR_POLY':lambda a,b:a+b-2*a*b,
    }

def best_single_probe(grid):
    ops=candidate_ops(); best=None
    for a,b in itertools.product(grid,repeat=2):
        if a==b: continue
        vals={n:f(a,b) for n,f in ops.items()}
        sep=min(abs(x-y) for x,y in itertools.combinations(vals.values(),2))
        if best is None or sep>best[0]: best=(sep,(a,b),vals)
    return best

def estimate_generator_from_identity(op, identity, grid, h=1e-5):
    d=[(op(x,identity+h)-op(x,identity-h))/(2*h) for x in grid]
    inv=[1/v for v in d]; phi=[0.0]
    for i in range(1,len(grid)):
        dx=grid[i]-grid[i-1]
        phi.append(phi[-1]+.5*(inv[i]+inv[i-1])*dx)
    return phi

def addmul(lam): return lambda a,b:a+b+lam*a*b

def lp(p): return lambda a,b:(a**p+b**p)**(1/p)

def corr_union(c): return lambda p,q:p+q-((1-c)*p*q+c*min(p,q))

def rmse(op,pairs,ys):
    return (sum((op(a,b)-y)**2 for (a,b),y in zip(pairs,ys))/len(ys))**.5

def grammar_search(pairs,ys):
    rows=[]
    for lam in [i/100 for i in range(-100,101,2)]: rows.append(('ADDMUL',lam,rmse(addmul(lam),pairs,ys)))
    for p in [0.5+i*.05 for i in range(51)]: rows.append(('LP',p,rmse(lp(p),pairs,ys)))
    for c in [i/100 for i in range(101)]: rows.append(('CORR_UNION',c,rmse(corr_union(c),pairs,ys)))
    return min(rows,key=lambda r:r[2])

def diagonal_family_lambda(xs,ys):
    return sum((y-2*x)*x*x for x,y in zip(xs,ys))/sum(x**4 for x in xs)

# Contract: diagonal identification is only relative to a preregistered identifiable family.
def diagonal_policy(predeclared, identifiable):
    return 'IDENTIFIED_WITHIN_PREDECLARED_FAMILY' if predeclared and identifiable else 'MIXED_PROBES_REQUIRED_FOR_UNRESTRICTED_OPERATION'
