# D01 PROVIDER -> CAST -> SMOKE EXECUTION PROTOCOL v1.0

1. Fresh-read D01 Founder Lock and current shared Audio Runtime.
2. Acquire a **secret-free authenticated** ElevenLabs ProviderSnapshot using the existing runtime workflow. Never persist API keys.
3. Validate snapshot freshness/account identity; compile provider inventory.
4. Supply D01 casting spec and shortlist only voice IDs present in that inventory.
5. Generate the cast-readiness manifest. Machine state may reach `READY_FOR_REAL_AUDITION`, never `voice_lock=true`.
6. Run zero/lowest-cost audition material for NARRATOR/MARA/ADRIAN/LILY/CELESTE using the existing audition lines.
7. Human score: intelligibility, naturalness, restraint, character separation, subtext, long/short stability, pronunciation, regeneration consistency.
8. Run Mara/Adrian pair gate and Lily child-credibility gate.
9. Lock only explicitly accepted voices; persist provider/model/settings/voice IDs without credentials.
10. Re-run zero-credit provider/model/output preflight.
11. Dispatch **only S01–S07** live smoke. No accidental full-E01 path.
12. Persist raw request IDs, model, voice IDs, exact source refs, raw WAV, hashes and alignment/provenance.
13. Human-review smoke: character identity, restraint, music-box clue, scar intimacy, phone intelligibility.
14. Selectively regenerate the smallest failed unit. Accepted units remain immutable.
15. Only after smoke PASS render R01–R08 clean voice.
16. Assemble CLEAN VOICE; run blind comprehension before story-bearing SFX/music.
17. Add canonical shared four-note motif only after clean-voice GO.
18. Measure provider spend/manual minutes/accepted minutes; null remains null, never zero.
19. Feed proven defect->repair->retest to Learning Registry/Self-Improvement.
20. Scale E02 only after accepted E01 proof; do not batch 120 episodes on architecture confidence alone.
