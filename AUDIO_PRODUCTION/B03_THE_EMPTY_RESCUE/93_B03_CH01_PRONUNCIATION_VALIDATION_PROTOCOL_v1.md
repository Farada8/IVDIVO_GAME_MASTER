# B03 CH01 — PRONUNCIATION VALIDATION PROTOCOL v1

Date: 2026-08-22  
Status: **PROTOCOL READY / PHONETIC LOCKS OPEN**

## Rule
Do not promote guessed IPA or an AI pronunciation guess to B03 authority. Names and place terms must be validated by listening evidence and/or a local/native-source check before full-scale render.

## Required terms
Priority CH01:
- Nika Zupan
- Jana Kovač
- Andrej Košir
- Koren Valley

Book-wide before scaled production:
- Upper Gorge
- Morgen Pass
- any later recurring Slovenian personal/place name discovered during CH02–29 compile

## Validation sequence
1. Preserve exact written spelling from locked text.
2. Run S0 without a pronunciation dictionary to expose provider baseline.
3. Record provider/model/voice ID and heard result; do not silently correct text.
4. Obtain a human/local/native reference for personal names with uncertain stress or vowel quality.
5. If correction is needed, use a pronunciation dictionary/phoneme or provider-supported pronunciation mechanism rather than altering locked manuscript text.
6. Re-render the smallest affected audition unit.
7. Blind-check intelligibility and consistency across narrator + character voices.
8. Lock one pronunciation entry with provenance, date and scope.
9. Apply the same lock to replay/continuity occurrences and later chapters.
10. Reopen only the pronunciation asset if evidence fails; Story Lock stays closed.

## Hard fails
- different pronunciations of the same recurring name without story reason;
- anglicizing by silently changing source spelling;
- guessed phonetic form recorded as CANON without human/listening evidence;
- voice candidate rejected solely because an unlocked dictionary entry was wrong;
- pronunciation fix that changes exact_text.

## Current state
No phonetic value is locked yet. This is intentional and fail-closed.
