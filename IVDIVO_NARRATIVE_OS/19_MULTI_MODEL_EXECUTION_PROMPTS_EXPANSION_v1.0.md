# IVDIVO — MULTI-MODEL EXECUTION PROMPTS EXPANSION v1.0

**Status:** CANONICAL OPERATIONAL SUPPLEMENT  
**Established:** 2026-08-21  
**Parent:** `IVDIVO_NARRATIVE_OS/14_MULTI_MODEL_HANDOFF_PROMPTS.md` v1.2  
**Purpose:** add 13 non-duplicative specialist prompts to the existing 13-function pack, bringing the total operational prompt coverage to 26 functions without creating a parallel canon.

The parent pack remains controlling for universal resume, agent packet law, integration, red-team, character/relationship, reader/market, reference, world/technical, feedback reconciliation, engine/code, research, handoff and human-evidence firewall.

This supplement covers missing operational failure modes discovered in cross-dialog production.

---

## 14. AUTHORITY / FRESHNESS / FRONTIER AUDITOR

> Restore Founder newest instruction, project-specific authority, current domain router, project execution state, `CURRENT_IVDIVO_SYSTEM_STATE.json`, current Drive mirrors and materially newer GitHub commits. Build a timestamp/version/hash-independent authority table: `SOURCE / STATUS / AUTHORITY LEVEL / VERIFIED FRONTIER / LAST COMPLETED / OPEN GATES / NEXT OBLIGATION / STALE POINTERS`. Flag any lower-authority or aggregate state that would regress work behind a newer verified project frontier. Do not repair story or production yet. Output `CURRENT FRONTIER`, `STALE POINTERS`, `CONFLICTS`, `SAFE REBASE`, and `BLOCKER IF UNRESOLVED`.

PASS when one unambiguous current frontier is resolved or conflict is explicitly fail-closed.

---

## 15. ROUTER / BOOTSTRAP CONSISTENCY LINTER

> Audit all current startup/router/config files referenced by the active domain. For every named path/Drive ID/schema/tool verify existence, current/superseded status and compatibility with the governing version. Detect broken mandatory paths, circular routing, stale PR/branch references, duplicate CURRENT claims and files that instruct a new chat to load an obsolete state. Do not create replacement systems when a current file can be repaired. Output `BROKEN LINK / STALE ROUTE / DUPLICATE AUTHORITY / MISSING BOOT DEPENDENCY / FIX / READBACK TEST`.

FATAL: mandatory bootstrap target missing or routes to a known obsolete frontier.

---

## 16. CHAT-LOCAL ASSET PERSISTENCE / ESCROW AUDITOR

> Apply `IVDIVO_NARRATIVE_OS/17_CHAT_LOCAL_ASSET_PERSISTENCE_AND_ESCROW_v1.0.md`. Inventory future-critical binary/large assets created or received by the active project: WAV, stems, ZIP, image, video, PDF/DOCX, render logs, alignment, provider outputs. Classify each as `CHAT_LOCAL_ONLY / PERSISTENCE_PENDING / DURABLE_WORKING / APPROVED_REFERENCE / UNRECOVERABLE_CHAT_ONLY / SUPERSEDED / REJECTED`. Verify bytes exist in durable Founder-authorized storage, pointer/provenance is registered, and readback works. Do not infer byte availability from filename/hash/metrics alone. If retrieval is impossible, preserve exact provenance and open `ASSET_PERSISTENCE_REQUIRED:<asset_id>`.

PASS requires `BYTES DURABLE + POINTER REGISTERED + PROVENANCE RECORDED + READBACK VERIFIED` for every downstream-critical asset.

---

## 17. CONCURRENT-WRITE / REBASE AUDITOR

> Assume sibling dialogs/models may be writing concurrently. Immediately before every material write, re-read the exact target revision/blob SHA and compare current frontier to the work product being applied. If revision changed, classify the delta: `COMPATIBLE / CONFLICTING / SUPERSEDING / UNRELATED`. Rebase compatible changes; fail closed on authority conflict; never force-overwrite newer state. Verify readback after write. Output `PREWRITE REVISION`, `CONCURRENT DELTA`, `REBASE DECISION`, `WRITE RESULT`, `POSTWRITE READBACK`.

Any blind overwrite of a newer verified sibling state is FATAL operational corruption.

---

## 18. PROMPT / ENGINE SEMANTIC DEDUPE + DRIFT AUDITOR

> Compare current prompts, engines, schemas, routers and repeated rules by function rather than filename. Build semantic families and identify `TRUE UNIQUE / DUPLICATE / EXTENSION / COMPETING ALTERNATIVE / SUPERSEDED / PROJECT-SPECIFIC`. Detect contradictory continuation laws, duplicated authority stacks, dead compatibility wrappers and prompts that differ only in branding. Prefer one controlling mechanism plus bounded supplements. Do not delete historical evidence unless explicitly authorized; instead fix CURRENT routing/status. Output `FAMILY / CONTROLLING ARTIFACT / REDUNDANT ARTIFACTS / MATERIAL UNIQUE DELTAS / DRIFT RISK / CONSOLIDATION ACTION`.

Duplicate wording adds zero evidence weight.

---

## 19. CROSS-AI INDEPENDENCE / PROVENANCE AUDITOR

> For every external-model finding used as evidence, verify exact source material/version, question, authority packet, independence condition and provenance. Detect copied summaries, model outputs that saw prior verdicts, shared unsupported assumptions and recommendations counted as multiple votes. Cluster findings into independent evidence families. Separate `DIAGNOSIS CONFIRMED / DIAGNOSIS PLAUSIBLE / UNSUPPORTED / NON-PARITY / DERIVED DUPLICATE`. No model may self-promote its recommendation to CURRENT.

Output evidence-family table and adjusted confidence without numeric pseudo-certainty.

---

## 20. PROJECT-STATE COMPLETENESS / NEXT-ACTION RESOLVER

> Audit the active project execution state as a resume pointer, not canon. Require enough fields to recover: project/branch/source/version/hash where applicable; story status; delivery mode; last completed artifact; open gates; current blocker; required evidence; prohibited actions; next action; working downstream artifacts; persistence status for critical assets. Determine whether the declared next action is actually `AUTHORIZED / DEPENDENCY-VALID / SAFE / ZERO-COST OR PAID / REVERSIBLE / TOOL-EXECUTABLE-HERE`. Missing material flags fail closed rather than guessing. Output one exact `HIGHEST UNBLOCKED NEXT OBLIGATION` or exact blocker.

Never regress from real post-render evidence to pre-render canary because aggregate state is stale.

---

## 21. STORY-FIRST STARVATION / FACTORY-DRIFT GUARD

> Audit whether engine, prompt, audio, automation, market or franchise work is starving the active story/product. Apply IVDIVO priority: `STORY CAUSALITY -> CHARACTER TRUTH -> EMOTIONAL IMPACT -> READER/LISTENER ENGAGEMENT -> CONTINUITY -> WORLD LOGIC -> GENRE -> MARKET -> FRANCHISE`. Identify work that is technically sophisticated but not downstream of a current story/product need. Classify `ESSENTIAL / SUPPORTING / PREMATURE / DUPLICATIVE / FACTORY-DRIFT`. Stop meta-engine expansion when the active story/product has a more valuable unblocked obligation.

Output `CURRENT PRODUCT GOAL`, `WHAT ACTUALLY MOVES IT`, `WHAT TO FREEZE`, `NEXT STORY/PRODUCT OBLIGATION`.

---

## 22. AUDIO PERCEPTUAL / COMMERCIAL QUALITY GATE

> Evaluate actual supplied audio only; do not infer listening quality from manifests. Audit acting/prosody, reaction timing, body presence, spatial blocking, intimacy, Foley, ambience, music dramaturgy, clue intelligibility, transitions, foreground/background movement, dynamics, mono/mobile translation, listener comprehension and desire to continue. Compare against appropriate premium references at matched playback loudness where reference audio is lawfully available. Separate `TECHNICAL QC` from `PERCEPTUAL QUALITY` and from `COMMERCIAL VALIDATION`. If no audio bytes are accessible, return `AUDIO_BYTES_REQUIRED` rather than simulated listening.

For romantic mystery specifically test whether the production feels like a lived dramatic scene rather than audiobook-with-effects.

---

## 23. LIVE PROVIDER SPEND / CANARY ECONOMICS GATE

> Before any paid API/provider execution, resolve exact evidence needed, cheapest decisive call set, current credits/cost exposure, reuseable evidence and stop conditions. Use the current provider canary/casting cascade. Never purchase a full manifest merely because it exists. Separate `TECHNICAL CANARY / FAIR COMPARISON / CASTING EVIDENCE / HARD PILOT / SCALE RENDER`. After each paid stage, decide whether evidence justifies the next spend. Output `CALLS / PURPOSE / MAX SPEND EXPOSURE / PASS EVIDENCE / STOP CONDITION / NEXT PAID STAGE`.

No voice lock from dry-run or technical canary alone.

---

## 24. RELEASE PROVENANCE / REPRODUCIBILITY GATE

> Audit a candidate release or master for reproducibility and provenance. Verify source/version/hash, build ID, accepted voice bindings, assets/stems, alignment, timeline, mix/master chain, QC, manual review, exact released bytes/hash, and all required rights/permissions declarations available to the project. Confirm no DRY_RUN or synthetic placeholder is promoted to release. Check that selective repair can trace descendants back to source assets. Output `REPRODUCIBLE / PARTIALLY REPRODUCIBLE / NON-REPRODUCIBLE`, missing dependencies, release blockers and archival requirements.

A filename called FINAL is not release evidence.

---

## 25. SECRET / PRIVACY / CONFIDENTIALITY AUDITOR

> Scan only project-controlled prompts, manifests, logs, GitHub/Drive text artifacts and handoff records for secrets or sensitive provider credentials. Detect API keys, auth tokens, passwords, cookies, private headers, accidental personal identifiers unnecessary for production and provider secrets embedded in examples. Do not echo secret values into the report; redact and identify location/type. Verify provider credentials are local/environment-only and production outputs do not leak them. Output `LOCATION / SECRET CLASS / SEVERITY / ROTATION OR REMOVAL ACTION / PREVENTION TEST`.

Never upload a discovered secret to another system for analysis.

---

## 26. DISASTER-RESUME / RECOVERY DRILL

> Simulate loss of the current chat, one stale Drive pointer and one unavailable binary asset without inventing missing information. Starting only from persisted current routers/state, determine whether another model can recover the project, distinguish current from superseded artifacts, find exact blockers and continue safely. Test the paths for `SOURCE MISSING`, `CHAT-LOCAL ASSET`, `STALE POINTER`, `CONCURRENT WRITE`, `PROVIDER EVIDENCE MISSING`, and `ROLLBACK REQUIRED`. For each return `RECOVERABLE / PARTIALLY RECOVERABLE / BLOCKED`, exact evidence path, repair and prevention action.

PASS means the studio can resume without Founder acting as memory, cloud storage or cross-chat courier except where an actual external/tool boundary requires Founder action.

---

## EXECUTION LAW FOR PROMPTS 14–26

These prompts are not decorative templates. When the Founder requests system audit/continuation, run only the subset capable of changing the current decision, or run all 13 for a deliberate whole-system hardening pass.

For each executed prompt persist:
- prompt number/function;
- sources inspected;
- findings by severity;
- fixes actually applied;
- verification/readback;
- unresolved blocker;
- reusable learning candidate if materially new.

Do not mark a prompt `PASS` merely because a document exists.

**TOTAL OPERATIONAL PROMPT FUNCTIONS AFTER THIS SUPPLEMENT: 26.**
