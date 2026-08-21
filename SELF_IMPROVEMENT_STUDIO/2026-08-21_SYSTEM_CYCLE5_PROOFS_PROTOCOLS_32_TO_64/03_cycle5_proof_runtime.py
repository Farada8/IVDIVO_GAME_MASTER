"""IVDIVO Cycle5 proof/enforcement runtime — WORKING PILOT / NOT CURRENT AUTHORITY."""
from __future__ import annotations
import hashlib, json, re, zipfile

# 01 Registry identity

def validate_registry_family(records):
    seen, dup = {}, []
    for r in records:
        cid = r["candidate_id"]
        if cid in seen:
            dup.append(cid)
        else:
            seen[cid] = r
    return {"status": "PASS" if not dup else "FAIL_DUPLICATE_ID", "duplicates": sorted(set(dup))}

def allocate_next_candidate_id(records):
    check = validate_registry_family(records)
    if check["status"] != "PASS":
        return {"status": "HOLD_COLLISION_PRESENT", "duplicates": check["duplicates"], "candidate_id": None}
    nums=[]
    for r in records:
        m=re.fullmatch(r"SI-(\d{4})", r["candidate_id"])
        if m:
            nums.append(int(m.group(1)))
    return {"status":"PASS","candidate_id":f"SI-{max(nums or [0])+1:04d}"}

# 02 Durable transaction reconciliation

def reconcile_transaction(stores, txn_id):
    rows=[s for s in stores if s.get("txn_id")==txn_id]
    if not rows:
        return {"status":"HOLD_NO_TRANSACTION"}
    states={r.get("state") for r in rows}
    if states=={"COMMITTED_VERIFIED"}:
        return {"status":"COMPLETE","repair":[]}
    if "REPAIR_REQUIRED" in states or len(states)>1:
        return {"status":"REPAIR_REQUIRED","repair":[r["store"] for r in rows if r.get("state")!="COMMITTED_VERIFIED"]}
    return {"status":"INCOMPLETE","repair":[r["store"] for r in rows]}

# 03 Checkpoint lineage

def _canonical_hash(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def make_checkpoint(seq, payload, parent_hash=None):
    body={"seq":seq,"payload":payload,"parent_hash":parent_hash}
    body["hash"]=_canonical_hash(body)
    return body

def validate_checkpoint_chain(items):
    prev=None
    for i,x in enumerate(items):
        body={"seq":x["seq"],"payload":x["payload"],"parent_hash":x.get("parent_hash")}
        if _canonical_hash(body)!=x.get("hash"):
            return {"status":"FAIL_TAMPER","index":i}
        if x.get("parent_hash")!=prev:
            return {"status":"FAIL_LINEAGE","index":i}
        prev=x["hash"]
    return {"status":"PASS","head":prev}

# 04 Interruption learning

def classify_interruption(event):
    required={"interruption_type","durable_before","durable_after","duplicate_work","recovery_minutes"}
    if not required.issubset(event):
        return {"status":"HOLD_MISSING_FIELDS"}
    if event["durable_after"] < event["durable_before"]:
        return {"status":"FAIL_STATE_LOSS"}
    lesson="CHECKPOINT_HELPED" if event["duplicate_work"] is False else "CHECKPOINT_INSUFFICIENT"
    return {"status":"PASS_OBSERVATION","lesson":lesson,"claim":"ONE_INCIDENT_ONLY"}

# 05 Book -> SI bridge

def reconcile_book_candidate(candidate, existing_mechanisms):
    key=candidate["mechanism_key"]
    if key in existing_mechanisms:
        return {"status":"MERGE_WITH_EXISTING","target":existing_mechanisms[key],"promotion":False}
    if candidate.get("evidence_state") in {"SINGLE_BOOK_BOUNDED_PILOT_PASS","PROJECT_PILOT_PASS"}:
        return {"status":"HOLD_FOR_CROSS_PROJECT_TEST","target":None,"promotion":False}
    return {"status":"REJECT","target":None,"promotion":False}

# 06 Book sensor transfer

def evaluate_book_sensor_transfer(source_hash, target_hash, positive_detected, healthy_control_changed):
    if not source_hash or not target_hash:
        return {"status":"HOLD_HASH_REQUIRED"}
    if healthy_control_changed:
        return {"status":"FAIL_FALSE_POSITIVE"}
    if positive_detected:
        return {"status":"PASS_TRANSFER_PILOT","promotion":"HOLD_SECOND_BOOK_OR_HUMAN"}
    return {"status":"HOLD_NO_SIGNAL"}

# 07 Frontier drift
_FRONTIER_RANK={"FOUNDER_LOCK_DECISION_GATE":60,"FINAL_STORY_GATE_PASS":50,"TEXT_COMPLETE":45,"WORKING_COMPLETE":30,"DRAFTING":20}

def resolve_frontier(candidates):
    if not candidates:
        return {"status":"HOLD_NO_FRONTIER"}
    ordered=sorted(candidates,key=lambda x:(x.get("observed_at",""),_FRONTIER_RANK.get(x.get("status",""),0)),reverse=True)
    winner=ordered[0]
    stale=[x for x in ordered[1:] if x.get("obligation")!=winner.get("obligation")]
    return {"status":"PASS","frontier":winner,"stale_count":len(stale)}

def block_frontier_regression(current, proposed):
    return {"status":"FAIL_STALE_WORK" if proposed.get("episode",0)<current.get("episode",0) else "PASS"}

# 08 Human Signal firewall

def classify_human_evidence(source_type, raw_answers_present=False, coached=False):
    if source_type=="FOUNDER_DIRECT":
        return {"status":"HUMAN_SOURCE","class":"FOUNDER_SIGNAL","synthetic":False}
    if source_type=="REAL_PARTICIPANTS":
        if coached or not raw_answers_present:
            return {"status":"HOLD_PROTOCOL_DEFECT","class":"HUMAN_SIGNAL_PENDING"}
        return {"status":"PASS","class":"HUMAN_SIGNAL","synthetic":False}
    if source_type in {"MODEL","SIMULATED_PERSONA"}:
        return {"status":"PASS_CLASSIFICATION","class":"MODEL_REVIEW","synthetic":True}
    return {"status":"HOLD_UNKNOWN_SOURCE"}

# 09 Evidence independence

def evidence_families(reports):
    families={}
    for r in reports:
        key=r.get("root_source_hash") or r.get("root_evidence_id") or r.get("report_id")
        families.setdefault(key,[]).append(r["report_id"])
    return {"family_count":len(families),"families":families}

# 10 Package witness

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(65536),b""):
            h.update(b)
    return h.hexdigest()

def witness_package(zip_path, expected_manifest=None):
    if not zipfile.is_zipfile(zip_path):
        return {"status":"FAIL_NOT_ZIP"}
    sha=sha256_file(zip_path)
    with zipfile.ZipFile(zip_path) as z:
        names=sorted(z.namelist())
    if expected_manifest is not None and sorted(expected_manifest)!=names:
        return {"status":"FAIL_MANIFEST_MISMATCH","sha256":sha}
    return {"status":"PASS","sha256":sha,"members":len(names)}

# 11 Promotion proof
_PROMOTION_REQUIRED={"application_target","regression","readback","rollback","evidence_boundary"}

def promotion_eligibility(record):
    missing=sorted(_PROMOTION_REQUIRED-set(record))
    if missing:
        return {"status":"HOLD_MISSING_PROOF","missing":missing,"promote":False}
    if record.get("regression")!="PASS" or record.get("readback")!="PASS":
        return {"status":"HOLD_FAILED_PROOF","promote":False}
    if record.get("external_required") and not record.get("external_evidence"):
        return {"status":"HOLD_EXTERNAL_EVIDENCE","promote":False}
    return {"status":"ELIGIBLE_FOR_AUTHORITY_REVIEW","promote":False}

# 12 Telemetry proof
_TELEMETRY_FIELDS={"event_id","project_id","kind","decision","evidence_class"}

def validate_telemetry_event(event):
    missing=sorted(_TELEMETRY_FIELDS-set(event))
    if missing:
        return {"status":"FAIL_MISSING_FIELDS","missing":missing}
    false_zero=[]
    for key in ("provider_spend","human_minutes","duration_seconds"):
        if event.get(key)==0 and event.get(key+"_measured") is False:
            false_zero.append(key)
    if false_zero:
        return {"status":"FAIL_FALSE_ZERO","fields":false_zero}
    return {"status":"PASS"}

# 13 Economics proof

def compute_economics(x):
    req=("provider_spend","human_minutes","accepted_minutes","human_hourly_cost")
    missing=[k for k in req if x.get(k) is None]
    if missing:
        return {"status":"HOLD_MISSING_MEASURED_DATA","missing":missing}
    if x["accepted_minutes"]<=0:
        return {"status":"FAIL_ACCEPTED_MINUTES"}
    total=x["provider_spend"]+(x["human_minutes"]/60)*x["human_hourly_cost"]
    return {"status":"PASS_EVIDENCE_COMPLETE","total_cost":round(total,4),"cost_per_accepted_minute":round(total/x["accepted_minutes"],4)}

# 14 Second-project replication

def evaluate_replication(first, second):
    if first.get("mechanism_hash")!=second.get("mechanism_hash"):
        return {"status":"FAIL_MECHANISM_CHANGED","promote":False}
    if first.get("project_id")==second.get("project_id"):
        return {"status":"HOLD_NOT_INDEPENDENT_PROJECT","promote":False}
    if first.get("result")!="PASS" or second.get("result")!="PASS":
        return {"status":"HOLD_REPLICATION_FAILED","promote":False}
    return {"status":"CROSS_PROJECT_REPLICATION_PASS","promote":"ELIGIBLE_FOR_SCOPE_REVIEW"}

# 15 Proof ledger
_EVIDENCE_CLASSES={"ENGINEERING_TEST","PERSISTED_READBACK","HUMAN_SIGNAL","LIVE_PROVIDER","MEASURED_ECONOMICS","MARKET_BEHAVIOR"}

def append_proof(ledger, proof):
    if proof.get("evidence_class") not in _EVIDENCE_CLASSES:
        return {"status":"FAIL_EVIDENCE_CLASS"}
    if not proof.get("source_ref"):
        return {"status":"FAIL_SOURCE_REQUIRED"}
    if proof.get("claim_class")=="HUMAN_SIGNAL" and proof["evidence_class"]!="HUMAN_SIGNAL":
        return {"status":"FAIL_EVIDENCE_SUBSTITUTION"}
    ledger.append(proof)
    return {"status":"PASS","count":len(ledger)}

# 16 Governor v2

def govern(options):
    if not options:
        return {"status":"HOLD_NO_OPTIONS"}
    eligible=[o for o in options if o.get("authorized",True)]
    if not eligible:
        return {"status":"HOLD_NO_AUTHORIZED_OPTION"}
    metas=[o for o in eligible if o.get("kind")=="META"]
    products=[o for o in eligible if o.get("kind") in {"BOOK","AUDIO","HUMAN_EVIDENCE","PROVIDER_EVIDENCE"}]
    best_meta=max(metas,key=lambda o:(o.get("priority",0),o.get("information_value",0),-o.get("effort",0))) if metas else None
    best_product=max(products,key=lambda o:(o.get("priority",0),o.get("information_value",0),-o.get("effort",0))) if products else None
    if best_meta and best_product:
        if best_product.get("information_value",0)>best_meta.get("information_value",0) and best_product.get("priority",0)>=best_meta.get("priority",0):
            return {"status":"ROUTE_PRODUCT_EVIDENCE","selected":best_product["id"],"rejected_meta":best_meta["id"]}
    ordered=sorted(eligible,key=lambda o:(o.get("priority",0),o.get("information_value",0),-o.get("effort",0)),reverse=True)
    return {"status":"PASS","selected":ordered[0]["id"]}
