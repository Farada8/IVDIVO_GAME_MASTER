"""Dependency-aware execution classifier for NMM Cycle5 prompts 01-32."""
from __future__ import annotations

EXTERNAL_PROVIDER=set(range(1,7))|set(range(9,16+1))
EXTERNAL_HUMAN=set(range(17,25))|{28,29,30,31}
ENGINEERING_ONLY={7,8,12,25,26,27,32}

def classify(prompt_id:int, *, credential_present:bool, provider_snapshot_present:bool, real_human_rows:int, source_bound:bool=False, finalists:int=0):
    if not 1 <= prompt_id <= 32:
        raise ValueError('PROMPT_ID_OUT_OF_RANGE')
    if prompt_id==1:
        return {'status':'HOLD_EXTERNAL_CREDENTIAL' if not credential_present else 'READY_PROVIDER_PREFLIGHT'}
    if prompt_id in {2,3,4,5,6,9,10,11,13,14,15,16}:
        if not provider_snapshot_present:
            return {'status':'HOLD_DEP_PROVIDER_SNAPSHOT'}
        return {'status':'READY_EXTERNAL_PROVIDER_STEP'}
    if prompt_id==8:
        return {'status':'PASS_ENGINEERING_SOURCE_BOUND' if source_bound else 'HOLD_SOURCE_BINDING'}
    if prompt_id in {17,18,19,20,21,22,23,24}:
        return {'status':'HOLD_EXTERNAL_HUMAN' if real_human_rows<=0 else 'READY_HUMAN_STEP'}
    if prompt_id in {28,29,30}:
        return {'status':'HOLD_EXTERNAL_HUMAN' if real_human_rows<=0 else 'READY_DEVICE_STEP'}
    if prompt_id==31:
        return {'status':'HOLD_NO_FINALISTS' if finalists<=0 else 'READY_HASH_BIND'}
    return {'status':'PASS_ENGINEERING'}
