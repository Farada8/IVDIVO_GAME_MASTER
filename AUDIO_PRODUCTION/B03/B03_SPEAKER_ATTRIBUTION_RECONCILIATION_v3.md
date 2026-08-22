# B03 — THE EMPTY RESCUE — SPEAKER ATTRIBUTION RECONCILIATION v3

**Date:** 2026-08-22  
**Status:** CANDIDATE — exact-repository CI pending  
**Text mutation:** none

## Result

- corrected-v2 base: **518 / 3715**
- fixed Speaker Attribution Engine runtime: **582 assignments**
- clean engine delta over corrected-v2: **81**
- corrected-v2-only proven assignments preserved: **17**
- reconciled candidate: **599 / 3715 = 16.12%**
- residual UNKNOWN: **3116**
- voice map: **NOT AUTHORIZED**

## CH01 FATAL caught before promotion

The generic runtime previously treated the only configured name in `The caller on Nika’s line said` as the reporting subject and therefore assigned Nika to `B03_CH01_S0172` (`The passenger door’s jammed.`).

Independent CH01 production authority is contextually reconciled **142 / 142** and identifies that turn as the real collision caller. The runtime was changed so aliases embedded in prepositional or possessive modifiers cannot win reporting-subject ownership. The regression is now permanent.

After the fix, all **12** CH01 assignments produced by the generic runtime agree with the independently audited CH01 lane; **4** of those are additional same-paragraph confirmations.

## Whole-book reconciliation

On overlap with corrected-v2, there are **18 raw label differences**:

- **17** are role-label granularity differences such as `TECHNICIAN` vs `LOCAL_NETWORK_TECHNICIAN`, `MEDICAL` vs `MEDICAL_CONTROL`, `RESCUER` vs `FIRST_RESCUER`. The corrected-v2 label is preserved in the merge. Role compatibility does not authorize voice-identity merging.
- **1** is substantive: `B03_CH29_S0312` corrected-v2 says `SMITH`, while locked local narration introduces the supervisor, continues `He had not slept either`, and the quote is followed by `he said`. Candidate correction: **SMITH → SUPERVISOR**.

## New delta by method

- `AUTO_SAME_PARAGRAPH_KNOWN_SPEAKER_PROPAGATION`: **48**
- `PRE_DIRECT_TAG`: **11**
- `POST_DIRECT_TAG`: **5**
- `AUTO_PRONOUN_GRAMMATICAL_SUBJECT_TRACKER`: **17**

The two contextual rules remain **B03 project-only** despite passing project validation. Universal promotion requires a second independent book/project replication.

## Next gate

`LOCAL 22/22 PASS` is not enough. This candidate becomes current only after the exact branch bytes pass GitHub Actions and current project state is then written through and re-read from `main`.
