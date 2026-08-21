#!/usr/bin/env python3
"""IVDIVO production proof-chain validator.

Candidate utility. It does not decide canon or grant Founder/human/provider authority.
It checks that a claimed gate verdict is supported by explicit evidence objects and
artifact readback identities.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

HUMAN_SOURCE_TYPES = {"HUMAN_NATIVE", "PRACTITIONER", "BLIND_LISTENER"}
EXTERNAL_LIVE_TYPES = HUMAN_SOURCE_TYPES | {"PROVIDER_RESPONSE", "MARKET_RESPONSE"}

def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def validate(payload: dict) -> dict:
    errors, holds, warnings = [], [], []
    evidence = payload.get("evidence")
    claims = payload.get("claims")
    gates = payload.get("gates")
    artifacts = payload.get("artifacts", [])
    if not isinstance(evidence, list) or not isinstance(claims, list) or not isinstance(gates, list):
        return {"status":"FAIL_CLOSED","errors":["MISSING_CORE_ARRAYS"],"holds":[],"warnings":[]}

    evidence_by_id = {}
    for ev in evidence:
        if not isinstance(ev, dict) or not ev.get("evidence_id"):
            errors.append("INVALID_EVIDENCE_OBJECT")
            continue
        eid = str(ev["evidence_id"])
        if eid in evidence_by_id:
            errors.append(f"DUPLICATE_EVIDENCE_ID:{eid}")
            continue
        evidence_by_id[eid] = ev
        if ev.get("source_type") in {"EXTERNAL_AI", "INFERENCE"} and ev.get("authority_weight", 0) > 60:
            warnings.append(f"MODEL_OR_INFERENCE_HIGH_WEIGHT:{eid}")

    artifact_by_id = {}
    for art in artifacts:
        if not isinstance(art, dict) or not art.get("artifact_id"):
            errors.append("INVALID_ARTIFACT_OBJECT")
            continue
        aid = str(art["artifact_id"])
        if aid in artifact_by_id:
            errors.append(f"DUPLICATE_ARTIFACT_ID:{aid}")
            continue
        artifact_by_id[aid] = art
        expected = art.get("sha256")
        readback = art.get("readback_sha256")
        if expected and readback and expected != readback:
            errors.append(f"ARTIFACT_READBACK_HASH_MISMATCH:{aid}")

    claim_results = {}
    for claim in claims:
        cid = str(claim.get("claim_id", ""))
        if not cid:
            errors.append("CLAIM_WITHOUT_ID")
            continue
        refs = claim.get("evidence_ids", [])
        min_weight = int(claim.get("min_authority_weight", 0))
        required_types = set(claim.get("required_source_types", []))
        require_human = bool(claim.get("requires_human_evidence", False))
        require_live = bool(claim.get("requires_live_external_evidence", False))
        required_artifacts = claim.get("required_artifact_ids", [])
        missing_refs = [eid for eid in refs if eid not in evidence_by_id]
        if missing_refs:
            claim_results[cid] = {"status":"FAIL", "reason":"MISSING_EVIDENCE", "missing":missing_refs}
            continue
        used = [evidence_by_id[eid] for eid in refs]
        pass_used = [ev for ev in used if ev.get("status") == "PASS" and int(ev.get("authority_weight",0)) >= min_weight]
        fail_used = [ev for ev in used if ev.get("status") in {"FAIL","REJECTED"}]
        if fail_used:
            claim_results[cid] = {"status":"FAIL","reason":"CONTRADICTING_FAIL_EVIDENCE","evidence":[e["evidence_id"] for e in fail_used]}
            continue
        if required_types and not required_types.intersection({ev.get("source_type") for ev in pass_used}):
            claim_results[cid] = {"status":"HOLD","reason":"REQUIRED_SOURCE_TYPE_MISSING"}
            continue
        if require_human and not any(ev.get("source_type") in HUMAN_SOURCE_TYPES for ev in pass_used):
            claim_results[cid] = {"status":"HOLD","reason":"HUMAN_EVIDENCE_REQUIRED"}
            continue
        if require_live and not any(ev.get("source_type") in EXTERNAL_LIVE_TYPES for ev in pass_used):
            claim_results[cid] = {"status":"HOLD","reason":"LIVE_EXTERNAL_EVIDENCE_REQUIRED"}
            continue
        missing_artifacts = [aid for aid in required_artifacts if aid not in artifact_by_id]
        bad_artifacts = [aid for aid in required_artifacts if aid in artifact_by_id and artifact_by_id[aid].get("sha256") != artifact_by_id[aid].get("readback_sha256")]
        if missing_artifacts:
            claim_results[cid] = {"status":"HOLD","reason":"REQUIRED_ARTIFACT_MISSING","missing":missing_artifacts}
            continue
        if bad_artifacts:
            claim_results[cid] = {"status":"FAIL","reason":"ARTIFACT_READBACK_FAILED","artifacts":bad_artifacts}
            continue
        if not pass_used:
            claim_results[cid] = {"status":"HOLD","reason":"NO_QUALIFYING_PASS_EVIDENCE"}
            continue
        claim_results[cid] = {"status":"PASS","evidence":[e["evidence_id"] for e in pass_used]}

    gate_results = {}
    for gate in gates:
        gid = str(gate.get("gate_id", ""))
        if not gid:
            errors.append("GATE_WITHOUT_ID")
            continue
        required_claims = gate.get("required_claim_ids", [])
        unresolved = [cid for cid in required_claims if cid not in claim_results]
        if unresolved:
            gate_results[gid] = {"status":"FAIL_CLOSED","reason":"CLAIM_RESULT_MISSING","claims":unresolved}
            continue
        states = [claim_results[cid]["status"] for cid in required_claims]
        declared = gate.get("declared_verdict")
        if "FAIL" in states or "FAIL_CLOSED" in states:
            computed = "FAIL"
        elif "HOLD" in states:
            computed = "HOLD"
        else:
            computed = "PASS"
        if gate.get("human_approval_required"):
            approval_id = gate.get("human_approval_evidence_id")
            approval = evidence_by_id.get(str(approval_id)) if approval_id else None
            if not approval or approval.get("status") != "PASS" or approval.get("source_type") not in (HUMAN_SOURCE_TYPES | {"FOUNDER"}):
                computed = "HOLD"
                holds.append(f"HUMAN_OR_FOUNDER_APPROVAL_REQUIRED:{gid}")
        if declared and declared != computed:
            errors.append(f"GATE_VERDICT_MISMATCH:{gid}:declared={declared}:computed={computed}")
        gate_results[gid] = {"status":computed,"required_claim_ids":required_claims}

    if errors:
        status = "FAIL_CLOSED"
    elif any(v["status"] == "FAIL" for v in gate_results.values()):
        status = "FAIL"
    elif any(v["status"] == "HOLD" for v in gate_results.values()) or holds:
        status = "HOLD"
    else:
        status = "PASS"

    proof_identity_payload = {
        "authority_snapshot": payload.get("authority_snapshot"),
        "claim_results": claim_results,
        "gate_results": gate_results,
        "artifact_identities": sorted(
            [(aid, a.get("sha256"), a.get("readback_sha256")) for aid, a in artifact_by_id.items()]
        ),
    }
    proof_id = _sha256_text(json.dumps(proof_identity_payload, sort_keys=True, separators=(",",":")))
    return {
        "status":status,
        "proof_id":proof_id,
        "claim_results":claim_results,
        "gate_results":gate_results,
        "errors":errors,
        "holds":holds,
        "warnings":warnings,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status":"FAIL_CLOSED","errors":[f"INPUT_ERROR:{exc}"]}))
        return 2
    result = validate(payload)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] in {"PASS","HOLD"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
