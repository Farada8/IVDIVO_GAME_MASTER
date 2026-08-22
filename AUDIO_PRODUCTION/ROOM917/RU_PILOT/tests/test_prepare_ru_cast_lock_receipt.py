#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve()
TOOL = HERE.parents[1] / "tools" / "prepare_ru_cast_lock_receipt.py"
VALIDATOR = HERE.parents[1] / "tools" / "validate_ru_cast_lock.py"
ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
S0_IDS = {
    "ELENA":"RU_S0_ELENA_BOUNDARY",
    "JULIAN":"RU_S0_JULIAN_72",
    "MINA":"RU_S0_MINA_INTRO",
    "CATE":"RU_S0_CATE_LENI_BIRD",
}
FV_IDS = {
    "ELENA":"RU_FV_ELENA_REPEAT",
    "JULIAN":"RU_FV_JULIAN_REPEAT",
    "MINA":"RU_FV_MINA_REPEAT",
    "CATE":"RU_FV_CATE_REPEAT",
}


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hh(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()


class CastLockCompilerTests(unittest.TestCase):
    def fixture(self, root: Path):
        snapshot=root/'snapshot.json'; bindings=root/'bindings.json'; s0=root/'s0.json'; finalist=root/'finalist.json'; review=root/'review.json'; out=root/'lock.json'
        candidates=[]; bind_roles={}
        for i,role in enumerate(ROLES,1):
            vid=f'voice-{role.lower()}-{i}'
            candidates.append({"voice_id":vid,"name":f"Voice {role}","category":"professional","ru_verified":True,"notice_period":365,"disable_at_unix":None})
            bind_roles[role]={"voice_id":vid,"provider_identity_check":"PASS","provider_durability_check":"PASS"}
        write(snapshot,{"status":"PASS_CANDIDATES_FOUND","authenticated_request_used":True,"paid_synthesis_calls":0,"generated_at":"2026-08-22T18:00:00Z","candidates":candidates})
        write(bindings,{"status":"PAID_S0_AUTHORIZED","canary_binding_only":True,"cast_lock":False,"roles":bind_roles})

        s0_audio=[]; fv_audio=[]
        role_hashes={}
        for role in ROLES:
            s0h=hh('s0-'+role); fvh=hh('fv-'+role)
            role_hashes[role]=(s0h,fvh)
            s0_audio.append({"path":f"01__{S0_IDS[role]}/{S0_IDS[role]}__audio.mp3","sha256":s0h,"bytes":100})
            fv_audio.append({"path":f"01__{FV_IDS[role]}/{FV_IDS[role]}__audio.mp3","sha256":fvh,"bytes":100})
        pair_hash={
            'ELENA_MINA':hh('pair-em'),
            'ELENA_JULIAN_1':hh('pair-ej1'),
            'ELENA_JULIAN_2':hh('pair-ej2'),
            'CATE_IDENTITY':hh('pair-cate'),
        }
        s0_audio += [
            {"path":"05__RU_S0_ELENA_MINA_RELATION/RU_S0_ELENA_MINA_RELATION__audio.mp3","sha256":pair_hash['ELENA_MINA'],"bytes":100},
            {"path":"06__RU_S0_ELENA_JULIAN_FRICTION/RU_S0_ELENA_JULIAN_FRICTION__audio.mp3","sha256":pair_hash['ELENA_JULIAN_1'],"bytes":100},
        ]
        fv_audio += [
            {"path":"05__RU_FV_ELENA_JULIAN_STATUS/RU_FV_ELENA_JULIAN_STATUS__audio.mp3","sha256":pair_hash['ELENA_JULIAN_2'],"bytes":100},
            {"path":"06__RU_FV_CATE_DOMESTIC/RU_FV_CATE_DOMESTIC__audio.mp3","sha256":pair_hash['CATE_IDENTITY'],"bytes":100},
        ]
        write(s0,{"stage_semantics":"S0_SCREENING_ONLY_NOT_CAST_LOCK","cast_locked":False,"full_episode_rendered":False,"audio_files":s0_audio})
        write(finalist,{"cast_locked":False,"full_episode_rendered":False,"human_listen_required":True,"audio_files":fv_audio})

        review_roles={}
        for role in ROLES:
            s0h,fvh=role_hashes[role]
            review_roles[role]={
                "selected_voice_id":bind_roles[role]['voice_id'],
                "provider_name":f"Voice {role}",
                "accepted_canary_ids":[S0_IDS[role],FV_IDS[role]],
                "accepted_canary_sha256":[s0h,fvh],
                "native_ru_pronunciation":"PASS",
                "pronunciation_score_0_5":4.5,
                "age_character_fit":"PASS",
                "naturalism":"PASS",
                "naturalism_score_0_5":4.5,
                "microemotion_subtext":"PASS",
                "precision_under_pressure":"PASS",
                "repeat_take_identity_consistency":"PASS",
                "founder_credibility":"YES",
                "score_0_30":27,
                "hard_reject_flags":[],
            }
        write(review,{
            "status":"POST_CANARY_REVIEW_COMPLETE",
            "acting_evidence_complete":True,
            "cast_lock":False,
            "full_e01_render_allowed":False,
            "provider_snapshot_sha256":digest(snapshot),
            "pre_canary_bindings_sha256":digest(bindings),
            "s0_canary_receipt_sha256":digest(s0),
            "finalist_verification_receipt_sha256":digest(finalist),
            "pronunciation_gate":"PASS",
            "all_selected_voice_ids_unique":"PASS",
            "roles":review_roles,
            "pair_tests":{
                "ELENA_MINA":{"status":"PASS","block_id":"RU_S0_ELENA_MINA_RELATION","audio_sha256":pair_hash['ELENA_MINA'],"source_stage":"S0"},
                "ELENA_JULIAN_1":{"status":"PASS","block_id":"RU_S0_ELENA_JULIAN_FRICTION","audio_sha256":pair_hash['ELENA_JULIAN_1'],"source_stage":"S0"},
                "ELENA_JULIAN_2":{"status":"PASS","block_id":"RU_FV_ELENA_JULIAN_STATUS","audio_sha256":pair_hash['ELENA_JULIAN_2'],"source_stage":"FINALIST"},
                "CATE_IDENTITY":{"status":"PASS","block_id":"RU_FV_CATE_DOMESTIC","audio_sha256":pair_hash['CATE_IDENTITY'],"source_stage":"FINALIST"},
            }
        })
        return snapshot,bindings,s0,finalist,review,out

    def call(self, files):
        snapshot,bindings,s0,finalist,review,out=files
        return subprocess.run(["python",str(TOOL),"--provider-snapshot",str(snapshot),"--bindings",str(bindings),"--s0-receipt",str(s0),"--finalist-receipt",str(finalist),"--review",str(review),"--out",str(out)],text=True,capture_output=True,check=False)

    def test_complete_real_evidence_compiles_validator_clean_lock(self):
        with tempfile.TemporaryDirectory() as td:
            files=self.fixture(Path(td)); proc=self.call(files)
            self.assertEqual(proc.returncode,0,proc.stderr+proc.stdout)
            out=files[-1]
            val=subprocess.run(["python",str(VALIDATOR),str(out)],text=True,capture_output=True,check=False)
            self.assertEqual(val.returncode,0,val.stderr+val.stdout)
            row=json.loads(out.read_text(encoding='utf-8'))
            self.assertEqual(row['status'],'LOCKED')
            self.assertTrue(row['global_lock_gate']['full_e01_dialogue_render_allowed'])

    def test_fake_pair_hash_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            files=self.fixture(Path(td)); review=files[4]
            row=json.loads(review.read_text(encoding='utf-8')); row['pair_tests']['ELENA_JULIAN_2']['audio_sha256']='f'*64; write(review,row)
            proc=self.call(files)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn('finalist audio evidence not found',proc.stderr+proc.stdout)

    def test_single_take_cannot_lock(self):
        with tempfile.TemporaryDirectory() as td:
            files=self.fixture(Path(td)); review=files[4]
            row=json.loads(review.read_text(encoding='utf-8')); row['roles']['ELENA']['accepted_canary_ids']=row['roles']['ELENA']['accepted_canary_ids'][:1]; row['roles']['ELENA']['accepted_canary_sha256']=row['roles']['ELENA']['accepted_canary_sha256'][:1]; write(review,row)
            proc=self.call(files)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn('at least two accepted take IDs/hashes required',proc.stderr+proc.stdout)

    def test_founder_borderline_cannot_lock(self):
        with tempfile.TemporaryDirectory() as td:
            files=self.fixture(Path(td)); review=files[4]
            row=json.loads(review.read_text(encoding='utf-8')); row['roles']['CATE']['founder_credibility']='BORDERLINE'; write(review,row)
            proc=self.call(files)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn('Founder final credibility must be YES',proc.stderr+proc.stdout)

    def test_selected_voice_cannot_drift_from_binding(self):
        with tempfile.TemporaryDirectory() as td:
            files=self.fixture(Path(td)); review=files[4]
            row=json.loads(review.read_text(encoding='utf-8')); row['roles']['MINA']['selected_voice_id']='other-voice'; write(review,row)
            proc=self.call(files)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn('differs from sealed audition binding',proc.stderr+proc.stdout)


if __name__=='__main__': unittest.main()
