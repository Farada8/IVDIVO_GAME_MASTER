from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from business import (
    BusinessQuoteService,
    Customer,
    Expense,
    FollowUp,
    Invoice,
    Job,
    Lead,
    Payment,
    Quote,
    Supplier,
)
from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class BusinessCoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        ProjectStateManager(self.home).create_project("demo", "Demo")
        self.service = BusinessQuoteService(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @staticmethod
    def complete_payload() -> dict:
        return {
            "quote_id": "q-known",
            "job_id": "j-known",
            "client_request": "Paint two rooms",
            "job_type": "painting",
            "description": "Prepare and paint walls",
            "area_quantity": {"value": "40", "unit": "m2"},
            "hours": "8",
            "labour_rate": "45.00",
            "materials": [
                {
                    "description": "paint",
                    "quantity": "2",
                    "unit": "tin",
                    "unit_price": "80.00",
                    "price_source": "explicit fixture input",
                },
                {
                    "description": "tape",
                    "quantity": "1",
                    "unit": "roll",
                    "unit_price": "10.00",
                },
            ],
            "margin_percent": "20",
            "currency": "EUR",
        }

    def test_complete_quote_uses_exact_decimal_math_and_persists_json_markdown(self) -> None:
        result = self.service.create_quote("demo", self.complete_payload())
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["estimate"]["labour"]["amount"], "360.00")
        self.assertEqual(result["estimate"]["materials"]["total"]["amount"], "170.00")
        self.assertEqual(result["estimate"]["subtotal"]["amount"], "530.00")
        self.assertEqual(result["estimate"]["margin"]["amount"], "106.00")
        self.assertEqual(result["estimate"]["total"]["amount"], "636.00")
        self.assertEqual(result["unknowns"], [])

        json_path = Path(result["artifacts"]["json"])
        md_path = Path(result["artifacts"]["markdown"])
        self.assertTrue(json_path.is_file())
        self.assertTrue(md_path.is_file())
        persisted = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(persisted["estimate"]["total"]["amount"], "636.00")
        text = md_path.read_text(encoding="utf-8")
        self.assertIn("Quote total | EUR 636.00", text)
        self.assertIn("No missing price, rate, quantity or margin is converted to zero.", text)

        output = MemoryStore(self.home / "runtime" / "state.db").get(
            result["artifacts"]["output_memory_id"]
        )
        self.assertEqual(output["kind"], "OUTPUT")
        self.assertEqual(output["project_id"], "demo")

    def test_missing_material_price_propagates_tbd_not_zero(self) -> None:
        payload = self.complete_payload()
        payload["quote_id"] = "q-missing-material"
        payload["job_id"] = "j-missing-material"
        payload["materials"][1]["unit_price"] = None
        result = self.service.create_quote("demo", payload)
        self.assertEqual(result["status"], "TBD")
        self.assertEqual(result["estimate"]["materials"]["total"]["status"], "TBD")
        self.assertIsNone(result["estimate"]["materials"]["total"]["amount"])
        self.assertEqual(result["estimate"]["subtotal"]["status"], "TBD")
        self.assertEqual(result["estimate"]["total"]["status"], "TBD")
        self.assertIn("MATERIAL_2_UNIT_PRICE_TBD", result["unknowns"])
        self.assertNotEqual(result["estimate"]["materials"]["total"]["amount"], "0.00")
        self.assertIn("TBD", Path(result["artifacts"]["markdown"]).read_text(encoding="utf-8"))

    def test_materials_not_required_is_explicit_known_zero(self) -> None:
        payload = self.complete_payload()
        payload["quote_id"] = "q-no-material"
        payload["job_id"] = "j-no-material"
        payload["materials"] = []
        payload["materials_not_required"] = True
        result = self.service.create_quote("demo", payload)
        self.assertEqual(result["estimate"]["materials"]["total"]["status"], "KNOWN")
        self.assertEqual(result["estimate"]["materials"]["total"]["amount"], "0.00")
        self.assertEqual(result["estimate"]["total"]["amount"], "432.00")

    def test_missing_labour_rate_propagates_tbd(self) -> None:
        payload = self.complete_payload()
        payload["quote_id"] = "q-no-rate"
        payload["job_id"] = "j-no-rate"
        payload["labour_rate"] = None
        result = self.service.create_quote("demo", payload)
        self.assertEqual(result["estimate"]["labour"]["status"], "TBD")
        self.assertIsNone(result["estimate"]["total"]["amount"])
        self.assertIn("LABOUR_RATE_TBD", result["unknowns"])

    def test_missing_margin_blocks_final_total(self) -> None:
        payload = self.complete_payload()
        payload["quote_id"] = "q-no-margin"
        payload["job_id"] = "j-no-margin"
        payload["margin_percent"] = None
        result = self.service.create_quote("demo", payload)
        self.assertEqual(result["estimate"]["subtotal"]["status"], "KNOWN")
        self.assertEqual(result["estimate"]["total"]["status"], "TBD")
        self.assertIn("MARGIN_PERCENT_TBD", result["unknowns"])

    def test_negative_values_fail_closed(self) -> None:
        for field in ("hours", "labour_rate", "margin_percent"):
            payload = self.complete_payload()
            payload["quote_id"] = f"q-neg-{field}"
            payload["job_id"] = f"j-neg-{field}"
            payload[field] = "-1"
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.service.create_quote("demo", payload)

    def test_minimum_entities_exist_and_serialize(self) -> None:
        entities = [
            Lead("l1", "Lead"),
            Customer("c1", "Customer"),
            Job("j1", "c1", "painting", "job"),
            Quote("q1", "demo", "j1", "TBD", "EUR", {"status": "TBD"}),
            Invoice("i1", "q1"),
            Supplier("s1", "Supplier"),
            Expense("e1", "j1", "fuel"),
            Payment("p1", "i1"),
            FollowUp("f1", "j1", "call"),
        ]
        self.assertEqual(
            [type(item).__name__ for item in entities],
            [
                "Lead",
                "Customer",
                "Job",
                "Quote",
                "Invoice",
                "Supplier",
                "Expense",
                "Payment",
                "FollowUp",
            ],
        )
        for item in entities:
            self.assertIsInstance(item.to_dict(), dict)
            self.assertTrue(item.to_dict()["id"])

    def test_entity_persistence_readback(self) -> None:
        result = self.service.create_quote("demo", self.complete_payload())
        reopened = BusinessQuoteService(self.home)
        job = reopened.store.load_entity("job", result["job"]["id"])
        quote = reopened.store.load_entity("quote", result["quote_id"])
        self.assertEqual(job["job_type"], "painting")
        self.assertEqual(quote["total"]["amount"], "636.00")

    def test_unknown_project_fails_before_artifact_write(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.service.create_quote("missing", self.complete_payload())
        self.assertFalse((self.home / "projects" / "missing").exists())

    def test_cli_roundtrip_persists_readable_and_structured_quote(self) -> None:
        cli_home = self.home / "cli-home"
        run_py = ROOT / "run.py"
        env = os.environ.copy()
        subprocess.run(
            [sys.executable, str(run_py), "--home", str(cli_home), "project", "create", "cli"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        request_path = self.home / "request.json"
        payload = self.complete_payload()
        payload["quote_id"] = "q-cli"
        payload["job_id"] = "j-cli"
        request_path.write_text(json.dumps(payload), encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(cli_home),
                "business",
                "quote",
                "cli",
                str(request_path),
            ],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["estimate"]["total"]["amount"], "636.00")
        self.assertTrue(Path(result["artifacts"]["json"]).is_file())
        self.assertTrue(Path(result["artifacts"]["markdown"]).is_file())

    def test_decimal_precision_is_not_binary_float_math(self) -> None:
        payload = {
            "quote_id": "q-precision",
            "job_id": "j-precision",
            "client_request": "precision fixture",
            "job_type": "test",
            "hours": "0.1",
            "labour_rate": "0.2",
            "materials": [],
            "materials_not_required": True,
            "margin_percent": "0",
            "currency": "EUR",
        }
        result = self.service.create_quote("demo", payload)
        self.assertEqual(result["estimate"]["labour"]["amount"], "0.02")
        self.assertEqual(result["estimate"]["total"]["amount"], "0.02")


if __name__ == "__main__":
    unittest.main()
