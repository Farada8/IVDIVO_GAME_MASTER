#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve()
TOOL = HERE.parents[1] / "tools" / "prepare_ru_finalist_verification_plan.py"
TEMPLATE = HERE.parents[1] / "ROOM917_RU_FINALIST_VERIFICATION_BUNDLE_v1.0.json"
ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
S0_ROLE_BLOCKS = {
    "ELENA": "RU_S0_ELENA_BOUNDARY",
    "JULIAN": "RU_S0_JULIAN_72",
    "MINA": "RU_S0_MINA_INTRO",
    "CATE": "RU_S0_CATE_LENI_BIRD",
}


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def h(ch: str) -> str:
    return ch * 64


class FinalistPlanTests(unittest.TestCase):
    def fixture(self, root: Path, s0_blocks: int = 6) -> tuple[Path, Path, Path, Path]:
        bindings = root / "bindings.json"
        s0 = root / "s0_receipt.json"
        screening = root / "screening.json"
        out = root / "finalist_plan.json"

        role_bindings = {}
        for i, role in enumerate(ROLES, 1):
            role_bindings[role] = {
                "voice_id": f"voice-{role.lower()}-{i}",
                "preview_listen": "PASS",
                "provider_identity_check": "PASS",
                "provider_durability_check": "PASS",
                "plausible_for_canary": "PASS",
                "canary_binding_only": True,
            }
        write(bindings, {
            "status": "PAID_S0_AUTHORIZED",
            "canary_binding_only": True,
            "cast_lock": False,
            "roles": role_bindings,
        })

        selected = list(S0_ROLE_BLOCKS.values())
        if s0_blocks >= 5:
            selected.append("RU_S0_ELENA_MINA_RELATION")
        if s0_blocks >= 6:
            selected.append("RU_S0_ELENA_JULIAN_FRICTION")
        write(s0, {
            "stage_semantics": "S0_SCREENING_ONLY_NOT_CAST_LOCK",
            "cast_locked": False,
            "full_episode_rendered": False,
            "selected_block_ids": selected,
        })

        roles = {}
        for i, role in enumerate(ROLES, 1):
            roles[role] = {
                "voice_id": role_bindings[role]["voice_id"],
                "screening": "PASS",
                "founder_screening": "YES",
                "believability_0_5": 4.5,
                "russian_naturalness_0_5": 4.5,
                "character_fit_0_5": 4.5,
                "hard_reject_flags": [],
                "audio_sha256": h(str(i)),
            }
        write(screening, {
            "status": "S0_SCREENING_PASS_TO_FINALIST_VERIFICATION",
            "s0_canary_receipt_sha256": digest(s0),
            "pre_canary_bindings_sha256": digest(bindings),
            "cast_lock": False,
            "full_e01_render_allowed": False,
            "roles": roles,
            "pair_evidence": {
                "ELENA_MINA": {
                    "s0_block_id": "RU_S0_ELENA_MINA_RELATION",
                    "rendered": s0_blocks >= 5,
                    "audio_sha256": h("a") if s0_blocks >= 5 else "",
                    "screening": "PASS" if s0_blocks >= 5 else "NOT_RENDERED",
                },
                "ELENA_JULIAN_1": {
                    "s0_block_id": "RU_S0_ELENA_JULIAN_FRICTION",
                    "rendered": s0_blocks >= 6,
                    "audio_sha256": h("b") if s0_blocks >= 6 else "",
                    "screening": "PASS" if s0_blocks >= 6 else "NOT_RENDERED",
                },
            },
        })
        return s0, screening, bindings, out

    def run_tool(self, s0: Path, screening: Path, bindings: Path, out: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([
            "python", str(TOOL),
            "--s0-receipt", str(s0),
            "--screening", str(screening),
            "--bindings", str(bindings),
            "--template", str(TEMPLATE),
            "--out", str(out),
        ], text=True, capture_output=True, check=False)

    def test_s0_six_reuses_two_pair_blocks_and_requires_six_finalist_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            s0, screening, bindings, out = self.fixture(Path(td), s0_blocks=6)
            proc = self.run_tool(s0, screening, bindings, out)
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            row = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(row["required_block_count"], 6)
            ids = set(row["selected_block_ids"])
            self.assertNotIn("RU_FV_ELENA_MINA_RELATION", ids)
            self.assertNotIn("RU_FV_ELENA_JULIAN_FRICTION", ids)
            self.assertIn("RU_FV_ELENA_JULIAN_STATUS", ids)
            self.assertIn("RU_FV_CATE_DOMESTIC", ids)

    def test_s0_four_requires_both_missing_pairs_for_total_eight(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            s0, screening, bindings, out = self.fixture(Path(td), s0_blocks=4)
            proc = self.run_tool(s0, screening, bindings, out)
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            row = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(row["required_block_count"], 8)
            ids = set(row["selected_block_ids"])
            self.assertIn("RU_FV_ELENA_MINA_RELATION", ids)
            self.assertIn("RU_FV_ELENA_JULIAN_FRICTION", ids)

    def test_rendered_pair_failure_blocks_progression(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            s0, screening, bindings, out = self.fixture(Path(td), s0_blocks=6)
            row = json.loads(screening.read_text(encoding="utf-8"))
            row["pair_evidence"]["ELENA_JULIAN_1"]["screening"] = "FAIL"
            write(screening, row)
            proc = self.run_tool(s0, screening, bindings, out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("must PASS or recast/repair", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())

    def test_screening_voice_must_match_bound_voice(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            s0, screening, bindings, out = self.fixture(Path(td), s0_blocks=6)
            row = json.loads(screening.read_text(encoding="utf-8"))
            row["roles"]["ELENA"]["voice_id"] = "different-voice"
            write(screening, row)
            proc = self.run_tool(s0, screening, bindings, out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("screening voice differs from bindings", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())

    def test_missing_real_audio_hash_blocks_progression(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            s0, screening, bindings, out = self.fixture(Path(td), s0_blocks=6)
            row = json.loads(screening.read_text(encoding="utf-8"))
            row["roles"]["CATE"]["audio_sha256"] = "not-a-hash"
            write(screening, row)
            proc = self.run_tool(s0, screening, bindings, out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("missing real S0 audio sha256", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
