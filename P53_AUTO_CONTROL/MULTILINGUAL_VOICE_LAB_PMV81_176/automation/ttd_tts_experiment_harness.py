#!/usr/bin/env python3
import json,hashlib

def build(texts,voices):
    if len(texts)!=len(voices): raise ValueError('texts/voices length mismatch')
    joined='\n'.join(texts)
    return {'artifact':'TTD_TTS_AB_DRY_MANIFEST','status':'DRY_RUN_NO_NETWORK','text_sha256':hashlib.sha256(joined.encode()).hexdigest(),'ttd_request':{'endpoint':'/v1/text-to-dialogue/with-timestamps','model_id':'eleven_v3','inputs':[{'text':t,'voice_id':v} for t,v in zip(texts,voices)]},'isolated_tts_requests':[{'endpoint':f'/v1/text-to-speech/{v}/with-timestamps','model_id':'eleven_v3','text':t} for t,v in zip(texts,voices)],'comparison_fields':['exact_text_fidelity','duration','turn_latency','chemistry_blind_score','regeneration_cost','editability','alignment_quality']}
if __name__=='__main__':
    texts=['Если я скажу «вправо», вы двигаетесь.','Сначала двигаюсь, потом спорю.']; voices=['VOICE_NAOMI_PLACEHOLDER','VOICE_ELI_PLACEHOLDER']
    print(json.dumps(build(texts,voices),ensure_ascii=False,indent=2))
