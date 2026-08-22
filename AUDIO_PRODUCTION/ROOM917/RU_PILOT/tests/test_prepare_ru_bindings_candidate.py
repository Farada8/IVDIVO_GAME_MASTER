#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve()
TOOL = HERE.parents[1] / "tools" / "prepare_ru_bindings_candidate.py"
ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
PAIRS = (
    "RU_PAIR_01_ELENA_MINA_LOBBY",
    "RU_PAIR_02_ELENA_JULIAN_DOORS",
    "RU_PAIR_03_ELENA_JULIAN_STATUS",
    "RU_PAIR_04_CATE_LINE_VS_CASSETTE",
)


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BindingsCandidateTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> tuple[Path, Path, Path, Path]:
        snapshot = root / "snapshot.json"
        shortlist = root / "shortlist.json"
        review = root / "review.json"
        out = root / "bindings_candidate.json"

        candidates = []
        role_rows = {}
        for i, role in enumerate(ROLES, 1):
            voice_id = f"voice-{role.lower()}-{i}"
            candidates.append({
                "voice_id": voice_id,
                "name": f"Voice {role}",
                "category": "professional",
                "ru_verified": True,
                "notice_period": 365,
                "disable_at_unix": None,
            })
            role_rows[role] = [{
                "voice_id": voice_id,
                "provider_name": f"Voice {role}",
                "ru_verified": True,
                "notice_period": 365,
                "disable_at_unix": None,
                "binding_eligible": False,
                "preview_listen": "PENDING",
                "provider_identity_check": "PENDING_HUMAN_REVIEW",
            }]

        write(snapshot, {
            "status": "PASS_CANDIDATES_FOUND",
            "paid_synthesis_calls": 0,
            "candidates": candidates,
        })
        write(shortlist, {
            "status": "READY_FOR_PREVIEW_LISTEN_NOT_BINDINGS",
            "provider_snapshot": {"sha256": digest(snapshot)},
            "roles": role_rows,
        })

        review_roles = {}
        for role in ROLES:
            voice = role_rows[role][0]
            review_roles[role] = {
                "selected_voice_id": voice["voice_id"],
                "provider_name": voice["provider_name"],
                "preview_listen": "PASS",
                "provider_identity_check": "PASS",
                "native_ru_pronunciation": "PASS",
                "age_character_fit": "PASS",
                "naturalism": "PASS",
                "microemotion_subtext": "PASS",
                "precision_under_pressure": "PASS",
                "repeat_take_identity_consistency": "PASS",
                "founder_credibility": "PASS",
                "score_0_30": 26,
                "hard_reject": False,
            }
        write(review, {
            "status": "REVIEW_COMPLETE",
            "provider_snapshot_sha256": digest(snapshot),
            "shortlist_proposal_sha256": digest(shortlist),
            "roles": review_roles,
            "pair_tests": {pair: "PASS" for pair in PAIRS},
            "pronunciation_gate": "PASS",
            "all_selected_voice_ids_unique": "PASS",
            "paid_s0_authorized": False,
            "cast_lock": False,
            "full_e01_render_allowed": False,
        })
        return snapshot, shortlist, review, out

    def run_tool(self, snapshot: Path, shortlist: Path, review: Path, out: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(TOOL), "--provider-snapshot", str(snapshot), "--shortlist", str(shortlist), "--review", str(review), "--out", str(out)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_completed_review_creates_non_paid_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            snapshot, shortlist, review, out = self.make_fixture(Path(td))
            proc = self.run_tool(snapshot, shortlist, review, out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            row = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(row["status"], "READY_FOR_PAID_CANARY_AUTHORIZATION")
            self.assertFalse(row["founder_paid_canary_authorized"])
            self.assertFalse(row["paid_s0_authorized"])
            self.assertFalse(row["cast_lock"])
            self.assertFalse(row["full_episode_render_allowed"])
            self.assertEqual(set(row["roles"]), set(ROLES))

    def test_review_cannot_smuggle_paid_authorization(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            snapshot, shortlist, review, out = self.make_fixture(Path(td))
            row = json.loads(review.read_text(encoding="utf-8"))
            row["paid_s0_authorized"] = True
            write(review, row)
            proc = self.run_tool(snapshot, shortlist, review, out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("review must not contain paid authorization", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())

    def test_score_below_threshold_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            snapshot, shortlist, review, out = self.make_fixture(Path(td))
            row = json.loads(review.read_text(encoding="utf-8"))
            row["roles"]["ELENA"]["score_0_30"] = 23
            write(review, row)
            proc = self.run_tool(snapshot, shortlist, review, out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("below 24/30", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
