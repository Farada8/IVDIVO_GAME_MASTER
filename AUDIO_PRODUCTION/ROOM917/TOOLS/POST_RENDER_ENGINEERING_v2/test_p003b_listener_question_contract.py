#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "p003b_listener_package_builder.py"
EXPECTED_CLASSES = ["ACTOR_BELIEF","AI_AUDIBLE","DEAD_SCENE","GEOGRAPHY","MYSTERY","SFX_MASKING"]
EXPECTED_QUESTIONS = [
    "Верю ли я актёру?",
    "Где слышно ИИ?",
    "Где сцена мёртвая?",
    "Понятна ли география?",
    "Работает ли тайна?",
    "Не мешают ли SFX словам?",
]
FORBIDDEN = ["next episode", "stop listening", "market", "retention", "want to continue"]

spec = importlib.util.spec_from_file_location("p003b_builder", TARGET)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

assert mod.QUESTION_CLASSES == EXPECTED_CLASSES, (mod.QUESTION_CLASSES, EXPECTED_CLASSES)
assert mod.QUESTIONS == EXPECTED_QUESTIONS, (mod.QUESTIONS, EXPECTED_QUESTIONS)
assert len(mod.QUESTION_CLASSES) == 6
assert len(mod.QUESTIONS) == 6
joined = " ".join(mod.QUESTIONS).lower()
for token in FORBIDDEN:
    assert token not in joined, f"non-P003B question leaked into blind package: {token}"

stereo = {"file":"R917_BLIND_E01_TARGET.wav","sha256":"0"*64,"playback":"PASS_A_FIRST"}
public = mod.build_public_manifest("TEST_PACKAGE", stereo)
assert set(public["files"]) == {"stereo_target"}, public["files"]
assert "machine_qc_status" not in public
serialized_public = str(public).lower()
assert "phone_proxy.wav" not in serialized_public
assert "mono.wav" not in serialized_public
assert "pass_b_candidate" not in serialized_public
assert public["question_classes"] == EXPECTED_CLASSES
assert public["questions"] == EXPECTED_QUESTIONS
assert any("P003B_UNSEAL_GATE" in rule for rule in public["listener_rules"])

pass_c = mod.build_pass_c_manifest(
    "TEST_PACKAGE",
    {"mono_folddown":{"file":"R917_BLIND_E01_MONO.wav"},"phone_band_mono":{"file":"R917_BLIND_E01_PHONE_PROXY.wav"}},
    "PASS_MACHINE_QC",
)
assert pass_c["status"] == "SEALED_UNTIL_P003B_UNSEAL_GATE"
assert "PASS_B_COMPLETE" in pass_c["open_only_after"]
assert "NO_OPEN_REPAIR" in pass_c["open_only_after"]
assert pass_c["machine_qc_status"] == "PASS_MACHINE_QC"
assert "mono_folddown" in pass_c["files"] and "phone_band_mono" in pass_c["files"]

print("PASS P003B six-question contract and blind/Pass-C firewall")
