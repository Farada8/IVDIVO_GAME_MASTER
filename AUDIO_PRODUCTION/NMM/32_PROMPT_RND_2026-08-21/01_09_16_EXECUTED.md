# NMM — EXECUTED PROMPTS 09–16

## PROMPT 09 — Casting / Performance

**Промт**  
Сформируй hard criteria для Isla и найди главный casting risk.

**Выполнение**  
Isla = evidentiary anchor: medium/medium-low grounded timbre, controlled conversational tempo, exact but natural articulation, status through narrowing questions, dryness with audible micro-reaction. Запрещены icy detective, noir narrator, robotic competence, femme-fatale whisper.

**Вывод**  
Главный риск — голос, который красив в demo, но через 10–12 минут превращает precision в монотонность/AI cadence.

**Решение**  
Isla не проходит lock без narration + live dialogue + short status line + micro-humor + fatigue/device tests.

**Статус:** `PASS_SPEC / VOICE_ID_PENDING`

## PROMPT 10 — Casting / Performance

**Промт**  
Сформируй hard criteria для Leo и раздели live identity от recorded confession state.

**Выполнение**  
Leo live = fluent, grounded, socially practiced, early-30s physical presence without macho trailer baritone. Recorded confession = тот же человек, но breath too fast, urgent self-command, frightened by his own conclusion. Нельзя кодировать drunk/drugged, villain confession, trauma whisper или horror possession.

**Вывод**  
Если recording и live звучат как разные актёры, central evidence identity ломается; если confession слишком guilty, listener получает ложный verdict.

**Решение**  
Один voice binding; разные performance states + post-chain. Lock требует A/B confession test и live/recorded identity continuity.

**Статус:** `PASS_SPEC / VOICE_ID_PENDING`

## PROMPT 11 — Casting / Performance

**Промт**  
Сформируй hard criteria для Vivian и проверку anti-spoiler.

**Выполнение**  
Vivian: composed, intelligent, socially efficient, measured tempo, low-effort authority; care manifests as containment. Запрещены villainess, corporate snake, ominous purr, false sweetness, secret-guilt pauses. Blind test должен воспринимать её как protect/control/reduce-risk, а не `killer voice`.

**Вывод**  
Для Vivian numeric attractiveness score вторичен; spoiler-neutrality — veto gate.

**Решение**  
Hard fail override: spoiler-coded performance rejects candidate независимо от общего score.

**Статус:** `PASS_SPEC / BLIND_TEST_PENDING`

## PROMPT 12 — Casting / Performance

**Промт**  
Определи cross-cast differentiation и оптимальную глубину кастинга secondary roles.

**Выполнение**  
Isla/Vivian различаются status grammar и rhythm, не только pitch; Isla/Leo — deliberate categorization vs fluent social rhythm; Security/Commentator — functional medium distinction. Secondary voices не требуют дорогого star-casting до доказательства pilot.

**Вывод**  
Слишком похожие lead voices вредят comprehension; чрезмерная инвестиция в короткие роли до pilot — плохая экономика.

**Решение**  
Приоритет S1: Isla, Leo, Vivian. Security/Commentator проходят S0/basic intelligibility и только затем минимальный role-fit test.

**Статус:** `PASS`

## PROMPT 13 — Render / Provider

**Промт**  
Раздели E01 на TTS vs TTD по dramatic/selective-regeneration logic и проверь это против текущего ElevenLabs contract.

**Выполнение**  
Наррация, confession master, commentator и clue/identity-risk lines подходят для isolated timestamp TTS. Многосторонние live scenes — TTD, если блок остаётся в одном clean processing domain. Официальная документация на 2026-08-21 подтверждает `/v1/text-to-dialogue/with-timestamps`, до 10 unique voice IDs и рекомендацию держать суммарный dialogue text <= ~2000 chars; default model currently `eleven_v3`.

**Вывод**  
TTD экономит conversational coherence, isolated TTS экономит selective regeneration risk. Нельзя максимизировать только один параметр.

**Решение**  
Project ceiling для TTD установить строже provider guidance: целиться <=1800 chars; clue/identity-critical lines изолировать.

**Статус:** `PASS`

## PROMPT 14 — Render / Provider

**Промт**  
Проверь processing-domain boundaries и clean-first law.

**Выполнение**  
D_NARRATION_DRY, D_LIVE_ROOM, D_PHONE_REMOTE, D_PHONE_RECORDING, D_BROADCAST и PERFORMANCE_SOUND должны иметь POST_CHAIN_BOUNDARY. ElevenLabs clean voice masters не должны содержать ambience, score, final reverb или phone EQ; device treatment делается downstream.

**Вывод**  
Baked processing лишает возможности selective repair, ломает reuse confession и загрязняет alignment/comparison.

**Решение**  
Provider voice output = clean source; все medium/acoustic differences — post-chain unless provider test explicitly proves unavoidable exception.

**Статус:** `PASS`

## PROMPT 15 — Render / Provider

**Промт**  
Определи text-normalization/pronunciation policy для exact-text проекта.

**Выполнение**  
Текущий ElevenLabs TTD contract поддерживает `apply_text_normalization=auto|on|off`; pronunciation dictionary locators — до 3 на TTD request. В NMM exact text уже пишет времена словами, поэтому автоматическая нормализация не нужна как базовая смысловая функция. Однако произношение Isla и других имён требует provider test.

**Вывод**  
`auto` может быть удобен, но в HARD LOCK проекте это дополнительная скрытая трансформация. Нельзя объявить проблему без live evidence, но риск реальный.

**Решение**  
S0 сравнивает `off` как production-default candidate; dictionary/phonetic solution используется локально. Любая normalized text drift проверяется против exact source before lock.

**Статус:** `PROPOSED_POLICY / S0_VERIFY`

## PROMPT 16 — Render / Provider

**Промт**  
Проверь alignment architecture против двух ElevenLabs timestamp schema.

**Выполнение**  
TTD response может иметь `voice_segments`, `alignment`, `normalized_alignment`; timestamp TTS — character alignment arrays и, в зависимости от wrapper, normalized alignment. Universal authority уже требует provider-neutral normalization before timeline.

**Вывод**  
Downstream consumer, читающий raw provider schema напрямую, привязывает проект к backend и создаёт silent break при schema change.

**Решение**  
Raw response архивировать, но timeline принимает только NORMALIZED_ALIGNMENT_RECORD. Unknown/malformed schema = FAIL_ALIGNMENT_*.

**Статус:** `PASS`
