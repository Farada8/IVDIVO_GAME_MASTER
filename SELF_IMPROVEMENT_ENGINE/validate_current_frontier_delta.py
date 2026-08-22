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
    if "RE_READ_CONTROLLING_STATE" not in authority["volatile_state_rule"]:
        fail("volatile state must require a fresh controlling-state read")

    c10 = data["cycle10_convergence"]
    if c10["status"] != "PERSISTENCE_CLOSURE_PASS" or c10["authority_promotion"]:
        fail("Cycle10 closure boundary changed")
    if c10["next64_policy"] != "DEPENDENCY_INDEXED_BACKLOG_NOT_AUTO_WIP":
        fail("Next64 must not become automatic WIP")
    if not c10["source_of_truth"]:
        fail("Cycle10 source pointer missing")

    norm = data["library_normalization_n09_n16"]
    if norm["status"] != "N09_N16_CROSS_STORE_PASS":
        fail("N09-N16 normalization must remain closed")
    if norm["authenticated_raw_fetches"] != norm["physical_entries_observed"]:
        fail("raw fetch coverage mismatch")
    if norm["sha256_coverage"] != "35_OF_35":
        fail("hash coverage must remain 35/35")
    if not norm["source_of_truth"]:
        fail("normalization source pointer missing")

    volatile = data["volatile_frontiers"]
    required = {
        "si0014_recovery_evidence",
        "si0015_routing_calibration",
        "artifact_placement_path_drift",
        "thread_topic_continuity_guard",
        "book_intelligence",
    }
    missing = required - set(volatile)
    if missing:
        fail(f"missing volatile frontier pointers: {sorted(missing)}")

    for name, front in volatile.items():
        if front.get("promotion_authorized_in_overlay"):
            fail(f"overlay cannot promote volatile frontier {name}")
        if "observed_snapshot_non_authoritative" not in front:
            fail(f"volatile frontier {name} lost non-authoritative snapshot label")
        if not (front.get("controlling_path") or front.get("controlling_paths") or front.get("controlling_state_rule")):
            fail(f"volatile frontier {name} lacks controlling-state pointer/rule")

    placement = volatile["artifact_placement_path_drift"]
    if placement["observed_snapshot_non_authoritative"].get("platform_middleware_installed") is not False:
        fail("chat connector platform middleware must not be claimed installed")
    if placement["wip_class"] != "OBSERVED_ARMED_CANDIDATE_NOT_AUTO_WIP":
        fail("artifact-placement observation must not become auto-WIP")

    topic = volatile["thread_topic_continuity_guard"]
    if topic["wip_class"] != "OBSERVED_MERGED_CANDIDATE_NOT_AUTO_WIP":
        fail("topic-continuity observation must not become auto-WIP")

    bi = volatile["book_intelligence"]
    if bi["observed_snapshot_non_authoritative"].get("universal_promotion"):
        fail("Book Intelligence universal promotion is not established")

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
        "TREAT_OVERLAY_SNAPSHOT_COUNTER_AS_LIVE_AUTHORITY",
        "COUNT_SOURCE_GROUNDED_MODEL_ADJUDICATION_AS_HUMAN_SIGNAL",
        "COUNT_SYNTHETIC_INTERRUPTION_AS_NATURAL_RECOVERY_EVENT",
        "COUNT_SYNTHETIC_TOPIC_CONTINUATION_AS_NATURAL_REAL_PILOT_EVENT",
        "COUNT_TEST_OR_REPLAY_AS_CHAT_CONNECTOR_LIVE_PLACEMENT_FAILURE",
        "START_ANOTHER_32_TO_64_META_LOOP_WITHOUT_A_NEW_BOTTLENECK",
    }
    missing_forbidden = required_forbidden - forbidden
    if missing_forbidden:
        fail(f"missing forbidden guards: {sorted(missing_forbidden)}")

    print("PASS_CURRENT_SELF_IMPROVEMENT_FRONTIER_DELTA_POINTER_MODEL")


if __name__ == "__main__":
    main()
