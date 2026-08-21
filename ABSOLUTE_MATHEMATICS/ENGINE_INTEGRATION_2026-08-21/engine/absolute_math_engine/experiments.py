from __future__ import annotations
import hashlib, json, time

class ExperimentRegistry:
    def __init__(self): self.items={}
    def preregister(self,experiment_id,hypothesis,metrics,thresholds,fixtures,allowed_followups=None):
        if experiment_id in self.items: raise ValueError("DUPLICATE_EXPERIMENT_ID")
        payload={"experiment_id":experiment_id,"hypothesis":hypothesis,"metrics":metrics,
                 "thresholds":thresholds,"fixtures":fixtures,"allowed_followups":list(allowed_followups or []),
                 "status":"PREREGISTERED","created_at":time.time()}
        payload["prereg_hash"]=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        self.items[experiment_id]=payload
        return payload
    def record(self,experiment_id,results,deviations=None):
        item=self.items[experiment_id]
        item["results"]=results; item["deviations"]=list(deviations or []); item["status"]="COMPLETED"
        return item
