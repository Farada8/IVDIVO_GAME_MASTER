# IVDIVO — FULL CHAT TRANSCRIPT RECOVERY + INGESTION PROTOCOL v1.0

**Status:** CANONICAL OPERATIONAL PROTOCOL — FOUNDER DIRECTIVE  
**Established:** 2026-08-21  
**Scope:** all IVDIVO writing, audio, visual, research, tooling and self-improvement workflows when a prior AI conversation is copied/exported/pasted into a new conversation, including generated big-paste attachments.  
**Parents:** Founder newest instruction -> current project/book authority -> `13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md` -> `18_SELF_IMPROVEMENT_META_ENGINE_v2.0.md`.  
**Purpose:** recover material work from an abruptly ended conversation without making the Founder manually reconstruct, classify or re-enter the work.

---

## 1. PRIMARY LAW

When the Founder transfers an old conversation by `Ctrl+A -> Ctrl+C -> paste`, export, pasted transcript, generated big-paste file or equivalent, the receiving IVDIVO session must treat it as a **RECOVERY CORPUS**.

The Founder is not required to explain which parts matter, which artifacts were supposedly created, which model said what, or where the prior conversation stopped.

The receiving session must perform:

`INGEST -> PARSE -> RECOVER PROJECT/FRONTIER -> EXTRACT MATERIAL DELTAS -> VERIFY PERSISTED CLAIMS -> CLASSIFY CHAT-ONLY OUTPUT -> DEDUPE -> RECONCILE AUTHORITY/FRESHNESS -> PERSIST ACCEPTED STATE/ARTIFACTS -> HARVEST SYSTEM LEARNING -> UPDATE POINTERS -> READBACK -> CONTINUE FROM REAL NEXT OBLIGATION`.

A transcript is evidence and recovery material. It is **not automatically canon or authority**.

---

## 2. TRIGGER CONDITIONS

Run this protocol when any of the following occurs:
- a full or partial previous conversation is pasted into a new chat;
- a copied conversation appears as a generated big-paste attachment;
- the Founder says the previous conversation ended abruptly and provides the transcript;
- an external AI transcript/export is supplied for continuation;
- a pasted recovery corpus contains claims that files, prompts, scripts, programs, tests or decisions were already created;
- the new chat begins with `continue / продолжай / и / дальше` plus a pasted prior transcript.

If the user separately types an instruction with the transcript, that instruction is the active task; the transcript is the recovery basis/supporting context.

---

## 3. SOURCE COMPLETENESS

Classify the recovery corpus:
- `FULL_TRANSCRIPT` — appears to include the complete conversation from start/frontier through termination;
- `PARTIAL_TRANSCRIPT` — clearly begins/ends midstream or omits sections;
- `UNKNOWN_COMPLETENESS` — completeness cannot be established;
- `MULTI_TRANSCRIPT_BUNDLE` — several sessions/models are included.

Never infer missing exact details merely because the transcript is probably incomplete.

For very large transcripts, process in bounded chunks with a `RECOVERY_LEDGER` so early findings are not lost before later chunks are read.

A large transcript is not considered ingested until the final chunk/tail is processed and all material findings have disposition.

---

## 4. RECOVERY CLASSIFICATION

Extract and label material items, not every conversational sentence.

Required classes:
- `FOUNDER_DIRECTIVE` — explicit instruction/approval/rejection/lock/change from Founder;
- `CANON_OR_AUTHORITY_CLAIM` — statement about current canon/authority/status;
- `WORK_COMPLETED_CLAIM` — assistant/model says work was done;
- `ARTIFACT_REFERENCE` — filename, Drive ID, GitHub path/commit/PR, File Library reference, build ID, hash;
- `CHAT_ONLY_OUTPUT` — substantial script/design/prompt/program/result present in transcript but not yet verified as persisted;
- `EXTERNAL_AI_FINDING` — Claude/Grok/GPT/Codex/other reviewer result;
- `SYSTEM_IMPROVEMENT` — reusable mechanism/prompt/process/program/QA/repair law;
- `PROJECT_DECISION` — project-specific accepted/working/rejected choice;
- `OPEN_GATE_OR_BLOCKER`;
- `NEXT_ACTION_CLAIM`;
- `SUPERSEDED_OR_REJECTED_BRANCH`;
- `FACT_OR_NUMBER_LOCK`;
- `HUMAN_OR_MARKET_EVIDENCE_CLAIM`;
- `SECRET_OR_CREDENTIAL` — never persist into GitHub/normal project docs.

Preserve source role and chronology where it affects authority.

---

## 5. TRANSCRIPT CLAIMS ARE NOT SELF-VERIFYING

Any line such as:
- “I saved it to Drive”;
- “GitHub was updated”;
- “the gate passed”;
- “Claude verified it”;
- “the file is current”;
- “this is locked”;

must be verified against available persisted sources before being treated as durable state.

Classification:
- persisted artifact found + provenance/status valid -> `VERIFIED_PERSISTED`;
- actual substantial output exists only in transcript -> `CHAT_ONLY_CANDIDATE`;
- only a summary/claim exists, but underlying output is absent -> `DISCOVERY_ONLY`;
- source cannot be recovered reliably -> `UNRECOVERABLE_CHAT_ONLY`;
- newer authority supersedes it -> `SUPERSEDED`;
- conflicts with higher authority -> `CONFLICT`.

Never fabricate a missing file merely because a prior assistant claimed to have created it.

---

## 6. PERSISTED-ARTIFACT RECONCILIATION

For each material artifact claim, search relevant available stores:
1. active project/source-of-truth;
2. GitHub main/current branches according to authority policy;
3. Google Drive current/working artifacts;
4. File Library/current uploads when relevant;
5. external-model result stores with provenance.

Verify where available:
- title/path/ID;
- version/revision/hash;
- status (`CURRENT / CANON / WORKING / CANDIDATE / SUPERSEDED / REJECTED / ARCHIVE`);
- parent/source version;
- PASS/FAIL/gate result;
- whether a newer artifact already replaced it.

File existence alone is not authority.

If the transcript contains a complete useful artifact that was never persisted, create/persist the smallest correct candidate artifact rather than asking the Founder to manually recreate it.

If only fragments exist, preserve fragments/provenance and mark missing sections `UNKNOWN`; do not fill them from memory.

---

## 7. SEMANTIC DEDUPE + FRESHNESS

Do not create duplicates from a pasted conversation.

For each recovered item compare against current persisted work:
- `SAME_CURRENT`;
- `DUPLICATE`;
- `EXTENSION`;
- `NEWER_STRONGER_COMPATIBLE`;
- `OLDER_STALE`;
- `COMPETING_ALTERNATIVE`;
- `PROJECT_SPECIFIC_ONLY`;
- `SYSTEM_CANDIDATE`;
- `CONFLICT_WITH_AUTHORITY`.

Newest timestamp or filename does not automatically win.

A newer compatible project-specific gate/frontier may rebase an older aggregate state pointer while preserving the older document's stable law.

---

## 8. FOUNDER DIRECTIVE RECOVERY

Founder statements inside the transcript retain their normal authority according to chronology.

Recover direct Founder decisions carefully:
- approval/lock;
- rejection;
- branch switch;
- exact canon correction;
- production priority override;
- explicit hold;
- requested universal system law.

Do not confuse an assistant paraphrase of a Founder decision with the original Founder statement if the original is absent.

When chronology is ambiguous or contradictory and materially affects canon, fail closed at `AUTHORITY_UNRESOLVED` rather than guessing.

---

## 9. CHAT-ONLY ARTIFACT RECOVERY

When substantial work exists in the transcript but not in persistent storage:

`EXTRACT ACTUAL CONTENT -> PRESERVE PROVENANCE -> CLASSIFY AS CHAT_ONLY_CANDIDATE -> COMPARE WITH CURRENT -> RUN REQUIRED QA/RED TEAM/REGRESSION -> PERSIST CANDIDATE OR ACCEPTED ARTIFACT -> UPDATE STATE -> READBACK`.

Examples:
- manuscript scenes;
- story architecture;
- prompts;
- code/program logic;
- render manifests;
- review findings;
- production run sheets;
- system procedures;
- external-AI handoffs.

Do not silently promote chat-only content directly into locked canon.

---

## 10. SELF-IMPROVEMENT HARVEST

Every recovery pass also asks:
- What did this conversation discover that improves future work?
- Did a repeated failure expose a missing system control?
- Did a project-specific solution generalize?
- Did a prompt/program/tool workflow become materially better?
- Did a prior rule prove unnecessary, duplicated or harmful?
- Did another AI provide independently useful evidence?

Reusable findings route through the current Self-Improvement Engine:

`RECOVERED SIGNAL -> DEDUPE -> CANDIDATE -> SCOPE -> DEVELOPMENT/PILOT AS NEEDED -> RED TEAM/REGRESSION -> PROMOTION -> APPLICATION -> VERIFICATION`.

Do not universalize project characters, culprit logic, exact clue chain, voice IDs, signature motifs, unique chronology or other distinctive project content.

---

## 11. RECOVERY LEDGER / MINIMUM STATE

For a large pasted transcript maintain equivalent fields:
- `recovery_id`;
- source model/chat if known;
- source date/range if known;
- completeness classification;
- active project(s)/line(s);
- chunks processed / final-tail processed;
- Founder directives recovered;
- artifact claims checked;
- verified persisted artifacts;
- chat-only candidates;
- conflicts/unknowns;
- superseded items;
- system-improvement candidates;
- secrets/credentials excluded;
- writes performed;
- readback status;
- current frontier;
- exact next unblocked obligation;
- remaining recovery gaps.

The ledger may be compact and need not preserve the entire conversational transcript.

---

## 12. SECRET / PRIVACY FIREWALL

A pasted transcript may accidentally contain API keys, passwords, tokens, private access links or other secrets.

Do not copy secrets into:
- GitHub;
- normal Drive production docs;
- prompts;
- manifests;
- learning ledgers;
- handoff cards.

Persist only the fact that a credential/user-side action exists when needed. Never treat a secret as project knowledge to be generalized.

---

## 13. WRITE-THROUGH MAP

Recovered material goes only to the correct controlling surface.

Examples:
- current project frontier -> project Current Authority/State;
- manuscript/source -> project script/manuscript artifact;
- canon decision -> canon/authority layer only with proper authority;
- external review -> review + disposition record;
- reusable craft/process mechanism -> Improvement Registry / Learning Ledger / appropriate Narrative OS or domain overlay after promotion;
- prompt/program change -> actual prompt/code + tests + pointer;
- cross-AI state -> `CURRENT_IVDIVO_CROSS_AI_HANDOFF.md` / bounded run card;
- aggregate frontier -> `CURRENT_IVDIVO_SYSTEM_STATE.json`.

Do not dump the entire raw transcript into every authority file.

---

## 14. COMPLETION GATE

Transcript recovery is complete only when:
1. final transcript tail/chunk was processed;
2. material Founder directives were classified;
3. material artifact claims were verified or marked unavailable;
4. chat-only substantive outputs received disposition;
5. conflicts/unknowns are recorded;
6. accepted project state is persisted;
7. reusable system learnings are routed into self-improvement memory;
8. relevant current pointers/handoffs are updated;
9. writes are read back/verified;
10. a real next obligation or real blocker is identified.

Then set `RECOVERY_STATUS = INGESTION_COMPLETE`.

If the transcript is partial, completion means all supplied material is ingested; missing unsupplied content remains explicitly unknown.

---

## 15. CONTINUATION AFTER RECOVERY

After `INGESTION_COMPLETE`, do not stop merely to summarize recovery if the next production obligation is safe, authorized, unblocked and executable.

Run:
`RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VERIFY -> PERSIST -> CONTINUE UNTIL REAL GATE`.

A Founder paste followed by “продолжай” means **recover first, then continue actual work**.

---

## 16. FAILURE MODES / HARD FAILS

FATAL/MAJOR operational failures include:
- trusting a prior assistant's “saved/locked/passed” claim without verification;
- dropping substantial chat-only work that was fully present in the transcript;
- silently converting transcript material into canon;
- overwriting newer persisted work with an older pasted transcript;
- reconstructing missing exact details from memory;
- failing to process the tail of an oversized transcript;
- duplicating an already-current artifact instead of reusing it;
- persisting secrets/credentials;
- extracting project-specific content into a universal mechanism;
- declaring ingestion complete while material unresolved items remain unclassified.

---

## 17. STANDARD FOUNDER WORKFLOW

The emergency manual transfer procedure is valid:

`OLD CHAT -> Ctrl+A -> Ctrl+C -> NEW CHAT -> paste -> “продолжай”`.

The receiving IVDIVO session owns the recovery/orchestration burden.

The Founder should not have to annotate the transcript manually unless an actual authority ambiguity remains after recovery.

---

## FINAL LAW

**THE TRANSCRIPT IS A RECOVERY CORPUS, NOT A NEW CANON.**

**VERIFY WHAT WAS REALLY SAVED. RECOVER WHAT EXISTS ONLY IN CHAT. DO NOT INVENT WHAT IS MISSING. PRESERVE WHAT MATTERS. HARVEST WHAT GENERALIZES. WRITE THROUGH. READ BACK. CONTINUE.**
