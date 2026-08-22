# DURABLE RECEIPT — ARTIFACT PLACEMENT + THREAD TOPIC CONTINUITY

Date: 2026-08-22
Status: RECORDED / NO GLOBAL SELF-IMPROVEMENT PROMOTION
Parent authority: SELF_IMPROVEMENT_META_ENGINE_V2_VERIFIED_CURRENT

## 1. Artifact Placement deployment boundary

Merged PR #449: `Self-Improvement: define ChatGPT connector deployment boundary and live readback capture`.
Merge commit: `c64790fdd892fd352b8a4e8ce44a3ba39e236683`.
Exact-head CI: 15/15 SUCCESS.

Canonical law:
`LOCAL_RUNTIME_GUARD != CHATGPT_PLATFORM_MIDDLEWARE`.

Two enforcement surfaces are now explicit:
- LOCAL_RUNTIME_ENFORCEMENT: automatic only for work routed through the local Personal AI runtime.
- CHAT_CONNECTOR_ENFORCEMENT: `SYNCHRONOUS_OPERATIONAL_READBACK_GATE`, not platform middleware.

Required Chat Connector sequence:
`WRITE -> PROVIDER READBACK -> CANONICAL INDEX/CURRENT READBACK -> CONNECTOR PLACEMENT CAPTURE -> COMPLETION CLAIM`.

Live connector ledger remains honest:
- `real_live_event_count = 0`
- no synthetic/replay/test event may satisfy the final live-evidence gate.

Issue #444 is closed as engineering-resolved. Parent Issue #356 remains open for the real future connector failure gate.

## 2. Thread Topic Continuity real pilot

Merged PR #455 recorded `TTG-REAL-002`.
Merge commit: `60cd9b3635157ba1af576a267afc12e00b4e7f69`.

Current real pilot counters:
- real continuation events: 2/3
- distinct project types: 1/2
- false project switches: 0
- healthy explicit-switch controls: 0/2
- side-query-return controls: 0/1

No promotion is authorized. The remaining continuation event must occur naturally in another project type; explicit-switch and side-query controls must also occur naturally with zero false blocking/switching.

## 3. Two-level routing convergence

Merged PR #464: `Self-Improvement: fresh-main Thread + Frontier two-level routing convergence`.
Merge commit: `4e21e26f2bcb2424a1582a306fccb839d6febe5c`.

Architecture:
`THREAD_TOPIC_LOCK -> PROJECT_FRONTIER_LOCK -> EXECUTION`.

Canonical routing laws:
- Thread Topic Guard is the sole project-switch authority.
- Active Frontier Guard has no project-switch authority.
- `NEW_PROJECT + OLD_PROJECT_GATE = ROUTING_CORRUPTION`.
- after a project switch, the target-project frontier must be restored before execution;
- sibling/supporting discovery cannot replace the active next gate;
- required dependency is bounded by a return token;
- unknown/conflicting frontier relation fails closed.

Validation on the clean PR #464 head passed both exact-head workflows:
- Self-Improvement Thread Topic Continuity Guard: SUCCESS
- Self-Improvement Thread + Frontier Two-Level Routing: SUCCESS

Supersession:
- PR #460 closed NOT MERGED — mechanical predecessor only.
- PR #278 closed NOT MERGED — content predecessor; useful defect provenance retained, duplicated project-switch behavior rejected.

## 4. GitHub authority updates

Post-merge two-level state update commits:
- `c190f0a0c6348de571c0b4ac0c97bd5e5e62e4ad`
- `ee130dea487c8e5aeafe770461e516554ee6002f`

Current authority remains:
`SELF_IMPROVEMENT_META_ENGINE_V2_VERIFIED_CURRENT`.
No global v3 promotion has been made.

## 5. Drive authority pointer

Canonical Drive authority document:
`CURRENT — IVDIVO SELF-IMPROVEMENT AUTHORITY`
Document ID: `1xare6Mz0FG6fDsY5QWx-hirI9D4A4BPtSG6vXY4sPa0`

Existing verified two-level marker:
`SI-THREAD-TOPIC-CONTINUITY-TWO-LEVEL-ROUTING-MERGED-PR464-20260822`

This receipt must be mirrored to that same Drive authority document; no duplicate authority document should be created.

## 6. Next honest gates

Artifact Placement:
- wait for a future real CHAT_CONNECTOR provider-backed placement/resource-type failure;
- catch it through provider/index readback before any false completion claim;
- persist it in the live ledger;
- independently confirm provider origin/readback.

Thread Topic Continuity:
- one more naturally occurring continuation event from another project type;
- two healthy explicit-switch controls;
- one side-query-return control;
- zero false project switches.

Do not manufacture evidence for either gate.

Readback marker:
`SI-DURABLE-RECEIPT-PLACEMENT-CONTINUITY-20260822`
