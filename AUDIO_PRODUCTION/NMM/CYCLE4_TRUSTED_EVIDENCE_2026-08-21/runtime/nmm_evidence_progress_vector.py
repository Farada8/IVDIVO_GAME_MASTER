"""Vector readiness: never compress internal proof and external truth into one misleading PASS."""
from __future__ import annotations
DIMS=("source_integrity","deterministic_regression","cross_storage_parity","provider_truth","human_truth","specialist_truth","economics_truth")
def compile_vector(evidence:dict)->dict:
    v={k:evidence.get(k,"UNKNOWN") for k in DIMS}
    internal=all(v[k]=="PASS" for k in ("source_integrity","deterministic_regression"))
    external=all(v[k]=="PASS" for k in ("provider_truth","human_truth"))
    release=all(v[k]=="PASS" for k in DIMS)
    return {"dimensions":v,"internal_engineering_ready":internal,"external_empirical_ready":external,"release_ready":release,
            "gate":"RELEASE_READY" if release else "EVIDENCE_INCOMPLETE"}
