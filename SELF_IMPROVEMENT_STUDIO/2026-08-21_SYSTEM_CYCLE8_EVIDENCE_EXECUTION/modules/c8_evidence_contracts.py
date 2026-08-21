"""Cycle 8 bounded evidence-contract harness.

Review/canary module only. It does not replace SI-0012, SI-0014, SI-0015,
the current registry transaction authority, or any story/project authority.
"""

from typing import Optional


ATTRACTION_STATES = {"ATTRACTION_AUTHORIZED", "ROMANCE_ACTIVE", "ROMANCE_LOCKED"}


def registry_reservation_view(committed_ids, reserved_ids, complete_visibility=True):
    if not complete_visibility:
        return {"status": "HOLD_PARTIAL_VISIBILITY", "next_id": None}
    committed, reserved = set(committed_ids), set(reserved_ids)
    collisions = sorted(committed & reserved)
    if collisions:
        return {"status": "HOLD_COLLISION", "collisions": collisions, "next_id": None}
    numbers = []
    for candidate_id in committed | reserved:
        if candidate_id.startswith("SI-") and candidate_id[3:].isdigit():
            numbers.append(int(candidate_id[3:]))
    n = max(numbers) + 1 if numbers else 1
    while f"SI-{n:04d}" in committed | reserved:
        n += 1
    return {"status": "PASS", "collisions": [], "next_id": f"SI-{n:04d}"}


def safe_missing_actions(store_states, paid_or_irreversible=False):
    if "STARTED_UNKNOWN" in store_states.values() and paid_or_irreversible:
        return {"decision": "QUARANTINE_NO_REPLAY", "actions": []}
    actions = [store for store, state in store_states.items() if state == "MISSING"]
    return {"decision": "DISPATCH_MISSING_SAFE_ONLY", "actions": actions}


def recovery_event(event):
    required = (
        "fresh_authority",
        "checkpoint",
        "post_restart_authority_readback",
        "recovery_readback",
        "project_id_match",
        "source_hash_match",
    )
    if not all(event.get(key) for key in required):
        return "HOLD_RECOVERY_EVIDENCE"
    if event.get("checkpoint_main_sha") != event.get("current_main_sha"):
        return "REBASE_FIRST"
    return "RECOVERY_EVENT_ACCEPTED"


def evidence_claim(evidence_class, root_source, claim_as=None):
    if claim_as == "HUMAN_SIGNAL" and evidence_class != "HUMAN_SIGNAL":
        return "REJECT_EVIDENCE_LAUNDERING"
    if not root_source:
        return "HOLD_MISSING_ROOT_SOURCE"
    return "PASS"


def evidence_family_count(records):
    return len({record["root_source"] for record in records if record.get("root_source")})


def economics_value(value: Optional[float], measured: bool):
    if value is None:
        return "UNKNOWN_VALID_NULL"
    if value == 0 and not measured:
        return "REJECT_FALSE_ZERO"
    return "PASS_MEASURED" if measured else "HOLD_UNMEASURED"


def stale_episode_check(candidate_episode, terminal_episode):
    return "REJECT_STALE_EPISODE" if candidate_episode <= terminal_episode else "REVIEW_NEW_EPISODE"


def secret_guard(payload):
    forbidden = {"api_key", "token", "secret", "authorization", "password"}
    return "REJECT_SECRET_FIELD" if any(key.lower() in forbidden for key in payload) else "PASS"


def package_identity(historical_sha, claimed_sha, post_package_commits):
    if post_package_commits and claimed_sha != historical_sha:
        return "REJECT_RELABEL"
    return "PASS"


def prompt_ir_parity(source, target, protected_keys):
    missing_or_changed = [key for key in protected_keys if source.get(key) != target.get(key)]
    return {
        "status": "PARITY_FAIL" if missing_or_changed else "PARITY_PASS",
        "missing_or_changed": missing_or_changed,
    }


def book_scope_widen(healthy_false_positives, third_project_pass, human_adjudications=0):
    if healthy_false_positives:
        return "HOLD_FALSE_POSITIVE"
    if not third_project_pass:
        return "HOLD_REPLICATION"
    if human_adjudications < 1:
        return "HOLD_HUMAN_ADJUDICATION"
    return "ALLOW_SCOPE_REVIEW"


def lock_ladder(
    provider_accepted=False,
    production_accepted=False,
    take_locked=False,
    voice_locked=False,
    release_locked=False,
):
    if release_locked:
        return "RELEASE_LOCKED"
    if voice_locked:
        return "VOICE_LOCKED"
    if take_locked:
        return "TAKE_LOCKED"
    if production_accepted:
        return "PRODUCTION_ACCEPTED"
    if provider_accepted:
        return "PROVIDER_ACCEPTED_ONLY"
    return "NONE"


def recovery_promotion_gate(genuine_recoveries, distinct_projects, false_resume_count):
    if false_resume_count > 0:
        return "BLOCK_FALSE_RESUME"
    if genuine_recoveries < 3 or distinct_projects < 2:
        return "HOLD_REAL_INTERRUPTION_COUNT"
    return "ALLOW_PROMOTION_REVIEW"


def governor(tasks):
    """Select lowest numeric priority, then highest information gain, among admissible tasks."""
    admissible = [task for task in tasks if task["admissible"]]
    if not admissible:
        return None
    chosen = sorted(admissible, key=lambda task: (task["priority"], -task["information_gain"]))[0]
    return chosen["id"]
