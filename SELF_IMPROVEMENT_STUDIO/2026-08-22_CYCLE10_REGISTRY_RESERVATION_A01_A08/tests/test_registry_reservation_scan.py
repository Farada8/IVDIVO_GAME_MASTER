import json, pathlib, unittest, importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("rr",ROOT/"runtime/registry_reservation_scan.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
BASE=json.loads((ROOT/"ACTIVE_REGISTRY_RESERVATION_SNAPSHOT_v1.json").read_text())

class TestReservation(unittest.TestCase):
    def complete(self):
        x=json.loads(json.dumps(BASE)); x["diff_coverage"]["visibility_complete"]=True; x["diff_coverage"]["hold_reason"]=None; return x
    def test01_real_snapshot_holds_partial(self): self.assertEqual(m.validate_snapshot(BASE)["status"],"HOLD_PARTIAL_VISIBILITY")
    def test02_partial_never_emits_next(self): self.assertNotIn("next_unreserved",m.validate_snapshot(BASE))
    def test03_complete_view_reserves_si0016(self): self.assertEqual(m.validate_snapshot(self.complete())["next_unreserved"],"SI-0017")
    def test04_two_pr_same_reservation_collision(self):
        x=self.complete(); x["reservations"].append(dict(x["reservations"][0],pr=999)); self.assertEqual(m.validate_snapshot(x)["status"],"HOLD_ID_COLLISION")
    def test05_committed_vs_reserved_collision(self):
        x=self.complete(); x["committed_registry"]["committed_ids"].append("SI-0016"); self.assertEqual(m.validate_snapshot(x)["status"],"HOLD_ID_COLLISION")
    def test06_stale_main_holds(self): self.assertEqual(m.validate_snapshot(self.complete(),"different")["status"],"HOLD_STALE_SNAPSHOT")
    def test07_same_main_can_pass(self):
        x=self.complete(); self.assertEqual(m.validate_snapshot(x,x["main_sha"])["status"],"PASS_COMPLETE_RESERVATION_VIEW")
    def test08_closed_pr_releases(self): self.assertEqual(m.reservation_lifecycle("closed",False,True),"RELEASED_CLOSED_UNMERGED")
    def test09_merged_pr_revalidate(self): self.assertEqual(m.reservation_lifecycle("closed",True,True),"REVALIDATE_AS_COMMITTED")
    def test10_candidate_removed_releases(self): self.assertEqual(m.reservation_lifecycle("open",False,False),"RELEASED_CANDIDATE_REMOVED")
    def test11_historical_does_not_reserve(self): self.assertEqual(m.classify_record({"status":"HISTORICAL_PROVENANCE_ONLY"}),"DOES_NOT_RESERVE")
    def test12_no_allocation_does_not_reserve(self): self.assertEqual(m.classify_record({"status":"NO_ALLOCATION_EXPLICIT"}),"DOES_NOT_RESERVE")
    def test13_ambiguous_is_discovery_only(self): self.assertEqual(m.classify_record({"status":"MAYBE"}),"AMBIGUOUS_DISCOVERY_ONLY")
    def test14_merge_time_main_advance(self): self.assertEqual(m.merge_time_revalidate(self.complete(),"new",[],[])["status"],"HOLD_STALE_SNAPSHOT")
    def test15_merge_time_collision(self):
        x=self.complete(); self.assertEqual(m.merge_time_revalidate(x,x["main_sha"],["SI-0016"],x["reservations"])["status"],"HOLD_ID_COLLISION")
    def test16_renumber_preserves_alias(self):
        r=m.renumber_candidate("SI-0016","SI-0017",{"pr":147,"candidate_blob_sha":"abc"}); self.assertTrue(r["preserve_provenance"]); self.assertEqual(r["historical_alias"],"SI-0016")

if __name__=="__main__": unittest.main(verbosity=2)
