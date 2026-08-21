#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQ = ROOT / "BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_REQUESTS_v1.json"
VOICE = ROOT / "BODYGUARD_E01_CURRENT_VOICE_MAP_TEMPLATE_v1.json"
TAKES = ROOT / "BODYGUARD_E01_TAKE_MANIFEST_TEMPLATE_v1.json"
DRIVER = ROOT / "bodyguard_e01_render_driver.py"

EXPECTED_SHA = "2af60ca3b58bc90a2863e8f6dbee2bf7541d6b1f2315e78704f12ca214da9149"

req = json.loads(REQ.read_text(encoding="utf-8"))
takes = json.loads(TAKES.read_text(encoding="utf-8"))

assert len(req["requests"]) == 190
assert sum(len(r["exact_text"].split()) for r in req["requests"]) == 1344
joined = "\n".join(r["exact_text"] for r in req["requests"])
assert hashlib.sha256(joined.encode("utf-8")).hexdigest() == EXPECTED_SHA
assert len(takes["take_rows"]) == 405
assert len({r["take_id"] for r in takes["take_rows"]}) == 405

proc = subprocess.run(
    [
        sys.executable,
        str(DRIVER),
        "--requests", str(REQ),
        "--voice-map", str(VOICE),
        "--take-manifest", str(TAKES),
        "--limit", "3",
    ],
    capture_output=True,
    text=True,
)

assert proc.returncode == 0, proc.stderr
assert "DRY RUN" in proc.stdout
assert "Planned rows: 3" in proc.stdout

print("PASS: authority, 190 blocks, 1344 words, 405 takes, dry-run.")
