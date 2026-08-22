from __future__ import annotations
import re
PROJECT_TERMS=['NINETY MISSING MINUTES','NMM','Isla','Leo','Vivian','Aaron Bell','Northbridge','extra whistle']
def strip_project_leakage(text):
 out=str(text)
 for t in PROJECT_TERMS: out=re.sub(re.escape(t),'[PROJECT]',out,flags=re.I)
 return out
def record(project_id,unit_id,defect_class,severity,symptom,root_cause,repair_action,result,human_result='NOT_TESTED',evidence=None):
 return {'project_id':project_id,'unit_id':unit_id,'defect_class':defect_class,'severity':severity,'symptom':symptom,'root_cause':root_cause,'repair_action':repair_action,'result':result,'human_result':human_result,'evidence':evidence or []}
def universal_candidate(rec,cross_project_count=1):
 cleaned={k:(strip_project_leakage(v) if isinstance(v,str) else v) for k,v in rec.items()}
 cleaned['promotion_status']='DISCOVERY_ONLY' if cross_project_count<2 else 'CANDIDATE_FOR_REVIEW'
 cleaned['auto_promote']=False; cleaned['cross_project_count']=cross_project_count
 return cleaned
