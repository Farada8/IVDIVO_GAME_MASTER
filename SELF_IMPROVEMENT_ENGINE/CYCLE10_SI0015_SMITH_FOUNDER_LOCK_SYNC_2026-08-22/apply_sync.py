#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT_STATE = ROOT / "PROJECT_STATES/IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json"
SYSTEM_STATE = ROOT / "CURRENT_IVDIVO_SYSTEM_STATE.json"
PORTFOLIO_STATE = ROOT / "CURRENT_IVDIVO_PORTFOLIO_FRONTIER_DELTA_2026-08-21.json"

NEXT = "ASSEMBLE_LOCKED_CH01_CH29_MANUSCRIPT_FROM_CURRENT_AUTHORITY_FILES_THEN_RUN_FINAL_COPY_FORMAT_EXPORT_GATE"
LOCK_RECEIPT = "PROJECTS/B03_SMITH_THE_EMPTY_RESCUE/FOUNDER_LOCK_RECEIPT_2026-08-22.md"
CURRENT_MD = "PROJECTS/B03_SMITH_THE_EMPTY_RESCUE/CURRENT_STATE.md"
PROJECT_JSON = "PROJECT_STATES/IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_project(data):
    data["schema_version"] = "2.6"
    data["updated"] = "2026-08-22"
    data["status"] = "FOUNDER_LOCKED_CH01_CH29_MANUSCRIPT_AUTHORITY"
    data["story_lock"] = True
    data["founder_lock"] = True
    data["founder_lock_decision"] = {
        "decision": "GRANTED",
        "date": "2026-08-22",
        "authority_path": LOCK_RECEIPT,
        "human_current_state": CURRENT_MD,
        "locked_scope": "CH01_CH29",
        "ch30_authorized": False,
        "substantive_change_control": "FOUNDER_UNLOCK_OR_CHANGE_ORDER_REQUIRED",
        "next_production_frontier": [
            "BUILD_CURRENT_AUTHORITY_CH01_CH29_MANIFEST",
            "ASSEMBLE_LOCKED_MANUSCRIPT",
            "RUN_COPY_FORMAT_EXPORT_GATE",
            "DOWNSTREAM_AUDIO_ADAPTATION_ONLY_UNDER_SEPARATE_PRODUCTION_AUTHORITY",
        ],
    }
    verified = data.setdefault("verified_block_state", {})
    verified["medical_factual_hold"] = {
        "status": "PASS_BLOCKER_CLOSED",
        "specialist_certification_claimed": False,
    }
    verified["network_relay_factual_hold"] = {
        "status": "PASS_AFTER_MINIMAL_TERMINOLOGY_REPAIR_BLOCKER_CLOSED"
    }
    frontier = data.setdefault("manuscript_frontier", {})
    frontier["completed_with_drive_evidence"] = "CH01_CH29"
    frontier["development_complete"] = True
    frontier["prose_expansion_authorized"] = False
    frontier["ch30_authorized"] = False
    frontier["founder_locked"] = True
    frontier["locked_scope"] = "CH01_CH29"
    frontier["current_lock_authority"] = LOCK_RECEIPT
    data["next_obligations"] = [
        "BUILD_CURRENT_AUTHORITY_CH01_CH29_MANIFEST",
        "ASSEMBLE_LOCKED_CH01_CH29_MANUSCRIPT",
        "RUN_FINAL_COPY_FORMAT_EXPORT_GATE",
        "ROUTE_DOWNSTREAM_AUDIO_ADAPTATION_ONLY_UNDER_SEPARATE_PRODUCTION_AUTHORITY",
    ]
    data["next_obligation"] = NEXT
    deny = set(data.get("do_not") or [])
    deny.update({
        "DO_NOT_WRITE_CH30",
        "DO_NOT_REOPEN_STORY_DEVELOPMENT_WITHOUT_FOUNDER_UNLOCK_OR_CHANGE_ORDER",
        "DO_NOT_TREAT_PRE_LOCK_FACTUAL_LINE_LOCK_PENDING_STATE_AS_CURRENT",
    })
    data["do_not"] = sorted(deny)
    return data


def founder_lock_summary():
    return {
        "project_id": "IVDIVO_BOOK_3_SMITH",
        "title": "SMITH I / OLD EARTH SECURITY — THE EMPTY RESCUE",
        "status": "FOUNDER_LOCKED",
        "date": "2026-08-22",
        "locked_frontier": "CH01_CH29_STORY_MANUSCRIPT",
        "project_state": PROJECT_JSON,
        "founder_lock_authority": LOCK_RECEIPT,
        "human_current_state": CURRENT_MD,
        "ch30_authorized": False,
        "reopen_rule": "ONLY_EXPLICIT_FOUNDER_UNLOCK_OR_CHANGE_ORDER_FOR_SUBSTANTIVE_CHANGE",
        "downstream_live_human_provider_evidence_not_implied": True,
    }


def active_project_summary():
    return {
        "project_id": "IVDIVO_BOOK_3_SMITH",
        "title": "SMITH I / OLD EARTH SECURITY — THE EMPTY RESCUE",
        "mode": "FOUNDER_LOCKED_MANUSCRIPT_ASSEMBLY_COPY_FORMAT_EXPORT",
        "project_state_path": PROJECT_JSON,
        "manuscript_frontier": "CH01_CH29_LOCKED",
        "story_lock": True,
        "founder_lock": "ISSUED",
        "next_unblocked_obligation": NEXT,
        "authority_boundary": "NO_CH30_NO_STORY_DEVELOPMENT_WITHOUT_FOUNDER_UNLOCK_OR_CHANGE_ORDER; LOCKED_MANUSCRIPT_ASSEMBLY_COPY_FORMAT_EXPORT_ONLY",
        "do_not_repeat": [
            "B03_CH25_DRAFT",
            "B03_CH26_DRAFT",
            "B03_CH27_DRAFT",
            "B03_CH28_DRAFT",
            "B03_CH29_DRAFT",
            "B03_CH30_DRAFT",
            "B03_P72_STORY_DEVELOPMENT_GATE",
            "B03_FOUNDER_LOCK_DECISION",
        ],
    }


def patch_system(data):
    data["schema_version"] = "2.4"
    data["updated"] = "2026-08-22"
    pf = data.setdefault("portfolio_frontier", {})
    locked = list(pf.get("text_locked_or_text_complete") or [])
    smith_marker = "IVDIVO_BOOK_3_SMITH_FOUNDER_LOCKED_CH01_CH29_MANUSCRIPT_AUTHORITY"
    if smith_marker not in locked:
        locked.append(smith_marker)
    pf["text_locked_or_text_complete"] = locked
    pf["development_complete_not_locked"] = [
        x for x in (pf.get("development_complete_not_locked") or [])
        if "SMITH" not in x
    ]
    pf["recent_founder_lock"] = founder_lock_summary()
    pf["active_project"] = active_project_summary()
    pf["state_status"] = "D10_FOUNDER_LOCKED; D01_FOUNDER_LOCKED_E01_E120; B03_SMITH_FOUNDER_LOCKED_CH01_CH29; B03_LOCKED_MANUSCRIPT_ASSEMBLY_NEXT; D09_PENDING_FOUNDER_LOCK"
    data["state_status"] = pf["state_status"]
    return data


def patch_portfolio(data):
    data["schema_version"] = "1.4"
    data["updated"] = "2026-08-22"
    data["purpose"] = "Non-destructive portfolio-frontier overlay for CURRENT_IVDIVO_SYSTEM_STATE.json. Project-specific authority/state remains higher. D10, D01 and B03/SMITH are Founder-locked; current B03 production frontier is locked CH01–29 manuscript assembly then copy/format/export."
    locked = list(data.get("text_complete_or_locked") or [])
    smith_marker = "IVDIVO_BOOK_3_SMITH_FOUNDER_LOCKED_CH01_CH29_MANUSCRIPT_AUTHORITY"
    if smith_marker not in locked:
        locked.append(smith_marker)
    data["text_complete_or_locked"] = locked
    data["b03_founder_lock"] = founder_lock_summary()
    data["active_project"] = active_project_summary()
    data["queue_after_d01_founder_lock"] = [
        "IVDIVO_BOOK_3_SMITH_FOUNDER_LOCKED_CH01_CH29_MANUSCRIPT_ASSEMBLY_COPY_FORMAT_EXPORT",
        "IVDIVO_BOOK_4_AFTER_BOOK_3_LOCKED_MANUSCRIPT_EXPORT",
        "WHOLE_PORTFOLIO_TEXT_LOCK_AUDIT",
        "AUDIO_NOVEL_STUDIO_BATCH_INGEST_AND_PRODUCTION",
    ]
    data["state_status"] = "D10_FOUNDER_LOCKED; D01_FOUNDER_LOCKED_E01_E120; B03_SMITH_FOUNDER_LOCKED_CH01_CH29; B03_LOCKED_MANUSCRIPT_ASSEMBLY_NEXT; D09_READY_FOR_FOUNDER_LOCK_DECISION"
    return data


def main():
    save(PROJECT_STATE, patch_project(load(PROJECT_STATE)))
    save(SYSTEM_STATE, patch_system(load(SYSTEM_STATE)))
    save(PORTFOLIO_STATE, patch_portfolio(load(PORTFOLIO_STATE)))


if __name__ == "__main__":
    main()
