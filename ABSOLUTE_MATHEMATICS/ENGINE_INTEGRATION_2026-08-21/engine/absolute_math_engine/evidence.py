from __future__ import annotations
import hashlib, json, time
from dataclasses import asdict
from .models import EvidenceRecord

CLAIM_CAPS={
    "SYNTHETIC_CONTROL":{"supports":["ALGORITHM_BEHAVIOR","COUNTEREXAMPLE_IN_FIXTURE"],"cannot":["NATURE","MARKET","HUMAN_QUALITY"]},
    "FORMAL_PROOF":{"supports":["THEOREM_UNDER_ASSUMPTIONS"],"cannot":["NOVELTY","EMPIRICAL_GENERALITY"]},
    "LITERATURE":{"supports":["PRIOR_ART","ESTABLISHED_ANALOGUE"],"cannot":["NEW_THEOREM_VALIDITY"]},
    "HUMAN_SIGNAL":{"supports":["HUMAN_RESPONSE"],"cannot":["UNIVERSAL_QUALITY"]},
}

def sha256_json(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()

class EvidenceLedger:
    def __init__(self): self.records=[]
    def append(self,record:EvidenceRecord): self.records.append(record)
    def snapshot(self):
        payload=[asdict(r) for r in self.records]
        return {"records":payload,"sha256":sha256_json(payload),"count":len(payload)}

class ClaimLedger:
    def __init__(self): self.claims={}
    def upsert(self,claim_id,status,text,assumptions=None,prohibited_overclaim=None):
        self.claims[claim_id]={"claim_id":claim_id,"status":status,"text":text,
            "assumptions":list(assumptions or []),"prohibited_overclaim":prohibited_overclaim,
            "updated_at":time.time()}
    def snapshot(self): return {"claims":list(self.claims.values()),"sha256":sha256_json(self.claims)}
