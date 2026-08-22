import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from cycle4_business_engine import *

tests=[]
def T(name,cond): tests.append((name,bool(cond)))
T('authority',authority_score('OFFICIAL_PRIMARY')>authority_score('TRUSTED_SECONDARY'))
T('correlation',len(correlation_dedupe([{'correlation_group':'A','source_authority':'TRUSTED_SECONDARY'},{'correlation_group':'A','source_authority':'OFFICIAL_PRIMARY'}]))==1)
T('workload_null_wtp',buyer_workload('b','w')['willingness_to_pay'] is None)
T('micro_market_hold',micro_market_gate({'buyer_segment':'','buyer_workload':'x','offer':'y','manual_first_deliverable':'z','evidence_grade':'E2'})['verdict']=='HOLD')
T('fatal_rank',rank_fatal_assumptions([{'id':'a','kill_power':1,'uncertainty':1,'testability':1},{'id':'b','kill_power':.2,'uncertainty':1,'testability':1}])[0]['id']=='a')
T('zero_cash_experiment',choose_no_outreach_experiment([{'id':'paid','founder_cash_eur':10,'requires_buyer_contact':False,'decision_value':10,'flip_probability':1,'time_hours':1},{'id':'free','founder_cash_eur':0,'requires_buyer_contact':False,'decision_value':5,'flip_probability':1,'time_hours':1}])['id']=='free')
T('fresh',decay(10,30)=='FRESH')
T('revalidate',decay(40,30)=='REVALIDATE')
T('stale',decay(70,30)=='STALE')
T('seven_domains_cash',seven_domains_gate({'buyer_segment':'b','why_now':{},'manual_first_deliverable':'d','founder_cash_pre_proof_eur':1,'access_path':'x'})['verdict']=='RESHAPE_OR_KILL')
T('seven_domains_pass',seven_domains_gate({'buyer_segment':'b','why_now':{'x':1},'manual_first_deliverable':'d','founder_cash_pre_proof_eur':0,'access_path':'x'})['verdict']=='PASS_TO_TEST')
T('recurring',recurring_value_gate(True,True)=='PASS')
T('recurring_fail',recurring_value_gate(True,False)=='NO_RETAINER_YET')
T('power_early',power_gate(False,True,True)=='TOO_EARLY')
T('acq_null',acquisition_stress(None,None,None)['verdict']=='HOLD_NULL_INPUT')
T('graduation',graduation('E2+',0,False)=='EXPLORE')
T('change_forced',classify_change({'claim':'NIS2 compliance obligation','title':'NIS2'})['motivation']=='FORCED_ACTION')
T('dedupe',len(dedupe_opportunities([{'buyer_segment':'A','buyer_workload':'B','offer':'C'},{'buyer_segment':'A','buyer_workload':'B','offer':'C'}]))==1)
assert len(tests)==18 and all(v for _,v in tests), tests
print('18/18 PASS')
