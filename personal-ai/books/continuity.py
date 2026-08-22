from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from memory.store import MemoryStore

from .core import BookProductionCore, _continuity_content_sha256

SEVERITIES = ("FATAL", "MAJOR", "MINOR", "STYLE")
BLOCKING_SEVERITIES = {"FATAL", "MAJOR"}

OBSERVATION_CATEGORIES = {
    "NAME",
    "AGE",
    "APPEARANCE",
    "RELATIONSHIP",
    "DATE_TIME",
    "LOCATION",
    "PROP",
}

SUPPORTED_DOMAINS = (
    "NAME",
    "AGE",
    "APPEARANCE",
    "RELATIONSHIP",
    "DATE_TIME",
    "LOCATION",
    "PROP",
    "EVENT_ORDER",
    "KNOWLEDGE",
    "COMPLETED_EVENT",
)

_DEFAULT_SEVERITY = {
    "NAME": "MAJOR",
    "AGE": "MAJOR",
    "APPEARANCE": "MINOR",
    "RELATIONSHIP": "MAJOR",
    "DATE_TIME": "FATAL",
    "LOCATION": "FATAL",
    "PROP": "MAJOR",
}

_DEFAULT_FIX = {
    "NAME": "Reconcile the canonical character name/alias mapping and update the conflicting reference.",
    "AGE": "Reconcile the character age against the same story-time scope and correct one assertion.",
    "APPEARANCE": "Reconcile the stable appearance attribute or mark an explicit in-story change.",
    "RELATIONSHIP": "Reconcile the relationship status for the same story-time scope.",
    "DATE_TIME": "Resolve the incompatible date/time assertions before preserving event order.",
    "LOCATION": "Resolve the impossible same-scope location conflict or correct the time scope.",
    "PROP": "Reconcile prop ownership/location for the same story-time scope.",
}


class ContinuityInputError(ValueError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


def _clean_text(value: Any, field: str) -> str:
    if value is None:
        raise ContinuityInputError(f"{field} is required")
    text = str(value).strip()
    if not text:
        raise ContinuityInputError(f"{field} cannot be empty")
    return text


def _chapter(value: Any, field: str) -> int:
    if isinstance(value, bool):
        raise ContinuityInputError(f"{field} must be an integer >= 1")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ContinuityInputError(f"{field} must be an integer >= 1") from exc
    if parsed < 1:
        raise ContinuityInputError(f"{field} must be an integer >= 1")
    return parsed


def _scalar(value: Any, field: str) -> str | int | float | bool | None:
    if isinstance(value, (dict, list)):
        raise ContinuityInputError(f"{field} must be a JSON scalar")
    return value


def _name_norm(value: Any) -> str:
    return " ".join(str(value).strip().casefold().split())


def _record_ref(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "input_ref": record["input_ref"],
        "record_id": record["id"],
        "chapter": record["chapter"],
        "excerpt": record["evidence"],
    }


@dataclass(frozen=True)
class Issue:
    severity: str
    chapter: int
    issue: str
    evidence_a: str
    evidence_b: str
    evidence_pair: tuple[dict[str, Any], dict[str, Any]]
    suggested_fix: str
    rule_id: str
    category: str
    subject: str

    def to_dict(self) -> dict[str, Any]:
        core = {
            "severity": self.severity,
            "chapter": self.chapter,
            "issue": self.issue,
            "evidence_a": self.evidence_a,
            "evidence_b": self.evidence_b,
            "evidence_pair": [dict(self.evidence_pair[0]), dict(self.evidence_pair[1])],
            "suggested_fix": self.suggested_fix,
            "rule_id": self.rule_id,
            "category": self.category,
            "subject": self.subject,
        }
        core["issue_id"] = "issue-" + _sha256(
            {
                "rule_id": self.rule_id,
                "category": self.category,
                "subject": self.subject,
                "evidence_pair": core["evidence_pair"],
            }
        )[:20]
        return core


def _render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Continuity report",
        "",
        f"- Report: `{report['report_id']}`",
        f"- Project: `{report['project_id']}`",
        f"- Book content SHA-256: `{report['book_content_sha256']}`",
        f"- Input SHA-256: `{report['input_sha256']}`",
        f"- Blocking status: **{report['blocking_status']}**",
        f"- Gate action: **{report['gate_action']}**",
        "",
        "## Summary",
        "",
    ]
    for severity in SEVERITIES:
        lines.append(f"- {severity}: {report['summary'][severity]}")
    lines.extend(
        [
            f"- Total issues: {report['summary']['TOTAL']}",
            "",
            "## Issues",
            "",
        ]
    )
    if not report["issues"]:
        lines.append("No contradictions were detected in the supplied structured evidence.")
    for index, issue in enumerate(report["issues"], start=1):
        pair = issue["evidence_pair"]
        lines.extend(
            [
                f"### {index}. [{issue['severity']}] {issue['rule_id']} — `{issue['issue_id']}`",
                "",
                issue["issue"],
                "",
                f"- Chapter: {issue['chapter']}",
                f"- Category: {issue['category']}",
                f"- Subject: `{issue['subject']}`",
                f"- Evidence A: {issue['evidence_a']} (`{pair[0]['input_ref']}`)",
                f"- Evidence B: {issue['evidence_b']} (`{pair[1]['input_ref']}`)",
                f"- Suggested fix: {issue['suggested_fix']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Evidence boundary",
            "",
            "This deterministic checker evaluates only the structured evidence supplied to its supported rules. It does not prove that a manuscript was exhaustively extracted or that no unsupported contradiction exists. It never writes a continuity PASS automatically.",
            "",
        ]
    )
    return "\n".join(lines)


class ContinuityChecker:
    """PL-09 deterministic checker over normalized continuity evidence."""

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.books = BookProductionCore(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")

    def check(self, project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ContinuityInputError("continuity input must be a JSON object")

        loaded = self.books.load(project_id)
        state = loaded["state"]
        if state["stage"] != "CONTINUITY":
            raise ContinuityInputError(
                "PL-09 check is only admissible while book stage == CONTINUITY"
            )
        root = Path(loaded["root"])

        observations = self._observations(payload.get("observations", []))
        event_order = self._event_order(payload.get("event_order", []))
        knowledge = self._knowledge(payload.get("knowledge", []))
        reveals = self._reveals(payload.get("reveals", []))
        completions = self._completions(payload.get("completions", []))

        issues: list[Issue] = []
        issues.extend(self._observation_issues(observations))
        issues.extend(self._event_order_issues(event_order))
        issues.extend(self._knowledge_issues(knowledge, reveals))
        issues.extend(self._completion_issues(completions))
        issues.sort(
            key=lambda item: (
                item.chapter,
                SEVERITIES.index(item.severity),
                item.rule_id,
                item.subject,
            )
        )

        issue_dicts = [item.to_dict() for item in issues]
        summary: dict[str, int] = {severity: 0 for severity in SEVERITIES}
        for issue in issue_dicts:
            summary[issue["severity"]] += 1
        summary["TOTAL"] = len(issue_dicts)
        blocking = summary["FATAL"] + summary["MAJOR"]

        input_hash = _sha256(payload)
        book_hash = _continuity_content_sha256(root)
        report_id = f"continuity-{book_hash[:12]}-{input_hash[:12]}"
        report: dict[str, Any] = {
            "schema": "ivdivo.personal_ai.continuity_report/0.2",
            "checker": "PL-09_DETERMINISTIC_STRUCTURED_CONTINUITY",
            "report_id": report_id,
            "project_id": project_id,
            "generated_at": _utc_now(),
            "book_content_sha256": book_hash,
            "input_sha256": input_hash,
            "supported_domains": list(SUPPORTED_DOMAINS),
            "summary": summary,
            "blocking_issue_count": blocking,
            "blocking_status": "FAIL" if blocking else "NO_BLOCKING_ISSUES_DETECTED",
            "gate_action": "EXPLICIT_FAIL_RECOMMENDED" if blocking else "MANUAL_REVIEW_REQUIRED",
            "automatic_pass_allowed": False,
            "issues": issue_dicts,
            "evidence_boundary": (
                "Only supplied structured evidence is checked; absence of detected issues is not proof of exhaustive manuscript continuity."
            ),
        }
        json_path = root / "continuity" / f"{report_id}.json"
        md_path = root / "continuity" / f"{report_id}.md"
        report["artifacts"] = {"json": str(json_path), "markdown": str(md_path)}

        memory = self.memory.store(
            json.dumps(report, sort_keys=True, ensure_ascii=False),
            kind="OUTPUT",
            source="PL-09 Continuity Checker",
            project_id=project_id,
            metadata={
                "report_id": report_id,
                "book_content_sha256": book_hash,
                "input_sha256": input_hash,
                "blocking_status": report["blocking_status"],
                "blocking_issue_count": blocking,
                "automatic_pass_allowed": False,
                "json_path": str(json_path),
                "markdown_path": str(md_path),
            },
        )
        report["output_memory_id"] = memory["id"]
        _write_json(json_path, report)
        md_path.write_text(_render_markdown(report), encoding="utf-8")
        return report

    @staticmethod
    def _record_id(raw: dict[str, Any], default: str, field: str) -> str:
        return _clean_text(raw.get("id") or default, f"{field}.id")

    def _observations(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            raise ContinuityInputError("observations must be a list")
        output: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for index, raw in enumerate(value, start=1):
            field = f"observations[{index}]"
            if not isinstance(raw, dict):
                raise ContinuityInputError(f"{field} must be an object")
            category = _clean_text(raw.get("category"), f"{field}.category").upper()
            if category not in OBSERVATION_CATEGORIES:
                raise ContinuityInputError(f"{field}.category unsupported: {category}")
            record_id = self._record_id(raw, f"obs-{index:03d}", field)
            if record_id in seen_ids:
                raise ContinuityInputError(f"duplicate observation id: {record_id}")
            seen_ids.add(record_id)
            output.append(
                {
                    "id": record_id,
                    "input_ref": field,
                    "category": category,
                    "subject": _clean_text(raw.get("subject"), f"{field}.subject"),
                    "field": _clean_text(raw.get("field"), f"{field}.field"),
                    "scope": _clean_text(raw.get("scope", "GLOBAL"), f"{field}.scope"),
                    "value": _scalar(raw.get("value"), f"{field}.value"),
                    "chapter": _chapter(raw.get("chapter"), f"{field}.chapter"),
                    "evidence": _clean_text(raw.get("evidence"), f"{field}.evidence"),
                }
            )
        return output

    def _event_order(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            raise ContinuityInputError("event_order must be a list")
        output: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for index, raw in enumerate(value, start=1):
            field = f"event_order[{index}]"
            if not isinstance(raw, dict):
                raise ContinuityInputError(f"{field} must be an object")
            record_id = self._record_id(raw, f"order-{index:03d}", field)
            if record_id in seen_ids:
                raise ContinuityInputError(f"duplicate event_order id: {record_id}")
            seen_ids.add(record_id)
            before = _clean_text(raw.get("before"), f"{field}.before")
            after = _clean_text(raw.get("after"), f"{field}.after")
            if before == after:
                raise ContinuityInputError(f"{field} cannot order an event before itself")
            output.append(
                {
                    "id": record_id,
                    "input_ref": field,
                    "before": before,
                    "after": after,
                    "chapter": _chapter(raw.get("chapter"), f"{field}.chapter"),
                    "evidence": _clean_text(raw.get("evidence"), f"{field}.evidence"),
                }
            )
        return output

    def _knowledge(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            raise ContinuityInputError("knowledge must be a list")
        output: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for index, raw in enumerate(value, start=1):
            field = f"knowledge[{index}]"
            if not isinstance(raw, dict):
                raise ContinuityInputError(f"{field} must be an object")
            record_id = self._record_id(raw, f"knowledge-{index:03d}", field)
            if record_id in seen_ids:
                raise ContinuityInputError(f"duplicate knowledge id: {record_id}")
            seen_ids.add(record_id)
            output.append(
                {
                    "id": record_id,
                    "input_ref": field,
                    "character": _clean_text(raw.get("character"), f"{field}.character"),
                    "fact": _clean_text(raw.get("fact"), f"{field}.fact"),
                    "chapter": _chapter(raw.get("chapter"), f"{field}.chapter"),
                    "evidence": _clean_text(raw.get("evidence"), f"{field}.evidence"),
                }
            )
        return output

    def _reveals(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            raise ContinuityInputError("reveals must be a list")
        output: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for index, raw in enumerate(value, start=1):
            field = f"reveals[{index}]"
            if not isinstance(raw, dict):
                raise ContinuityInputError(f"{field} must be an object")
            record_id = self._record_id(raw, f"reveal-{index:03d}", field)
            if record_id in seen_ids:
                raise ContinuityInputError(f"duplicate reveal id: {record_id}")
            seen_ids.add(record_id)
            output.append(
                {
                    "id": record_id,
                    "input_ref": field,
                    "fact": _clean_text(raw.get("fact"), f"{field}.fact"),
                    "chapter": _chapter(raw.get("chapter"), f"{field}.chapter"),
                    "evidence": _clean_text(raw.get("evidence"), f"{field}.evidence"),
                }
            )
        return output

    def _completions(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            raise ContinuityInputError("completions must be a list")
        output: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for index, raw in enumerate(value, start=1):
            field = f"completions[{index}]"
            if not isinstance(raw, dict):
                raise ContinuityInputError(f"{field} must be an object")
            record_id = self._record_id(raw, f"completion-{index:03d}", field)
            if record_id in seen_ids:
                raise ContinuityInputError(f"duplicate completion id: {record_id}")
            seen_ids.add(record_id)
            repeatable = raw.get("repeatable", False)
            if not isinstance(repeatable, bool):
                raise ContinuityInputError(f"{field}.repeatable must be boolean")
            output.append(
                {
                    "id": record_id,
                    "input_ref": field,
                    "event": _clean_text(raw.get("event"), f"{field}.event"),
                    "chapter": _chapter(raw.get("chapter"), f"{field}.chapter"),
                    "evidence": _clean_text(raw.get("evidence"), f"{field}.evidence"),
                    "repeatable": repeatable,
                }
            )
        return output

    def _observation_issues(self, observations: list[dict[str, Any]]) -> list[Issue]:
        groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = {}
        for record in observations:
            key = (
                record["category"],
                record["subject"],
                record["field"],
                record["scope"],
            )
            groups.setdefault(key, []).append(record)

        issues: list[Issue] = []
        for (category, subject, field, scope), records in groups.items():
            ordered = sorted(records, key=lambda item: (item["chapter"], item["id"]))
            baseline = ordered[0]
            baseline_value = baseline["value"]
            for other in ordered[1:]:
                if other["value"] == baseline_value:
                    continue
                severity = _DEFAULT_SEVERITY[category]
                rule_id = f"{category}_CONFLICT"
                if category == "NAME" and _name_norm(other["value"]) == _name_norm(
                    baseline_value
                ):
                    severity = "STYLE"
                    rule_id = "NAME_STYLE_VARIANT"
                issues.append(
                    Issue(
                        severity=severity,
                        chapter=max(baseline["chapter"], other["chapter"]),
                        issue=(
                            f"Conflicting {category.lower()} assertions for {subject}.{field} "
                            f"within scope {scope}: {baseline_value!r} vs {other['value']!r}."
                        ),
                        evidence_a=f"CH{baseline['chapter']}: {baseline['evidence']}",
                        evidence_b=f"CH{other['chapter']}: {other['evidence']}",
                        evidence_pair=(_record_ref(baseline), _record_ref(other)),
                        suggested_fix=_DEFAULT_FIX[category],
                        rule_id=rule_id,
                        category=category,
                        subject=subject,
                    )
                )
        return issues

    def _event_order_issues(self, constraints: list[dict[str, Any]]) -> list[Issue]:
        by_pair: dict[tuple[str, str], dict[str, Any]] = {}
        issues: list[Issue] = []
        emitted: set[frozenset[str]] = set()
        for record in constraints:
            reverse = by_pair.get((record["after"], record["before"]))
            pair_key = frozenset({record["before"], record["after"]})
            if reverse is not None and pair_key not in emitted:
                emitted.add(pair_key)
                issues.append(
                    Issue(
                        severity="FATAL",
                        chapter=max(record["chapter"], reverse["chapter"]),
                        issue=(
                            f"Event order is mutually contradictory: {reverse['before']} before {reverse['after']} "
                            f"and {record['before']} before {record['after']}."
                        ),
                        evidence_a=f"CH{reverse['chapter']}: {reverse['evidence']}",
                        evidence_b=f"CH{record['chapter']}: {record['evidence']}",
                        evidence_pair=(_record_ref(reverse), _record_ref(record)),
                        suggested_fix="Choose the authoritative event order and repair the conflicting sequence reference.",
                        rule_id="EVENT_ORDER_INVERSE",
                        category="EVENT_ORDER",
                        subject=f"{record['before']}|{record['after']}",
                    )
                )
            by_pair[(record["before"], record["after"])] = record
        return issues

    def _knowledge_issues(
        self,
        knowledge: list[dict[str, Any]],
        reveals: list[dict[str, Any]],
    ) -> list[Issue]:
        earliest_reveal: dict[str, dict[str, Any]] = {}
        for reveal in reveals:
            current = earliest_reveal.get(reveal["fact"])
            if current is None or reveal["chapter"] < current["chapter"]:
                earliest_reveal[reveal["fact"]] = reveal

        issues: list[Issue] = []
        for known in knowledge:
            reveal = earliest_reveal.get(known["fact"])
            if reveal is None or known["chapter"] >= reveal["chapter"]:
                continue
            issues.append(
                Issue(
                    severity="MAJOR",
                    chapter=known["chapter"],
                    issue=(
                        f"{known['character']} uses/knows fact {known['fact']} in CH{known['chapter']} "
                        f"before its earliest supplied reveal in CH{reveal['chapter']}."
                    ),
                    evidence_a=f"CH{known['chapter']}: {known['evidence']}",
                    evidence_b=f"CH{reveal['chapter']}: {reveal['evidence']}",
                    evidence_pair=(_record_ref(known), _record_ref(reveal)),
                    suggested_fix="Move the knowledge acquisition earlier with evidence, delay the character knowledge, or correct the reveal record.",
                    rule_id="KNOWLEDGE_BEFORE_REVEAL",
                    category="KNOWLEDGE",
                    subject=known["character"],
                )
            )
        return issues

    def _completion_issues(self, completions: list[dict[str, Any]]) -> list[Issue]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for record in completions:
            if not record["repeatable"]:
                grouped.setdefault(record["event"], []).append(record)
        issues: list[Issue] = []
        for event, records in grouped.items():
            ordered = sorted(records, key=lambda item: (item["chapter"], item["id"]))
            if len(ordered) < 2:
                continue
            first = ordered[0]
            for other in ordered[1:]:
                issues.append(
                    Issue(
                        severity="MAJOR",
                        chapter=other["chapter"],
                        issue=(
                            f"Non-repeatable event {event} is marked completed again in CH{other['chapter']} "
                            f"after completion in CH{first['chapter']}."
                        ),
                        evidence_a=f"CH{first['chapter']}: {first['evidence']}",
                        evidence_b=f"CH{other['chapter']}: {other['evidence']}",
                        evidence_pair=(_record_ref(first), _record_ref(other)),
                        suggested_fix="Remove the duplicate completion, mark the event repeatable if canon supports it, or distinguish the events with unique IDs.",
                        rule_id="ALREADY_COMPLETED_EVENT",
                        category="COMPLETED_EVENT",
                        subject=event,
                    )
                )
        return issues
