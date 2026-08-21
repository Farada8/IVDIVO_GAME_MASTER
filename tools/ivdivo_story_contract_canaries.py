from __future__ import annotations

STORY_FIELDS=("hero","want","why_now","opposition","wrong_strategy","price","midpoint","climax_choice","resolution","series_hook_status")

def approval_event_gate(r,o):
    if not o or o.get("type")!=r.get("type") or o.get("target")!=r.get("target") or not o.get("authority_source"):
        return "APPROVAL_EVENT_MISSING"
    return "PASS"

def story_core_gate(s):
    missing=[f for f in STORY_FIELDS if s.get(f) in (None,"","UNKNOWN")]
    return {"status":"STORY_CORE_READY" if not missing else "PROSE_NO_GO","missing":missing}

def character_continuity_gate(status,requested_use="MANUSCRIPT"):
    s=(status or "UNKNOWN").upper()
    if s in {"CANON","LOCKED"}: return "USE"
    if s=="OPTION": return "OPTION_ONLY"
    return "UNKNOWN_HOLD" if requested_use.upper() in {"MANUSCRIPT","CANON","LOCK"} else "REFERENCE_ONLY"

def ordinary_life_pressure_gate(domains):
    if not domains: return "COMPETENCE_ONLY_RISK"
    functional=sum(bool(d.get("causal_pressure")) and bool(d.get("choice_or_price")) for d in domains)
    decorative=sum(bool(d.get("present")) and not bool(d.get("causal_pressure")) for d in domains)
    if functional==0 and decorative: return "CHECKLIST_EXPOSITION_RISK"
    return "FUNCTIONAL_COVERAGE" if functional else "COMPETENCE_ONLY_RISK"

def opposition_legitimacy_gate(o):
    if not all(o.get(k) for k in ("goal","competence","legitimate_interest","cost_of_yielding")): return "CARDBOARD_OPPOSITION"
    return "FALSE_EQUIVALENCE_RISK" if o.get("forced_equal_moral_weight") else "LEGITIMATE_RESISTANCE"

def wrong_strategy_gate(t):
    ok=all(t.get(k) for k in ("strategy","action","resistance","consequence","price")) and t.get("deletion_changes_chain")
    return "CAUSALLY_PROVEN" if ok else "DECORATIVE_FLAW"

def midpoint_gate(d):
    ok=d.get("earned_evidence") and d.get("pre_model")!=d.get("post_model") and d.get("strategy_delta")
    return "MIDPOINT_RECLASSIFICATION" if ok else "ESCALATION_ONLY"

def climax_ownership_gate(d):
    if d.get("ensemble_mode") and d.get("ensemble_choice_dependency"): return "ENSEMBLE_VALID"
    return "OWNED_CLIMAX" if all(d.get(k) for k in ("protagonist_choice","pressure","price","resolution_dependency")) else "PASSIVE_CLIMAX"

def resolution_hook_gate(main_closed,hook_present,hook_reopens=False):
    if hook_present and (not main_closed or hook_reopens): return "HOOK_QUARANTINED"
    if main_closed and hook_present: return "CLOSED_THEN_HOOK"
    return "CLOSED_NO_HOOK" if main_closed else "OPEN_STORY"

def scene_state_change_gate(s):
    req=("who","want","why_now","resistance","start_state","end_state")
    ok=all(s.get(k) not in (None,"") for k in req) and s["start_state"]!=s["end_state"]
    return "SCENE_EARNS_EXISTENCE" if ok else "CUT_COMPRESS_REDESIGN"

def dialogue_action_gate(d):
    if not d.get("objective") or not d.get("resistance"): return "INFO_EXCHANGE_RISK"
    if not d.get("listening_reaction") or not d.get("change"): return "REVISION_REQUIRED"
    return "DIALOGUE_ACTION"

def voice_separation_gate(corpora):
    fps=[(f.get("question_style"),f.get("disagreement_style"),f.get("repair_style"),f.get("syntax"),f.get("metaphor_source"),f.get("stress_degradation")) for f in corpora.values()]
    return "COLLISION_WATCH" if len(fps)!=len(set(fps)) else "SEPARATED"

def world_through_life_gate(d):
    lived={"job","home","transport","money","law","food","school","bureaucracy","relationship","humor","mistake","emergency"}
    return "EARNED_WORLD_REVEAL" if d.get("lived_domain") in lived and d.get("plot_pressure") else "LORE_ONLY_RISK"

def institution_differentiation_gate(rows):
    if len(rows)<2: return "MONOLITHIC"
    sig=[(r.get("jurisdiction"),r.get("knowledge"),r.get("incentive"),r.get("constraint"),r.get("internal_disagreement")) for r in rows]
    return "MORALIZED_DUPLICATE" if len(sig)!=len(set(sig)) else "DIFFERENTIATED"

def knowledge_jurisdiction_gate(knowledge_scope,jurisdiction_scope,requested_action,authority_evidence=False):
    if requested_action in {"COMMAND","POLICE","JUDICIAL","ADMIN"} and not authority_evidence: return "OVERREACH"
    if requested_action=="ADVICE" and knowledge_scope and jurisdiction_scope in (None,"","NONE"): return "ADVISORY_ONLY"
    if authority_evidence: return "AUTHORIZED"
    return "AUTHORIZED_ADVICE" if requested_action=="ADVICE" else "UNRESOLVED"

def mystery_epistemic_gate(c):
    req=("source","observation","interpretation","confidence","alternatives","disclosure_time","non_proof")
    if any(k not in c for k in req): return "EPISTEMIC_OVERCLAIM"
    if c.get("evidence_available_time") and c["evidence_available_time"]>c["disclosure_time"]: return "RETROACTIVE_EVIDENCE_RISK"
    return "EPISTEMIC_OVERCLAIM" if c.get("observation")==c.get("interpretation") else "FAIR_CLUE_RECORD"

def reference_firewall_gate(d):
    if any(d.get(k) for k in ("distinctive_plot","distinctive_sequence","distinctive_dialogue","signature_invention")): return "COPY_RISK"
    return "SAFE_TRANSFORM" if d.get("abstract_mechanism") and d.get("transformed_application") else "REFERENCE_ONLY"

def cross_ai_evidence_dedupe(findings):
    roots={}
    for f in findings: roots.setdefault(f.get("root_source") or "UNKNOWN",[]).append(f)
    return {"evidence_families":len(roots),"groups":roots}

def evidence_class_gate(required,observed):
    return "SUPPORTED" if required==observed else "EVIDENCE_CLASS_MISMATCH"

def human_signal_gate(raw_response,eligible,synthesized_before_raw=False):
    if synthesized_before_raw: return "CONTAMINATED"
    return "HUMAN_SIGNAL_AVAILABLE" if raw_response is not None and eligible else "HOLD_REAL_HUMAN"

def metric_gate(value,measured,source_ref=None):
    if not measured: return "UNKNOWN_NULL" if value is None else "FAIL_FALSE_ZERO"
    if not source_ref: return "FAIL_NO_SOURCE"
    return "MEASURED_ZERO" if value==0 else "MEASURED_VALUE"

def persistence_closure_gate(d):
    req=("github_write","drive_write","github_readback","drive_readback","pointer_reconciled","stale_scan","final_readback")
    return "PERSISTENCE_CLOSURE_PASS" if all(d.get(k) for k in req) else "SYNC_PENDING"

def concurrent_delta_gate(branch_behind,path_conflict,unique_compatible_delta):
    if path_conflict: return "FRONTIER_CONFLICT"
    if branch_behind and unique_compatible_delta: return "REBASE_SALVAGE"
    return "SUPERSEDED" if branch_behind else "FAST_FORWARD"

def registry_id_gate(proposed,committed,reserved,visibility_complete=True):
    if not visibility_complete: return "PARTIAL_VISIBILITY_HOLD"
    return "COLLISION" if proposed in set(committed)|set(reserved) else "ID_AVAILABLE"

def promotion_tribunal(d):
    if d.get("false_positive_blocker") or not d.get("contract") or not d.get("canary"): return "HOLD"
    if d.get("requested_scope")=="UNIVERSAL" and not d.get("cross_project_replication"):
        return "ACCEPT_WITH_SCOPE" if d.get("project_pilot") else "HOLD"
    if d.get("project_pilot") and d.get("application_readback") and d.get("cross_project_replication"): return "PROMOTE"
    return "ACCEPT_WITH_SCOPE" if d.get("project_pilot") else "HOLD"

def engine_worthiness_gate(d):
    if d.get("semantic_duplicate"): return "REJECT_DUPLICATE"
    if d.get("existing_extension_suffices"): return "EXTEND"
    return "BUILD" if d.get("recurrent") and d.get("state_need") and d.get("coordination_need") else "ADAPTER_ONLY"

def story_to_audio_handoff_gate(d):
    if not all(d.get(k) for k in ("story_lock","source_version","source_hash","text_protection")): return "SOURCE_HOLD"
    return "STORY_REOPEN_PROHIBITED" if d.get("audio_attempts_story_mutation") else "AUDIO_INGEST_READY"

def portfolio_governor(actions):
    admissible=[x for x in actions if x.get("admissible")]
    if not admissible: return None
    return max(admissible,key=lambda x:(x.get("authority_priority",0),x.get("dependency_priority",0),x.get("information_value",0))).get("id")
