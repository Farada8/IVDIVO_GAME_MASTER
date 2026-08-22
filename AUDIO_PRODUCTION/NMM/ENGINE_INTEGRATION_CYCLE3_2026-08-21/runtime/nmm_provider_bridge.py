from __future__ import annotations

def build_delegation(source_fingerprint,voice_bindings=None):
 return {'schema':'NMM_PROVIDER_DELEGATION_REQUEST_v1','delegate_to':['provider_preflight.py','controlled_provider_dispatch.py','elevenlabs_adapter.py','alignment_normalizer.py'],'source_fingerprint':source_fingerprint,'voice_bindings':voice_bindings or {},'live_dispatch_authorized':False,'missing':['authenticated_capability_snapshot','explicit_spend_authorization'],'law':'This adapter never stores secrets, calls provider itself, auto-substitutes voices, or turns provider acceptance into take lock.'}
