#!/usr/bin/env python3
import json
import unittest
from pathlib import Path

from authority_hygiene_guard import (
    HOLD,
    PASS,
    QUARANTINE,
    evaluate_authority,
)

HERE = Path(__file__).resolve().parent
RULES = json.loads((HERE / "AUTHORITY_HYGIENE_RULES_v1.json").read_text(encoding="utf-8"))


class AuthorityHygieneGuardTest(unittest.TestCase):
    def test_current_source_passes(self):
        candidate = {
            "drive_id": "1Rz_Tv83fNhQIuPnMA4jRkESmgiu8xA-GZnctbQYDP_I",
            "title": "ROOM 917 — E01 ELEVENLABS ACTOR + SOUND DIRECTOR MASTER v1.0",
            "content": (
                "ACTIVE ENGINE: THE INSURABLE FIRE\n"
                "CAST: ELENA REED / JULIAN ASHCROFT / MINA SHAH / CATE-ON-THE-LINE\n"
                "DO NOT USE obsolete Gideon / Mara Quinn / Celia / Quiet Register production cues"
            ),
        }
        self.assertEqual(evaluate_authority(candidate, RULES)["status"], PASS)

    def test_legacy_mara_source_is_quarantined(self):
        candidate = {
            "drive_id": "16fdc16IHn6YXtJCcmfd5Ft4r4Mt0Jyep",
            "title": "ROOM_917_E01_STUDIO_SFX_CUE_SHEET",
            "content": (
                "Authentic 917 line has NO steady 50 Hz hum. "
                "Mara remains a human voice. "
                "Tiny raw 'Nellie-bird' playback."
            ),
        }
        self.assertEqual(evaluate_authority(candidate, RULES)["status"], QUARANTINE)

    def test_unknown_source_holds(self):
        candidate = {
            "drive_id": "unknown",
            "title": "ROOM917 E01 notes",
            "content": "ACTIVE ENGINE: THE INSURABLE FIRE",
        }
        self.assertEqual(evaluate_authority(candidate, RULES)["status"], HOLD)


if __name__ == "__main__":
    unittest.main()
