from __future__ import annotations
import hashlib,json
REQUIRED={'DETERMINISTIC':['source','mutation','asset_ingest'],'PROVIDER':['snapshot','bindings','live_canary'],'HUMAN':['blind_listener'],'SPECIALIST':['medical','legal'],'ECONOMICS':['measured_cost']}
def build(proofs):
 classes={}; missing=[]
 for cls,keys in REQUIRED.items():
  classes[cls]={k:bool(proofs.get(k)) for k in keys}
  missing += [f'{cls}:{k}' for k in keys if not proofs.get(k)]
 payload={'schema':'NMM_PROOF_BUNDLE_v1','classes':classes,'missing':missing,'release':'NO_GO' if missing else 'GO_FOR_FOUNDER_RELEASE_DECISION'}
 payload['bundle_sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
 return payload
