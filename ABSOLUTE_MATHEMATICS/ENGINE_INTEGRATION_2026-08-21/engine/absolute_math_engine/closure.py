from __future__ import annotations

def total_variation(p,q):
    return 0.5*sum(abs(a-b) for a,b in zip(p,q))

def matvec(v,P):
    return [sum(v[i]*P[i][j] for i in range(len(v))) for j in range(len(P[0]))]

def dobrushin(P):
    return 0.5*max(sum(abs(P[i][k]-P[j][k]) for k in range(len(P[0]))) for i in range(len(P)) for j in range(len(P)))

def rollout_error(initial,true_P,approx_P,horizons=(1,2,4,8,16)):
    t=max(horizons); a=list(initial); b=list(initial); out={}
    for step in range(1,t+1):
        a=matvec(a,true_P); b=matvec(b,approx_P)
        if step in horizons: out[step]=total_variation(a,b)
    return out

def contractive_bound(epsilon,alpha,t):
    if alpha<0 or alpha>1: raise ValueError("alpha must be in [0,1]")
    return epsilon*t if alpha==1 else epsilon*(1-alpha**t)/(1-alpha)

def closure_contract(one_step_defect,metric,normalization,horizon,stability):
    return {"one_step_defect":float(one_step_defect),"metric":metric,"normalization":normalization,
            "validated_horizon":int(horizon),"stability":stability}
