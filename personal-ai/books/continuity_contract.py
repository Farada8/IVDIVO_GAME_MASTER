from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from memory.store import MemoryStore

from .continuity import (
    ContinuityChecker as _BaseContinuityChecker,
    ContinuityInputError,
    _canonical_json,
    _render_markdown,
    _write_json,
)


class ContinuityChecker(_BaseContinuityChecker):
    """Strengthened PL-09 contract with stable issue identity and PL-02 output persistence."""

    def __init__(self, home: Path) -> None:
        super().__init__(home)
        self.memory = MemoryStore(Path(home) / "runtime" / "state.db")

    @staticmethod
    def _evidence_index(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
        index: dict[str, dict[str, Any]] = {}
        for section in ("observations", "event_order", "knowledge", "reveals", "completions"):
            raw_records = payload.get(section, [])
            if not isinstance(raw_records, list):
                continue
            for position, raw in enumerate(raw_records):
                if not isinstance(raw, dict):
                    continue
                try:
                    chapter = int(raw.get("chapter"))
                except (TypeError, ValueError):
                    continue
                excerpt = str(raw.get("evidence", "")).strip()
                if chapter < 1 or not excerpt:
                    continue
                rendered = f"CH{chapter}: {excerpt}"
                record_id = str(raw.get("id") or f"{section}-{position + 1:03d}").strip()
                index.setdefault(
                    rendered,
                    {
                        "input_ref": f"{section}[{position}]",
                        "record_id": record_id,
                        "chapter": chapter,
                        "excerpt": excerpt,
                    },
                )
        return index

    @staticmethod
    def _issue_id(issue: dict[str, Any]) -> str:
        fingerprint = {
            "severity": issue["severity"],
            "chapter": issue["chapter"],
            "issue": issue["issue"],
            "rule_id": issue["rule_id"],
            "category": issue["category"],
            "subject": issue["subject"],
            "evidence_pair": issue["evidence_pair"],
        }
        return "issue-" + hashlib.sha256(_canonical_json(fingerprint)).hexdigest()[:20]

    def check(self, project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        report = super().check(project_id, payload)
        evidence_index = self._evidence_index(payload)

        for issue in report["issues"]:
            evidence_pair: list[dict[str, Any]] = []
            for field in ("evidence_a", "evidence_b"):
                rendered = issue[field]
                ref = evidence_index.get(rendered)
                if ref is None:
                    raise ContinuityInputError(
                        f"internal evidence binding failed for {issue['rule_id']}: {rendered}"
                    )
                evidence_pair.append(dict(ref))
            issue["evidence_pair"] = evidence_pair
            issue["issue_id"] = self._issue_id(issue)

        memory_record = self.memory.store(
            json.dumps(report, sort_keys=True, ensure_ascii=False),
            kind="OUTPUT",
            source="PL-09 Continuity Checker",
            project_id=project_id,
            metadata={
                "report_id": report["report_id"],
                "blocking_status": report["blocking_status"],
                "blocking_issue_count": report["blocking_issue_count"],
                "automatic_pass_allowed": False,
                "book_content_sha256": report["book_content_sha256"],
                "input_sha256": report["input_sha256"],
            },
        )
        report["output_memory_id"] = memory_record["id"]

        json_path = Path(report["artifacts"]["json"])
        md_path = Path(report["artifacts"]["markdown"])
        _write_json(json_path, report)
        md_path.write_text(_render_markdown(report), encoding="utf-8")
        return report
