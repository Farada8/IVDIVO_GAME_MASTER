from __future__ import annotations
from collections import Counter
from math import log2

def entropy(xs):
    xs=list(xs); n=len(xs)
    if n==0: return 0.0
    c=Counter(xs)
    return -sum((v/n)*log2(v/n) for v in c.values())

def mutual_information(x,y):
    return entropy(x)+entropy(y)-entropy(zip(x,y))

def conditional_mutual_information(x,y,z):
    return entropy(zip(x,z))+entropy(zip(y,z))-entropy(z)-entropy(zip(x,y,z))

def sufficiency_gate(future, omitted, state, threshold_bits=0.01, gate_name="CONDITIONAL_INFORMATION"):
    value=conditional_mutual_information(future,omitted,state)
    return {"gate":gate_name,"passed":value<=threshold_bits,
            "metric_bits":value,"threshold_bits":threshold_bits}
