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


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BindingsCandidateTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> tuple[Path, Path, Path, Path]:
        snapshot = root / "snapshot.json"
        shortlist = root / "shortlist.json"
        review = root / "pre_canary_review.json"
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

        write(snapshot, {"status": "PASS_CANDIDATES_FOUND", "paid_synthesis_calls": 0, "candidates": candidates})
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
                "provider_durability_check": "PASS",
                "plausible_for_canary": "PASS",
            }
        write(review, {
            "status": "PRE_CANARY_REVIEW_COMPLETE",
            "provider_snapshot_sha256": digest(snapshot),
            "shortlist_proposal_sha256": digest(shortlist),
            "roles": review_roles,
            "all_selected_voice_ids_unique": "PASS",
            "acting_evidence_complete": False,
            "pronunciation_canary_gate": "NOT_RUN_YET",
            "pair_tests": "NOT_RUN_YET",
            "repeat_take_identity_consistency": "NOT_RUN_YET",
            "founder_cast_credibility": "NOT_RUN_YET",
            "paid_s0_authorized": False,
            "cast_lock": False,
            "full_e01_render_allowed": False,
        })
        return snapshot, shortlist, review, out

    def run_tool(self, snapshot: Path, shortlist: Path, review: Path, out: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(TOOL), "--provider-snapshot", str(snapshot), "--shortlist", str(shortlist), "--review", str(review), "--out", str(out)],
            text=True, capture_output=True, check=False,
        )

    def test_pre_canary_review_creates_non_paid_candidate_without_fake_acting_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            snapshot, shortlist, review, out = self.make_fixture(Path(td))
            proc = self.run_tool(snapshot, shortlist, review, out)
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            row = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(row["status"], "READY_FOR_PAID_CANARY_AUTHORIZATION")
            self.assertEqual(row["pre_canary_binding_gate"], "PASS")
            self.assertTrue(row["canary_binding_only"])
            self.assertFalse(row["acting_evidence_complete"])
            self.assertEqual(row["pair_tests"], "NOT_RUN_YET")
            self.assertEqual(row["pronunciation_gate"], "NOT_RUN_YET")
            self.assertEqual(row["founder_credibility_gate"], "NOT_RUN_YET")
            self.assertFalse(row["cast_lock"])

    def test_review_cannot_smuggle_pair_pass_upstream(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            snapshot, shortlist, review, out = self.make_fixture(Path(td))
            row = json.loads(review.read_text(encoding="utf-8"))
            row["pair_tests"] = "PASS"
            write(review, row)
            proc = self.run_tool(snapshot, shortlist, review, out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("pair tests must not be pre-passed", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())

    def test_review_cannot_smuggle_founder_cast_pass_upstream(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            snapshot, shortlist, review, out = self.make_fixture(Path(td))
            row = json.loads(review.read_text(encoding="utf-8"))
            row["founder_cast_credibility"] = "PASS"
            write(review, row)
            proc = self.run_tool(snapshot, shortlist, review, out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("Founder cast credibility must not be pre-passed", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())

    def test_durability_below_365_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            snapshot, shortlist, review, out = self.make_fixture(Path(td))
            row = json.loads(shortlist.read_text(encoding="utf-8"))
            row["roles"]["ELENA"][0]["notice_period"] = 90
            write(shortlist, row)
            # preserve sealed shortlist hash in review after intentional fixture mutation
            rev = json.loads(review.read_text(encoding="utf-8"))
            rev["shortlist_proposal_sha256"] = digest(shortlist)
            write(review, rev)
            proc = self.run_tool(snapshot, shortlist, review, out)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("notice period below 365", proc.stderr + proc.stdout)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
