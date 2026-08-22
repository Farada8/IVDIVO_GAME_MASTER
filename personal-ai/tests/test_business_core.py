from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from business import BusinessCore
from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class BusinessCoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.projects = ProjectStateManager(self.home)
        self.projects.create_project("biz", "Business")
        self.core = BusinessCore(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_sourced_quote_is_ready_and_persisted_without_assumed_tax(self) -> None:
        result = self.core.create_document(
            "biz",
            {
                "client": "Client A",
                "currency": "EUR",
                "items": [
                    {
                        "description": "Painting",
                        "quantity": "10",
                        "unit": "m2",
                        "unit_price": "25.50",
                        "price_source": "customer-approved rate card 2026-08-22",
                    }
                ],
            },
            document_type="quote",
        )
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["subtotal_ex_tax"], "255.00")
        self.assertEqual(result["tax"]["status"], "NOT_SPECIFIED")
        self.assertIsNone(result["tax"]["amount"])
        self.assertIsNone(result["total_inc_tax"])
        self.assertEqual(result["assumptions"], [])
        artifact = Path(result["artifact_path"])
        self.assertTrue(artifact.is_file())
        stored_artifact = json.loads(artifact.read_text(encoding="utf-8"))
        self.assertEqual(stored_artifact["output_memory_id"], result["output_memory_id"])
        output = MemoryStore(self.home / "runtime" / "state.db").get(result["output_memory_id"])
        self.assertEqual(output["kind"], "OUTPUT")
        self.assertEqual(output["metadata"]["status"], "READY")
        self.assertEqual(output["project_id"], "biz")

    def test_missing_price_blocks_final_total_but_persists_audit_result(self) -> None:
        result = self.core.create_document(
            "biz",
            {
                "client": "Client B",
                "currency": "EUR",
                "items": [
                    {
                        "id": "known",
                        "description": "Known rate",
                        "quantity": "2",
                        "unit": "hour",
                        "unit_price": "40",
                        "price_source": "written client rate",
                    },
                    {
                        "id": "unknown",
                        "description": "Unknown material",
                        "quantity": "3",
                        "unit": "unit",
                    },
                ],
            },
            document_type="estimate",
        )
        self.assertEqual(result["status"], "NEEDS_PRICE_EVIDENCE")
        self.assertEqual(result["priced_subtotal"], "80.00")
        self.assertIsNone(result["subtotal_ex_tax"])
        self.assertIsNone(result["total_inc_tax"])
        self.assertEqual(
            result["missing_price_evidence"],
            [{"item_id": "unknown", "reasons": ["MISSING_UNIT_PRICE", "MISSING_PRICE_SOURCE"]}],
        )
        self.assertTrue(Path(result["artifact_path"]).is_file())
        memory = MemoryStore(self.home / "runtime" / "state.db").get(result["output_memory_id"])
        self.assertEqual(memory["metadata"]["status"], "NEEDS_PRICE_EVIDENCE")

    def test_unit_price_without_source_is_not_ready(self) -> None:
        result = self.core.create_document(
            "biz",
            {
                "client": "Client C",
                "currency": "EUR",
                "items": [
                    {
                        "description": "Labour",
                        "quantity": "1",
                        "unit": "day",
                        "unit_price": "130",
                    }
                ],
            },
            document_type="quote",
        )
        self.assertEqual(result["status"], "NEEDS_PRICE_EVIDENCE")
        self.assertEqual(result["items"][0]["line_total"], None)
        self.assertEqual(result["missing_price_evidence"][0]["reasons"], ["MISSING_PRICE_SOURCE"])

    def test_persisted_price_source_id_is_resolved_and_hashed(self) -> None:
        memory = MemoryStore(self.home / "runtime" / "state.db")
        source = memory.store(
            "Rate confirmed: 18.75 EUR per unit",
            kind="SOURCE",
            source="signed schedule",
            project_id="biz",
        )
        result = self.core.create_document(
            "biz",
            {
                "client": "Client D",
                "currency": "EUR",
                "items": [
                    {
                        "description": "Material",
                        "quantity": "4",
                        "unit": "unit",
                        "unit_price": "18.75",
                        "price_source_id": source["id"],
                    }
                ],
            },
            document_type="estimate",
        )
        evidence = result["items"][0]["price_evidence"]
        self.assertEqual(result["status"], "READY")
        self.assertEqual(evidence["memory_id"], source["id"])
        self.assertEqual(evidence["memory_kind"], "SOURCE")
        self.assertEqual(evidence["memory_hash"], source["content_hash"])
        self.assertEqual(result["subtotal_ex_tax"], "75.00")

    def test_missing_or_invalid_source_id_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not resolve"):
            self.core.create_document(
                "biz",
                {
                    "client": "Client E",
                    "currency": "EUR",
                    "items": [
                        {
                            "description": "Line",
                            "quantity": 1,
                            "unit": "unit",
                            "unit_price": 10,
                            "price_source_id": "does-not-exist",
                        }
                    ],
                },
                document_type="quote",
            )

        memory = MemoryStore(self.home / "runtime" / "state.db")
        source = memory.store("old rate", kind="SOURCE", source="old", project_id="biz")
        memory.invalidate(source["id"], "superseded")
        with self.assertRaisesRegex(ValueError, "not ACTIVE"):
            self.core.create_document(
                "biz",
                {
                    "client": "Client E",
                    "currency": "EUR",
                    "items": [
                        {
                            "description": "Line",
                            "quantity": 1,
                            "unit": "unit",
                            "unit_price": 10,
                            "price_source_id": source["id"],
                        }
                    ],
                },
                document_type="quote",
            )

    def test_decimal_math_is_exact_and_tax_requires_source(self) -> None:
        ready = self.core.create_document(
            "biz",
            {
                "client": "Client F",
                "currency": "EUR",
                "items": [
                    {
                        "description": "Tiny unit",
                        "quantity": "3",
                        "unit": "unit",
                        "unit_price": "0.10",
                        "price_source": "explicit test rate",
                    }
                ],
                "tax_rate": "0.23",
                "tax_source": "explicit tax instruction",
            },
            document_type="quote",
        )
        self.assertEqual(ready["status"], "READY")
        self.assertEqual(ready["subtotal_ex_tax"], "0.30")
        self.assertEqual(ready["tax"]["amount"], "0.07")
        self.assertEqual(ready["total_inc_tax"], "0.37")

        blocked = self.core.create_document(
            "biz",
            {
                "client": "Client F",
                "currency": "EUR",
                "items": [
                    {
                        "description": "Line",
                        "quantity": "1",
                        "unit": "unit",
                        "unit_price": "100",
                        "price_source": "explicit rate",
                    }
                ],
                "tax_rate": "0.23",
            },
            document_type="quote",
        )
        self.assertEqual(blocked["status"], "NEEDS_TAX_EVIDENCE")
        self.assertEqual(blocked["subtotal_ex_tax"], "100.00")
        self.assertIsNone(blocked["tax"]["amount"])
        self.assertIsNone(blocked["total_inc_tax"])

    def test_invalid_business_inputs_fail_closed(self) -> None:
        base_item = {
            "description": "Line",
            "quantity": "1",
            "unit": "unit",
            "unit_price": "10",
            "price_source": "rate",
        }
        for request in (
            {"client": "", "currency": "EUR", "items": [base_item]},
            {"client": "X", "currency": "EURO", "items": [base_item]},
            {"client": "X", "currency": "EUR", "items": []},
            {"client": "X", "currency": "EUR", "items": [{**base_item, "quantity": "0"}]},
            {"client": "X", "currency": "EUR", "items": [{**base_item, "unit_price": "-1"}]},
            {"client": "X", "currency": "EUR", "items": [base_item], "tax_rate": "1.1", "tax_source": "x"},
        ):
            with self.subTest(request=request):
                with self.assertRaises(ValueError):
                    self.core.create_document("biz", request, document_type="quote")

    def test_cli_ready_and_blocked_enforcement(self) -> None:
        run_py = ROOT / "run.py"
        cli_home = self.home / "cli"
        subprocess.run(
            [sys.executable, str(run_py), "--home", str(cli_home), "project", "create", "cli-biz"],
            check=True,
            capture_output=True,
            text=True,
        )
        ready_path = self.home / "ready.json"
        ready_path.write_text(
            json.dumps(
                {
                    "client": "CLI",
                    "currency": "EUR",
                    "items": [
                        {
                            "description": "Service",
                            "quantity": "2",
                            "unit": "hour",
                            "unit_price": "50",
                            "price_source": "CLI supplied rate",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        passed = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(cli_home),
                "business",
                "quote",
                "cli-biz",
                str(ready_path),
                "--enforce-ready",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(passed.returncode, 0, passed.stderr)
        self.assertEqual(json.loads(passed.stdout)["subtotal_ex_tax"], "100.00")

        blocked_path = self.home / "blocked.json"
        blocked_path.write_text(
            json.dumps(
                {
                    "client": "CLI",
                    "currency": "EUR",
                    "items": [{"description": "Unknown", "quantity": 1, "unit": "unit"}],
                }
            ),
            encoding="utf-8",
        )
        failed = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(cli_home),
                "business",
                "estimate",
                "cli-biz",
                str(blocked_path),
                "--enforce-ready",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(failed.returncode, 2)
        self.assertEqual(json.loads(failed.stdout)["status"], "NEEDS_PRICE_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
