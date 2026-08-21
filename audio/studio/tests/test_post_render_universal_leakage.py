import unittest
from pathlib import Path


class UniversalPostRenderLeakageTests(unittest.TestCase):
    def test_universal_runtime_contains_no_project_story_tokens(self):
        runtime = Path(__file__).resolve().parents[1] / "runtime"
        targets = [
            runtime / "post_render_contracts.py",
            runtime / "post_render_engineering.py",
            runtime / "post_render_learning.py",
            runtime / "post_render_pcm_qc.py",
        ]
        forbidden = [
            "GREYHAVEN", "ELENA REED", "JULIAN ASHCROFT", "CATE REED",
            "ROOM917", "ROOM 917", "NINETY MISSING MINUTES", "BODYGUARD",
            "LESSON ZERO", "ETHAN", "AOIFE",
        ]
        for path in targets:
            text = path.read_text(encoding="utf-8").upper()
            for token in forbidden:
                self.assertNotIn(token, text, f"{path.name} leaked project token {token}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
