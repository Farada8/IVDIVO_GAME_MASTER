# NMM CYCLE4 PROTOCOL BUNDLE v1

---

## FILE: NMM_ESCROW_CONTENT_READBACK_PROTOCOL_v1.md

# NMM ESCROW CONTENT READBACK PROTOCOL v1
A URL/file ID/hash record is only metadata evidence. Persistence is PASS only after bytes are independently materialized/read back and SHA-256 matches the expected artifact. Partial listings are marked PARTIAL. Ambiguous multi-store writes enter REPAIR_REQUIRED and route through current SI-0014 durable recovery; NMM does not create a competing transaction engine.

---

## FILE: NMM_EXTERNAL_SPECIALIST_REVIEW_PROTOCOL_v1.md

# NMM EXTERNAL SPECIALIST REVIEW PROTOCOL v1
Predeclare reviewer role/qualification, packet hash, question set and conflict disclosure. Keep the packet narrow: sports-medicine plausibility and publication-facing legal/procedural claims only. Story authority is outside reviewer scope. Capture exact finding, severity, evidence, disposition and changed artifacts. No reviewer metadata is treated as proof that review occurred without a completed declaration and response artifact.

---

## FILE: NMM_PROVIDER_AUTHENTICATED_SNAPSHOT_PROTOCOL_v2.md

# NMM PROVIDER AUTHENTICATED SNAPSHOT PROTOCOL v2
1. Run the current universal `audio/studio/provider_preflight.py`; NMM does not create a provider client.
2. Capture provider/model/output-format/capability/voice metadata with secrets removed.
3. Bind the snapshot to the preflight artifact SHA-256 and timestamp.
4. Reject unauthenticated, stale (>24h), ambiguous, or secret-bearing snapshots.
5. Voice IDs may become shortlist metadata only; no voice/take lock follows from availability.
6. Before spend, run the universal controlled dispatch pre-spend gate.
7. If the environment has no credential, status is `HOLD_NO_CREDENTIAL`, not PASS.

---

## FILE: NMM_REAL_HUMAN_WHISTLE_PROTOCOL_v2.md

# NMM REAL HUMAN WHISTLE PROTOCOL v2
The listener receives only the listener-safe pack, never this engineering folder.

Predeclared sealed protocol SHA-256: `34fe8b7c43eca3fef5c03ffe499599a02f29b71479271bb55d1236be45c3b2ee`
Trial-set SHA-256: `6f7a1ed281bcffd8829a4598a9b229c402b1147e2970283c5ad5d6d0a241c1cd`
Thresholds: accuracy >= 0.75; mean realism >= 3.5/5.

Run headphones first, then actual phone speaker. Record raw answers before scoring. No correctness feedback between trials. The scorer is run only after answers are frozen. Any threshold/protocol edit invalidates the test. PASS does not itself lock a story master; device translation, coding notes and narrative suitability still require review.

---

## FILE: NMM_SELF_IMPROVEMENT_PROMOTION_PROTOCOL_v2.md

# NMM SELF-IMPROVEMENT PROMOTION PROTOCOL v2
1. Record real `DEFECT -> ROOT CAUSE -> REPAIR -> RETEST -> RESULT` evidence.
2. Strip NMM names, exact text, clue identities, timings and project assets.
3. One project remains `DISCOVERY_ONLY` regardless of deterministic score.
4. A second independent real project may make a mechanism `CANDIDATE_FOR_REVIEW`; it does not promote authority.
5. Human-dependent claims require human evidence. Provider claims require authenticated provider evidence.
6. Explicit Founder/human review is required for universal acceptance.
7. Existing SI-0014/Cycle5 registry/transaction machinery is reused; no parallel registry is created.
