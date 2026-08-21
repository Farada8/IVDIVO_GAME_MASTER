"""Long-horizon drift detector for IVDIVO Saga100.

Flags macro-franchise failure patterns without overriding current-book authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class DriftFinding:
    code: str
    severity: str
    message: str


def detect_long_horizon_drift(snapshot: Mapping[str, object]) -> list[DriftFinding]:
    findings: list[DriftFinding] = []

    if int(snapshot.get("new_lore_terms", 0)) > int(snapshot.get("story_decisions_changed_by_lore", 0)) * 3 + 6:
        findings.append(DriftFinding("LORE_INFLATION", "MAJOR", "Lore growth exceeds decision-bearing story use."))

    if bool(snapshot.get("smith_replaced_by_advanced_actor", False)) or bool(snapshot.get("smith_only_exposition", False)):
        findings.append(DriftFinding("SMITH_OBSOLESCENCE", "MAJOR", "Smith/OES lost active professional function by fiat rather than earned evolution."))

    orbital_fields = set(snapshot.get("orbital_lived_fields", []) or [])
    if snapshot.get("line") == "ORBITAL" and len(orbital_fields & {"housing","work","money","transport","maintenance","law","family","social_life"}) < 3:
        findings.append(DriftFinding("ORBITAL_AS_DECOR", "MAJOR", "Orbital setting lacks enough lived-civilization causal fields."))

    if snapshot.get("line") == "CONFEDERATION_FRONTIER":
        anti_utopia = set(snapshot.get("anti_utopia_fields", []) or [])
        required = {"limit","cost","internal_disagreement","failure","governance"}
        if len(anti_utopia & required) < 4:
            findings.append(DriftFinding("CONFEDERATION_UTOPIA_LEAK", "MAJOR", "Advanced civilization lacks enough limits/cost/disagreement/failure/governance."))
        if bool(snapshot.get("confederation_moral_referee", False)):
            findings.append(DriftFinding("CONFEDERATION_MORAL_REFEREE", "MAJOR", "Confederation is resolving human moral disputes by superior-authority assertion."))

    if snapshot.get("line") == "CROSSING":
        if int(snapshot.get("irreducible_line_dependencies", 0)) < 2 or bool(snapshot.get("permanent_team_default", False)):
            findings.append(DriftFinding("FAN_SERVICE_CROSSING", "MAJOR", "Crossing is not causally necessary or defaults to permanent-team franchise logic."))
        if bool(snapshot.get("advanced_actor_auto_commands", False)):
            findings.append(DriftFinding("JURISDICTION_COLLAPSE", "FATAL", "Capability/knowledge has been silently converted into command authority."))

    if bool(snapshot.get("protagonist_only_thesis_mouthpiece", False)):
        findings.append(DriftFinding("PROTAGONIST_MOUTHPIECE", "MAJOR", "Hero exists primarily to state the civilization thesis instead of pursue a human want."))

    if bool(snapshot.get("current_execution_loaded", False)) is False and snapshot.get("scope") == "ACTIVE_BOOK_EXECUTION":
        findings.append(DriftFinding("STALE_STATE_ROUTING", "FATAL", "Active-book work is proceeding without current execution authority."))
    if snapshot.get("scope") in {"LONG_HORIZON_SAGA", "SAGA_SEQUENCE"} and not bool(snapshot.get("strategic_authority_loaded", False)):
        findings.append(DriftFinding("STRATEGIC_AUTHORITY_OMISSION", "MAJOR", "Long-horizon work omitted the strategic authority layer."))

    if bool(snapshot.get("macro_plan_overrides_local_story", False)):
        findings.append(DriftFinding("MACRO_OVERRIDES_STORY", "FATAL", "Long-horizon neatness is overriding a current complete-book story decision."))

    if bool(snapshot.get("forced_fourth_crossing", False)):
        findings.append(DriftFinding("RIGID_3_PLUS_1", "MAJOR", "Crossing is being forced by ordinal cadence despite failed eligibility."))

    if bool(snapshot.get("capability_jump_without_evidence", False)):
        findings.append(DriftFinding("CAPABILITY_INFLATION", "MAJOR", "Civilization capability advanced without story evidence and recorded consequence."))

    return findings


def highest_severity(findings: Sequence[DriftFinding]) -> str:
    order = {"NONE": 0, "POLISH": 1, "MEDIUM": 2, "MAJOR": 3, "FATAL": 4}
    if not findings:
        return "NONE"
    return max((f.severity for f in findings), key=lambda s: order[s])
