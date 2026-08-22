# B03 — SPEAKER ATTRIBUTION RECONCILIATION v3

**Status:** CANDIDATE — exact-repo CI + state write-through pending  
**Date:** 2026-08-22

## Result

- Base corrected-v2: **518 / 3715**.
- Fixed Speaker Attribution Engine v1.3 runtime: **582 assignments**.
- Clean new delta over corrected-v2: **81**.
- Base-only proven assignments preserved: **17**.
- Reconciled candidate: **599 / 3715 = 16.12%**; UNKNOWN **3116**.
- Story/prose byte changes: **0**.
- Voice map: **NOT AUTHORIZED**.

## FATAL regression caught and repaired

Generic runtime previously misread `The caller on Nika’s line said` as if `Nika` were the reporting subject. Independent CH01 142/142 authority proved the speaker is the real collision caller. Runtime now rejects aliases inside prepositional/possessive modifiers as reporting subjects. Local repo-layout regression is **22/22 PASS**.

## Conflict reconciliation

- Raw overlaps with different labels: **18**.
- **17** are role-granularity differences only; base labels remain preserved in the merged authority.
- One substantive correction: `B03_CH29_S0312` **SMITH → SUPERVISOR**. Locked narration introduces the supervisor, continues `He had not slept either`, then the quote is followed by `he said`.

## New delta

- `AUTO_SAME_PARAGRAPH_KNOWN_SPEAKER_PROPAGATION`: 48
- `PRE_DIRECT_TAG`: 11
- `POST_DIRECT_TAG`: 5
- `AUTO_PRONOUN_GRAMMATICAL_SUBJECT_TRACKER`: 17

Project-only rules remain project-scoped until independent second-book replication. Coverage is not a promotion criterion.

## Voice identity boundary

Role-family or role-granularity compatibility is not proof that two labels are the same person. `TECHNICIAN`, `RELAY_TECHNICIAN` and `LOCAL_NETWORK_TECHNICIAN`, for example, may be semantically compatible role labels without authorizing one shared voice identity. Voice identity merge requires separate textual/canon evidence.
