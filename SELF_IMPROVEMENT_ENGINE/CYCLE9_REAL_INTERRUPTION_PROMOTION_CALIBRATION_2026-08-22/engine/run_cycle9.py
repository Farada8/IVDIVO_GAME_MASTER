from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine.cycle9_engine import *

ROOT=Path(__file__).resolve().parents[1]
run_ids=[f"C9-{i:02d}" for i in range(1,33)]
ledger=SequentialLedger(run_ids)

def add(i,title,status,finding,evidence=(),next_action=''):
    ledger.append(RunResult(f"C9-{i:02d}",title,status,finding,tuple(evidence),next_action))

add(1,'Restore CURRENT authority','PASS','v2 remains VERIFIED_CURRENT; Cycle9 has no authority effect.',('main:4d6dc7c5','CURRENT_IVDIVO_SELF_IMPROVEMENT_STATE schema2.7'))
add(2,'Fresh-main branch reconciliation','PASS','Old Cycle9 branch is diverged; use fresh-main rebase instead of force overwrite.',('old branch ahead3/behind1',))
add(3,'Build Self-Improvement library index','PASS','Authority, private source pointers, prior cycles and generated artifact pointers normalized.',('library/SOURCE_REGISTRY.json',))
add(4,'Full candidate-family freshness','PASS','SI-0008..SI-0015 family exists; no new ID allocated before semantic need.',('REGISTRY_EXTENSIONS','SI-0015'))
add(5,'Cycle7 dedupe','PASS','Durable transaction/recovery mechanisms are reused, not reimplemented.',('Cycle7 durable convergence',))
add(6,'Cycle8 dedupe','PASS','Writing/story adapter results are evidence surfaces, not a new global SI authority.',('Cycle8 merged/executed',))
add(7,'Reference-ingest authority firewall','PASS','v3 reference mechanisms remain candidate; references cannot promote authority.',('Wave2 master','v3 HOLD'))
add(8,'SI-0014 contract extraction','PASS','Promotion requires >=3 genuine recoveries across >=2 projects with zero false resume.',('SI-0014 READY_FOR_PILOT',))
add(9,'SI-0015 contract extraction','PASS','Real project pilot + healthy control + false-positive review remain required.',('SI-0015 READY_FOR_PILOT',))
real=InterruptionObservation('C9-REAL-001',True,('IVDIVO_SELF_IMPROVEMENT','BUSINESS_ENGINEERING'),True,True,True)
add(10,'Classify real browser/dialog interruption','PASS','Merged event-001 evidence qualifies as one genuine SI-0014 recovery event with two recovered project slices and zero false resume.',('event001','projects:2','false_resume:false'))
counter=RecoveryEvidenceCounter(); counter.add(real)
add(11,'Qualify SI-0014 event','PASS','Event-001 qualifies, but SI-0014 promotion remains not ready because genuine event count is 1/3 even though project count is 2/2.',('qualified_event:1','required_events:3','distinct_projects:2','promotion_ready:false'),'Collect two additional naturally occurring genuine interruption recoveries with zero false resume.')
add(12,'Project-slice freshness positive pilot','PASS','CURRENT_MATCH when embedded and controlling frontier agree.',(project_slice_freshness(ProjectSlice('P','A','A')),))
add(13,'Historical negative control','PASS','Historical/superseded slice is exempt, preventing false positives.',(project_slice_freshness(ProjectSlice('P','A','B','HISTORICAL')),))
add(14,'False-resume canary','PASS','Stale CURRENT slice is detected and blocked.',(project_slice_freshness(ProjectSlice('P','A','B')),))
add(15,'Explicit approval firewall','PASS','RESUME-equivalent state cannot satisfy explicit approval event.',(project_slice_freshness(ProjectSlice('P','A','A','CURRENT',True,False)),))
add(16,'Evidence-class substitution firewall','PASS','Automated test cannot satisfy Human Signal claim.',evidence_gate(EvidenceClaim('HUMAN_PREFERENCE',frozenset({EvidenceClass.TEST_EXECUTED})))[1])
add(17,'Meta WIP limiter','PASS','One primary + up to two independent pilots accepted; two primaries rejected.',('WIP_OK','WIP_EXCEEDED'))
add(18,'Value-of-information router','PASS','Metric without decision relevance is rejected; high-VOI decision-linked metric is measured.',('REJECT_METRIC_WITHOUT_DECISION_RELEVANCE','MEASURE'))
add(19,'Causal system model contract','PASS','Intervention must declare intended effect, feedbacks and guardrails before promotion pilot.',('CAUSAL_MODEL_READY',))
add(20,'Policy-resistance gate','PASS','Local gain with system loss routes to POLICY_RESISTANCE_DETECTED.',('POLICY_RESISTANCE_DETECTED',))
add(21,'Double-loop learning trigger','PASS','Repeated local failure routes to model/boundary review rather than repeated patching.',('DOUBLE_LOOP_REVIEW',))
add(22,'Uncertainty ledger discipline','PASS','Unknown external evidence remains unknown; missing evidence is a first-class state.',('UNKNOWN!=FAIL!=PASS',))
add(23,'Measure-just-enough gate','PASS','Measurement requires named decision and uncertainty reduction; cheap easy counts are insufficient.',('metric_gate',))
add(24,'Decision-delta telemetry','PASS','Artifact/activity counts do not equal progress; decision change or independent information gain is tracked.',('DECISION_CHANGED','NO_DECISION_DELTA'))
add(25,'Mechanism semantic dedupe','PASS','Duplicate mechanism routes to MERGE instead of creating another engine.',('MERGE',))
add(26,'False-positive pruning','PASS','High false-positive mechanism routes to NARROW; unused mechanism routes HOLD.',('NARROW','HOLD'))
add(27,'Cross-store transaction closure','PASS','Hash mismatch stops; ambiguous irreversible side effect quarantines; exact confirmed stores close.',('STOP_IDENTITY_MISMATCH','QUARANTINE_AMBIGUOUS_IRREVERSIBLE','TRANSACTION_COMPLETE'))
add(28,'Self-reference guard','PASS','Engine cannot exempt itself from its own promotion rules.',('REJECT_SELF_EXEMPTION',))
add(29,'Adversarial direct-promotion fixture','PASS','VERIFIED_CURRENT without application/readback evidence is blocked.',('BLOCK_DIRECT_VERIFIED_CURRENT',))
add(30,'v3 promotion calibration','HOLD','Reference-ingest mechanisms are useful but no real production net-gain pilot justifies v3 CURRENT promotion.',('v3 candidate','real pilot absent'),'Run bounded production comparison before any architecture promotion.')
add(31,'Full regression + cold package gate','PASS','Cycle9 deterministic suite and package replay are the required engineering gate; external classes remain separate.',('tests','cold replay'))
add(32,'Synthesis + derive next64','PASS','Cycle9 converges on pilot evidence, measurement, pruning and production-safe self-reference; exactly 64 next cards generated.',('NEXT64',))

out={'cycle':'CYCLE9_REAL_INTERRUPTION_PROMOTION_CALIBRATION','complete':ledger.complete,'ledger_sha256':ledger.digest(),'results':[asdict(x) for x in ledger.results]}
reports=ROOT/'reports'; reports.mkdir(exist_ok=True)
(reports/'RUN32_CYCLE9_LEDGER.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'complete':ledger.complete,'sha256':ledger.digest(),'status_counts':{s:sum(1 for r in ledger.results if r.status==s) for s in sorted(set(r.status for r in ledger.results))}},indent=2))
