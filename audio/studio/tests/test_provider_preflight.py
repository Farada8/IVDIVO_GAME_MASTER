import json
import os
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import provider_preflight as pp


class ProviderPreflightTests(unittest.TestCase):
    def setUp(self):
        self.orig_get=pp._get_json
        self.orig_key=os.environ.get("ELEVENLABS_API_KEY")

    def tearDown(self):
        pp._get_json=self.orig_get
        if self.orig_key is None: os.environ.pop("ELEVENLABS_API_KEY",None)
        else: os.environ["ELEVENLABS_API_KEY"]=self.orig_key

    def test_missing_secret_fails(self):
        os.environ.pop("ELEVENLABS_API_KEY",None)
        r=pp.preflight(["eleven_v3"],[])
        self.assertEqual(r["status"],"FAIL")
        self.assertIn("FAIL_PROVIDER_CREDENTIAL",r["failures"])

    def test_mocked_models_and_voice_pass(self):
        os.environ["ELEVENLABS_API_KEY"]="TEST_SECRET_NOT_REAL"
        def fake(path,key,timeout=15.0):
            self.assertEqual(key,"TEST_SECRET_NOT_REAL")
            if path=="/v1/models": return [{"model_id":"eleven_v3","name":"v3","can_do_text_to_speech":True}], {"http_status":200}
            if path=="/v1/voices/v1": return {"voice_id":"v1","name":"Voice 1","category":"generated"}, {"http_status":200}
            raise RuntimeError(json.dumps({"failure":"FAIL_PROVIDER_CAPABILITY","http_status":404}))
        pp._get_json=fake
        r=pp.preflight(["eleven_v3"],["v1"])
        self.assertEqual(r["status"],"PASS")
        self.assertEqual(r["voices"]["v1"]["status"],"PASS")

if __name__=="__main__": unittest.main()
