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
print("PASS P003B six-question contract")
