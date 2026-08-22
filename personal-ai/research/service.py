from __future__ import annotations

import csv
import hashlib
import json
from datetime import date
from decimal import Decimal, DivisionByZero, InvalidOperation
from pathlib import Path
from typing import Any

from evidence import EvidenceStore
from memory.store import MemoryStore
from projects.manager import ProjectStateManager

RESEARCH_STATUSES = ("OBSERVED", "CALCULATED", "INFERRED", "UNKNOWN")
CALCULATION_OPERATIONS = ("SUM", "SUBTRACT", "MULTIPLY", "DIVIDE")


class ResearchInputError(ValueError):
    pass


def _clean_text(value: Any, field: str) -> str:
    text = str(value).strip() if value is not None else ""
    if not text:
        raise ResearchInputError(f"{field} cannot be empty")
    return text


def _iso_date(value: Any, field: str) -> date:
    raw = _clean_text(value, field)
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise ResearchInputError(f"{field} must be YYYY-MM-DD") from exc


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _input_hash(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def _decimal(value: Any, field: str) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ResearchInputError(f"{field} must be numeric or null")
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ResearchInputError(f"{field} must be numeric or null") from exc
    if not parsed.is_finite():
        raise ResearchInputError(f"{field} must be finite")
    return parsed


def _decimal_json(value: Decimal | None) -> str | None:
    if value is None:
        return None
    normalized = value.normalize()
    return format(normalized, "f")


class BusinessResearchService:
    """PL-07 deterministic provenance-first business research packet builder."""

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.evidence = EvidenceStore(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")

    def create_research(self, project_id: str, request: dict[str, Any]) -> dict[str, Any]:
        project = self.projects.load_project(_clean_text(project_id, "project_id"))
        normalized = self._validate_request(request)
        digest = _input_hash(normalized)
        research_id = f"research-{digest[:16]}"
        root = Path(project["root"]) / "artifacts" / "research" / research_id
        manifest_path = root / "manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("input_sha256") != digest:
                raise RuntimeError("research id collision with different input hash")
            return self.load_research(project_id, research_id)

        root.mkdir(parents=True, exist_ok=False)
        source_rows, source_lookup = self._persist_sources(project_id, normalized)
        calculations = self._run_calculations(project_id, normalized, source_lookup)
        calculation_lookup = {item["id"]: item for item in calculations}
        claims, claim_lookup = self._persist_claims(
            project_id, normalized, source_lookup, calculation_lookup
        )
        conclusions = self._validate_conclusions(
            normalized, claim_lookup, calculation_lookup
        )
        comparison = self._comparison_rows(normalized)
        open_questions = self._open_questions(normalized)

        _write_json(root / "sources.json", {"sources": source_rows})
        _write_json(
            root / "claims.json",
            {"claims": claims, "calculations": calculations},
        )
        self._write_comparison(root / "comparison.csv", comparison)
        (root / "conclusions.md").write_text(
            self._conclusions_markdown(normalized, conclusions), encoding="utf-8"
        )
        (root / "open_questions.md").write_text(
            self._open_questions_markdown(open_questions), encoding="utf-8"
        )

        output_memory = self.memory.store(
            _canonical_json(
                {
                    "research_id": research_id,
                    "question": normalized["question"],
                    "geography": normalized["geography"],
                    "industry": normalized["industry"],
                    "as_of": normalized["as_of"],
                    "source_count": len(source_rows),
                    "claim_count": len(claims),
                    "calculation_count": len(calculations),
                    "conclusion_count": len(conclusions),
                    "open_question_count": len(open_questions),
                }
            ),
            kind="OUTPUT",
            source="PL-07 Business Research",
            metadata={
                "research_id": research_id,
                "question": normalized["question"],
                "as_of": normalized["as_of"],
                "input_sha256": digest,
            },
            project_id=project_id,
        )

        manifest = {
            "schema": "ivdivo.personal_ai.business_research/0.1",
            "research_id": research_id,
            "project_id": project_id,
            "question": normalized["question"],
            "geography": normalized["geography"],
            "industry": normalized["industry"],
            "as_of": normalized["as_of"],
            "freshness_max_days": normalized.get("freshness_max_days"),
            "input_sha256": digest,
            "output_memory_id": output_memory["id"],
            "files": [
                "sources.json",
                "claims.json",
                "comparison.csv",
                "conclusions.md",
                "open_questions.md",
            ],
            "evidence_boundary": (
                "Research packet organizes supplied evidence/calculations. "
                "It does not make source presence equivalent to truth, and UNKNOWN/null never means zero/false."
            ),
        }
        _write_json(manifest_path, manifest)
        return self.load_research(project_id, research_id)

    def load_research(self, project_id: str, research_id: str) -> dict[str, Any]:
        project = self.projects.load_project(_clean_text(project_id, "project_id"))
        if not research_id.startswith("research-") or "/" in research_id or "\\" in research_id:
            raise ResearchInputError("invalid research_id")
        root = Path(project["root"]) / "artifacts" / "research" / research_id
        required = [
            "manifest.json",
            "sources.json",
            "claims.json",
            "comparison.csv",
            "conclusions.md",
            "open_questions.md",
        ]
        missing = [name for name in required if not (root / name).is_file()]
        if missing:
            raise FileNotFoundError(f"research packet incomplete: {missing}")
        return {
            "root": str(root),
            "manifest": json.loads((root / "manifest.json").read_text(encoding="utf-8")),
            "sources": json.loads((root / "sources.json").read_text(encoding="utf-8")),
            "claims": json.loads((root / "claims.json").read_text(encoding="utf-8")),
            "comparison_csv": (root / "comparison.csv").read_text(encoding="utf-8"),
            "conclusions_md": (root / "conclusions.md").read_text(encoding="utf-8"),
            "open_questions_md": (root / "open_questions.md").read_text(encoding="utf-8"),
        }

    def _validate_request(self, request: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(request, dict):
            raise ResearchInputError("request must be a JSON object")
        normalized = json.loads(_canonical_json(request))
        normalized["question"] = _clean_text(normalized.get("question"), "question")
        normalized["geography"] = _clean_text(normalized.get("geography"), "geography")
        normalized["industry"] = _clean_text(normalized.get("industry"), "industry")
        as_of = _iso_date(normalized.get("as_of"), "as_of")
        normalized["as_of"] = as_of.isoformat()
        freshness = normalized.get("freshness_max_days")
        if freshness is not None:
            if isinstance(freshness, bool) or not isinstance(freshness, int) or freshness < 0:
                raise ResearchInputError("freshness_max_days must be a non-negative integer or null")
        for field in ("sources", "claims", "calculations", "comparison", "conclusions", "open_questions"):
            value = normalized.get(field, [])
            if not isinstance(value, list):
                raise ResearchInputError(f"{field} must be a list")
            normalized[field] = value
        return normalized

    def _persist_sources(
        self, project_id: str, request: dict[str, Any]
    ) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
        result: list[dict[str, Any]] = []
        lookup: dict[str, dict[str, Any]] = {}
        as_of = _iso_date(request["as_of"], "as_of")
        threshold = request.get("freshness_max_days")
        for index, item in enumerate(request["sources"]):
            if not isinstance(item, dict):
                raise ResearchInputError(f"sources[{index}] must be an object")
            key = _clean_text(item.get("key"), f"sources[{index}].key")
            if key in lookup:
                raise ResearchInputError(f"duplicate source key: {key}")
            document_text = _clean_text(
                item.get("document_text"), f"sources[{index}].document_text"
            )
            excerpt = _clean_text(item.get("excerpt"), f"sources[{index}].excerpt")
            source_as_of_raw = item.get("source_as_of")
            age_days: int | None = None
            if source_as_of_raw is None:
                freshness_status = "UNKNOWN"
                source_as_of = None
            else:
                parsed = _iso_date(source_as_of_raw, f"sources[{index}].source_as_of")
                source_as_of = parsed.isoformat()
                age_days = (as_of - parsed).days
                if age_days < 0:
                    freshness_status = "FUTURE"
                elif threshold is None:
                    freshness_status = "DATED"
                elif age_days <= threshold:
                    freshness_status = "FRESH"
                else:
                    freshness_status = "STALE"
            title = _clean_text(item.get("title", key), f"sources[{index}].title")
            common_metadata = {
                "research_source_key": key,
                "title": title,
                "url": item.get("url"),
                "source_as_of": source_as_of,
                "retrieved_at": item.get("retrieved_at"),
                "freshness_status": freshness_status,
                "age_days": age_days,
            }
            document = self.evidence.create_document(
                project_id,
                document_text,
                source_label=title,
                metadata={**common_metadata, "research_role": "DOCUMENT"},
            )
            source = self.evidence.create_source(
                project_id,
                document["id"],
                excerpt,
                source_label=title,
                metadata={**common_metadata, "research_role": "SOURCE"},
            )
            row = {
                "key": key,
                "title": title,
                "url": item.get("url"),
                "source_as_of": source_as_of,
                "retrieved_at": item.get("retrieved_at"),
                "freshness_status": freshness_status,
                "age_days": age_days,
                "document_id": document["id"],
                "source_id": source["id"],
                "content_hash": source["content_hash"],
            }
            result.append(row)
            lookup[key] = row
        return result, lookup

    def _run_calculations(
        self,
        project_id: str,
        request: dict[str, Any],
        source_lookup: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        seen: set[str] = set()
        for index, item in enumerate(request["calculations"]):
            if not isinstance(item, dict):
                raise ResearchInputError(f"calculations[{index}] must be an object")
            calc_id = _clean_text(item.get("id"), f"calculations[{index}].id")
            if calc_id in seen:
                raise ResearchInputError(f"duplicate calculation id: {calc_id}")
            seen.add(calc_id)
            operation = _clean_text(item.get("operation"), f"calculations[{index}].operation").upper()
            if operation not in CALCULATION_OPERATIONS:
                raise ResearchInputError(f"unsupported calculation operation: {operation}")
            operands_raw = item.get("operands")
            if not isinstance(operands_raw, list) or not operands_raw:
                raise ResearchInputError(f"calculations[{index}].operands must be a non-empty list")
            operands = [
                _decimal(value, f"calculations[{index}].operands[{position}]")
                for position, value in enumerate(operands_raw)
            ]
            source_keys = item.get("source_keys", [])
            if not isinstance(source_keys, list):
                raise ResearchInputError(f"calculations[{index}].source_keys must be a list")
            source_ids = self._source_ids(source_keys, source_lookup, f"calculations[{index}]")
            if any(value is None for value in operands):
                result_value = None
                status = "UNKNOWN"
                unknown_reason = "one or more calculation operands are missing"
            else:
                result_value = self._calculate(operation, [value for value in operands if value is not None])
                status = "CALCULATED"
                unknown_reason = None
            text = item.get("text") or (
                f"Calculation {calc_id}: {operation} -> {_decimal_json(result_value) if result_value is not None else 'UNKNOWN'}"
            )
            claim = self.evidence.create_claim(
                project_id,
                _clean_text(text, f"calculations[{index}].text"),
                "TEST_RESULT",
                source_ids=source_ids,
                metadata={
                    "research_role": "CALCULATION",
                    "calculation_id": calc_id,
                    "operation": operation,
                    "operands": [_decimal_json(value) for value in operands],
                    "result": _decimal_json(result_value),
                    "research_status": status,
                    "unknown_reason": unknown_reason,
                },
            )
            results.append(
                {
                    "id": calc_id,
                    "operation": operation,
                    "operands": [_decimal_json(value) for value in operands],
                    "result": _decimal_json(result_value),
                    "status": status,
                    "unknown_reason": unknown_reason,
                    "source_keys": list(source_keys),
                    "source_ids": source_ids,
                    "claim_id": claim["id"],
                    "verified_state": claim["metadata"]["verified_state"],
                }
            )
        return results

    @staticmethod
    def _calculate(operation: str, operands: list[Decimal]) -> Decimal:
        try:
            if operation == "SUM":
                return sum(operands, Decimal("0"))
            if operation == "SUBTRACT":
                if len(operands) != 2:
                    raise ResearchInputError("SUBTRACT requires exactly two operands")
                return operands[0] - operands[1]
            if operation == "MULTIPLY":
                result = Decimal("1")
                for value in operands:
                    result *= value
                return result
            if operation == "DIVIDE":
                if len(operands) != 2:
                    raise ResearchInputError("DIVIDE requires exactly two operands")
                if operands[1] == 0:
                    raise ResearchInputError("DIVIDE denominator cannot be zero")
                return operands[0] / operands[1]
        except (DivisionByZero, InvalidOperation) as exc:
            raise ResearchInputError(f"invalid {operation} calculation") from exc
        raise ResearchInputError(f"unsupported calculation operation: {operation}")

    def _persist_claims(
        self,
        project_id: str,
        request: dict[str, Any],
        source_lookup: dict[str, dict[str, Any]],
        calculation_lookup: dict[str, dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
        results: list[dict[str, Any]] = []
        lookup: dict[str, dict[str, Any]] = {}
        type_map = {
            "OBSERVED": "SOURCE_CLAIM",
            "CALCULATED": "TEST_RESULT",
            "INFERRED": "AI_INFERENCE",
            "UNKNOWN": "HYPOTHESIS",
        }
        for index, item in enumerate(request["claims"]):
            if not isinstance(item, dict):
                raise ResearchInputError(f"claims[{index}] must be an object")
            key = _clean_text(item.get("key"), f"claims[{index}].key")
            if key in lookup:
                raise ResearchInputError(f"duplicate claim key: {key}")
            status = _clean_text(item.get("status"), f"claims[{index}].status").upper()
            if status not in RESEARCH_STATUSES:
                raise ResearchInputError(f"unsupported research claim status: {status}")
            source_keys = item.get("source_keys", [])
            if not isinstance(source_keys, list):
                raise ResearchInputError(f"claims[{index}].source_keys must be a list")
            source_ids = self._source_ids(source_keys, source_lookup, f"claims[{index}]")
            calculation_id = item.get("calculation_id")
            if status == "OBSERVED" and not source_ids:
                raise ResearchInputError("OBSERVED claim requires at least one source")
            if status == "CALCULATED":
                calculation_id = _clean_text(calculation_id, f"claims[{index}].calculation_id")
                if calculation_id not in calculation_lookup:
                    raise ResearchInputError(f"unknown calculation_id: {calculation_id}")
                calculation = calculation_lookup[calculation_id]
                if calculation["status"] != "CALCULATED":
                    status = "UNKNOWN"
                source_ids = list(dict.fromkeys(source_ids + calculation["source_ids"]))
            confidence = item.get("confidence")
            claim = self.evidence.create_claim(
                project_id,
                _clean_text(item.get("text"), f"claims[{index}].text"),
                type_map[status],
                source_ids=source_ids,
                confidence=confidence,
                metadata={
                    "research_role": "CLAIM",
                    "research_claim_key": key,
                    "research_status": status,
                    "calculation_id": calculation_id,
                },
            )
            row = {
                "key": key,
                "text": claim["content"],
                "status": status,
                "claim_type": claim["metadata"]["claim_type"],
                "claim_id": claim["id"],
                "source_keys": list(source_keys),
                "source_ids": source_ids,
                "calculation_id": calculation_id,
                "confidence": claim.get("confidence"),
                "verified_state": claim["metadata"]["verified_state"],
            }
            results.append(row)
            lookup[key] = row
        return results, lookup

    def _validate_conclusions(
        self,
        request: dict[str, Any],
        claim_lookup: dict[str, dict[str, Any]],
        calculation_lookup: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for index, item in enumerate(request["conclusions"]):
            if not isinstance(item, dict):
                raise ResearchInputError(f"conclusions[{index}] must be an object")
            status = _clean_text(item.get("status"), f"conclusions[{index}].status").upper()
            if status not in RESEARCH_STATUSES:
                raise ResearchInputError(f"unsupported conclusion status: {status}")
            claim_keys = item.get("claim_keys", [])
            calculation_ids = item.get("calculation_ids", [])
            if not isinstance(claim_keys, list) or not isinstance(calculation_ids, list):
                raise ResearchInputError("conclusion references must be lists")
            if not claim_keys and not calculation_ids:
                raise ResearchInputError("every conclusion must trace to claim/source or calculation evidence")
            claims: list[dict[str, Any]] = []
            for key in claim_keys:
                key = _clean_text(key, "conclusion claim key")
                if key not in claim_lookup:
                    raise ResearchInputError(f"unknown conclusion claim key: {key}")
                claims.append(claim_lookup[key])
            calculations: list[dict[str, Any]] = []
            for calc_id in calculation_ids:
                calc_id = _clean_text(calc_id, "conclusion calculation id")
                if calc_id not in calculation_lookup:
                    raise ResearchInputError(f"unknown conclusion calculation id: {calc_id}")
                calculations.append(calculation_lookup[calc_id])
            source_ids = sorted(
                {
                    source_id
                    for claim in claims
                    for source_id in claim.get("source_ids", [])
                }
                | {
                    source_id
                    for calculation in calculations
                    for source_id in calculation.get("source_ids", [])
                }
            )
            if not source_ids and not calculations:
                raise ResearchInputError("conclusion claim references do not trace to any source or calculation")
            results.append(
                {
                    "text": _clean_text(item.get("text"), f"conclusions[{index}].text"),
                    "status": status,
                    "claim_keys": [claim["key"] for claim in claims],
                    "claim_ids": [claim["claim_id"] for claim in claims],
                    "calculation_ids": [calc["id"] for calc in calculations],
                    "source_ids": source_ids,
                }
            )
        return results

    @staticmethod
    def _comparison_rows(request: dict[str, Any]) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for index, row in enumerate(request["comparison"]):
            if not isinstance(row, dict):
                raise ResearchInputError(f"comparison[{index}] must be an object")
            rows.append(dict(row))
        return rows

    @staticmethod
    def _open_questions(request: dict[str, Any]) -> list[str]:
        result: list[str] = []
        for index, item in enumerate(request["open_questions"]):
            if isinstance(item, dict):
                text = item.get("question")
            else:
                text = item
            result.append(_clean_text(text, f"open_questions[{index}]"))
        return result

    @staticmethod
    def _source_ids(
        source_keys: list[Any], source_lookup: dict[str, dict[str, Any]], context: str
    ) -> list[str]:
        result: list[str] = []
        for raw in source_keys:
            key = _clean_text(raw, f"{context}.source_key")
            if key not in source_lookup:
                raise ResearchInputError(f"unknown source key: {key}")
            source_id = source_lookup[key]["source_id"]
            if source_id not in result:
                result.append(source_id)
        return result

    @staticmethod
    def _write_comparison(path: Path, rows: list[dict[str, Any]]) -> None:
        columns: list[str] = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            if not columns:
                handle.write("")
                return
            writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="raise")
            writer.writeheader()
            for row in rows:
                writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in columns})

    @staticmethod
    def _conclusions_markdown(
        request: dict[str, Any], conclusions: list[dict[str, Any]]
    ) -> str:
        lines = [
            "# Business Research Conclusions",
            "",
            f"- Question: {request['question']}",
            f"- Geography: {request['geography']}",
            f"- Industry: {request['industry']}",
            f"- As of: {request['as_of']}",
            "",
        ]
        if not conclusions:
            lines.extend(["No conclusions supplied.", ""])
        for index, item in enumerate(conclusions, start=1):
            lines.extend(
                [
                    f"## {index}. [{item['status']}]",
                    "",
                    item["text"],
                    "",
                    f"- Claim keys: {', '.join(item['claim_keys']) or 'none'}",
                    f"- Claim IDs: {', '.join(item['claim_ids']) or 'none'}",
                    f"- Calculation IDs: {', '.join(item['calculation_ids']) or 'none'}",
                    f"- Source IDs: {', '.join(item['source_ids']) or 'none'}",
                    "",
                ]
            )
        lines.extend(
            [
                "## Evidence boundary",
                "",
                "OBSERVED means supplied source evidence was recorded, not that an independent verifier proved truth. CALCULATED means a bounded arithmetic operation was executed over supplied operands. INFERRED remains inference. UNKNOWN remains unknown; missing evidence is never rewritten as zero or false.",
                "",
            ]
        )
        return "\n".join(lines)

    @staticmethod
    def _open_questions_markdown(open_questions: list[str]) -> str:
        lines = ["# Open Questions", ""]
        if not open_questions:
            return "\n".join(lines + ["None recorded.", ""])
        return "\n".join(lines + [f"- {item}" for item in open_questions] + [""])
