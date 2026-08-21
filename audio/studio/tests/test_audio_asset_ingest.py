import io
import unittest
import wave
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from audio_asset_ingest import ingest_audio_bytes, inspect_wav


def wav_bytes(*, rate=48000, channels=1, width=2, frames=480):
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(width)
        w.setframerate(rate)
        w.writeframes(b"\x00" * frames * channels * width)
    return out.getvalue()


class AudioAssetIngestTests(unittest.TestCase):
    def test_valid_wav_passes_and_hashes(self):
        data = wav_bytes(rate=48000, channels=2, width=3)
        canonical, evidence = ingest_audio_bytes(data, source_format="WAV", source_ref="fixture.wav")
        self.assertEqual(canonical, data)
        self.assertEqual(evidence["gate"], "PASS")
        self.assertEqual(evidence["technical"]["sample_rate_hz"], 48000)
        self.assertEqual(evidence["technical"]["channels"], 2)
        self.assertEqual(evidence["technical"]["bit_depth"], 24)
        self.assertEqual(evidence["source_sha256"], evidence["canonical_sha256"])

    def test_44100_wav_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "FAIL_AUDIO_SAMPLE_RATE"):
            ingest_audio_bytes(wav_bytes(rate=44100), source_format="WAV", source_ref="bad.wav")

    def test_three_channels_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "FAIL_AUDIO_CHANNEL_COUNT"):
            ingest_audio_bytes(wav_bytes(channels=3), source_format="WAV", source_ref="bad.wav")

    def test_raw_pcm_requires_metadata(self):
        with self.assertRaisesRegex(ValueError, "RAW_PCM_METADATA"):
            ingest_audio_bytes(b"\x00\x00" * 10, source_format="PCM_S16LE", source_ref="raw.pcm")

    def test_raw_pcm_wraps_losslessly_into_48k_wav(self):
        pcm = b"\x00\x00" * 480
        canonical, evidence = ingest_audio_bytes(
            pcm,
            source_format="PCM_S16LE",
            source_ref="raw.pcm",
            raw_pcm_sample_rate=48000,
            raw_pcm_channels=1,
        )
        technical = inspect_wav(canonical)
        self.assertEqual(technical["sample_rate_hz"], 48000)
        self.assertEqual(technical["channels"], 1)
        self.assertEqual(evidence["transformation"], "LOSSLESS_CONTAINER_WRAP_PCM16LE_TO_WAV")
        self.assertNotEqual(evidence["source_sha256"], evidence["canonical_sha256"])

    def test_malformed_pcm_fails(self):
        with self.assertRaisesRegex(ValueError, "PCM_LENGTH"):
            ingest_audio_bytes(
                b"\x00\x00\x00",
                source_format="PCM_S16LE",
                source_ref="raw.pcm",
                raw_pcm_sample_rate=48000,
                raw_pcm_channels=1,
            )

    def test_unknown_format_fails(self):
        with self.assertRaisesRegex(ValueError, "FORMAT_UNSUPPORTED"):
            ingest_audio_bytes(b"abc", source_format="MAGIC", source_ref="x")


if __name__ == "__main__":
    unittest.main(verbosity=2)
