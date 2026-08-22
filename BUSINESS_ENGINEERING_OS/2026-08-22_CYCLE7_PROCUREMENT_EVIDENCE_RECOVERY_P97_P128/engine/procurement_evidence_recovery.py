from typing import Optional

def pack_acquisition_gate(official_url_known, complete_bytes):
    if complete_bytes: return "PACK_ACQUIRED"
    return "BLOCKED_AUTHENTICATED_DOCUMENT_SURFACE" if official_url_known else "BLOCKED_NO_OFFICIAL_ROUTE"

def supplier_packet_gate(verified_packet): return "SUPPLIER_PACKET_VERIFIED" if verified_packet else "HOLD_NO_VERIFIED_SUPPLIER_PACKET"
def requirement_join_gate(pack_complete,supplier_verified): return "JOIN_ALLOWED" if pack_complete and supplier_verified else "BLOCKED_INCOMPLETE_EVIDENCE"
def classify_gap(required,applicable,evidence_present,curable_before_deadline=None):
    if not applicable or not required: return "NOT_APPLICABLE"
    if evidence_present: return "MET"
    if curable_before_deadline is True: return "CURABLE_BEFORE_DEADLINE"
    if curable_before_deadline is False: return "NONCURABLE"
    return "UNKNOWN"
def meat_gate(full_pack,weights_known): return "MEAT_EXTRACTED" if full_pack and weights_known else "PARTIAL_MEAT"
def site_constraint_gate(full_pack): return "SITE_CONSTRAINTS_EXTRACTED" if full_pack else "PARTIAL_PUBLIC_SCOPE"
def finance_gate(estimated_value_known,full_terms_known): return "FINANCE_TERMS_EXTRACTED" if full_terms_known else ("PARTIAL_PUBLIC_FINANCE" if estimated_value_known else "FINANCE_UNKNOWN")
def pa4_gate(pack_complete,supplier_verified,blinded,independent,same_packet_hash):
    if not(pack_complete and supplier_verified): return "BLOCKED_PA4_PACKET_INCOMPLETE"
    return "PA4_REVIEW_ALLOWED" if blinded and independent and same_packet_hash else "BLOCKED_PA4_INDEPENDENCE"
def real_user_gate(no_outreach,authorized,target_user):
    if no_outreach and not authorized: return "HOLD_NO_OUTREACH"
    return "REAL_USER_TEST_ALLOWED" if authorized and target_user else "HOLD_REAL_TARGET_USER"
def substitute_residual(native_alerts,bid_pipeline_tools,consultants): return "RESIDUAL_QUALIFICATION_EVIDENCE_READINESS" if native_alerts and bid_pipeline_tools and consultants else "SUBSTITUTE_MATRIX_INCOMPLETE"
def field_refresh_gate(source_changed,deadline_passed,addendum_seen): return "REVALIDATE" if source_changed or deadline_passed or addendum_seen else "CURRENT_UNTIL_NEXT_TRIGGER"
def false_confidence_guard(polished,complete_pack,supplier_verified): return "REJECT_CONFIDENCE_PROMOTION" if polished and not(complete_pack and supplier_verified) else "ALLOW_ONLY_EVIDENCED_ASSERTIONS"
def wip_gate(primary,pilots): return "PASS_WIP" if primary<=1 and pilots<=2 else "REJECT_WIP"
def si_candidate_gate(repeated_independent_cases,regression_safe): return "CANDIDATE_FOR_REVIEW" if repeated_independent_cases>=2 and regression_safe else "HOLD_CANDIDATE_ONLY"
def pa5_gate(real_target_user,decision_used,timestamped): return "PA5_ELIGIBLE" if real_target_user and decision_used and timestamped else "PA5_FALSE"
def e3_gate(external_behavioral_cost,provenance): return "E3_ELIGIBLE" if external_behavioral_cost and provenance else "E3_FALSE"
def e4_gate(cash,binding_transaction,provenance): return "E4_ELIGIBLE" if cash is not None and cash>0 and binding_transaction and provenance else "E4_FALSE"
def cycle_close_gate(pr191,pr202,github_readback,drive_readback,ci_green): return "CYCLE_CLOSE_ALLOWED" if all([pr191,pr202,github_readback,drive_readback,ci_green]) else "HOLD_PERSISTENCE"
def null_safe_number(value,measured): return value if measured else None
