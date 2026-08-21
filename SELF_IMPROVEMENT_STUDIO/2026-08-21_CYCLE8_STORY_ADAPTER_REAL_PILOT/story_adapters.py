def _is_unknown(v):
    return v is None or v == '' or v == 'UNKNOWN' or v == 'NOT_PROVIDED'

STORY_CORE_FIELDS=['hero','want','why_now','opposition','wrong_strategy','price','midpoint','climax_choice','resolution','series_hook_status']

def source_adequacy(required_fields,payload,source_role):
    missing=[f for f in required_fields if _is_unknown(payload.get(f))]
    if not missing:return {'status':'ADEQUATE','missing':[]}
    if source_role in {'ROUTING_STATE','FINAL_GATE_SUMMARY','PARTIAL_AUTHORITY_SUMMARY'}:
        return {'status':'INSUFFICIENT_SOURCE_NOT_STORY_DEFECT','missing':missing,'source_role':source_role}
    return {'status':'MISSING_REQUIRED_STORY_DATA','missing':missing,'source_role':source_role}

def story_core_compiler(payload,source_role):
    q=source_adequacy(STORY_CORE_FIELDS,payload,source_role)
    return q if q['status']!='ADEQUATE' else {'status':'STORY_CORE_READY','missing':[]}

def character_continuity_unknown_gate(fact_status,requested_use,source_authority):
    s=(fact_status or 'UNKNOWN').upper()
    if s in {'CANON','LOCKED','APPROVED'} and source_authority:return {'status':'USE'}
    if s in {'OPTION','WORKING','WORKING_OPTION','NOT_CANON'}:
        if requested_use in {'CANON_DEPENDENCY','MANUSCRIPT_DEPENDENCY','LOCKED_FACT'}:return {'status':'FOUNDER_DECISION_REQUIRED'}
        return {'status':'OPTION_ONLY'}
    return {'status':'UNKNOWN_HOLD'}

def ordinary_life_pressure_coverage(payload,source_role):
    q=source_adequacy(['major_character','ordinary_life_domains','plot_pressure_links'],payload,source_role)
    if q['status']!='ADEQUATE':return q
    if not payload['ordinary_life_domains']:return {'status':'COMPETENCE_ONLY_RISK'}
    if not payload['plot_pressure_links']:return {'status':'CHECKLIST_EXPOSITION_RISK'}
    return {'status':'FUNCTIONAL_COVERAGE'}

def opposition_legitimacy_matrix(payload,source_role):
    q=source_adequacy(['opponent_goal','evidence','competence','legitimate_interest','cost_of_yielding','right_domain'],payload,source_role)
    if q['status']!='ADEQUATE':return q
    if not payload['opponent_goal'] or not payload['competence']:return {'status':'CARDBOARD_OPPOSITION'}
    if not payload['legitimate_interest'] and not payload['right_domain']:return {'status':'CARDBOARD_OPPOSITION'}
    if payload.get('moral_weight_equalized') is True:return {'status':'FALSE_EQUIVALENCE_RISK'}
    return {'status':'LEGITIMATE_RESISTANCE'}

def wrong_strategy_causality_proof(payload,source_role):
    q=source_adequacy(['hero_strategy','actions','resistance','consequences','price','deletion_changes_chain'],payload,source_role)
    if q['status']!='ADEQUATE':return q
    return {'status':'CAUSALLY_PROVEN' if payload['deletion_changes_chain'] is True else 'DECORATIVE_FLAW'}

def midpoint_reclassification_validator(payload,source_role):
    q=source_adequacy(['pre_midpoint_model','evidence_event','post_midpoint_model','strategy_delta','stakes_delta'],payload,source_role)
    if q['status']!='ADEQUATE':return q
    if payload['pre_midpoint_model']==payload['post_midpoint_model'] and not payload['strategy_delta']:return {'status':'ESCALATION_ONLY'}
    return {'status':'MIDPOINT_RECLASSIFICATION'}

def climax_ownership_gate(payload,source_role):
    q=source_adequacy(['protagonist_choice','pressure','price','resolution_dependency','ensemble_mode'],payload,source_role)
    if q['status']!='ADEQUATE':return q
    if payload['ensemble_mode'] is True:return {'status':'ENSEMBLE_VALID'}
    if payload['protagonist_choice'] and payload['resolution_dependency'] is True and payload['price']:return {'status':'OWNED_CLIMAX'}
    return {'status':'PASSIVE_CLIMAX'}

def resolution_closure_hook_quarantine(main_conflict_closed,hook_present,hook_reopens_conflict):
    if hook_present and (not main_conflict_closed or hook_reopens_conflict):return {'status':'HOOK_QUARANTINED'}
    if main_conflict_closed and hook_present:return {'status':'CLOSED_THEN_HOOK'}
    if main_conflict_closed:return {'status':'CLOSED_NO_HOOK'}
    return {'status':'OPEN_STORY'}

def world_through_life_validator(payload,source_role):
    q=source_adequacy(['world_fact','delivery_scene','lived_domain','plot_pressure'],payload,source_role)
    if q['status']!='ADEQUATE':return q
    return {'status':'EARNED_WORLD_REVEAL' if payload['lived_domain'] and payload['plot_pressure'] else 'LORE_ONLY_RISK'}

def institutional_conflict_differentiator(payload,source_role):
    q=source_adequacy(['institutions','jurisdiction','knowledge','incentives','successes','crimes','constraints','internal_disagreement'],payload,source_role)
    if q['status']!='ADEQUATE':return q
    rows=payload['institutions']
    if len(rows)<2:return {'status':'MONOLITHIC'}
    sig={(r.get('jurisdiction'),r.get('knowledge'),r.get('incentives'),r.get('constraints')) for r in rows}
    return {'status':'DIFFERENTIATED' if len(sig)>=2 else 'MORALIZED_DUPLICATE'}

def knowledge_jurisdiction_separation_gate(knowledge_scope,jurisdiction_scope,requested_action,authority_evidence=False):
    if requested_action in {'COMMAND','POLICE','JUDICIAL','ADMIN'} and not authority_evidence:return {'status':'OVERREACH'}
    if requested_action=='ADVICE' and knowledge_scope and not jurisdiction_scope:return {'status':'ADVISORY_ONLY'}
    if authority_evidence:return {'status':'AUTHORIZED'}
    if requested_action=='ADVICE':return {'status':'AUTHORIZED_ADVICE'}
    return {'status':'UNRESOLVED'}

def mystery_epistemic_ladder(payload,source_role):
    q=source_adequacy(['clue_source','observation','interpretation','confidence','alternatives','disclosure_time','non_proof'],payload,source_role)
    if q['status']!='ADEQUATE':return q
    if payload.get('retroactive_unavailable_evidence') is True:return {'status':'RETROACTIVE_EVIDENCE_RISK'}
    if not payload['clue_source'] or not payload['non_proof']:return {'status':'EPISTEMIC_OVERCLAIM'}
    if payload['observation']==payload['interpretation'] and payload['confidence']=='CERTAIN':return {'status':'EPISTEMIC_OVERCLAIM'}
    return {'status':'FAIR_CLUE_RECORD'}
