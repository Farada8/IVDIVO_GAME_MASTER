from __future__ import annotations


def route_path(path: dict) -> str:
    kind = path.get("kind")

    if kind == "DIRECT_SERVICE":
        if path.get("order_observed"):
            return "PROMOTION_ELIGIBLE_REAL_ORDER_EVIDENCE"
        if path.get("quote_request_observed") or path.get("reply_observed"):
            return "ADVANCE_REAL_RESPONSE_EVIDENCE"
        if path.get("real_lead_signal"):
            return "CONDITIONAL_FRONT_RUNNER_REAL_LEAD_SIGNAL"
        return "HOLD_NO_REAL_LEAD_SIGNAL"

    if kind == "PROCUREMENT":
        if not path.get("current_pack_acquired"):
            return "EXPLORE_CURRENT_PACK_FIRST"
        if not path.get("capability_join_ready"):
            return "HOLD_CAPABILITY_JOIN_REQUIRED"
        return "ADVANCE_BOUNDED_PROCUREMENT_DECISION"

    if kind == "SME_IMPLEMENTATION":
        if not path.get("real_workflow_packet"):
            return "HOLD_REAL_WORKFLOW_PACKET_REQUIRED"
        if not path.get("operator_pain_observed"):
            return "HOLD_OPERATOR_PAIN_EVIDENCE_REQUIRED"
        if path.get("pilot_request_observed"):
            return "PROMOTION_ELIGIBLE_REAL_PILOT_REQUEST"
        return "ADVANCE_BOUNDED_PILOT_DISCOVERY"

    return "HOLD_UNKNOWN_PATH"


def may_promote_primary(path: dict) -> bool:
    route = route_path(path)
    return route in {
        "PROMOTION_ELIGIBLE_REAL_ORDER_EVIDENCE",
        "PROMOTION_ELIGIBLE_REAL_PILOT_REQUEST",
        "ADVANCE_BOUNDED_PROCUREMENT_DECISION",
    }
