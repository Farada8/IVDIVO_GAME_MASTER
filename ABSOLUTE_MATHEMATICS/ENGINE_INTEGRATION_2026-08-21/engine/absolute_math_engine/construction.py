from __future__ import annotations
from math import ceil, log

def locality_depth(distance,radius):
    if radius<=0: raise ValueError("radius must be >0")
    return ceil(distance/radius)

def arity_depth(n_inputs,arity):
    if n_inputs<=1: return 0
    if arity<2: raise ValueError("arity must be >=2")
    return ceil(log(n_inputs,arity))

def spectrum(*,n_inputs,distance,radius,arity,communication_bits=None,memory_bits=None,time_cost=None):
    ld=locality_depth(distance,radius); ad=arity_depth(n_inputs,arity)
    return {"locality_depth_lb":ld,"arity_depth_lb":ad,"combined_depth_lb":max(ld,ad),
            "communication_bits":communication_bits,"memory_bits":memory_bits,"time_cost":time_cost}

def pareto_dominates(a,b,keys):
    return all(a[k]<=b[k] for k in keys) and any(a[k]<b[k] for k in keys)
