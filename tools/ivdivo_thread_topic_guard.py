from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import re


CONTINUATION_TOKENS = {
    "и",
    "дальше",
    "продолжай",
    "продолжить",
    "ок",
    "окей",
    "да",
    "ага",
    "continue",
    "go on",
    "next",
    "okay",
    "ok",
    "yes",
}


@dataclass(frozen=True)
class TopicDecision:
    status: str
    active_project: Optional[str]
    active_topic: Optional[str]
    active_next_gate: Optional[str] = None
    return_token: Optional[str] = None
    drift_blocked: bool = False
    reason: str = ""


def _normalize(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"[.!?,;:…]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def is_bare_continuation(text: str) -> bool:
    """Return True only for a short turn that does not itself carry a new topic."""
    return _normalize(text) in CONTINUATION_TOKENS


def _return_token(project: str, topic: str, next_gate: Optional[str]) -> str:
    return f"RETURN_TOPIC::{project}::{topic}::{next_gate or ''}"


def route_turn(
    *,
    active_project: Optional[str],
    active_topic: Optional[str],
    user_text: str,
    active_next_gate: Optional[str] = None,
    proposed_project: Optional[str] = None,
    proposed_topic: Optional[str] = None,
    explicit_user_switch: bool = False,
    pending_switch_target: Optional[str] = None,
    user_confirms_pending_switch: bool = False,
    side_query: bool = False,
    required_dependency: bool = False,
    discovered_context_project: Optional[str] = None,
    assistant_initiated_pivot: bool = False,
) -> TopicDecision:
    """Fail-closed router that protects the active conversation topic.

    The caller may supply structured intent metadata, but a generic continuation turn
    never authorizes a project switch by itself. Newer or more salient sibling context
    is supporting evidence only unless the user explicitly switches or the current
    task proves a required cross-project dependency.
    """

    if not active_project or not active_topic:
        if is_bare_continuation(user_text):
            return TopicDecision(
                "HOLD_RESTORE_THREAD_TOPIC_BEFORE_CONTINUE",
                active_project,
                active_topic,
                active_next_gate,
                reason="Bare continuation requires restoration of the existing thread topic; it may not select a project by salience.",
            )
        if explicit_user_switch and proposed_project and proposed_topic:
            return TopicDecision(
                "SWITCH_AUTHORIZED",
                proposed_project,
                proposed_topic,
                active_next_gate,
                reason="Explicit user switch establishes a new thread topic.",
            )
        return TopicDecision(
            "HOLD_NO_ACTIVE_THREAD_TOPIC",
            active_project,
            active_topic,
            active_next_gate,
            reason="No active thread topic is available; restore or obtain explicit user scope before execution.",
        )

    if pending_switch_target and user_confirms_pending_switch:
        if not proposed_project or proposed_project != pending_switch_target:
            return TopicDecision(
                "HOLD_SWITCH_CONFIRMATION_TARGET_MISMATCH",
                active_project,
                active_topic,
                active_next_gate,
                reason="A short affirmative can authorize only the exact pending switch target it was bound to.",
            )
        return TopicDecision(
            "SWITCH_AUTHORIZED_BY_BOUND_CONFIRMATION",
            proposed_project,
            proposed_topic or active_topic,
            active_next_gate,
            reason="User confirmation is bound to a previously explicit switch offer for this exact target.",
        )

    if explicit_user_switch:
        if not proposed_project:
            return TopicDecision(
                "HOLD_EXPLICIT_SWITCH_WITHOUT_TARGET",
                active_project,
                active_topic,
                active_next_gate,
                reason="Explicit switch intent requires a target project.",
            )
        return TopicDecision(
            "SWITCH_AUTHORIZED",
            proposed_project,
            proposed_topic or active_topic,
            active_next_gate,
            reason="Explicit user switch outranks the previous thread topic.",
        )

    if is_bare_continuation(user_text):
        drift = bool(proposed_project and proposed_project != active_project)
        drift = drift or bool(assistant_initiated_pivot)
        drift = drift or bool(discovered_context_project and discovered_context_project != active_project)
        return TopicDecision(
            "CONTINUE_ACTIVE_TOPIC",
            active_project,
            active_topic,
            active_next_gate,
            drift_blocked=drift,
            reason="Generic continuation inherits the active thread topic and cannot switch projects.",
        )

    if side_query:
        return TopicDecision(
            "ANSWER_SIDE_QUERY_THEN_RETURN",
            active_project,
            active_topic,
            active_next_gate,
            return_token=_return_token(active_project, active_topic, active_next_gate),
            reason="A bounded question about another project does not rebind the thread topic.",
        )

    if required_dependency:
        return TopicDecision(
            "CROSS_PROJECT_DEPENDENCY_WITH_RETURN_TOKEN",
            active_project,
            active_topic,
            active_next_gate,
            return_token=_return_token(active_project, active_topic, active_next_gate),
            reason="Required cross-project work is bounded and must return to the original topic.",
        )

    if discovered_context_project and discovered_context_project != active_project:
        if not proposed_project or proposed_project == active_project:
            return TopicDecision(
                "SUPPORTING_CONTEXT_ONLY_KEEP_TOPIC",
                active_project,
                active_topic,
                active_next_gate,
                reason="Retrieved sibling context may inform the answer but cannot rebind the active thread.",
            )

    if proposed_project in (None, active_project):
        if proposed_topic and proposed_topic != active_topic:
            return TopicDecision(
                "UPDATE_TOPIC_WITHIN_ACTIVE_PROJECT",
                active_project,
                proposed_topic,
                active_next_gate,
                reason="The request changes topic inside the same active project without cross-project drift.",
            )
        return TopicDecision(
            "CONTINUE_ACTIVE_TOPIC",
            active_project,
            active_topic,
            active_next_gate,
            reason="No authorized cross-project switch was requested.",
        )

    return TopicDecision(
        "HOLD_CROSS_PROJECT_SWITCH_UNAUTHORIZED",
        active_project,
        active_topic,
        active_next_gate,
        drift_blocked=True,
        reason="A different project was proposed without explicit user switch evidence; preserve the thread topic.",
    )


def resolve_return_token(return_token: Optional[str]) -> TopicDecision:
    if not return_token or not return_token.startswith("RETURN_TOPIC::"):
        return TopicDecision(
            "HOLD_INVALID_RETURN_TOKEN",
            None,
            None,
            reason="A valid topic return token is required.",
        )
    parts = return_token.split("::", 3)
    if len(parts) != 4 or not parts[1] or not parts[2]:
        return TopicDecision(
            "HOLD_INVALID_RETURN_TOKEN",
            None,
            None,
            reason="Malformed topic return token.",
        )
    return TopicDecision(
        "RETURN_TO_ORIGINAL_TOPIC",
        parts[1],
        parts[2],
        parts[3] or None,
        return_token=return_token,
        reason="Bounded detour ended; restore the original thread topic and project frontier.",
    )
