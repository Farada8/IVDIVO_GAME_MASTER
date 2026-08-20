import base64
import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import elevenlabs_adapter as ea


class ElevenLabsAdapterTests(unittest.TestCase):
    def test_compile_ttd(self):
        block={"block_id":"B1","block_type":"TTD_BLOCK","model_id":"eleven_v3","turns":[{"unit_id":"u1","exact_text":"Hello.","voice_id":"v1"},{"unit_id":"u2","exact_text":"Hi.","voice_id":"v2"}]}
        c=ea.compile_block(block)
        self.assertEqual(c["endpoint_profile"],"ELEVEN_TTD_TIMESTAMPS_V1")
        self.assertEqual(c["body"]["inputs"][1]["voice_id"],"v2")
        self.assertEqual(len(c["request_hash"]),64)

    def test_compile_tts(self):
        block={"block_id":"B2","block_type":"ISOLATED_TTS","exact_text":"Leni-bird.","voice_id":"v3","model_id":"eleven_v3"}
        c=ea.compile_block(block)
        self.assertEqual(c["endpoint_profile"],"ELEVEN_TTS_TIMESTAMPS_V1")

    def test_pronunciation_limit(self):
        block={"block_id":"B2","block_type":"ISOLATED_TTS","exact_text":"x","voice_id":"v3","pronunciation_dictionary_locators":[{"id":str(i),"version_id":"1"} for i in range(4)]}
        with self.assertRaises(ValueError): ea.compile_block(block)

    def test_persist_voice_segments(self):
        block={"block_id":"B1","block_type":"TTD_BLOCK","turns":[{"unit_id":"u1","exact_text":"Hello.","voice_id":"v1"},{"unit_id":"u2","exact_text":"Hi.","voice_id":"v2"}]}
        c=ea.compile_block(block)
        raw={"audio_base64":base64.b64encode(b"ID3FAKEAUDIO").decode(),"voice_segments":[{"voice_id":"v1","start_time_seconds":0.0,"end_time_seconds":0.5,"dialogue_input_index":0},{"voice_id":"v2","start_time_seconds":0.5,"end_time_seconds":0.8,"dialogue_input_index":1}]}
        with tempfile.TemporaryDirectory() as d:
            ev=ea.persist(c,raw,{"http_status":200},Path(d))
            norm=json.loads(Path(ev["normalized_alignment_artifact"]).read_text())
            self.assertEqual(norm["source_schema"],"voice_segments")
            self.assertEqual(len(norm["records"]),2)

    def test_persist_character_alignment(self):
        block={"block_id":"B2","block_type":"ISOLATED_TTS","exact_text":"Hi","voice_id":"v3"}
        c=ea.compile_block(block)
        raw={"audio_base64":base64.b64encode(b"FAKE").decode(),"alignment":{"characters":["H","i"],"character_start_times_seconds":[0.0,0.2],"character_end_times_seconds":[0.2,0.4]}}
        with tempfile.TemporaryDirectory() as d:
            ev=ea.persist(c,raw,{"http_status":200},Path(d))
            norm=json.loads(Path(ev["normalized_alignment_artifact"]).read_text())
            self.assertEqual(norm["source_schema"],"character_alignment")
            self.assertEqual(norm["records"][0]["end_seconds"],0.4)

if __name__=="__main__": unittest.main()
