"""Cycle5 external-evidence readiness vector."""
from __future__ import annotations
DIMS=('provider_snapshot','cast_metadata','s0_manifest','provider_canaries','alignment','human_headphones','human_phone','multi_listener','finalists','asset_ledger')
def compile(states:dict)->dict:
    out={k:states.get(k,'UNKNOWN') for k in DIMS}
    out['provider_truth']=all(out[k]=='PASS' for k in ('provider_snapshot','cast_metadata','provider_canaries','alignment'))
    out['human_truth']=all(out[k]=='PASS' for k in ('human_headphones','human_phone','multi_listener','finalists','asset_ledger'))
    out['cycle5_external_ready']=out['provider_truth'] and out['human_truth'] and out['s0_manifest']=='PASS'
    out['release_ready']=False
    return out
