import unittest
from tools.ivdivo_routing_consistency import check

def layer(role,status="FOUNDER_LOCKED",event="lock1",next_action="NEXT_PROJECT"):
    return {"role":role,"observed_status":status,"event_artifact_id":event,"next_action":next_action}

class RoutingTests(unittest.TestCase):
    def test_founder_lock_happy(self):
        p={"event":"FOUNDER_LOCK","project_id":"D10","event_artifact_id":"lock1",
           "layers":[layer("PROJECT_STATE"),layer("PORTFOLIO_ROUTER"),layer("WORKSTATE")]}
        self.assertEqual(check(p)["status"],"PASS")
    def test_missing_aggregate_is_issue_not_story_rewrite(self):
        p={"event":"FOUNDER_LOCK","project_id":"D10","event_artifact_id":"lock1",
           "layers":[layer("PROJECT_STATE")]}
        o=check(p); self.assertEqual(o["status"],"ISSUES_FOUND")
        self.assertTrue(all(r["action"]!="CONTINUE_STORY_PROSE" for r in o["repairs"]))
    def test_stale_status_patch_only(self):
        p={"event":"FOUNDER_LOCK","project_id":"D10","event_artifact_id":"lock1",
           "layers":[layer("PROJECT_STATE"),layer("PORTFOLIO_ROUTER","READY_FOR_LOCK"),layer("WORKSTATE")]}
        o=check(p); self.assertIn("STATUS_STALE:PORTFOLIO_ROUTER:READY_FOR_LOCK",o["issues"])
    def test_provenance_mismatch(self):
        p={"event":"FOUNDER_LOCK","project_id":"D10","event_artifact_id":"lock1",
           "layers":[layer("PROJECT_STATE"),layer("PORTFOLIO_ROUTER",event="lock2"),layer("WORKSTATE")]}
        self.assertIn("EVENT_PROVENANCE_MISMATCH:PORTFOLIO_ROUTER",check(p)["issues"])
    def test_locked_story_prose_route_fails(self):
        p={"event":"FOUNDER_LOCK","project_id":"D10","event_artifact_id":"lock1",
           "layers":[layer("PROJECT_STATE",next_action="GENERATE_E25"),layer("PORTFOLIO_ROUTER"),layer("WORKSTATE")]}
        self.assertEqual(check(p)["status"],"FAIL")
    def test_optional_aggregate_event_drift_is_flagged(self):
        result=check({"event":"FINAL_STORY_GATE_PASS","project_id":"D01","event_artifact_id":"gate",
          "layers":[
            {"role":"PROJECT_STATE","observed_status":"FINAL_STORY_GATE_PASS","event_artifact_id":"gate"},
            {"role":"PORTFOLIO_ROUTER","observed_status":"FINAL_STORY_GATE_PASS","event_artifact_id":"gate"},
            {"role":"SYSTEM_AGGREGATE","track_event":True,"normalized_event":"ACTIVE_STORY","event_artifact_id":"old"}
          ]})
        self.assertEqual(result["status"],"ISSUES_FOUND")
        self.assertTrue(any(i.startswith("EVENT_STATE_STALE:SYSTEM_AGGREGATE") for i in result["issues"]))
    def test_unknown_event_fails_closed(self):
        self.assertEqual(check({"event":"MAGIC","project_id":"X","event_artifact_id":"a","layers":[]})["status"],"FAIL_CLOSED")
    def test_final_gate_requires_no_founder_lock_inference(self):
        p={"event":"FINAL_STORY_GATE_PASS","project_id":"D01","event_artifact_id":"gate1",
           "layers":[{"role":"PROJECT_STATE","observed_status":"FINAL_STORY_GATE_PASS","event_artifact_id":"gate1"},
                     {"role":"PORTFOLIO_ROUTER","observed_status":"FINAL_STORY_GATE_PASS","event_artifact_id":"gate1"}]}
        self.assertEqual(check(p)["status"],"PASS")
    def test_story_mutation_request_fails(self):
        p={"event":"FOUNDER_LOCK","project_id":"D10","event_artifact_id":"lock1",
           "layers":[dict(layer("PROJECT_STATE"),story_text_mutation_requested=True),layer("PORTFOLIO_ROUTER"),layer("WORKSTATE")]}
        self.assertEqual(check(p)["status"],"FAIL")

if __name__=="__main__": unittest.main()
