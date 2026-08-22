from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Iterable, Sequence

class Cycle5Error(RuntimeError): pass
class SplitBrainError(Cycle5Error): pass
class StaleFactLockError(Cycle5Error): pass
class MutationGuardError(Cycle5Error): pass
class StateDriftError(Cycle5Error): pass

class EvidenceClass(IntEnum):
    NONE=0; MODEL=1; DRY=2; MACHINE=3; PROVIDER=4; HUMAN=5; FOUNDER=6

CLAIM_FLOORS={"MODEL_FINDING":EvidenceClass.MODEL,"DRY_GATE_PASS":EvidenceClass.DRY,"MACHINE_GATE_PASS":EvidenceClass.MACHINE,"PROVIDER_RESULT":EvidenceClass.PROVIDER,"HUMAN_PASS":EvidenceClass.HUMAN,"FOUNDER_LOCK":EvidenceClass.FOUNDER}

@dataclass(frozen=True)
class SurfaceRecord:
    surface_id:str; scope:str; authority_rank:int; revision:str; state_hash:str; supersedes:tuple[str,...]=()

def resolve_current_surface(records:Sequence[SurfaceRecord],scope:str)->SurfaceRecord:
    candidates=[r for r in records if r.scope==scope]
    if not candidates: raise SplitBrainError(f"NO_SURFACE:{scope}")
    rank=max(r.authority_rank for r in candidates); top=[r for r in candidates if r.authority_rank==rank]
    if len(top)==1: return top[0]
    for c in top:
        others={r.surface_id for r in top if r.surface_id!=c.surface_id}
        if others and others.issubset(set(c.supersedes)): return c
    if len({r.state_hash for r in top})==1: return sorted(top,key=lambda r:(r.revision,r.surface_id))[-1]
    raise SplitBrainError("SPLIT_BRAIN:"+",".join(sorted(r.surface_id for r in top)))

def claim_allowed(evidence:EvidenceClass,claim:str)->bool:
    if claim not in CLAIM_FLOORS: raise KeyError(f"UNKNOWN_CLAIM:{claim}")
    return evidence>=CLAIM_FLOORS[claim]

@dataclass(frozen=True)
class ReadinessVector:
    story_gate:bool=False; founder_lock:bool=False; provider:bool=False; human:bool=False; market:bool=False
    def invariant_ok(self)->bool: return not (self.founder_lock and not self.story_gate)

@dataclass(frozen=True)
class FactLock:
    fact_id:str; value_hash:str; version:int; owner:str
    def commit(self,expected_hash:str,expected_version:int,new_hash:str)->"FactLock":
        if expected_hash!=self.value_hash or expected_version!=self.version:
            raise StaleFactLockError(f"STALE_FACT_LOCK:{self.fact_id}:expected={expected_version}/{expected_hash}:actual={self.version}/{self.value_hash}")
        return FactLock(self.fact_id,new_hash,self.version+1,self.owner)

@dataclass(frozen=True)
class EvidenceRecord:
    record_id:str; family_id:str; evidence_class:EvidenceClass; source_id:str

def independent_family_count(records:Iterable[EvidenceRecord])->int: return len({r.family_id for r in records})
def strongest_family_evidence(records:Iterable[EvidenceRecord])->dict[str,EvidenceClass]:
    result={}
    for r in records: result[r.family_id]=max(result.get(r.family_id,EvidenceClass.NONE),r.evidence_class)
    return result

@dataclass(frozen=True)
class MutationIntent:
    target:str; expected_hash:str; new_hash:str; reversible:bool=True; approval_required:bool=False
    def preflight(self,actual_hash:str,approved:bool=False)->None:
        if actual_hash!=self.expected_hash: raise MutationGuardError(f"STALE_TARGET:{self.target}:expected={self.expected_hash}:actual={actual_hash}")
        if self.approval_required and not approved: raise MutationGuardError(f"APPROVAL_REQUIRED:{self.target}")

@dataclass
class TransactionJournal:
    transaction_id:str; targets:tuple[str,...]; status:str="PREPARED"; applied:list[str]=field(default_factory=list); acknowledgements:set[str]=field(default_factory=set); failure:str|None=None
    def record_write(self,target:str,acknowledgement:str)->None:
        if target not in self.targets: raise MutationGuardError(f"OUT_OF_SCOPE_TARGET:{target}")
        if acknowledgement in self.acknowledgements: return
        self.acknowledgements.add(acknowledgement)
        if target not in self.applied: self.applied.append(target)
        self.status="COMMITTED" if set(self.applied)==set(self.targets) else "PARTIAL"
    def mark_failure(self,reason:str)->None:
        self.failure=reason; self.status="REPAIR_REQUIRED" if self.applied else "FAILED_NO_WRITE"
    def next_unapplied(self)->list[str]: return [t for t in self.targets if t not in self.applied]
    def replay_safe(self,target:str,acknowledgement:str)->bool: return target in self.targets and acknowledgement in self.acknowledgements

REQUIRED_STATE_FIELDS={"schema_version","status","authority_order","resume_algorithm"}
def validate_state_shape(state:dict)->None:
    missing=sorted(REQUIRED_STATE_FIELDS-set(state))
    if missing: raise StateDriftError("MISSING_FIELDS:"+",".join(missing))
    if not isinstance(state["authority_order"],list) or not state["authority_order"]: raise StateDriftError("INVALID_AUTHORITY_ORDER")
    if not isinstance(state["resume_algorithm"],list) or not state["resume_algorithm"]: raise StateDriftError("INVALID_RESUME_ALGORITHM")

@dataclass(frozen=True)
class RoutedTask:
    task_id:str; priority:int; information_value:float; external_blocked:bool=False; meta:bool=False

def select_next_task(tasks:Sequence[RoutedTask],system_fatal:bool=False)->RoutedTask|None:
    ready=[t for t in tasks if not t.external_blocked]
    if not ready: return None
    p1p2=[t for t in ready if t.priority in (1,2) and not t.meta]
    if p1p2 and not system_fatal: return sorted(p1p2,key=lambda t:(t.priority,-t.information_value,t.task_id))[0]
    return sorted(ready,key=lambda t:(t.priority,-t.information_value,t.task_id))[0]
