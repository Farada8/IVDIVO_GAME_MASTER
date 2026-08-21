import io, tempfile, unittest, wave
from pathlib import Path
import wave4_runtime_promotion_candidate as c

class T(unittest.TestCase):
    def test_01_manifest(self):
        m=c.canary_manifest(); self.assertEqual((m["request_count"],m["spoken_units"],m["provider_characters"]),(3,36,2163))
    def test_02_identity_pass(self): self.assertEqual(c.validate_canary_identity(c.canary_manifest())["status"],"PASS")
    def test_03_request_drift(self):
        m=c.canary_manifest(); m["request_count"]=4
        with self.assertRaises(ValueError): c.validate_canary_identity(m)
    def test_04_unit_drift(self):
        m=c.canary_manifest(); m["spoken_units"]=35
        with self.assertRaises(ValueError): c.validate_canary_identity(m)
    def test_05_char_drift(self):
        m=c.canary_manifest(); m["provider_characters"]=2164
        with self.assertRaises(ValueError): c.validate_canary_identity(m)
    def test_06_hash_drift(self):
        import copy
        m=copy.deepcopy(c.canary_manifest()); m["blocks"]["CH01_S02_RB001"]["hash"]="bad"
        with self.assertRaises(ValueError): c.validate_canary_identity(m)
    def test_07_pron_manifest(self):
        p=c.pronunciation_audition_manifest(); self.assertFalse(p["pronunciation_lock"]); self.assertEqual([x["block_id"] for x in p["targets"]],["CH01_S02_RB001","CH01_S02_RB003"])
    def test_08_ledger_plan(self):
        with tempfile.TemporaryDirectory() as d:
            L=c.SpendLedger(Path(d)/"l.json"); self.assertEqual(L.plan("h","b"),"PLANNED")
    def test_09_ledger_reuse(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"l.json"; L=c.SpendLedger(p); L.plan("h","b"); L.transition("h","ACCEPTED","r","x",0.1)
            self.assertEqual(c.SpendLedger(p).plan("h","b"),"REUSED_ACCEPTED")
    def test_10_ledger_ambiguous(self):
        with tempfile.TemporaryDirectory() as d:
            L=c.SpendLedger(Path(d)/"l.json"); L.plan("h","b"); L.transition("h","AMBIGUOUS","req")
            self.assertEqual(L.plan("h","b"),"RECONCILE_REQUIRED")
    def test_11_accepted_immutable(self):
        with tempfile.TemporaryDirectory() as d:
            L=c.SpendLedger(Path(d)/"l.json"); L.plan("h","b"); L.transition("h","ACCEPTED")
            with self.assertRaises(ValueError): L.transition("h","REJECTED")
    def test_12_ambiguous_accept(self):
        a=c.Attempt("h","b","AMBIGUOUS","req1")
        r=c.reconcile_ambiguous(a,lambda rid:{"accepted":True,"response_hash":"z"}); self.assertEqual(r["action"],"REUSE")
    def test_13_ambiguous_fail(self):
        a=c.Attempt("h","b","AMBIGUOUS","req1")
        r=c.reconcile_ambiguous(a,lambda rid:{"definitive_failure":True}); self.assertEqual(r["action"],"RETRY_ALLOWED")
    def test_14_ambiguous_hold(self):
        a=c.Attempt("h","b","AMBIGUOUS","req1")
        r=c.reconcile_ambiguous(a,lambda rid:None); self.assertEqual(r["action"],"NO_RETRY")
    def test_15_error_auth(self): self.assertEqual(c.normalize_provider_error(401)["category"],"AUTH")
    def test_16_error_rate(self): self.assertEqual(c.normalize_provider_error(429)["category"],"RATE_LIMIT")
    def test_17_error_quota(self): self.assertEqual(c.normalize_provider_error(402,"quota","credits")["category"],"QUOTA")
    def test_18_error_align(self): self.assertEqual(c.normalize_provider_error(500,"alignment_error")["category"],"ALIGNMENT")
    def test_19_pcm(self):
        b=c.pcm_s16le_to_wav(b"\0\0"*480)
        with wave.open(io.BytesIO(b),"rb") as w: self.assertEqual((w.getframerate(),w.getnchannels()),(48000,1))
    def test_20_pcm_rate_fail(self):
        with self.assertRaises(ValueError): c.pcm_s16le_to_wav(b"\0\0"*10,44100)
    def test_21_fingerprint(self): self.assertEqual(c.asset_fingerprint(b"a")["sha256"],c.asset_fingerprint(b"a")["sha256"])
    def test_22_ttd(self):
        r=c.normalize_alignment({"voice_segments":[{"dialogue_input_index":0,"start_time_seconds":0,"end_time_seconds":1}]},turn_ids=["U1"]); self.assertEqual(r[0]["turn_id"],"U1")
    def test_23_ttd_bad(self):
        with self.assertRaises(ValueError): c.normalize_alignment({"voice_segments":[{"dialogue_input_index":1,"start_time_seconds":0,"end_time_seconds":1}]},turn_ids=["U1"])
    def test_24_tts(self):
        r=c.normalize_alignment({"alignment":{"character_start_times_seconds":[0,.1],"character_end_times_seconds":[.1,.2]}},turn_id="U1"); self.assertEqual(r["end"],.2)
    def test_25_unknown_alignment(self):
        with self.assertRaises(ValueError): c.normalize_alignment({"x":1},turn_id="U")
    def test_26_capability_pass(self): self.assertEqual(c.capability_drift({"voice_ids":["v1"],"model_ids":["m1"]},{"voices":{"v1":{}},"models":["m1"]})["status"],"PASS")
    def test_27_capability_fail(self):
        r=c.capability_drift({"voice_ids":["v1"],"model_ids":["m1"]},{"voices":{},"models":[]}); self.assertEqual(r["status"],"FAIL_DRIFT"); self.assertFalse(r["auto_substitution"])
    def test_28_ethan_invalidation(self): self.assertEqual(c.role_binding_invalidation("ETHAN"),["CH01_S02_RB001","CH01_S02_RB002"])
    def test_29_narrator_invalidation(self): self.assertEqual(c.role_binding_invalidation("NARRATOR"),["CH01_S02_RB001","CH01_S02_RB002","CH01_S02_RB003"])
    def test_30_pron_invalidation(self): self.assertEqual(c.pronunciation_invalidation(),["CH01_S02_RB001","CH01_S02_RB003"])
    def test_31_live_prov_hold(self): self.assertEqual(c.live_provenance_gate([])["status"],"HOLD")
    def test_32_live_prov_pass(self):
        rec=[{"request_hash":"h","provider_request_id":"r","audio_sha256":"a","alignment_raw":{},"binding_version":"b"} for _ in range(3)]
        self.assertEqual(c.live_provenance_gate(rec)["status"],"PASS")
    def test_33_coverage_pass(self):
        u=[f"U{i}" for i in range(36)]; self.assertEqual(c.unit_alignment_coverage(u,u)["status"],"PASS")
    def test_34_coverage_duplicate(self):
        u=["U1","U2"]; self.assertEqual(c.unit_alignment_coverage(u,["U1","U1","U2"])["status"],"FAIL")
    def test_35_synthetic_firewall(self): self.assertFalse(c.synthetic_timing_firewall("SYNTHETIC_FIXTURE")["timeline_allowed"])
    def test_36_live_firewall(self): self.assertTrue(c.synthetic_timing_firewall("LIVE_PROVIDER_ALIGNMENT")["timeline_allowed"])

if __name__=="__main__": unittest.main(verbosity=2)
