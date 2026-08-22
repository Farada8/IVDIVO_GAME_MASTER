from __future__ import annotations

import json
import math
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DIRECTIONS = {"higher_is_better", "lower_is_better"}
_FLOAT_TOLERANCE = 1e-12


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a finite number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{field} must be a finite number")
    return value


def _strictly_below(value: float, limit: float) -> bool:
    return value < limit and not math.isclose(
        value,
        limit,
        rel_tol=_FLOAT_TOLERANCE,
        abs_tol=_FLOAT_TOLERANCE,
    )


@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    baseline: float
    candidate: float
    direction: str = "higher_is_better"
    weight: float = 1.0
    critical: bool = False
    max_regression: float = 0.0

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "BenchmarkCase":
        if not isinstance(raw, dict):
            raise ValueError("each benchmark case must be a JSON object")
        case_id = str(raw.get("id", "")).strip()
        if not case_id:
            raise ValueError("benchmark case id cannot be empty")
        direction = str(raw.get("direction", "higher_is_better")).strip()
        if direction not in DIRECTIONS:
            raise ValueError(f"invalid benchmark direction for {case_id}: {direction}")
        weight = _number(raw.get("weight", 1.0), f"{case_id}.weight")
        if weight <= 0:
            raise ValueError(f"{case_id}.weight must be > 0")
        max_regression = _number(raw.get("max_regression", 0.0), f"{case_id}.max_regression")
        if max_regression < 0:
            raise ValueError(f"{case_id}.max_regression must be >= 0")
        critical = raw.get("critical", False)
        if not isinstance(critical, bool):
            raise ValueError(f"{case_id}.critical must be boolean")
        return cls(
            case_id=case_id,
            baseline=_number(raw.get("baseline"), f"{case_id}.baseline"),
            candidate=_number(raw.get("candidate"), f"{case_id}.candidate"),
            direction=direction,
            weight=weight,
            critical=critical,
            max_regression=max_regression,
        )


@dataclass(frozen=True)
class BenchmarkCaseResult:
    case_id: str
    baseline: float
    candidate: float
    raw_delta: float
    oriented_delta: float
    direction: str
    weight: float
    critical: bool
    max_regression: float
    regression: bool
    status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BenchmarkResult:
    run_id: str
    suite: str
    status: str
    decision: str
    weighted_delta: float
    min_weighted_delta: float
    critical_regressions: tuple[str, ...]
    noncritical_regressions: tuple[str, ...]
    cases: tuple[BenchmarkCaseResult, ...]
    evaluated_at: str

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["critical_regressions"] = list(self.critical_regressions)
        value["noncritical_regressions"] = list(self.noncritical_regressions)
        value["cases"] = [case.to_dict() for case in self.cases]
        return value


def evaluate_suite(suite: dict[str, Any]) -> BenchmarkResult:
    if not isinstance(suite, dict):
        raise ValueError("benchmark suite must be a JSON object")
    name = str(suite.get("name", "")).strip()
    if not name:
        raise ValueError("benchmark suite name cannot be empty")
    min_weighted_delta = _number(
        suite.get("min_weighted_delta", 0.0), "min_weighted_delta"
    )
    raw_cases = suite.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ValueError("benchmark suite must contain at least one case")

    cases = [BenchmarkCase.from_dict(raw) for raw in raw_cases]
    ids = [case.case_id for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("benchmark case ids must be unique")

    results: list[BenchmarkCaseResult] = []
    weighted_sum = 0.0
    total_weight = 0.0
    critical_regressions: list[str] = []
    noncritical_regressions: list[str] = []

    for case in cases:
        raw_delta = case.candidate - case.baseline
        oriented_delta = raw_delta if case.direction == "higher_is_better" else -raw_delta
        regression = _strictly_below(oriented_delta, -case.max_regression)
        if regression:
            if case.critical:
                critical_regressions.append(case.case_id)
            else:
                noncritical_regressions.append(case.case_id)
        results.append(
            BenchmarkCaseResult(
                case_id=case.case_id,
                baseline=case.baseline,
                candidate=case.candidate,
                raw_delta=raw_delta,
                oriented_delta=oriented_delta,
                direction=case.direction,
                weight=case.weight,
                critical=case.critical,
                max_regression=case.max_regression,
                regression=regression,
                status="FAIL" if regression else "PASS",
            )
        )
        weighted_sum += oriented_delta * case.weight
        total_weight += case.weight

    weighted_delta = weighted_sum / total_weight
    if critical_regressions:
        status = "FAIL"
        decision = "REJECT_CRITICAL_REGRESSION"
    elif _strictly_below(weighted_delta, min_weighted_delta):
        status = "FAIL"
        decision = "REJECT_AGGREGATE_DELTA"
    else:
        status = "PASS"
        decision = "ACCEPT"

    return BenchmarkResult(
        run_id=f"bench-{uuid.uuid4().hex}",
        suite=name,
        status=status,
        decision=decision,
        weighted_delta=weighted_delta,
        min_weighted_delta=min_weighted_delta,
        critical_regressions=tuple(critical_regressions),
        noncritical_regressions=tuple(noncritical_regressions),
        cases=tuple(results),
        evaluated_at=_utc_now(),
    )


def load_suite(path: Path) -> dict[str, Any]:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"benchmark suite not found: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("benchmark suite must decode to a JSON object")
    return value


def run_suite(path: Path, home: Path) -> dict[str, Any]:
    result = evaluate_suite(load_suite(path))
    report_dir = Path(home) / "runtime" / "benchmarks"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{result.run_id}.json"
    payload = result.to_dict()
    payload["suite_path"] = str(Path(path).resolve())
    payload["report_path"] = str(report_path)
    tmp = report_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(report_path)
    return payload
