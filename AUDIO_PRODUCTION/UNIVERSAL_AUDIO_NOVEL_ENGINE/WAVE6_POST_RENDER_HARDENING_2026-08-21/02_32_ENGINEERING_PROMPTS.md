# WAVE6 — 32 SEQUENTIAL ENGINEERING PROMPTS

These are executable run cards, not brainstorming prompts. Each prompt must end PASS / HOLD / BLOCKED from evidence. No human/provider/live-audio result may be fabricated.

## A — Freshness, convergence, authority

### W6-01 — Fresh-main state scan
Read current `main` head, recent commits and active audio runtime. Identify changes newer than the prior Wave5 state. Do not assume a branch is fresh because its name says fresh. Output: exact freshness boundary.

### W6-02 — Google Drive parallel-state scan
Read current Workstate and recent Audio/Self-Improvement folders. Identify Drive mirrors that are newer, duplicate, stale or missing relative to GitHub. Output: mirror delta map.

### W6-03 — ROOM917 post-render architecture-vs-implementation audit
Compare architecture, README, contract bundle and executable modules. Find claims that are weaker or stronger than implementation. Output: FATAL/MAJOR/MEDIUM engineering defects only.

### W6-04 — Wave5/Studio Evidence/production-control dedupe
Map what is already canonical on current main. Explicitly forbid new provider/alignment/director/economics duplicates. Output: KEEP / EXTEND / DO-NOT-DUPLICATE matrix.

### W6-05 — SI-0009 reconciliation
Read SI-0009 and its project evidence. Decide what can be hardened without colliding with another reserved self-improvement ID or prematurely promoting domain authority.

## B — Machine contracts and patch authority

### W6-06 — Universal contract root
Create a project-neutral post-render contract family under `audio/studio/contracts/post_render`. No project story data.

### W6-07 — Canonical interval contract
Normalize new output to `start_seconds/end_seconds`; legacy `start_s/end_s` may be read only. Reject non-finite/negative/reversed intervals.

### W6-08 — Accepted timing authority contract
Absolute timing may advance only from `ACCEPTED_ALIGNMENT` or `LIVE_TIMELINE`. Directorial inference remains semantic.

### W6-09 — Protected timing completeness gate
If any declared protected silence/pause lacks accepted/live timing, auto-patch authorization must HOLD.

### W6-10 — Classifier candidate vs patch authorization
Demote machine classifier output to candidate/nomination semantics. Add independent authorization requiring stronger evidence.

### W6-11 — Source master pre-touch identity
Bind every authorized patch to exact source master SHA-256; mismatch must block before accepted lineage advances.

### W6-12 — Asset provenance binding
Require asset ID + SHA-256 + rights state + 48 kHz + mono/stereo declaration + explicit gain. Path alone is insufficient.

### W6-13 — Headroom / no-silent-clipping contract
Create a pre-render headroom gate. Machine renderer may not hide a failed gain decision by clipping output and declaring PASS.

### W6-14 — Single bed-domain containment
A patch interval crossing multiple required bed domains must HOLD unless a higher explicit project contract decomposes it.

### W6-15 — Deterministic authorization hash
Hash master identity + interval + asset identity + gain + bed domain + lineage hash + headroom evidence. Same evidence must produce same authorization identity.

### W6-16 — Restart-safe patch ledger
Persist patch lifecycle: PLANNED → AUTHORIZED → RENDERED → REGRESSION_PASS → HUMAN_PASS. Prevent silent identity drift/repaid/repeated work and terminal mutation.

## C — Evidence semantics and post-render QC

### W6-17 — Artifact evidence verifier
Replace `file exists == pass` with verified bytes/hash/schema/status. Stale or semantic-HOLD artifacts do not advance the router.

### W6-18 — Project-neutral byte regression
Remove universal dependency on any ROOM917 Scene3 timestamp. Feed authorized/protected/changed ranges from project overlay data.

### W6-19 — Human listen evidence contract
Require artifact hash + reviewer type + reviewed-at + PASS/FAIL/HOLD. Machine cannot synthesize human P003B evidence.

### W6-20 — Self-Improvement telemetry bridge
Emit mechanism-level event with provider spend, provider requests, human minutes, rework cycles, accepted minutes, avoided rerender, false positives and manual overrides when measured.

### W6-21 — Project story-leakage firewall
Reject project names/characters/cues/assets from universal mechanism payloads when declared forbidden by source project policy.

### W6-22 — Two-project promotion gate
One project or synthetic duplicate evidence cannot promote domain law. Require two independent real locked projects with human listen and regression PASS.

### W6-23 — PCM clipping detector
Analyze canonical candidate WAV and fail/hold on near/full-scale clipping samples. No auto-repair.

### W6-24 — Patch-boundary seam detector
Flag abrupt sample discontinuities at authorized range start/end. Advisory/HOLD only; no machine artistic substitution.

## D — Adversarial execution

### W6-25 — Unresolved protected-pause attack
Construct a lineage with a semantic protected pause but no accepted timing. Attempt repair elsewhere. Expected: authorization HOLD.

### W6-26 — Master hash drift attack
Nominate a valid-looking patch but supply different master bytes/hash. Expected: pre-touch HOLD.

### W6-27 — Asset provenance/gain attack
Test missing rights, wrong sample rate and positive gain. Expected: fail closed, no substitution.

### W6-28 — Unauthorized/protected byte-change attack
Feed changed ranges outside authorization and within protected ranges. Expected: regression FAIL.

### W6-29 — Synthetic promotion attack
Supply perfect synthetic test evidence as a second “project.” Expected: domain promotion HOLD.

### W6-30 — Universal runtime leakage attack
Static-scan universal post-render runtime for ROOM917/Lesson Zero/NMM/BODYGUARD story/project tokens. Expected: zero project leakage.

## E — Integration and next frontier

### W6-31 — Full current-branch CI + Red Team
Run canonical Audio Studio test discovery, not only new tests. Any pre-existing or new regression remains visible. Inspect logs and repair rather than weakening tests.

### W6-32 — Synthesis / exact next empirical frontier
Integrate findings, statuses, unresolved evidence and self-improvement implications. Produce one shortest path to domain promotion and Audio Novel Engine v1 without generating unnecessary architecture.
