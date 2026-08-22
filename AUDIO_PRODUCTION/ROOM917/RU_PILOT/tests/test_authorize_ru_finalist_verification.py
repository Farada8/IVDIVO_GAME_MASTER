#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve()
TOOL = HERE.parents[1] / "tools" / "authorize_ru_finalist_verification.py"
SCOPE = "ROOM917_RU_FINALIST_VERIFICATION_ONLY"


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class FinalistAuthorizationTests(unittest.TestCase):
    def fixture(self, root: Path, required: int = 6) -> tuple[Path, Path]:
        plan = root / "plan.json"
        out = root / "authorized.json"
        ids = [f"BLOCK_{i}" for i in range(required)]
        write(plan, {
            "status": "READY_FOR_FINALIST_SPEND_AUTHORIZATION",
            "project_id": "ROOM917",
            "locale": "ru-RU",
            "required_block_count": required,
            "selected_block_ids": ids,
            "blocks": [{"block_id": x} for x in ids],
            "provider_call_made": False,
            "provider_spend_made": False,
            "cast_lock": False,
            "full_e01_render_allowed": False,
        })
        return plan, out

    def call(self, plan: Path, out: Path, confirm: str = "NO", scope: str = SCOPE, blocks: int = 6):
        return subprocess.run([
            "python", str(TOOL),
            "--plan", str(plan),
            "--out", str(out),
            "--confirm-spend", confirm,
            "--scope", scope,
            "--max-blocks", str(blocks),
            "--authorization-note", "unit-test finalist authorization",
        ], text=True, capture_output=True, check=False)

    def test_no_confirmation_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            plan, out = self.fixture(Path(td), 6)
            proc = self.call(plan, out, confirm="NO", blocks=6)
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(out.exists())

    def test_wrong_scope_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            plan, out = self.fixture(Path(td), 6)
            proc = self.call(plan, out, confirm="YES", scope="FULL_EPISODE", blocks=6)
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(out.exists())

    def test_exact_six_authorized_without_provider_call(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            plan, out = self.fixture(Path(td), 6)
            proc = self.call(plan, out, confirm="YES", blocks=6)
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            row = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(row["status"], "PAID_FINALIST_VERIFICATION_AUTHORIZED")
            self.assertEqual(row["authorized_block_count"], 6)
            self.assertFalse(row["provider_call_made"])
            self.assertFalse(row["provider_spend_made"])
            self.assertFalse(row["cast_lock"])
            self.assertFalse(row["full_e01_render_allowed"])

    def test_over_authorization_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            plan, out = self.fixture(Path(td), 6)
            proc = self.call(plan, out, confirm="YES", blocks=7)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("exactly equal plan requirement 6", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())

    def test_under_authorization_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            plan, out = self.fixture(Path(td), 8)
            proc = self.call(plan, out, confirm="YES", blocks=7)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("exactly equal plan requirement 8", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
