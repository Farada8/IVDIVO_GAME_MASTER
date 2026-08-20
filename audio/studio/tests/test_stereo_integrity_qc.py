import tempfile
import unittest
import wave
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stereo_integrity_qc import metrics, diagnose


def write_stereo(path: Path, left, right, sr=48000):
    x = np.stack([left, right], axis=1)
    y = np.clip(x * 32767, -32768, 32767).astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(y.tobytes())


class StereoIntegrityTests(unittest.TestCase):
    def test_detects_mixer_collapse(self):
        sr = 48000
        t = np.arange(sr) / sr
        left = 0.2 * np.sin(2 * np.pi * 440 * t)
        right = 0.2 * np.sin(2 * np.pi * 550 * t)
        mono = (left + right) / 2
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / 'source.wav'
            stem = Path(d) / 'stem.wav'
            write_stereo(source, left, right, sr)
            write_stereo(stem, mono, mono, sr)
            result = diagnose(metrics(source), metrics(stem), 'NATURAL_STEREO')
            self.assertEqual(result['diagnosis'], 'MIXER_COLLAPSE')
            self.assertEqual(result['status'], 'FAIL')

    def test_intentional_mono_is_legal(self):
        sr = 48000
        t = np.arange(sr) / sr
        mono = 0.2 * np.sin(2 * np.pi * 440 * t)
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / 'source.wav'
            stem = Path(d) / 'stem.wav'
            write_stereo(source, mono, mono, sr)
            write_stereo(stem, mono, mono, sr)
            result = diagnose(metrics(source), metrics(stem), 'MONO_INTENTIONAL')
            self.assertEqual(result['diagnosis'], 'INTENTIONAL_MONO')
            self.assertEqual(result['status'], 'PASS')


if __name__ == '__main__':
    unittest.main()
