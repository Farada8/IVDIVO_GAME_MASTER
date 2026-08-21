# WAVE 2 SYNTHESIS + RELEASE DELTA

## Executive finding
Wave 2 did not discover a need for another architecture redesign. It narrowed the v1.0 release problem to evidence and integration.

### What is now demonstrated
1. LESSON ZERO canary identity is deterministic: 3 requests, 36 units, 2163 characters, fixed hashes.
2. Dependency-scoped invalidation works as a contract: voice changes affect all canary speech; pronunciation changes only the blocks that contain controlled terms.
3. Resume/idempotency and selective rerender have explicit fail-closed behavior.
4. Both observed ElevenLabs alignment families have one required normalized boundary before timeline.
5. Provider-specific fields can remain outside domain objects.
6. Silent reactions, pause function, reply latency and microphone choreography can be represented without changing the manuscript or spoken-unit accounting.
7. Machine QC and human performance judgment have a clear responsibility boundary.

### What remains genuinely open
A. Authenticated voice inventory + three provisional LESSON ZERO bindings.
B. Pronunciation audition for Ифа / Контакт.
C. Exactly three live canary requests and durable raw provenance.
D. Real alignment → normalized alignment → sample-accurate canary timeline.
E. 8–10 minute/long-form voice fatigue evidence before final voice lock.
F. Actual production CLI clean-build/resume/invalidation regression, not harness-only proof.
G. Human listening and economic measurements before PRODUCTION_READY v1.0.

## Earliest-cause conclusion
The next bottleneck is not AutoMix, music, or generic architecture. It is LIVE CAST/PERFORMANCE EVIDENCE. Any downstream artistic mix work before those three voices and their real timing exist is speculative.

## Promotion decisions
ACCEPT:
- normalized alignment boundary for TTD/TTS;
- ambiguous-provider-response quarantine;
- scoped invalidation by binding/pronunciation version;
- block-level selective rerender;
- silent reaction anchors not counted as spoken text;
- functional pause taxonomy;
- reply-latency state plan;
- microphone choreography contract;
- eight performance hard-fail categories.

ACCEPT_WITH_MODIFICATION:
- one-command orchestration: harness contract accepted, production CLI evidence still required;
- voice/model drift: deterministic binding guard accepted, current provider capability evidence still required.

HOLD_FOR_TEST:
- all voice locks;
- pronunciation locks;
- real timeline;
- fatigue/AI-tell judgments;
- commercial/premium mix claims;
- cost-per-accepted-minute;
- final v1.0 release.

## New release status
ENGINE ARCHITECTURE: GO
SECOND-PROJECT DRY PORTABILITY: GO
DETERMINISTIC CONTRACT REGRESSION: GO
LIVE SECOND-PROJECT PORTABILITY: HOLD
HUMAN PERFORMANCE GATE: HOLD
PRODUCTION CLI INTEGRATION GATE: PARTIAL
V1.0 RELEASE: HOLD

Exact next external action:
authenticated provider voice inventory -> provisional Narrator/Ethan/Aoife candidates -> pronunciation/direction auditions -> pair gate -> exact 3-request live canary.

Exact next internal action that can proceed without provider spend:
port the Wave2 harness rules into the actual production modules/CI and prepare golden fixtures for Wave3.
