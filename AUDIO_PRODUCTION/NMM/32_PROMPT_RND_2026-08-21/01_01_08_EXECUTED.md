# NMM — EXECUTED PROMPTS 01–08

## PROMPT 01 — Authority / Canon

**Промт**  
Восстанови текущую authority NMM для аудиопроизводства и перечисли всё, что запрещено переносить из старых веток.

**Выполнение**  
Authority восстановлена из `00_NMM_AUDIO_AUTHORITY_MANIFEST_v1.0` и текущего IVDIVO Audio Production Authority. Действующая история: CURRENT REPAIRED E01–E24, TEXT LOCKED, Delivery Mode C — DRAMATIZED AUDIOBOOK. Episode 25 не авторизован. Производственно известный culprit — Vivian — обязан оставаться spoiler-protected. Старые Mercer/Calder/22:07 материалы, pre-medical-repair causality, superseded Claude development history и дубликаты проекта запрещены как production input.

**Вывод**  
Текущий production-риск — не нехватка сюжета, а branch contamination. Любой downstream артефакт без source authority/branch fingerprint потенциально опасен.

**Решение**  
Каждый build должен начинаться с authority ID/revision/hash и явного `NO_BRANCH_FALLBACK`.

**Статус:** `PASS`

## PROMPT 02 — Authority / Canon

**Промт**  
Проверь exact-text coverage E01 и разреши конфликт 1496 vs 1494 без переписывания текста.

**Выполнение**  
Deterministic extraction уже назначил 269/269 spoken paragraph occurrences ровно одному RENDER или ALIAS. Revision history показала: ранний declared count = 1488, текущий net delta = +6, поэтому аудиокомпилятор должен считать 1494 tokens. Строка `1496` в source metadata устарела на +2; spoken prose не меняется.

**Вывод**  
Смысловой и occurrence coverage — полный. Дефект относится к metadata/counting, не к литературному тексту.

**Решение**  
Для audio compiler использовать `CANONICAL_SPOKEN_COUNT=1494`; source metadata `1496` хранить как stale metadata evidence, а не как target.

**Статус:** `PASS_WITH_METADATA_OVERRIDE`

## PROMPT 03 — Authority / Canon

**Промт**  
Спроектируй fail-closed source fingerprint law для provider render.

**Выполнение**  
Зафиксирована двухступенчатая provenance-модель: Google revision fingerprint подтверждает authority, а downstream compilation хранит cryptographic SHA-256 source export + spoken occurrence ledger + sanitized request hash. Provider dispatch запрещён при несоответствии любого обязательного fingerprint.

**Вывод**  
Один Drive revision ID недостаточен для машинной воспроизводимости, но он полезен как authority pointer; криптографический hash должен жить ближе к render packet.

**Решение**  
Gate: `AUTHORITY_REVISION_PASS && SOURCE_SHA_PASS && OCCURRENCE_LEDGER_SHA_PASS && REQUEST_SHA_CREATED`.

**Статус:** `PASS`

## PROMPT 04 — Authority / Canon

**Промт**  
Проверь правило повторного использования confession/whistle и запрети drift между повторами.

**Выполнение**  
Render plan задаёт один `CONFESSION_MASTER` и ASSET_ALIAS для последующих replay. Sound registry задаёт один `W_EXTRA_SHORT_MASTER` и один `W_OFFICIAL_LONG_MASTER`. Повторный TTS/render для этих событий создаёт риск другого acting state, timing, noise bed и acoustic identity.

**Вывод**  
Replay identity — не эстетика, а часть доказательной честности mystery.

**Решение**  
После lock: никаких rerender повторов; только exact excerpt/alias из master asset. Drift = FATAL production defect.

**Статус:** `PASS`

## PROMPT 05 — Listener / Dramaturgy

**Промт**  
Определи минимальный one-listen fact set E01.

**Выполнение**  
Минимум: voice note приходит Isla в 11:47; содержит `I killed him`, `Don't trust my memories`, `Find the extra whistle`; Bell найден позже, discovery logged 12:04; genuine words не равны верному murder conclusion; Isla сохраняет original source; memory unreliable; short extra whistle отличен от official long whistle; финальная рабочая гипотеза — whistle in message not from match.

**Вывод**  
Главная comprehension нагрузка E01 — не футбол, а разделение: time / source / belief / fact / acoustic clue.

**Решение**  
Все mix/performance решения должны защищать эти 8 facts; human test задаёт их без подсказки.

**Статус:** `PASS`

## PROMPT 06 — Listener / Dramaturgy

**Промт**  
Проведи non-football accessibility audit E01.

**Выполнение**  
Сюжетная причинность объясняется через обычные категории: время, голосовое сообщение, обнаружение тела, память, запись, два разных свистка. Спортивная терминология ограничена контекстом `champions`, referee whistle, stadium. Основной риск — если звуковая сцена перегрузит listener и заставит его решать футбольную механику вместо temporal contradiction.

**Вывод**  
Новой экспозиции не требуется. Доступность должна достигаться миксом, speaker clarity и sonic contrast, а не переписыванием.

**Решение**  
В high-information beats снижать ambience/music; не добавлять football jargon в SFX/announcer improvisation.

**Статус:** `PASS`

## PROMPT 07 — Listener / Dramaturgy

**Промт**  
Проведи spoiler-fairness audit для Vivian в аудио.

**Выполнение**  
Listener contract и voice bible прямо запрещают villain music, sinister reverb, predatory low-frequency emphasis, secret-guilt pauses и actor direction `play the culprit`. Vivian должна звучать как разумная institutional counterforce с реальной заботой/контролем.

**Вывод**  
Кастинг может разрушить mystery даже при идеальном тексте. Низкий «злодейский» тембр — скрытая утечка разгадки.

**Решение**  
Vivian получает blind spoiler-neutrality gate: если 2+ listeners независимо называют её убийцей преимущественно из-за звучания, voice/direction FAIL.

**Статус:** `PASS_SPEC / PENDING_REAL_LISTEN`

## PROMPT 08 — Listener / Dramaturgy

**Промт**  
Проверь romance pacing E01 и сформулируй аудиограницы chemistry.

**Выполнение**  
E01 relationship movement = suspicion -> first respect. Романтическая тема и breathy intimacy запрещены. Chemistry должна возникать из attention, resistance, status negotiation, добровольного риска и micro-humor. Для pair test выбран конфликтный, не романтический материал.

**Вывод**  
Если chemistry слышна только на мягких/романтических репликах, кастинг слаб для этого сезона.

**Решение**  
S4 pair gate тестировать на status/boundary dialogue; романтическое смягчение не использовать как shortcut.

**Статус:** `PASS_SPEC / PENDING_PAIR_EVIDENCE`
