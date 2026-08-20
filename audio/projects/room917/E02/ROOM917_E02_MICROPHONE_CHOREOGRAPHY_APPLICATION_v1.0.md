# ROOM 917 E02 — MICROPHONE CHOREOGRAPHY APPLICATION v1.0

**Episode:** E02 — LENI-BIRD  
**Status:** WORKING PRODUCTION OVERLAY / BELOW LOCKED STORY CANON  
**Source authority:** ROOM 917 — PHASE D — Episodes 01–03 — v1.0  
**Universal system:** IVDIVO Microphone Choreography / Virtual Radio Stage Engine v1.0

## Production decision
E02 is no longer staged as static close-mic dialogue with post-pan. It uses `HYBRID_STAGE`: performance behavior is generated/recorded truthfully first, then continuous actor geometry is imposed relative to the listener/microphone and coupled to Foley/world sound.

No spoken text or story fact is changed.

## Scene 1 — Switchboard alcove, morning
- Elena works close to the evidence/board position, Mina functions as independent witness, Julian physically enters through the alcove door carrying two coffees.
- Julian's coffee approach is treated as a real social action, then spatially freezes when Elena says, “You knew the fourth note.”
- Mina's attempt to leave for the office becomes a short withdrawal trajectory; Elena's “Stay. You are the independent witness.” stops that movement and re-establishes witness geometry.
- Elena's sealed-copy handoff is an object-linked movement, not an arbitrary pan event.
- No near-ear intimacy is authorized in E02.

## Scene 2 — Elena's hotel room
- The space is smaller and acoustically closer.
- Elena owns the cassette/deck position; Mina is supportive but not crowding her; Julian starts nearer the room threshold and only moves farther in when he accepts the evidence demonstration.
- “Headphones on. Nobody speaks until I stop the deck.” creates a static listening tableau: no decorative actor movement over the cassette evidence.
- Cate-on-cassette remains DEVICE-MEDIATED audio from the portable deck; it is not spatialized as a live character standing in Elena's room.
- Elena's stop/switch/sample actions are coupled to deck Foley.

## Scene 3 — Switchboard + front desk
This scene gets the strongest choreography because the script already contains a physical verification path.

- Listener POV remains near the old switchboard.
- Mina physically leaves the alcove, crosses the lobby to reception, dials the modern hotel number, and answers the distant front-desk phone.
- Her voice must genuinely recede/change depth rather than merely pan left/right.
- After “I'm hanging up,” Mina returns toward the alcove while Elena and Julian continue the local-circuit test.
- She must be physically back near the board by “Is that a seven?” because she is now visually confirming the filed-off hidden terminal.
- Elena remains physically tied to the probe/contacts/terminal path.
- Julian stays near the test until the hidden terminal appears; only then does he close distance and physically assert the stop/boundary.

## Spatial laws for this episode
- `POSITION != PAN`.
- Body direction and head direction are independent.
- Every move has a story/action cause.
- Voice trajectory and footstep/Foley trajectory must describe the same body.
- No absolute production timestamps before accepted voice alignment.
- No critical clue can exist only in stereo/binaural placement.
- Phone/mono playback preserves all dialogue and causal meaning.
- No unearned near-ear romantic treatment.

## Current engine integration
The uploaded IVDIVO ENGINE v11 has been patched to `IVDIVO-ENGINE/6.1.0-microphone-choreography`:
- typed capture mode/topology/polar-pattern models;
- per-scene `microphone_choreography` in EpisodeManifest;
- score compiler support;
- fail-closed semantic plan compiler;
- ROOM 917 E02 three-scene production overlay;
- regression tests.

The patch also repaired one pre-existing normalizer provenance defect in the supplied v11 baseline: attribution connectors such as `then finally answered` were being silently dropped. They are now preserved as non-spoken metadata.

**Regression result:** `236 passed, 0 failed`.

## Next production handoff
The choreography plan must now feed the E02 Audio Staging / Director Score / Foley Score / Spatial Automation manifests before ElevenLabs live rendering and before final music/mix decisions.