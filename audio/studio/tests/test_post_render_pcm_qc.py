import tempfile
import unittest
import wave
from pathlib import Path
import sys

import numpy as np

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

from post_render_pcm_qc import candidate_render_qc, patch_boundary_qc, signal_qc


def write_wav(path: Path, x: np.ndarray, sr=48000):
    if x.ndim == 1:
        x = x[:, None]
    y = np.clip(x, -1, 0.999969).reshape(-1)
    raw = np.round(y * 32767).astype("<i2").tobytes()
    with wave.open(str(path), "wb") as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(raw)


class PostRenderPcmQcTests(unittest.TestCase):
    def test_clean_low_level_audio_passes(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "clean.wav"
            t = np.arange(4800) / 48000
            write_wav(path, 0.1 * np.sin(2 * np.pi * 440 * t))
            out = signal_qc(path)
            self.assertEqual(out["status"], "PASS")
            self.assertEqual(out["clip_sample_count"], 0)

    def test_full_scale_samples_fail_clipping(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "clip.wav"
            x = np.zeros(4800)
            x[100:120] = 1.0
            write_wav(path, x)
            out = signal_qc(path, clipping_threshold=0.999)
            self.assertEqual(out["status"], "FAIL_CLIPPING")
            self.assertGreater(out["clip_sample_count"], 0)

    def test_abrupt_patch_boundary_holds(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "jump.wav"
            x = np.zeros(4800)
            x[2400:] = 0.8
            write_wav(path, x)
            out = patch_boundary_qc(path, [{"start_seconds": 0.05, "end_seconds": 0.08}], max_boundary_jump=0.2)
            self.assertEqual(out["status"], "HOLD_BOUNDARY_DISCONTINUITY")

    def test_candidate_qc_never_auto_repairs(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "clean.wav"
            write_wav(path, np.zeros(4800))
            out = candidate_render_qc(path, [{"start_seconds": 0.02, "end_seconds": 0.04}])
            self.assertEqual(out["status"], "PASS")
            self.assertFalse(out["silent_clipping_allowed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
