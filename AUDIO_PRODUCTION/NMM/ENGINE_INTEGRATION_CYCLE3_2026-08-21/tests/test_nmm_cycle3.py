import json,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'runtime'))
import nmm_source_guard as sg, nmm_asset_evidence as ae, nmm_evidence_debt as ed, nmm_human_evidence as he, nmm_learning_bridge as lb, nmm_proof_bundle as pb, nmm_frontier_router as fr
class T(unittest.TestCase):
 def test_source_baseline(self):
  exp={'source_sha256':'5c3d86b271524614ad7adf37c71bafba74f9f63a292ada46ad567ff75e88a1c0','e01_sha256':'f95871c17cd2501c6a3ca36fe1d0dd850ebae2118fe2ca1de75274a53c75de9b','ledger_sha256':'7128bb3b74289533b9e8be279958c8a9dfb40564c7255e9b0e11306c988bae5a','occurrences':269,'tokens':1494}
  source=ROOT/'fixtures/NMM_E01_SOURCE.txt'
  if source.exists(): self.assertEqual(sg.gate(source,exp)['gate'],'PASS')
 def test_mutations_fail(self):
  p=json.loads((ROOT/'proofs/NMM_SOURCE_MUTATION_PROOF_v1.json').read_text()); self.assertTrue(all(p[k]['gate']=='FAIL' for k in ['delete','duplicate','alter','forbidden']))
 def test_human_not_faked(self):
  p=he.make_protocol('x',['a'],['q'],.8); self.assertEqual(he.score(p,[])['result'],'NOT_RUN'); self.assertFalse(he.score(p,[])['pass_claim_allowed'])
 def test_learning_one_project_discovery_only(self):
  r=lb.record('NMM','u','CLUE','M','Isla extra whistle','Northbridge cause','Leo repair','IMPROVED'); c=lb.universal_candidate(r,1); self.assertEqual(c['promotion_status'],'DISCOVERY_ONLY'); self.assertFalse(c['auto_promote']); self.assertNotIn('Isla',json.dumps(c)); self.assertNotIn('Northbridge',json.dumps(c))
 def test_proof_bundle_no_go(self): self.assertEqual(pb.build({'source':True,'mutation':True,'asset_ingest':True})['release'],'NO_GO')
 def test_frontier(self): self.assertEqual(fr.next_frontier({'SOURCE_GUARDS':True}),'AUTH_PROVIDER_SNAPSHOT'); self.assertFalse(fr.generic_runtime_change_allowed({'demonstrated_generic_gap':False}))
if __name__=='__main__': unittest.main()
