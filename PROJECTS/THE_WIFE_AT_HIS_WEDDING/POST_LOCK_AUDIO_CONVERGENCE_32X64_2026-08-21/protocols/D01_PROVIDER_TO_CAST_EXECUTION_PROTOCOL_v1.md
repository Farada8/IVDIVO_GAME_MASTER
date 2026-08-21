# D01 PROVIDER -> CAST -> SMOKE EXECUTION PROTOCOL v1.1

Fresh-main dependency: merged Audio Wave11 provider-evidence intake. D01 must consume that shared provider evidence path rather than create a project-local snapshot/intake mechanism.

1. Fresh-read D01 Founder Lock, current D01 project state and current shared Audio Runtime.
2. Resolve `provider_execution_state.py` from admissible Wave11 intake evidence.
3. If state is `NO_ADMISSIBLE_PROVIDER_EVIDENCE`, use the already-merged read-only provider snapshot workflow; never persist API keys and do not invent a parallel D01 provider reader.
4. Consume the exact secret-free `AUTH_PROVIDER` artifact through Wave11 `provider_evidence_intake.py`; validate workflow run/attempt/source lineage, freshness and account identity.
5. If repeatability is required, acquire the second read-only snapshot and classify capability/account/volatile drift before cast binding.
6. Accept only the normalized verified provider inventory produced by the shared Wave11/Wave10 chain.
7. Supply D01 casting spec and shortlist only voice IDs present in that inventory.
8. Generate D01 cast-readiness v1.1. Machine state may reach `READY_FOR_REAL_AUDITION`, never `voice_lock=true`.
9. Pass cast readiness through `provider_execution_state.py`; machine routing stops at real audition preparation.
10. Run zero/lowest-cost audition material for NARRATOR/MARA/ADRIAN/LILY/CELESTE using existing D01 audition lines.
11. Human score: intelligibility, naturalness, restraint, character separation, subtext, long/short stability, pronunciation, regeneration consistency.
12. Run Mara/Adrian pair gate and Lily child-credibility gate.
13. Lock only explicitly accepted voices; persist provider/model/settings/voice IDs without credentials.
14. Re-run zero-credit provider/model/output preflight.
15. Dispatch **only S01–S07** live smoke. No accidental full-E01 path.
16. Persist raw request IDs, model, voice IDs, exact source refs, raw WAV, hashes and alignment/provenance.
17. Human-review smoke: character identity, restraint, music-box clue, scar intimacy, phone intelligibility.
18. Selectively regenerate the smallest failed unit. Accepted units remain immutable.
19. Only after smoke PASS render R01–R08 clean voice, run blind comprehension, add the canonical shared four-note motif after clean-voice GO, and measure provider spend/manual minutes/accepted minutes. Null remains null, never zero.
20. Feed proven defect -> repair -> retest into Learning Registry/Self-Improvement and scale E02 only after accepted E01 provider/human/economic proof; do not batch 120 episodes on architecture confidence alone.
