import unittest, wave, io
import wave2_contract_harness as h

class Wave2Tests(unittest.TestCase):
    def test_clean_dry(self):
        b=h.clean_dry_build(); self.assertEqual(b["spoken_units"],36); self.assertFalse(b["dispatch_allowed"])
    def test_repro_hash(self):
        self.assertEqual(h.canonical_hash(h.clean_dry_build()),h.canonical_hash(h.clean_dry_build()))
    def test_resume(self):
        L={}; x="abc"; self.assertEqual(h.resume_request(x,L),"PLANNED"); self.assertEqual(h.resume_request(x,L),"REUSED")
    def test_voice_invalidation(self): self.assertEqual(h.invalidate("voice_binding_version"),set(h.CANARY_BLOCKS))
    def test_pron_invalidation(self): self.assertEqual(h.invalidate("pronunciation_version"),{"CH01_S02_RB001","CH01_S02_RB003"})
    def test_selective(self): self.assertEqual(h.selective_rerender("CH01_S02_RB002"),["CH01_S02_RB002"])
    def test_provider_neutral(self):
        c=h.provider_neutral_compilation(); self.assertNotIn("api_key",c); self.assertNotIn("endpoint",c)
    def test_401(self): self.assertFalse(h.normalize_error(401)["retryable"])
    def test_429(self): self.assertTrue(h.normalize_error(429)["retryable"])
    def test_retry_429(self): self.assertEqual(h.retry_policy(h.normalize_error(429)),"BACKOFF_RETRY")
    def test_ambiguous(self): self.assertEqual(h.retry_policy(h.normalize_error(500),True),"QUARANTINE_AMBIGUOUS")
    def test_pcm48(self):
        w=h.pcm_s16le_to_wav(b"\x00\x00"*480)
        with wave.open(io.BytesIO(w),'rb') as f: self.assertEqual(f.getframerate(),48000)
    def test_ttd_alignment(self):
        raw={"voice_segments":[{"dialogue_input_index":0,"start_time_seconds":0.0,"end_time_seconds":1.0}]}
        self.assertEqual(h.normalize_ttd_alignment(raw,["U1"])[0]["turn_id"],"U1")
    def test_tts_alignment(self):
        raw={"alignment":{"character_start_times_seconds":[0,.1],"character_end_times_seconds":[.1,.2]}}
        self.assertEqual(h.normalize_tts_alignment(raw,"U1")["end"],.2)
    def test_missing_alignment(self):
        with self.assertRaises(ValueError): h.normalize_tts_alignment({},"U1")
    def test_voice_drift(self): self.assertNotEqual(h.voice_drift("A","B"),"PASS")
    def test_media_separation(self): self.assertEqual({h.media_bus(x) for x in ("dialogue","music","sfx")},{"DIALOGUE","MUSIC","SFX"})
    def test_second_provider_mock(self):
        self.assertEqual(h.normalized_provider_response("mock2","H")["request_hash"],"H")
    def test_silent_anchor(self): self.assertEqual(h.silent_reaction_anchor()["spoken_unit_delta"],0)
    def test_pause_functions(self): self.assertNotIn("DRAMATIC",h.VALID_PAUSE_FUNCTIONS)
    def test_latency_and_mic_and_hardfails(self):
        self.assertGreater(len(set(h.reply_latency_plan().values())),2)
        self.assertEqual(h.microphone_states(),{"CLOSE_INTIMATE","NORMAL","ACROSS_ROOM","MEDIA"})
        self.assertEqual(len(h.PERFORMANCE_HARD_FAILS),8)

if __name__=="__main__": unittest.main(verbosity=2)
