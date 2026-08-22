from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROOM917_TESTS = ROOT / "AUDIO_PRODUCTION" / "ROOM917" / "TOOLS" / "POST_RENDER_ENGINEERING_v2" / "tests"
sys.path.insert(0, str(ROOM917_TESTS))

from test_p003b_automix_eligibility_gate import P003BAutoMixEligibilityGateTests  # noqa: F401,E402
