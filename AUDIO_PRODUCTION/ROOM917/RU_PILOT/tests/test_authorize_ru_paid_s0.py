#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve()
TOOL = HERE.parents[1] / "tools" / "authorize_ru_paid_s0.py"
ROLES = ("ELENA", "JULIAN", "MINA", "CATE")


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class PaidAuthorizationTests(unittest.TestCase):
    def fixture(self, root: Path) -> tuple[Path, Path]:
        source = root / "candidate.json"
        out = root / "authorized.json"
        roles = {}
        for i, role in enumerate(ROLES, 1):
            roles[role] = {
                "voice_id": f"voice-{role.lower()}-{i}",
                "provider_name": f"Voice {role}",
                "preview_listen": "PASS",
                "provider_identity_check": "PASS",
                "provider_durability_check": "PASS",
                "plausible_for_canary": "PASS",
                "canary_binding_only": True,
            }
        write(source, {
            "schema_version": "ivdivo.room917_ru_s0_native_bindings_candidate/2.0",
            "status": "READY_FOR_PAID_CANARY_AUTHORIZATION",
            "project_id": "ROOM917",
            "locale": "ru-RU",
            "provider": "ElevenLabs",
            "model_id": "eleven_v3",
            "roles": roles,
            "pre_canary_binding_gate": "PASS",
            "canary_binding_only": True,
            "acting_evidence_complete": False,
            "pair_tests": "NOT_RUN_YET",
            "pronunciation_gate": "NOT_RUN_YET",
            "founder_credibility_gate": "NOT_RUN_YET",
            "founder_paid_canary_authorized": False,
            "paid_s0_authorized": False,
            "cast_lock": False,
            "full_episode_render_allowed": False,
        })
        return source, out

    def call(self, source: Path, out: Path, confirm: str = "NO", scope: str = "ROOM917_RU_S0_CANARY_ONLY", blocks: int = 4) -> subprocess.CompletedProcess[str]:
        return subprocess.run([
            "python", str(TOOL),
            "--bindings-candidate", str(source),
            "--out", str(out),
            "--confirm-spend", confirm,
            "--scope", scope,
            "--max-blocks", str(blocks),
            "--authorization-note", "unit-test explicit authorization",
        ], text=True, capture_output=True, check=False)

    def test_default_no_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            source, out = self.fixture(Path(td))
            proc = self.call(source, out, confirm="NO")
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(out.exists())

    def test_wrong_scope_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            source, out = self.fixture(Path(td))
            proc = self.call(source, out, confirm="YES", scope="FULL_EPISODE")
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(out.exists())

    def test_explicit_authorization_only_writes_canary_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            source, out = self.fixture(Path(td))
            proc = self.call(source, out, confirm="YES", blocks=4)
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            row = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(row["status"], "PAID_S0_AUTHORIZED")
            self.assertTrue(row["founder_paid_canary_authorized"])
            self.assertTrue(row["paid_s0_authorized"])
            self.assertEqual(row["authorized_max_blocks"], 4)
            self.assertTrue(row["canary_binding_only"])
            self.assertFalse(row["acting_evidence_complete"])
            self.assertEqual(row["pair_tests"], "NOT_RUN_YET")
            self.assertFalse(row["authorization"]["provider_call_made"])
            self.assertFalse(row["authorization"]["provider_spend_made"])
            self.assertFalse(row["authorization"]["workflow_auto_dispatched"])
            self.assertFalse(row["cast_lock"])
            self.assertFalse(row["full_episode_render_allowed"])

    def test_fake_prepassed_cast_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            source, out = self.fixture(Path(td))
            row = json.loads(source.read_text(encoding="utf-8"))
            row["pair_tests"] = "PASS"
            write(source, row)
            proc = self.call(source, out, confirm="YES")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("must not pre-pass pair tests", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
