from __future__ import annotations
REQUIRED=['SOURCE_FINGERPRINT','COMPILER_MUTATION_PROOFS','CANONICAL_ASSET_INGEST','AUTHENTICATED_PROVIDER_SNAPSHOT','VOICE_BINDINGS','REAL_CAST_AUDITIONS','HARD_PILOT_AUDIO','REAL_ALIGNMENT','DEVICE_QC','BLIND_HUMAN','SPECIALIST_HOLDS','MEASURED_ECONOMICS']
def assess(evidence):
 open_items=[k for k in REQUIRED if not evidence.get(k)]
 deterministic={'SOURCE_FINGERPRINT','COMPILER_MUTATION_PROOFS','CANONICAL_ASSET_INGEST'}
 return {'open':open_items,'deterministic_closed':all(evidence.get(k) for k in deterministic),'release':'NO_GO' if open_items else 'GO_FOR_FOUNDER_RELEASE_DECISION','law':'Missing proof remains open; classes do not substitute for one another.'}
