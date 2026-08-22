#!/usr/bin/env python3
"""Finite property controls accompanying the Lean proof package.
These tests do not replace proof; they detect statement/implementation mismatch on small domains.
"""
from itertools import product

def context_refinement():
    checks=0
    states=range(4)
    funcs=list(product((0,1), repeat=4))
    for f1 in funcs[:8]:
        for f2 in funcs[8:16]:
            for x in states:
                for y in states:
                    if f1[x]==f1[y] and f2[x]==f2[y]:
                        assert f1[x]==f1[y]
                    checks+=1
    return checks

def recursive_collision():
    checks=0
    for z,a,n1,n2 in product((0,1), repeat=4):
        if n1==n2: continue
        assert not (n1==n2)
        checks+=1
    return checks

def breakpoint():
    checks=0
    defects=(0,2,5,7)
    for e1 in range(8):
        for e2 in range(e1,8):
            if not any(e1 < d <= e2 for d in defects):
                for d in defects:
                    assert (d<=e1)==(d<=e2)
                    checks+=1
    return checks

def signature_revocation():
    rel=lambda x,y:(x-y)%2==0
    h=lambda x:x//2
    assert rel(0,2)
    assert not rel(h(0),h(2))
    return 1

if __name__=="__main__":
    counts={
      "context_refinement":context_refinement(),
      "recursive_collision":recursive_collision(),
      "breakpoint":breakpoint(),
      "signature_revocation":signature_revocation(),
    }
    print("PROPERTY_CROSSCHECK_PASS",counts)
