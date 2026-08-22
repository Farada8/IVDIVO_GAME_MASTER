#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve()
TOOL = HERE.parents[1] / "tools" / "prepare_ru_cast_shortlist.py"
spec = importlib.util.spec_from_file_location("prepare_ru_cast_shortlist", TOOL)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ShortlistCompilerTests(unittest.TestCase):
    def write_snapshot(self, root: Path, payload: dict) -> Path:
        path = root / "snapshot.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def test_auth_hold_stays_zero_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            snapshot = self.write_snapshot(root, {
                "status": "HOLD_PROVIDER_AUTH_REQUIRED",
                "paid_synthesis_calls": 0,
                "query_policy": {
                    "language": "ru",
                    "category": "professional",
                    "min_notice_period_days": 365,
                    "include_custom_rates": False,
                    "include_live_moderated": False,
                },
                "candidates": [],
                "ranked_role_candidates": {role: [] for role in mod.ROLES},
            })
            result = mod.compile_shortlist(snapshot, 3)
            self.assertEqual(result["status"], "HOLD_PROVIDER_AUTH_REQUIRED")
            self.assertFalse(result["cast_lock"])
            self.assertFalse(result["paid_s0_authorized"])
            self.assertFalse(result["full_e01_render_allowed"])
            self.assertTrue(all(not result["roles"][role] for role in mod.ROLES))

    def test_valid_snapshot_produces_review_only_shortlist(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            candidates = []
            rankings = {role: [] for role in mod.ROLES}
            for i, role in enumerate(mod.ROLES, 1):
                voice_id = f"native-{role.lower()}-{i}"
                candidate = {
                    "voice_id": voice_id,
                    "name": f"Voice {role}",
                    "category": "professional",
                    "language": "ru",
                    "gender": "male" if role == "JULIAN" else "female",
                    "age": "middle_aged",
                    "accent": "russian",
                    "descriptive": "grounded warm conversational",
                    "use_case": "characters",
                    "preview_url": f"https://example.invalid/{voice_id}.mp3",
                    "notice_period": 365,
                    "disable_at_unix": None,
                    "live_moderation_enabled": False,
                    "rate": 1.0,
                    "ru_verified": True,
                }
                candidates.append(candidate)
                rankings[role].append({
                    "voice_id": voice_id,
                    "name": candidate["name"],
                    "score": 90,
                    "preview_url": candidate["preview_url"],
                    "reasons": ["fixture"],
                })

            snapshot = self.write_snapshot(root, {
                "status": "PASS_CANDIDATES_FOUND",
                "paid_synthesis_calls": 0,
                "query_policy": {
                    "language": "ru",
                    "category": "professional",
                    "min_notice_period_days": 365,
                    "include_custom_rates": False,
                    "include_live_moderated": False,
                },
                "candidates": candidates,
                "ranked_role_candidates": rankings,
            })
            result = mod.compile_shortlist(snapshot, 3)
            self.assertEqual(result["status"], "READY_FOR_PREVIEW_LISTEN_NOT_BINDINGS")
            self.assertFalse(result["auto_cast"])
            self.assertFalse(result["cast_lock"])
            self.assertFalse(result["paid_s0_authorized"])
            self.assertFalse(result["full_e01_render_allowed"])
            for role in mod.ROLES:
                self.assertEqual(len(result["roles"][role]), 1)
                row = result["roles"][role][0]
                self.assertEqual(row["preview_listen"], "PENDING")
                self.assertEqual(row["provider_identity_check"], "PENDING_HUMAN_REVIEW")
                self.assertFalse(row["binding_eligible"])

    def test_diagnostic_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            diagnostic = next(iter(mod.DIAGNOSTIC_IDS))
            candidate = {
                "voice_id": diagnostic,
                "name": "Forbidden diagnostic",
                "category": "professional",
                "notice_period": 365,
                "disable_at_unix": None,
                "live_moderation_enabled": False,
                "rate": 1.0,
                "ru_verified": True,
            }
            rankings = {role: [] for role in mod.ROLES}
            rankings["ELENA"] = [{"voice_id": diagnostic, "name": candidate["name"], "score": 99}]
            snapshot = self.write_snapshot(root, {
                "status": "PASS_CANDIDATES_FOUND",
                "paid_synthesis_calls": 0,
                "query_policy": {
                    "language": "ru",
                    "category": "professional",
                    "min_notice_period_days": 365,
                    "include_custom_rates": False,
                    "include_live_moderated": False,
                },
                "candidates": [candidate],
                "ranked_role_candidates": rankings,
            })
            result = mod.compile_shortlist(snapshot, 3)
            self.assertEqual(result["status"], "HOLD_INCOMPLETE_ROLE_SHORTLIST")
            self.assertTrue(result["rejected_candidates"])
            self.assertIn("historical_diagnostic_voice_id_forbidden", result["rejected_candidates"][0]["failures"])


if __name__ == "__main__":
    unittest.main()
