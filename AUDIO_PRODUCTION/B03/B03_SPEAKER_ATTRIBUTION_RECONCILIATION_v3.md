# B03 — THE EMPTY RESCUE — SPEAKER ATTRIBUTION RECONCILIATION v3

**Date:** 2026-08-22  
**Status:** VERIFIED — EXACT REPOSITORY CI PASS  
**Text mutation:** none

## Result

- corrected-v2 base: **518 / 3715**
- fixed Speaker Attribution Engine runtime: **582 assignments**
- clean engine delta over corrected-v2: **81**
- corrected-v2-only proven assignments preserved: **17**
- reconciled current candidate: **599 / 3715 = 16.12%**
- residual UNKNOWN: **3116**
- voice map: **NOT AUTHORIZED**

## Exact-repository verification

GitHub PR **#436** tested the actual PR merge result, not a local copy.

- tested PR head: `016d24c655ba0c710ff01a3dab83aa7acc0a37d9`
- tested merge ref: `bea3fdb86f793988f47d5868ab2bcf396b092a8b`
- workflow run: `32571914177`
- job: `97028433852`
- `pytest`: **22 passed**
- runtime `py_compile`: **PASS**

The status therefore advances from local candidate to `VERIFIED_EXACT_REPO_CI_PASS`. Main write-through/readback remains the merge gate.

## CH01 FATAL caught before promotion

The generic runtime previously treated the only configured name in `The caller on Nika’s line said` as the reporting subject and therefore assigned Nika to `B03_CH01_S0172` (`The passenger door’s jammed.`).

Independent CH01 production authority is contextually reconciled **142 / 142** and identifies that turn as the real collision caller. The runtime was changed so aliases embedded in prepositional or possessive modifiers cannot win reporting-subject ownership. The regression is permanent.

After the fix, all **12** CH01 assignments produced by the generic runtime agree with the independently audited CH01 lane; **4** are additional same-paragraph confirmations.

## Whole-book reconciliation

On overlap with corrected-v2 there are **18 raw label differences**:

- **17** are role-label granularity differences such as `TECHNICIAN` vs `LOCAL_NETWORK_TECHNICIAN`, `MEDICAL` vs `MEDICAL_CONTROL`, `RESCUER` vs `FIRST_RESCUER`. The corrected-v2 label is preserved. Role compatibility does not authorize voice-identity merging.
- **1** is substantive: `B03_CH29_S0312` corrected-v2 says `SMITH`, while locked local narration introduces the supervisor, continues `He had not slept either`, and the quote is followed by `he said`. Verified correction: **SMITH → SUPERVISOR**.

## New delta by method

- `AUTO_SAME_PARAGRAPH_KNOWN_SPEAKER_PROPAGATION`: **48**
- `PRE_DIRECT_TAG`: **11**
- `POST_DIRECT_TAG`: **5**
- `AUTO_PRONOUN_GRAMMATICAL_SUBJECT_TRACKER`: **17**

The two contextual rules remain **B03 project-only**. Universal promotion still requires independent second-book/project replication.

## Next gate

Merge PR #436, re-read the files from `main`, then continue from **599 / 3715**. Do not authorize a scaled voice map from this partial coverage.
