import io, json, os, tempfile, unittest, wave, subprocess, sys
from pathlib import Path
import wave3_production_core as c

class Wave3ProductionTests(unittest.TestCase):
    def test_01_clean_manifest(self):
        m=c.clean_dry_manifest(); self.assertFalse(m["dispatch_allowed"]); self.assertEqual(m["spoken_units"],36); self.assertEqual(m["characters"],2163)
    def test_02_canary_identity_pass(self): self.assertEqual(c.validate_canary_identity(c.clean_dry_manifest())["status"],"PASS")
    def test_03_block_hash_drift(self):
        m=c.clean_dry_manifest(); m=json.loads(json.dumps(m)); m["blocks"]["CH01_S02_RB001"]["hash"]="x"
        with self.assertRaises(ValueError): c.validate_canary_identity(m)
    def test_04_unit_coverage_drift(self):
        m=c.clean_dry_manifest(); m=json.loads(json.dumps(m)); m["blocks"]["CH01_S02_RB002"]["units"]=[25,26]
        with self.assertRaises(ValueError): c.validate_canary_identity(m)
    def test_05_ledger_plan_persist(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"ledger.json"; L=c.SpendLedger(p); self.assertEqual(L.plan("h","RB"),"PLANNED"); self.assertTrue(p.exists())
    def test_06_ledger_accept_reuse(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"ledger.json"; L=c.SpendLedger(p); L.plan("h","RB"); L.transition("h","ACCEPTED","req1","resp1"); self.assertEqual(c.SpendLedger(p).plan("h","RB"),"REUSED_ACCEPTED")
    def test_07_ledger_ambiguous_blocks_retry(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"ledger.json"; L=c.SpendLedger(p); L.plan("h","RB"); L.transition("h","AMBIGUOUS","req1"); self.assertEqual(L.plan("h","RB"),"RECONCILE_REQUIRED")
            with self.assertRaises(ValueError): L.transition("h","SENT")
    def test_08_accepted_immutable(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"ledger.json"; L=c.SpendLedger(p); L.plan("h","RB"); L.transition("h","ACCEPTED")
            with self.assertRaises(ValueError): L.transition("h","REJECTED")
    def test_09_error_auth(self): self.assertEqual(c.normalize_provider_error(401)["category"],"AUTH")
    def test_10_error_rate(self): self.assertEqual(c.normalize_provider_error(429)["category"],"RATE_LIMIT")
    def test_11_error_quota(self): self.assertEqual(c.normalize_provider_error(402,"quota_exceeded")["category"],"QUOTA")
    def test_12_error_alignment(self): self.assertEqual(c.normalize_provider_error(500,"alignment_error")["category"],"ALIGNMENT")
    def test_13_error_voice(self): self.assertEqual(c.normalize_provider_error(400,"voice_missing")["category"],"VOICE")
    def test_14_retry_ambiguous(self): self.assertEqual(c.retry_decision(c.normalize_provider_error(503),True),"QUARANTINE_AMBIGUOUS")
    def test_15_retry_rate(self): self.assertEqual(c.retry_decision(c.normalize_provider_error(429)),"BACKOFF_RETRY")
    def test_16_pcm48_valid(self):
        b=c.pcm_s16le_to_wav(b"\x00\x00"*480)
        with wave.open(io.BytesIO(b),"rb") as w: self.assertEqual(w.getframerate(),48000); self.assertEqual(w.getsampwidth(),2)
    def test_17_pcm_bad_rate(self):
        with self.assertRaises(ValueError): c.pcm_s16le_to_wav(b"\x00\x00"*10,44100)
    def test_18_pcm_bad_length(self):
        with self.assertRaises(ValueError): c.pcm_s16le_to_wav(b"\x00")
    def test_19_audio_hash_stable(self): self.assertEqual(c.audio_hash(b"a"), c.audio_hash(b"a"))
    def test_20_ttd_alignment(self):
        raw={"voice_segments":[{"dialogue_input_index":0,"start_time_seconds":0.0,"end_time_seconds":1.0}]}; self.assertEqual(c.normalize_alignment(raw,turn_ids=["U1"])[0]["source_schema"],"voice_segments")
    def test_21_ttd_bad_index(self):
        raw={"voice_segments":[{"dialogue_input_index":1,"start_time_seconds":0.0,"end_time_seconds":1.0}]}
        with self.assertRaises(ValueError): c.normalize_alignment(raw,turn_ids=["U1"])
    def test_22_tts_alignment(self):
        raw={"alignment":{"character_start_times_seconds":[0,.1],"character_end_times_seconds":[.1,.2]}}; self.assertEqual(c.normalize_alignment(raw,turn_id="U1")["end"],.2)
    def test_23_unknown_alignment(self):
        with self.assertRaises(ValueError): c.normalize_alignment({"x":1},turn_id="U1")
    def test_24_capability_pass(self): self.assertEqual(c.capability_drift({"voice_ids":["v1"],"model_ids":["m1"]},{"voices":{"v1":{}},"models":["m1"]})["status"],"PASS")
    def test_25_capability_drift_no_substitute(self):
        r=c.capability_drift({"voice_ids":["v1"],"model_ids":["m1"]},{"voices":{},"models":[]}); self.assertEqual(r["status"],"FAIL_DRIFT"); self.assertFalse(r["auto_substitution"])
    def test_26_second_provider_mock(self): self.assertEqual(c.ProviderAdapterMock2().render({"request_hash":"h","block_id":"RB"})["provider"],"mock2")
    def test_27_silent_reaction_zero_units(self): self.assertEqual(c.promote_silent_reaction({"anchor_id":"A","character_id":"E","trigger":"U","silent_action":"wait","silence_policy":"PROTECTED"})["spoken_unit_delta"],0)
    def test_28_silent_reaction_missing(self):
        with self.assertRaises(ValueError): c.promote_silent_reaction({})
    def test_29_pause_semantic(self):
        r=c.compile_pause(["AFTERMATH","LISTENING","NO_REPLY"],[450,750,1200]); self.assertIsNone(r.get("absolute_time")); self.assertEqual(r["timing_status"],"SEMANTIC_UNTIL_ALIGNMENT")
    def test_30_pause_dramatic_rejected(self):
        with self.assertRaises(ValueError): c.compile_pause(["DRAMATIC"])
    def test_31_latency_semantic(self): self.assertIsNone(c.compile_reply_latency("U24","U26","PROTECTED_WAIT")["absolute_time"])
    def test_32_latency_bad_state(self):
        with self.assertRaises(ValueError): c.compile_reply_latency("A","B","UNIFORM")
    def test_33_mic_close(self): self.assertFalse(c.compile_microphone_choreography("AOIFE","CLOSE",["POOL_EDGE"])["mix_pan_required"])
    def test_34_mic_bad(self):
        with self.assertRaises(ValueError): c.compile_microphone_choreography("AOIFE","EXTREME_LEFT")
    def test_35_ai_tell_non_authoritative(self):
        r=c.ai_tell_flags(["yes.","yes.","yes.","yes."],[1,1,1,1],[2,2,2,2]); self.assertTrue(r["flags"]); self.assertFalse(r["authoritative"]); self.assertFalse(r["auto_reject"])
    def test_36_ai_tell_can_be_empty(self): self.assertFalse(c.ai_tell_flags(["a","b","c","d"],[.5,.9,1.2,.7],[1,2,1.5,2.5])["auto_reject"])
    def test_37_lock_holds_without_fatigue(self): self.assertEqual(c.performance_lock_gate({"multi_state":1,"pronunciation":1,"human_review":1,"pair":1,"fatigue":0})["status"],"HOLD")
    def test_38_lock_requires_human(self): self.assertEqual(c.performance_lock_gate({"multi_state":1,"pronunciation":1,"human_review":0,"pair":1,"fatigue":1})["status"],"HOLD")
    def test_39_lock_code_path(self):
        r=c.performance_lock_gate({"multi_state":1,"pronunciation":1,"human_review":1,"pair":1,"fatigue":1}); self.assertEqual(r["status"],"LOCKED"); self.assertFalse(r["machine_may_auto_lock"])
    def test_40_binding_invalidation(self): self.assertEqual(c.scoped_invalidation("binding_version"),sorted(c.CANARY_BLOCKS))
    def test_41_pron_invalidation(self): self.assertEqual(c.scoped_invalidation("pronunciation_version"),["CH01_S02_RB001","CH01_S02_RB003"])
    def test_42_orchestration_gate(self): self.assertEqual(c.orchestration_acceptance({"clean_build":1,"resume":1,"scoped_invalidation":1,"selective_rerender":1,"fail_closed":1})["status"],"PASS_CANDIDATE")
    def test_43_cli_build_resume(self):
        with tempfile.TemporaryDirectory() as d:
            cli=Path(__file__).with_name("ivdivo_audio_candidate_cli.py"); env=dict(os.environ); env["PYTHONPATH"]=str(Path(__file__).parent)
            p=subprocess.run([sys.executable,str(cli),"build","--out",d],capture_output=True,text=True,env=env); self.assertEqual(p.returncode,0,p.stderr); self.assertEqual(json.loads(p.stdout)["dispatch_allowed"],False)
            p2=subprocess.run([sys.executable,str(cli),"resume","--out",d],capture_output=True,text=True,env=env); self.assertEqual(p2.returncode,0,p2.stderr); self.assertEqual(json.loads(p2.stdout)["resent_requests"],0)
    def test_44_cli_invalidation(self):
        cli=Path(__file__).with_name("ivdivo_audio_candidate_cli.py"); env=dict(os.environ); env["PYTHONPATH"]=str(Path(__file__).parent)
        p=subprocess.run([sys.executable,str(cli),"invalidate","pronunciation_version"],capture_output=True,text=True,env=env); self.assertEqual(p.returncode,0,p.stderr); self.assertEqual(json.loads(p.stdout)["invalidated"],["CH01_S02_RB001","CH01_S02_RB003"])

if __name__=="__main__": unittest.main(verbosity=2)
