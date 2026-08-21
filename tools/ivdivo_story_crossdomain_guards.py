from __future__ import annotations

def approval_event_gate(required,observed):
    if not observed or observed.get('type')!=required.get('type') or observed.get('target')!=required.get('target') or not observed.get('authority_source'):
        return 'APPROVAL_EVENT_MISSING'
    return 'PASS'

def scene_state_change_gate(scene):
    req=('who','want','why_now','resistance','start_state','end_state')
    ok=all(scene.get(k) not in (None,'') for k in req) and scene['start_state']!=scene['end_state']
    return 'SCENE_EARNS_EXISTENCE' if ok else 'CUT_COMPRESS_REDESIGN'

def dialogue_action_gate(data):
    if not data.get('objective') or not data.get('resistance'): return 'INFO_EXCHANGE_RISK'
    if not data.get('listening_reaction') or not data.get('change'): return 'REVISION_REQUIRED'
    return 'DIALOGUE_ACTION'

def voice_separation_gate(corpora):
    fps=[(f.get('question_style'),f.get('disagreement_style'),f.get('repair_style'),f.get('syntax'),f.get('metaphor_source'),f.get('stress_degradation')) for f in corpora.values()]
    return 'COLLISION_WATCH' if len(fps)!=len(set(fps)) else 'SEPARATED'

def reference_firewall_gate(data):
    if any(data.get(k) for k in ('distinctive_plot','distinctive_sequence','distinctive_dialogue','signature_invention')): return 'COPY_RISK'
    return 'SAFE_TRANSFORM' if data.get('abstract_mechanism') and data.get('transformed_application') else 'REFERENCE_ONLY'

def cross_ai_evidence_dedupe(findings):
    roots={}
    for f in findings: roots.setdefault(f.get('root_source') or 'UNKNOWN',[]).append(f)
    return {'evidence_families':len(roots),'groups':roots}

def evidence_class_gate(required,observed):
    return 'SUPPORTED' if required==observed else 'EVIDENCE_CLASS_MISMATCH'

def human_signal_gate(raw_response,eligible,synthesized_before_raw=False):
    if synthesized_before_raw: return 'CONTAMINATED'
    return 'HUMAN_SIGNAL_AVAILABLE' if raw_response is not None and eligible else 'HOLD_REAL_HUMAN'

def metric_gate(value,measured,source_ref=None):
    if not measured: return 'UNKNOWN_NULL' if value is None else 'FAIL_FALSE_ZERO'
    if not source_ref: return 'FAIL_NO_SOURCE'
    return 'MEASURED_ZERO' if value==0 else 'MEASURED_VALUE'

def persistence_closure_gate(data):
    req=('github_write','drive_write','github_readback','drive_readback','pointer_reconciled','stale_scan','final_readback')
    return 'PERSISTENCE_CLOSURE_PASS' if all(data.get(k) for k in req) else 'SYNC_PENDING'

def concurrent_delta_gate(branch_behind,path_conflict,unique_compatible_delta):
    if path_conflict: return 'FRONTIER_CONFLICT'
    if branch_behind and unique_compatible_delta: return 'REBASE_SALVAGE'
    return 'SUPERSEDED' if branch_behind else 'FAST_FORWARD'

def registry_id_gate(proposed,committed,reserved,visibility_complete=True):
    if not visibility_complete: return 'PARTIAL_VISIBILITY_HOLD'
    return 'COLLISION' if proposed in set(committed)|set(reserved) else 'ID_AVAILABLE'

def promotion_tribunal(data):
    if data.get('false_positive_blocker') or not data.get('contract') or not data.get('canary'): return 'HOLD'
    if data.get('requested_scope')=='UNIVERSAL' and not data.get('cross_project_replication'):
        return 'ACCEPT_WITH_SCOPE' if data.get('project_pilot') else 'HOLD'
    if data.get('project_pilot') and data.get('application_readback') and data.get('cross_project_replication'): return 'PROMOTE'
    return 'ACCEPT_WITH_SCOPE' if data.get('project_pilot') else 'HOLD'

def engine_worthiness_gate(data):
    if data.get('semantic_duplicate'): return 'REJECT_DUPLICATE'
    if data.get('existing_extension_suffices'): return 'EXTEND'
    return 'BUILD' if data.get('recurrent') and data.get('state_need') and data.get('coordination_need') else 'ADAPTER_ONLY'

def story_to_audio_handoff_gate(data):
    if not all(data.get(k) for k in ('story_lock','source_version','source_hash','text_protection')): return 'SOURCE_HOLD'
    return 'STORY_REOPEN_PROHIBITED' if data.get('audio_attempts_story_mutation') else 'AUDIO_INGEST_READY'

def portfolio_governor(actions):
    admissible=[x for x in actions if x.get('admissible')]
    if not admissible: return None
    return max(admissible,key=lambda x:(x.get('authority_priority',0),x.get('dependency_priority',0),x.get('information_value',0))).get('id')
