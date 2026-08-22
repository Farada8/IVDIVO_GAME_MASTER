import importlib.util
import pathlib
import unittest

ENGINE = pathlib.Path(__file__).resolve().parents[1] / "engine" / "business_public_artifact_engine.py"
spec = importlib.util.spec_from_file_location("business_public_artifact_engine", ENGINE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
Evidence = mod.Evidence
evidence_ceiling = mod.evidence_ceiling
null_safe_number = mod.null_safe_number
budget_proxy = mod.budget_proxy
incumbent_bundling = mod.incumbent_bundling
data_readiness = mod.data_readiness
recurrence_gate = mod.recurrence_gate
zero_cash_route = mod.zero_cash_route
privacy_gate = mod.privacy_gate
supersession_gate = mod.supersession_gate
freshness_gate = mod.freshness_gate
library_evidence_weight = mod.library_evidence_weight
namespace_collision = mod.namespace_collision
wip_gate = mod.wip_gate
human_exit_gate = mod.human_exit_gate

class PublicArtifactEngineTests(unittest.TestCase):
    def test_01_public_caps_e2(self): self.assertEqual(evidence_ceiling([Evidence("PUBLIC_SIGNAL","eTenders")]), "E2_PUBLIC_SIGNAL")
    def test_02_knowledge_not_market(self): self.assertEqual(evidence_ceiling([Evidence("KNOWLEDGE","book")]), "K_ONLY")
    def test_03_human_distinct(self): self.assertEqual(evidence_ceiling([Evidence("HUMAN","raw")]), "E3_HUMAN_INTEREST")
    def test_04_payment_distinct(self): self.assertEqual(evidence_ceiling([Evidence("PAYMENT","receipt")]), "E4_PAYMENT")
    def test_05_unmeasured_zero_null(self): self.assertIsNone(null_safe_number(0,False))
    def test_06_measured_zero_valid(self): self.assertEqual(null_safe_number(0,True),0)
    def test_07_budget_proxy(self): self.assertEqual(budget_proxy(100000), "BUDGET_PROXY_ONLY")
    def test_08_unknown_budget(self): self.assertEqual(budget_proxy(None), "UNKNOWN")
    def test_09_discovery_bundled_mutates(self): self.assertEqual(incumbent_bundling(True,False,False),"MUTATE_TO_QUALIFICATION_EVIDENCE")
    def test_10_all_bundled_kills(self): self.assertEqual(incumbent_bundling(True,True,True),"KILL_UNDIFFERENTIATED")
    def test_11_public_data_ready(self): self.assertEqual(data_readiness(8,10),"AUTOMATION_CANDIDATE")
    def test_12_hybrid_data(self): self.assertEqual(data_readiness(6,10),"HYBRID_MANUAL_REVIEW")
    def test_13_private_site_blocks(self): self.assertEqual(data_readiness(9,10,1),"HUMAN_OR_CLIENT_DATA_REQUIRED")
    def test_14_recurring_job(self): self.assertEqual(recurrence_gate(12,True),"RECURRING_JOB")
    def test_15_one_off(self): self.assertEqual(recurrence_gate(1,True),"ONE_OFF_OR_WEAK")
    def test_16_manual_zero_cash(self): self.assertEqual(zero_cash_route("analysis",False,False,False),"MANUAL_SERVICE_FIRST")
    def test_17_partner_route(self): self.assertEqual(zero_cash_route("service",True,True,False),"BROKER_ORCHESTRATE")
    def test_18_capital_hold(self): self.assertEqual(zero_cash_route("service",True,False,False),"HOLD_CAPITAL_REQUIRED")
    def test_19_private_nonopen_rejected(self): self.assertEqual(privacy_gate(True,False,True),"REJECT_NONOPEN_PERSONAL_DATA")
    def test_20_stale_guidance_revalidate(self): self.assertEqual(supersession_gate("v1","v2"),"REVALIDATE")
    def test_21_stale_main_revalidate(self): self.assertEqual(freshness_gate("a","b"),"REBASE_REVALIDATE")
    def test_22_duplicate_zero_weight(self): self.assertEqual(library_evidence_weight(True,False),0)
    def test_23_namespace_collision(self): self.assertEqual(namespace_collision("A","B"),"REJECT_COLLISION")
    def test_24_wip_and_no_outreach(self):
        self.assertEqual(wip_gate(1,2),"PASS_WIP")
        self.assertEqual(human_exit_gate(True,False,True,True),"HOLD_NO_OUTREACH")

if __name__ == "__main__": unittest.main()
