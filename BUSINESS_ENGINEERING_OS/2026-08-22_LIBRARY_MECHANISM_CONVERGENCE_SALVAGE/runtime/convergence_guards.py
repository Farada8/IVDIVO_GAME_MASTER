#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

@dataclass(frozen=True)
class NamespaceClaim:
    namespace: str
    semantic_owner: str
    source_ref: str
    status: str = "CLAIMED"

def _norm(value: str) -> str:
    return value.strip().upper()

def namespace_collision_gate(proposed: NamespaceClaim, existing: Sequence[NamespaceClaim]) -> dict:
    pns, powner = _norm(proposed.namespace), _norm(proposed.semantic_owner)
    collisions, compatible = [], []
    for claim in existing:
        if _norm(claim.namespace) != pns:
            continue
        row = {"namespace": claim.namespace, "semantic_owner": claim.semantic_owner, "source_ref": claim.source_ref, "status": claim.status}
        (compatible if _norm(claim.semantic_owner) == powner else collisions).append(row)
    if collisions:
        return {"status":"HOLD_NAMESPACE_COLLISION","allocation_allowed":False,"auto_rename":False,"collisions":collisions,"compatible_claims":compatible}
    return {"status":"PASS_NAMESPACE_AVAILABLE_OR_SAME_OWNER","allocation_allowed":True,"auto_rename":False,"collisions":[],"compatible_claims":compatible}

def concurrent_authority_restore(*, expected_main_sha: str, observed_main_sha: str, expected_library_physical_files: int, observed_library_physical_files: int, expected_open_pr_heads: Mapping[int,str], observed_open_pr_heads: Mapping[int,str], drive_current_pointer: str|None) -> dict:
    drift = {}
    if expected_main_sha != observed_main_sha:
        drift["main_sha"] = {"expected": expected_main_sha, "observed": observed_main_sha}
    if expected_library_physical_files != observed_library_physical_files:
        drift["library_physical_files"] = {"expected": expected_library_physical_files, "observed": observed_library_physical_files}
    pr_drift = {}
    for number, expected_head in expected_open_pr_heads.items():
        observed = observed_open_pr_heads.get(number)
        if observed != expected_head:
            pr_drift[str(number)] = {"expected": expected_head, "observed": observed}
    if pr_drift:
        drift["open_pr_heads"] = pr_drift
    if not drive_current_pointer:
        drift["drive_current_pointer"] = {"expected":"NONEMPTY","observed":drive_current_pointer}
    if drift:
        return {"status":"HOLD_AUTHORITY_DRIFT_RECONCILE_BEFORE_WRITE","write_allowed":False,"authority_promotion":False,"drift":drift}
    return {"status":"PASS_FRESH_AUTHORITY_SNAPSHOT","write_allowed":True,"authority_promotion":False,"drift":{}}

def dataset_neq_engine(*, object_count: int, persisted: bool, has_unique_runtime_contract: bool) -> dict:
    if object_count < 0:
        raise ValueError("object_count must be nonnegative")
    return {"status":"ENGINE_REVIEW_CANDIDATE" if has_unique_runtime_contract else "ADAPTER_OR_EVIDENCE_PACK","object_count":object_count,"persisted":bool(persisted),"has_unique_runtime_contract":bool(has_unique_runtime_contract),"auto_core_promotion":False}

def library_delta_after_cycle_gate(*, prior_count: int, current_count: int, enumerated_delta_ids: Iterable[str]) -> dict:
    ids = tuple(dict.fromkeys(str(x) for x in enumerated_delta_ids))
    if prior_count < 0 or current_count < prior_count:
        return {"status":"FAIL_INVALID_LIBRARY_COUNTS","closure_allowed":False}
    expected = current_count-prior_count
    if len(ids) != expected:
        return {"status":"HOLD_LIBRARY_DELTA_NOT_ENUMERATED","expected_delta":expected,"observed_unique_delta_ids":len(ids),"closure_allowed":False}
    return {"status":"PASS_LIBRARY_DELTA_ENUMERATED","expected_delta":expected,"observed_unique_delta_ids":len(ids),"closure_allowed":True}
