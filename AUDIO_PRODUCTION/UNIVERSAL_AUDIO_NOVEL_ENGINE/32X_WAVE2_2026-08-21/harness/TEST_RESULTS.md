# WAVE 2 DETERMINISTIC HARNESS — TEST RESULTS

Command: `python -m unittest -v test_wave2_contract_harness.py`
Result: 21 tests, 21 PASS, 0 FAIL, 0 ERROR.

Covered:
- dry canary identity / 36 units
- deterministic canonical hash
- resume reuse
- voice-binding invalidation
- pronunciation-scoped invalidation
- block-level selective rerender
- provider-neutral domain object
- 401/429 error classification
- bounded retry + ambiguous-attempt quarantine
- PCM S16LE 48k → WAV wrapping
- TTD voice_segments normalization
- TTS character-alignment normalization
- missing-alignment fail closed
- voice binding drift
- dialogue/music/SFX media separation
- second-provider normalized mock
- silent reaction zero-spoken-unit behavior
- functional pause taxonomy
- non-uniform reply latency
- microphone choreography state set
- eight performance hard-fail categories

Important boundary: this harness proves deterministic contracts. It does NOT prove the production CLI is wired to these rules, does NOT perform an ElevenLabs call, and does NOT substitute for human listening.
