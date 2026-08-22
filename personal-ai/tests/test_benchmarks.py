from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from benchmarks import evaluate_suite, run_suite


class BenchmarkRunnerTest(unittest.TestCase):
    def test_improving_candidate_passes(self) -> None:
        result = evaluate_suite(
            {
                "name": "improves",
                "cases": [
                    {"id": "quality", "baseline": 0.7, "candidate": 0.8, "critical": True},
                    {
                        "id": "latency",
                        "baseline": 3.0,
                        "candidate": 2.5,
                        "direction": "lower_is_better",
                    },
                ],
            }
        )
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.decision, "ACCEPT")
        self.assertGreater(result.weighted_delta, 0)
        self.assertEqual(result.critical_regressions, ())

    def test_critical_regression_rejects_even_when_aggregate_improves(self) -> None:
        result = evaluate_suite(
            {
                "name": "critical-overrides-average",
                "cases": [
                    {
                        "id": "critical-safety",
                        "baseline": 1.0,
                        "candidate": 0.9,
                        "critical": True,
                        "weight": 1.0,
                    },
                    {
                        "id": "large-noncritical-gain",
                        "baseline": 0.0,
                        "candidate": 10.0,
                        "critical": False,
                        "weight": 100.0,
                    },
                ],
            }
        )
        self.assertGreater(result.weighted_delta, 0)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.decision, "REJECT_CRITICAL_REGRESSION")
        self.assertEqual(result.critical_regressions, ("critical-safety",))

    def test_noncritical_regression_can_be_visible_while_suite_passes(self) -> None:
        result = evaluate_suite(
            {
                "name": "visible-noncritical-regression",
                "cases": [
                    {"id": "quality", "baseline": 1.0, "candidate": 1.5, "weight": 3},
                    {"id": "minor", "baseline": 1.0, "candidate": 0.9, "weight": 1},
                ],
            }
        )
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.noncritical_regressions, ("minor",))
        minor = next(case for case in result.cases if case.case_id == "minor")
        self.assertTrue(minor.regression)
        self.assertEqual(minor.status, "FAIL")

    def test_aggregate_threshold_rejects_without_critical_regression(self) -> None:
        result = evaluate_suite(
            {
                "name": "aggregate-gate",
                "min_weighted_delta": 0.05,
                "cases": [
                    {
                        "id": "small-gain",
                        "baseline": 1.0,
                        "candidate": 1.01,
                        "max_regression": 0.1,
                    }
                ],
            }
        )
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.decision, "REJECT_AGGREGATE_DELTA")
        self.assertEqual(result.critical_regressions, ())

    def test_lower_is_better_orientation_and_regression_tolerance(self) -> None:
        better = evaluate_suite(
            {
                "name": "lower-better",
                "cases": [
                    {
                        "id": "latency",
                        "baseline": 2.0,
                        "candidate": 1.5,
                        "direction": "lower_is_better",
                        "critical": True,
                    }
                ],
            }
        )
        self.assertAlmostEqual(better.cases[0].oriented_delta, 0.5)
        self.assertEqual(better.status, "PASS")

        tolerated = evaluate_suite(
            {
                "name": "tolerated-lower-regression",
                "min_weighted_delta": -0.2,
                "cases": [
                    {
                        "id": "latency",
                        "baseline": 2.0,
                        "candidate": 2.1,
                        "direction": "lower_is_better",
                        "critical": True,
                        "max_regression": 0.1,
                    }
                ],
            }
        )
        self.assertFalse(tolerated.cases[0].regression)
        self.assertEqual(tolerated.status, "PASS")

    def test_invalid_suite_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_suite({"name": "empty", "cases": []})
        with self.assertRaises(ValueError):
            evaluate_suite(
                {
                    "name": "duplicates",
                    "cases": [
                        {"id": "same", "baseline": 1, "candidate": 1},
                        {"id": "same", "baseline": 1, "candidate": 1},
                    ],
                }
            )
        with self.assertRaises(ValueError):
            evaluate_suite(
                {
                    "name": "bad-weight",
                    "cases": [{"id": "x", "baseline": 1, "candidate": 1, "weight": 0}],
                }
            )
        with self.assertRaises(ValueError):
            evaluate_suite(
                {
                    "name": "nan",
                    "cases": [{"id": "x", "baseline": math.nan, "candidate": 1}],
                }
            )

    def test_run_suite_persists_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            suite_path = root / "suite.json"
            suite_path.write_text(
                json.dumps(
                    {
                        "name": "persisted",
                        "cases": [{"id": "q", "baseline": 1, "candidate": 2}],
                    }
                ),
                encoding="utf-8",
            )
            result = run_suite(suite_path, root / "home")
            report = Path(result["report_path"])
            self.assertTrue(report.is_file())
            stored = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(stored["run_id"], result["run_id"])
            self.assertEqual(stored["status"], "PASS")
            self.assertEqual(stored["suite"], "persisted")

    def test_cli_demo_and_enforced_failure(self) -> None:
        run_py = ROOT / "run.py"
        demo = ROOT / "benchmarks" / "fixtures" / "demo_suite.json"
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            passed = subprocess.run(
                [sys.executable, str(run_py), "--home", str(home), "benchmark", "run", str(demo), "--enforce"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(passed.returncode, 0, passed.stderr)
            pass_result = json.loads(passed.stdout)
            self.assertEqual(pass_result["status"], "PASS")
            self.assertTrue(Path(pass_result["report_path"]).is_file())

            failing_suite = Path(tmp) / "failing.json"
            failing_suite.write_text(
                json.dumps(
                    {
                        "name": "critical-failure",
                        "cases": [
                            {
                                "id": "critical",
                                "baseline": 1.0,
                                "candidate": 0.0,
                                "critical": True,
                            },
                            {"id": "gain", "baseline": 0.0, "candidate": 100.0, "weight": 100},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            failed = subprocess.run(
                [
                    sys.executable,
                    str(run_py),
                    "--home",
                    str(home),
                    "benchmark",
                    "run",
                    str(failing_suite),
                    "--enforce",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(failed.returncode, 2)
            fail_result = json.loads(failed.stdout)
            self.assertEqual(fail_result["decision"], "REJECT_CRITICAL_REGRESSION")
            self.assertIn("critical", fail_result["critical_regressions"])


if __name__ == "__main__":
    unittest.main()
