from __future__ import annotations
import re

ID_RE = re.compile(r"^SI-(\d{4})$")

def _n(si_id: str) -> int:
    m = ID_RE.match(si_id)
    if not m:
        raise ValueError(f"invalid SI id: {si_id}")
    return int(m.group(1))

def validate_snapshot(snapshot: dict, current_main_sha: str | None = None) -> dict:
    cov = snapshot.get("open_pr_metadata_coverage", {})
    diff = snapshot.get("diff_coverage", {})
    if not cov.get("metadata_complete"):
        return {"status":"HOLD_PARTIAL_VISIBILITY","reason":"OPEN_PR_METADATA_INCOMPLETE"}
    if not diff.get("visibility_complete"):
        return {"status":"HOLD_PARTIAL_VISIBILITY","reason":diff.get("hold_reason","DIFF_VISIBILITY_INCOMPLETE")}
    if current_main_sha is not None and current_main_sha != snapshot.get("main_sha"):
        return {"status":"HOLD_STALE_SNAPSHOT","snapshot_main":snapshot.get("main_sha"),"current_main":current_main_sha}

    committed=set(snapshot["committed_registry"]["committed_ids"])
    reserved={}
    collisions=[]
    for r in snapshot.get("reservations",[]):
        if r.get("status") != "RESERVED_OPEN_PR":
            continue
        cid=r["candidate_id"]
        if cid in committed:
            collisions.append({"candidate_id":cid,"kind":"COMMITTED_VS_OPEN_RESERVATION","pr":r.get("pr")})
        if cid in reserved:
            collisions.append({"candidate_id":cid,"kind":"OPEN_PR_VS_OPEN_PR","prs":[reserved[cid],r.get("pr")]})
        reserved[cid]=r.get("pr")
    if collisions:
        return {"status":"HOLD_ID_COLLISION","collisions":collisions}

    used={_n(x) for x in committed | set(reserved)}
    nxt=1
    while nxt in used:
        nxt += 1
    return {"status":"PASS_COMPLETE_RESERVATION_VIEW","next_unreserved":f"SI-{nxt:04d}","allocation_authorized":True}

def merge_time_revalidate(snapshot: dict, current_main_sha: str, current_committed_ids: list[str], current_open_reservations: list[dict]) -> dict:
    if current_main_sha != snapshot.get("main_sha"):
        return {"status":"HOLD_STALE_SNAPSHOT","reason":"MAIN_ADVANCED_RESCAN_REQUIRED"}
    committed=set(current_committed_ids)
    seen={}
    collisions=[]
    for r in current_open_reservations:
        if r.get("status") != "RESERVED_OPEN_PR":
            continue
        cid=r["candidate_id"]
        if cid in committed:
            collisions.append((cid,"COMMITTED_VS_RESERVED"))
        if cid in seen:
            collisions.append((cid,"RESERVED_VS_RESERVED"))
        seen[cid]=r.get("pr")
    return {"status":"HOLD_ID_COLLISION","collisions":collisions} if collisions else {"status":"PASS_REVALIDATED"}

def reservation_lifecycle(pr_state: str, merged: bool, candidate_still_present: bool, superseded: bool=False) -> str:
    if superseded:
        return "RELEASED_SUPERSEDED"
    if merged:
        return "REVALIDATE_AS_COMMITTED"
    if pr_state == "closed":
        return "RELEASED_CLOSED_UNMERGED"
    if pr_state == "open" and candidate_still_present:
        return "RESERVED_OPEN_PR"
    if pr_state == "open" and not candidate_still_present:
        return "RELEASED_CANDIDATE_REMOVED"
    return "HOLD_UNKNOWN_LIFECYCLE"

def classify_record(record: dict) -> str:
    s=record.get("status")
    if s=="RESERVED_OPEN_PR":
        return "RESERVES"
    if s in {"HISTORICAL_PROVENANCE_ONLY","CANDIDATE_RECORDS_ONLY_NOT_REGISTRY_WRITE_THROUGH",
             "NO_ALLOCATION_EXPLICIT","NO_NEW_ID_OBSERVED","RELEASED_CLOSED_UNMERGED",
             "RELEASED_SUPERSEDED","RELEASED_CANDIDATE_REMOVED"}:
        return "DOES_NOT_RESERVE"
    return "AMBIGUOUS_DISCOVERY_ONLY"

def renumber_candidate(old_id: str, new_id: str, provenance: dict) -> dict:
    if old_id == new_id:
        raise ValueError("renumber must change id")
    _n(old_id); _n(new_id)
    return {
        "status":"REN_NUMBER_REQUIRED_BEFORE_MERGE",
        "old_candidate_id":old_id,
        "new_candidate_id":new_id,
        "preserve_provenance":True,
        "source_pr":provenance.get("pr"),
        "source_blob_sha":provenance.get("candidate_blob_sha"),
        "historical_alias":old_id
    }
