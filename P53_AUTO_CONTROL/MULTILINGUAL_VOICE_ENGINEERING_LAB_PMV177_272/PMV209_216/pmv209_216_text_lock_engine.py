#!/usr/bin/env python3
"""
IVDIVO / BODYGUARD — PMV209–PMV216 RU Text Lock Engine v1.0

Purpose:
  Convert four narrow external review streams + performed timing evidence
  into a fail-closed RU audition-text authority.

This engine never fabricates reviewer evidence and never promotes canon on its own.

Stages:
  PMV209 validate_review
  PMV210 resolve_conflicts
  PMV211 compile_patch_candidate
  PMV212 lock_stage_protocol
  PMV213 lock_live_audio_lexicon
  PMV214 lock_close_protection_lexicon
  PMV215 validate_performed_timing
  PMV216 release_ru_text_authority
"""

from __future__ import annotations
import argparse, hashlib, json
from collections import defaultdict
from typing import Any

VALID_DECISIONS = {"KEEP", "PATCH", "HOLD"}

class GateError(RuntimeError):
    pass

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def validate_review(response: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    reviewer = response.get("reviewer", {})
    role = reviewer.get("role")
    if role not in registry["roles"]:
        raise GateError(f"unknown reviewer role: {role}")
    spec = registry["roles"][role]
    items = response.get("items", [])
    if len(items) < spec["required_min_items"]:
        raise GateError(f"too few reviewed items for {role}")
    seen = set(); normalized = []
    for item in items:
        iid = item.get("item_id")
        if iid not in spec["allowed_item_ids"]: raise GateError(f"item {iid} not allowed for {role}")
        if iid in seen: raise GateError(f"duplicate item {iid}")
        seen.add(iid)
        decision = item.get("decision")
        if decision not in VALID_DECISIONS: raise GateError(f"invalid decision {decision} for {iid}")
        replacement = item.get("replacement_text")
        if decision == "PATCH" and not (isinstance(replacement, str) and replacement.strip()):
            raise GateError(f"PATCH without replacement for {iid}")
        confidence = item.get("confidence_0_100")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 100:
            raise GateError(f"invalid confidence for {iid}")
        normalized.append({
            "item_id": iid, "decision": decision,
            "reason_code": item.get("reason_code", "OTHER"),
            "reason": item.get("reason", "").strip(),
            "replacement_text": replacement.strip() if isinstance(replacement, str) else None,
            "confidence_0_100": confidence,
        })
    return {"artifact":"BODYGUARD_VALIDATED_EXTERNAL_REVIEW_v1","status":"VALIDATED_NOT_APPLIED","provenance":{"reviewer_id":reviewer.get("reviewer_id"),"role":role,"locale":reviewer.get("locale","ru-RU"),"qualification_note":reviewer.get("qualification_note","")},"items":normalized,"authority_effect":"EVIDENCE_ONLY"}

def resolve_conflicts(validated_reviews: list[dict[str, Any]], domain_map: dict[str, str]) -> dict[str, Any]:
    precedence={"spoken_naturalness":["NATIVE_RU"],"stage_protocol":["STAGE"],"live_audio":["LIVE_AUDIO"],"close_protection":["CLOSE_PROTECTION"]}
    grouped=defaultdict(list)
    for review in validated_reviews:
        role=review["provenance"]["role"]
        for item in review["items"]: grouped[item["item_id"]].append({**item,"role":role})
    resolved=[]; conflicts=[]
    for iid,evidence in sorted(grouped.items()):
        domain=domain_map.get(iid,"spoken_naturalness")
        preferred=precedence.get(domain,[])
        authoritative=[x for x in evidence if x["role"] in preferred] or evidence
        decisions={x["decision"] for x in authoritative}
        replacements={x["replacement_text"] for x in authoritative if x["decision"]=="PATCH"}
        if "HOLD" in decisions or len(decisions)>1 or len(replacements)>1:
            conflicts.append({"item_id":iid,"domain":domain,"evidence":evidence})
        else:
            winner=max(authoritative,key=lambda x:x["confidence_0_100"])
            resolved.append({"item_id":iid,"domain":domain,"decision":winner["decision"],"replacement_text":winner.get("replacement_text"),"reason":winner.get("reason"),"winning_role":winner["role"],"confidence_0_100":winner["confidence_0_100"]})
    return {"artifact":"BODYGUARD_REVIEW_CONFLICT_RESOLUTION_v1","status":"HOLD" if conflicts else "RESOLVED","resolved":resolved,"conflicts":conflicts,"hard_law":"Unresolved review conflict blocks text lock; no majority vote overrides domain expertise."}

def compile_patch_candidate(anchors: dict[str, Any], resolution: dict[str, Any]) -> dict[str, Any]:
    if resolution["status"] != "RESOLVED": raise GateError("review conflicts unresolved")
    decisions={x["item_id"]:x for x in resolution["resolved"]}; changed=[]; output=[]
    for anchor in anchors["anchors"]:
        decision=decisions.get(anchor["block_id"]); text=anchor["text_ru"]
        if decision and decision["decision"]=="PATCH": text=decision["replacement_text"]; changed.append(anchor["block_id"])
        output.append({**anchor,"text_ru_candidate":text,"text_ru_candidate_sha256":sha256_text(text)})
    return {"artifact":"BODYGUARD_E01_RU_AUDITION_PATCH_CANDIDATE_v1","status":"CANDIDATE_NOT_LOCKED","source":anchors["artifact"],"changed_block_ids":changed,"anchors":output,"required_next":["semantic regression","domain locks","performed timing","RU text release gate"]}

def lock_stage_protocol(stage_review: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    if stage_review["provenance"]["role"] != "STAGE": raise GateError("wrong reviewer role for stage lock")
    items={x["item_id"]:x for x in stage_review["items"]}; required={"STAGE_STANDBY","STAGE_ACK","STAGE_GO"}
    if not required.issubset(items): raise GateError("missing stage protocol decisions")
    if any(items[i]["decision"]=="HOLD" for i in required): raise GateError("HOLD remains in stage protocol")
    locked=dict(candidate); locked["artifact"]="BODYGUARD_RU_STAGE_PROTOCOL_STATE_MACHINE_v1_0"; locked["status"]="PRACTITIONER_LOCKED"; locked["practitioner_decisions"]={i:items[i] for i in sorted(required)}
    return locked

def lock_domain_lexicon(review: dict[str, Any], candidates: dict[str, Any]) -> dict[str, Any]:
    role=review["provenance"]["role"]; role_to_domain={"LIVE_AUDIO":"LIVE_AUDIO","CLOSE_PROTECTION":"CLOSE_PROTECTION"}
    if role not in role_to_domain: raise GateError("unsupported lexicon reviewer role")
    domain=role_to_domain[role]; items={x["item_id"]:x for x in review["items"]}; expected=set(candidates[domain])
    if not expected.issubset(items): raise GateError(f"incomplete {domain} review")
    if any(items[i]["decision"]=="HOLD" for i in expected): raise GateError(f"HOLD remains in {domain}")
    entries={}
    for iid in sorted(expected):
        d=items[iid]; entries[iid]={"concept":candidates[domain][iid]["concept"],"decision":d["decision"],"locked_text":d["replacement_text"] if d["decision"]=="PATCH" else candidates[domain][iid]["working"][0],"confidence_0_100":d["confidence_0_100"],"reason":d["reason"]}
    return {"artifact":f"BODYGUARD_RU_{domain}_LEXICON_v1_0","status":"PRACTITIONER_LOCKED","domain":domain,"entries":entries}

def validate_performed_timing(contract: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    required=set(contract["required_anchor_ids"]); grouped=defaultdict(list)
    for take in evidence.get("takes",[]): grouped[take["block_id"]].append(take)
    missing=sorted(required-set(grouped)); failed=[]; passed=[]
    for bid in sorted(required & set(grouped)):
        good=[t for t in grouped[bid] if t.get("function_preserved") and not t.get("clipped") and not t.get("mispronounced") and not t.get("unnatural_pause")]
        (passed if good else failed).append(bid)
    verdict="PASS" if not missing and not failed else "FAIL"
    return {"artifact":"BODYGUARD_RU_PERFORMED_TIMING_GATE_v1","verdict":verdict,"missing":missing,"failed":failed,"passed_count":len(passed)}

def release_ru_text_authority(patch_candidate: dict[str, Any], stage_lock: dict[str, Any], audio_lock: dict[str, Any], protection_lock: dict[str, Any], timing_gate: dict[str, Any]) -> dict[str, Any]:
    checks={"stage":stage_lock.get("status")=="PRACTITIONER_LOCKED","audio":audio_lock.get("status")=="PRACTITIONER_LOCKED","protection":protection_lock.get("status")=="PRACTITIONER_LOCKED","timing":timing_gate.get("verdict")=="PASS"}
    if not all(checks.values()): raise GateError(f"release prerequisites not PASS: {checks}")
    lines=[x["text_ru_candidate"] for x in patch_candidate["anchors"]]
    return {"artifact":"BODYGUARD_E01_RU_AUDITION_TEXT_AUTHORITY_v1_0","status":"LOCKED_FOR_VOICE_AUDITION","ordered_text_sha256":sha256_text("\n".join(lines)),"anchors":patch_candidate["anchors"],"evidence":{"stage":stage_lock["artifact"],"audio":audio_lock["artifact"],"protection":protection_lock["artifact"],"timing":timing_gate["artifact"]},"next_gate":"AUTHENTICATED_PROVIDER_PREFLIGHT"}

def main() -> int:
    ap=argparse.ArgumentParser(description="PMV209–216 RU text-lock engine"); ap.add_argument("--self-test",action="store_true"); args=ap.parse_args()
    if args.self_test:
        print("MODULE_IMPORT_PASS"); print("stages=PMV209,PMV210,PMV211,PMV212,PMV213,PMV214,PMV215,PMV216"); return 0
    ap.print_help(); return 0

if __name__ == "__main__":
    raise SystemExit(main())
