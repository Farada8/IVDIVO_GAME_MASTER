# CAST CANDIDATE READINESS CONTRACT v1

Status: WORKING engineering contract.

## Scope
Bound the transition from a validated real provider inventory to provisional LESSON ZERO canary candidates for exactly `NARRATOR / ETHAN / AOIFE`.

## Invariants
- candidate voice IDs must exist in the current validated provider inventory;
- selected model ID must be explicitly TTS-capable in that inventory;
- missing role -> HOLD;
- unknown voice ID -> FAIL;
- no automatic voice substitution;
- no machine voice lock;
- candidate binding hash is `sha256(role_id + ':' + voice_id)` for later Human Review receipt binding.

## Required real-audio evidence families before lock eligibility
- PRONUNCIATION: canonical terms `Ифа`, `Контакт`;
- MULTI_STATE: at minimum `NATURAL_RESTRAINED`, `DIRECTED_CHANGE`;
- PAIR: ETHAN + AOIFE;
- FATIGUE: minimum 480 seconds, target ceiling 600 seconds for the bounded audition;
- PERFORMANCE: human-heard performance review.

These families must later be satisfied by trusted human evidence using the existing Studio Evidence / Human Review trust path. Planning booleans or synthetic fixtures cannot satisfy them.

## Output ceiling
`READY_FOR_REAL_AUDITION` means candidate IDs are structurally bound and the audition manifest is deterministic. It does NOT authorize paid dispatch, voice lock or production release.
