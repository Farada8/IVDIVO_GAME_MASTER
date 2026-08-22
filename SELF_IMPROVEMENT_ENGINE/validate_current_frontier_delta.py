#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "CURRENT_IVDIVO_SELF_IMPROVEMENT_FRONTIER_DELTA_2026-08-22.json"


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def main() -> None:
    data = json.loads(STATE.read_text(encoding="utf-8"))

    authority = data["authority"]
    if authority["engine_status"] != "V2_VERIFIED_CURRENT":
        fail("v2 must remain current")
    if authority["v3_status"] == "VERIFIED_CURRENT":
        fail("v3 promotion is not authorized")
    if authority["new_global_si_id"] is not None:
        fail("no new SI id is authorized by reconciliation")

    c10 = data["cycle10_convergence"]
    if c10["status"] != "PERSISTENCE_CLOSURE_PASS":
        fail("Cycle10 convergence closure must remain PASS")
    if c10["authority_promotion"]:
        fail("Cycle10 closure cannot promote authority")
    if c10["next64_policy"] != "DEPENDENCY_INDEXED_BACKLOG_NOT_AUTO_WIP":
        fail("Next64 must not become automatic WIP")

    norm = data["library_normalization_n09_n16"]
    if norm["status"] != "N09_N16_CROSS_STORE_PASS":
        fail("N09-N16 normalization must remain closed")
    if norm["authenticated_raw_fetches"] != norm["physical_entries_observed"]:
        fail("raw fetch coverage mismatch")
    if norm["sha256_coverage"] != "35_OF_35":
        fail("hash coverage must remain 35/35")

    si14 = data["si0014_recovery_evidence"]
    if si14["physical_interruption_incidents"] >= si14["required_incidents"] and not si14["promotion_authorized"]:
        fail("SI-0014 event threshold changed; reconciliation must be re-evaluated")
    if si14["promotion_authorized"]:
        fail("SI-0014 promotion is not authorized")

    si15 = data["si0015_routing_calibration"]
    if (
        si15["independent_human_expected_label_review"] == "PROVEN"
        and si15["live_operational_routing_telemetry"] == "PROVEN"
        and not si15["promotion_authorized"]
    ):
        fail("SI-0015 evidence changed; reconciliation must be re-evaluated")
    if si15["promotion_authorized"]:
        fail("SI-0015 promotion is not authorized")

    placement = data["artifact_placement_path_drift"]
    if placement["authority_effect"] != "NONE":
        fail("artifact-placement candidate cannot change global authority")
    if placement["platform_middleware_claimed"]:
        fail("chat connector platform middleware is not installed/proven")
    if placement["promotion_authorized"]:
        fail("artifact-placement candidate cannot auto-promote")
    if placement["chat_connector_live_real_event_count"] != 0:
        fail("live connector event count changed; reconciliation must be re-evaluated")
    if placement["wip_class"] != "OBSERVED_ARMED_CANDIDATE_NOT_AUTO_WIP":
        fail("artifact-placement monitoring must not become auto-WIP")

    topic = data["thread_topic_continuity_guard"]
    if topic["authority_effect"] != "NONE" or topic["global_si_id"] is not None:
        fail("topic-continuity candidate cannot change global authority")
    if topic["promotion_authorized"]:
        fail("topic-continuity candidate cannot auto-promote")
    if topic["real_continuation_events"] >= topic["required_real_continuation_events"]:
        fail("topic-continuity natural-event threshold changed; reconciliation must be re-evaluated")
    if topic["wip_class"] != "OBSERVED_MERGED_CANDIDATE_NOT_AUTO_WIP":
        fail("topic-continuity monitoring must not become auto-WIP")

    bi = data["book_intelligence"]
    if bi["universal_promotion"]:
        fail("Book Intelligence universal promotion requires second independent pilot")

    wip = data["current_meta_wip"]
    bounded = sum(bool(wip[k]) for k in ("bounded_pilot_1", "bounded_pilot_2"))
    if bounded > 2:
        fail("meta WIP exceeds two bounded pilots")
    if len(wip.get("observed_not_auto_wip", [])) < 3:
        fail("observed non-WIP candidates were lost from frontier")

    forbidden = set(data["forbidden"])
    required_forbidden = {
        "AUTO_PROMOTE_V3",
        "ALLOCATE_NEW_SI_ID_FROM_CYCLE_COUNT_OR_TEST_COUNT",
        "COUNT_SOURCE_GROUNDED_MODEL_ADJUDICATION_AS_HUMAN_SIGNAL",
        "COUNT_SYNTHETIC_INTERRUPTION_AS_NATURAL_RECOVERY_EVENT",
        "COUNT_SYNTHETIC_TOPIC_CONTINUATION_AS_NATURAL_REAL_PILOT_EVENT",
        "COUNT_TEST_OR_REPLAY_AS_CHAT_CONNECTOR_LIVE_PLACEMENT_FAILURE",
        "START_ANOTHER_32_TO_64_META_LOOP_WITHOUT_A_NEW_BOTTLENECK",
    }
    missing = required_forbidden - forbidden
    if missing:
        fail(f"missing forbidden guards: {sorted(missing)}")

    print("PASS_CURRENT_SELF_IMPROVEMENT_FRONTIER_DELTA")


if __name__ == "__main__":
    main()
