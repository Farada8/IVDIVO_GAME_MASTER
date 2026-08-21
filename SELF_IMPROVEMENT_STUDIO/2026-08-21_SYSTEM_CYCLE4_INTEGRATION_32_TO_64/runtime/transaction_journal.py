from __future__ import annotations
import uuid
def begin(targets:list[str])->dict:return {"tx_id":str(uuid.uuid4()),"status":"PREPARED","targets":targets,"applied":[],"failed":[],"rollback":[]}
def mark_applied(tx:dict,target:str,old_hash:str,new_hash:str):
    tx=dict(tx);tx["applied"]=list(tx["applied"])+[{"target":target,"old_hash":old_hash,"new_hash":new_hash}];tx["status"]="PARTIAL" if len(tx["applied"])<len(tx["targets"]) else "APPLIED_PENDING_READBACK";return tx
def mark_failed(tx:dict,target:str,reason:str):
    tx=dict(tx);tx["failed"]=list(tx["failed"])+[{"target":target,"reason":reason}];tx["status"]="REPAIR_REQUIRED" if tx["applied"] else "ABORTED";return tx
def finalize(tx:dict,readback_ok:bool):
    tx=dict(tx);tx["status"]="COMMITTED_VERIFIED" if readback_ok and not tx["failed"] and len(tx["applied"])==len(tx["targets"]) else "REPAIR_REQUIRED";return tx
