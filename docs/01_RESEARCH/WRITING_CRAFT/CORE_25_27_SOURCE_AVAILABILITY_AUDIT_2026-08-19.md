# CORE #25–27 SOURCE AVAILABILITY AUDIT — 2026-08-19

Status: VERIFIED / UPDATED
Purpose: prevent preview fragments, misleading filenames and collection containers from being counted as FULL READ sources.

## #25 Kazuo Ishiguro — *Klara and the Sun*

Drive folder: `KAZUO_ISHIGURO_SPECULATIVE` (`1EYpJvQQlfRhRAEtp2xrnJYyTgJHYH0TK`).

Candidates inspected:
- `137797196.zip` (`18f00GVXJ0-4cTaX6JRHjBfNhocg4SZje`)
- `64854856.fb2.zip` (`127_Lt98sN1x4q5cT6I-T2Jk5jt3iypcc`)

Result:
Both contain the same *Klara and the Sun* preview text. Normalized text comparison indicates duplicate content. Both terminate with the LitRes-style notice indicating the end of an ознакомительный fragment. Approximate available text: ~19.6k words, not the complete novel.

Lifecycle status:
`REGISTERED / SOURCE LOCATED → INTEGRITY VERIFIED = FAIL (PREVIEW ONLY) → FULL READ BLOCKED`.

Do not count either archive as a separate source or as a completed book.

## #26 Kazuo Ishiguro — *Never Let Me Go*

Candidate:
- `67424097.zip` (`1EDKWTmVgwiYMduuTuBAvp07cWdBsmfhP`)

Result:
Contains *Never Let Me Go* / «Не отпускай меня», but only an ознакомительный fragment, approximately ~19.6k words, with preview termination marker.

Lifecycle status:
`REGISTERED / SOURCE LOCATED → INTEGRITY VERIFIED = FAIL (PREVIEW ONLY) → FULL READ BLOCKED`.

## Misleading combined EPUB

`Kadzuo_Isiguro_Netipichnye_antiutopii._Komplekt_iz_3_knig_ltr.epub` (`1sVZDhbGL-KTCksg0EIXNWu5V6w6B3hMl`) was inspected because metadata implies a three-book Ishiguro set.

Result:
The available payload is not a complete three-Ishiguro-novel source suitable for Core #25/#26 strict reading. It must not be used to bypass the preview limitation.

## Literary Ishiguro folder

`KAZUO_ISHIGURO_LITERARY` contains additional numeric ZIP files. Inspection identified preview-only Ishiguro texts (including *The Remains of the Day* / *When We Were Orphans* representations), not the complete Core #25/#26 targets.

## #27 Martha Wells — *All Systems Red*

Drive folder: `MARTHA_WELLS_MURDERBOT` (`1UGyyOvUyhX7di-Y_RgwjSvzv-21w60La`).

Retained collection source:
- `Uells_Marta_[Dnevniki_Killerbota]_Otkaz_vseh_sistem_(sbornik).zip` (`1rUi2lk2ZF4PnuSVVY3OhtPhdEPeSeOMb`)

Updated collection-boundary verification:
The internal FB2 contains exactly two fiction works after front matter:
1. `Отказ всех систем` / *All Systems Red* — approximately 24.7k extracted words.
2. `Искусственное состояние` / *Artificial Condition* — approximately 24.8k extracted words.

The earlier collection ambiguity is therefore resolved at the work-boundary level. The collection container must still not be counted as a single “book” or as two copies of one source.

*All Systems Red* contains eight numbered chapters and the terminal departure/message scene and remains independently completed.

Lifecycle status for Core #27:
`REGISTERED → INTEGRITY VERIFIED → FULL READ → ... → SYNTHESIZED = COMPLETE`.

### Artificial Condition note

*Artificial Condition* has now been continuously read and synthesized as a separate reference source. However, this audit does **not** assert a Core slot for it because an authoritative Core-40 mapping for the next slot was not found in the current source-of-record search. It therefore must not increase the Core count merely because it shares the same collection archive.

## Queue consequence

- #25 remains blocked until a complete exact source is uploaded/found.
- #26 remains blocked until a complete exact source is uploaded/found.
- #27 remains completed and may be counted in strict Core.
- *Artificial Condition* is a distinct strict-complete reference work, but is not assigned a Core number here without authoritative mapping.
- Queue may move beyond #27 without pretending #25/#26 were completed.

## Dedupe rule reinforced

Numeric filenames, multiple archives and collection containers do not imply unique knowledge. Book identity must be established from internal metadata/text and work boundaries; duplicate preview text is one unavailable/incomplete source state, not multiple books.
