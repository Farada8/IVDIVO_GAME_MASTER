from __future__ import annotations
import hashlib

def make_protocol(protocol_id,stimuli,question_ids,threshold):
 return {'schema':'NMM_HUMAN_PROTOCOL_v1','protocol_id':protocol_id,'stimulus_hashes':[hashlib.sha256(s.encode()).hexdigest() for s in stimuli],'question_ids':question_ids,'threshold_predeclared':threshold,'status':'READY_NOT_RUN','raw_answers':[]}
def score(protocol,answers):
 if protocol.get('status')=='READY_NOT_RUN' and not answers: return {'result':'NOT_RUN','pass_claim_allowed':False}
 if not answers: raise ValueError('NO_HUMAN_ANSWERS')
 correct=sum(1 for a in answers if a.get('correct') is True); total=len(answers); rate=correct/total
 return {'result':'PASS' if rate>=protocol['threshold_predeclared'] else 'FAIL','correct':correct,'total':total,'rate':rate,'pass_claim_allowed':True}
