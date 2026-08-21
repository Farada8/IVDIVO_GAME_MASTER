"""NMM adapter to the universal authenticated provider snapshot gate. No auth logic duplicated here."""
from __future__ import annotations

def credential_state(env:dict)->dict:
    present=bool(env.get('ELEVENLABS_API_KEY'))
    return {'credential_present':present,'status':'READY_ACQUIRE_AUTHENTICATED_SNAPSHOT' if present else 'HOLD_NO_CREDENTIAL','secret_persisted':False}

def admit_verified_snapshot(validator_result:dict)->dict:
    if validator_result.get('status')!='PASS' or validator_result.get('verified') is not True:
        return {'status':'FAIL_CLOSED_UNIVERSAL_PROVIDER_CONTRACT'}
    return {'status':'PROVIDER_METADATA_ADMISSIBLE','snapshot_hash':validator_result.get('snapshot_hash'),'voice_lock':False,'take_lock':False}
