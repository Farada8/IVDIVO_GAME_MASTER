import unittest
from tools.ivdivo_mirror_integrity import compare

def rec(lid="A", **kw):
    d={"logical_id":lid,"authority_epoch":"1","frontier_token":"F1","status_token":"CURRENT",
       "mirror_mode":"SEMANTIC","content_fingerprint":"x","source_revision":"r1"}
    d.update(kw); return d

class MirrorTests(unittest.TestCase):
    def test_semantic_match(self):
        self.assertEqual(compare({"github_records":[rec()], "drive_records":[rec()]})["status"],"PASS")
    def test_missing_drive(self):
        o=compare({"github_records":[rec()], "drive_records":[]})
        self.assertEqual(o["status"],"ISSUES_FOUND")
        self.assertIn("MISSING_DRIVE_MIRROR",o["items"][0]["issues"])
    def test_frontier_divergence(self):
        o=compare({"github_records":[rec()], "drive_records":[rec(frontier_token="F2")]})
        self.assertIn("FRONTIER_DIVERGENCE",o["items"][0]["issues"])
    def test_status_divergence(self):
        o=compare({"github_records":[rec()], "drive_records":[rec(status_token="STALE")]})
        self.assertIn("STATUS_DIVERGENCE",o["items"][0]["issues"])
    def test_exact_bytes_requires_hash(self):
        o=compare({"github_records":[rec(mirror_mode="EXACT_BYTES")],"drive_records":[rec(mirror_mode="EXACT_BYTES")]})
        self.assertIn("RAW_HASH_REQUIRED",o["items"][0]["issues"])
    def test_exact_hash_mismatch(self):
        o=compare({"github_records":[rec(mirror_mode="EXACT_BYTES",raw_sha256="a")],
                   "drive_records":[rec(mirror_mode="EXACT_BYTES",raw_sha256="b")]})
        self.assertIn("RAW_HASH_MISMATCH",o["items"][0]["issues"])
    def test_expected_revision_stale(self):
        o=compare({"github_records":[rec(expected_peer_revision="r2")],"drive_records":[rec(source_revision="r3")]})
        self.assertIn("EXPECTED_DRIVE_REVISION_STALE",o["items"][0]["issues"])
    def test_invalid_duplicate_fails_closed(self):
        o=compare({"github_records":[rec(),rec()], "drive_records":[rec()]})
        self.assertEqual(o["status"],"FAIL_CLOSED")

if __name__=="__main__": unittest.main()
