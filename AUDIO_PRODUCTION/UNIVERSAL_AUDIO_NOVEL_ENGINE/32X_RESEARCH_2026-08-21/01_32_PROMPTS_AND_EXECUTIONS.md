# IVDIVO AUDIO NOVEL ENGINE — 32 PROMPTS EXECUTED SEQUENTIALLY

**Method:** each prompt was executed against the current Audio Authority v3.3, Program Contract v2.0, ROOM 917 live evidence and LESSON ZERO second-project dry portability evidence. Results are classified rather than treated as automatically accepted canon.

---

## 01 — PRODUCT BOUNDARY
**PROMPT:** Зафиксируй product boundary IVDIVO Audio Novel Engine v1.0: что движок делает, чего не делает, какие входы/выходы обязательны и где заканчивается ответственность Story Engine.

**EXECUTION / RESULT:** После `SOURCE_LOCK` движок не сочиняет новую историю. Он принимает версионированный locked manuscript/script + project overlay + delivery mode, компилирует режиссуру, каст, performance, Foley/SFX/ambience/music, provider requests, alignment/timeline, mix/QC/repair и выдаёт production package/master. Любая сюжетная правка возвращается выше в Story Engine.

**DECISION:** ACCEPTED.  
**ENGINE CONSEQUENCE:** source/story firewall является обязательным v1.0 gate.

## 02 — DELIVERY MODE SELECTOR
**PROMPT:** Спроектируй обязательный DELIVERY_MODE_SELECTOR для narrated audiobook, multi-voice audiobook, dramatized audiobook и full audio drama; определи fail-closed правила против скрытого перехода между режимами.

**EXECUTION / RESULT:** Закреплены четыре режима: A Narrated — narrator dominant/minimal sound; B Multi-Voice — exact source + stable character voices; C Dramatized — exact source + direction/Foley/ambience/music; D Full Audio Drama — adaptation only under explicit authority + `ADAPTATION_DIFF`. Неявный drift между режимами = `FAIL_DELIVERY_MODE_DRIFT`.

**DECISION:** ACCEPTED.

## 03 — SOURCE INGEST + PROVENANCE
**PROMPT:** Разработай SOURCE_INGEST + provenance contract: hash, branch, version, forbidden branches, build ID, reused-take/asset lineage.

**EXECUTION / RESULT:** Обязательны `SOURCE_HASH_SHA256`, `SOURCE_VERSION`, `ACTIVE_BRANCH`, authority/overlay versions, delivery mode, build ID, forbidden branches/tokens и provenance chain. Reused take/asset без original build/ID/reuse reason/compatibility check не может быть locked.

**DECISION:** ACCEPTED.

## 04 — SCENE/SPOKEN-UNIT SEGMENTATION
**PROMPT:** Проверь универсальную сегментацию книги в `SCENE_MAP + SPOKEN_UNIT_MAP` и требование 100% exact-text coverage без ручного JSON.

**EXECUTION / RESULT:** LESSON ZERO Chapter 1 уже дал second-project proof: **146/146 spoken units** представлены ровно один раз и компилируются в **11 render blocks / 11 dry requests**. Это доказывает переносимость сегментационного слоя вне ROOM 917.

**DECISION:** PROVEN_DRY.  
**v1.0 ACCEPTANCE:** zero missing units, zero duplicate units, no manual JSON repair.

## 05 — ADAPTATION DIFF
**PROMPT:** Определи правила `ADAPTATION_DIFF` для перехода от книги к dramatized/full-drama версии без потери авторского смысла.

**EXECUTION / RESULT:** Для Narrated/Multi-Voice/Dr‌amatized источник остаётся authoritative; spoken rewrite не допускается без отдельной авторизации. Для Full Drama каждая изменённая единица хранит `SOURCE_TEXT → PERFORMANCE_VERSION → REASON → MEANING_CHANGE → APPROVAL_REQUIRED`. Актёрский prompt не может скрывать адаптацию.

**DECISION:** ACCEPTED.

## 06 — LISTENER CONTRACT
**PROMPT:** Разработай `LISTENER_CONTRACT` как машинный контроль плотности звука и внимания.

**EXECUTION / RESULT:** Каждый beat должен объявлять `LISTENER_MUST_UNDERSTAND / MAY_FEEL / MUST_WAIT_FOR / FOCUS_OWNER / SECONDARY_SUPPORT / SUPPRESS / DANGEROUS_MISUNDERSTANDING / COMPREHENSION_CRITICAL`. Это первичный control surface для density и AutoMix.

**DECISION:** ACCEPTED.

## 07 — DRAMATIC FORCE MAP
**PROMPT:** Сформируй `DRAMATIC_FORCE_MAP`, который связывает звук с изменением отношений/знания, а не с абстрактной эмоцией.

**EXECUTION / RESULT:** Принят `STATE_IN → PRESSURE → TURN → STATE_OUT` по earned forces: trust/distrust/desire/fear/control/vulnerability/knowledge/uncertainty и др. Music/sound не получают право сообщать эмоцию, которой нет в действии сцены.

**DECISION:** ACCEPTED.

## 08 — CHARACTER PERFORMANCE STATE
**PROMPT:** Определи `CharacterPerformanceState` и минимальный набор playable behaviors для TTS/актёра.

**EXECUTION / RESULT:** Нужны immediate want, resistance, tactic, subtext, status, energy, tempo, breath, listening, reply mode, state_out, forbidden performance. Provider получает playable behavior — reply speed, projection, phrase-ending, breath function, hesitation, emphasis, orientation, distance, interruption/withholding — а не только «sad / sexy / cinematic».

**DECISION:** ACCEPTED.

## 09 — SILENT REACTION + LISTENING
**PROMPT:** Разработай `SILENT_REACTION_ANCHOR` и listening engine для сцен, где персонаж действует молча.

**EXECUTION / RESULT:** Молчание становится first-class dramatic object: trigger, silent action, optional breath/Foley, silence policy, state_out, semantic anchor. Оно не считается spoken coverage и не вызывает provider request без отдельного performance sound.

**DECISION:** ACCEPTED.

## 10 — RENDER BLOCK COMPILATION
**PROMPT:** Определи универсальные правила `TTD_BLOCK / ISOLATED_TTS / VOCALIZATION / PERFORMANCE_SOUND / LOCKED_ASSET`.

**EXECUTION / RESULT:** Context-dependent dialogue → TTD; clue/identity/pronunciation/performance-critical line → isolated; vocalization только как оправданная невербальная реакция; performance sound не считается spoken text; recurring accepted sound может быть locked asset. ROOM 917 + LESSON ZERO подтверждают переносимость этой схемы.

**DECISION:** PROVEN_DRY.

## 11 — VOICE BINDING / CAST LOCK
**PROMPT:** Разработай `VOICE_BINDING_LEDGER` и доказательный voice-lock gate, исключающий lock по одному красивому sample.

**EXECUTION / RESULT:** Статусы `CANDIDATE / SMOKE_ONLY / APPROVED / LOCKED / SUPERSEDED`. Lock требует multi-state evidence, directed-change response, hard-fail pass, pair/ensemble compatibility where relevant и fatigue/listenability test. Provider request проверяется против ledger; drift = fail closed.

**DECISION:** ACCEPTED.

## 12 — PRONUNCIATION / MULTILINGUAL
**PROMPT:** Разработай pronunciation/multilingual gate и примени к LESSON ZERO RU.

**EXECUTION / RESULT:** Pronunciation map versioned и привязан к voice/request provenance. В LESSON ZERO RU критические проверки включают **«Ифа»** и **«Контакт»**; canary не может пройти без естественного произношения. Механизм переносим на имена/термины любого языка.

**DECISION:** READY_FOR_LIVE.

## 13 — PROVIDER ABSTRACTION
**PROMPT:** Спроектируй provider abstraction: ElevenLabs как первый adapter, но без vendor lock в ядре.

**EXECUTION / RESULT:** Внутренние artifacts должны оставаться provider-neutral; adapter переводит `PerformanceCompilation / SFX / Music` в конкретный API. Сохраняются model/version/voice ID, request hash и response/alignment provenance. ElevenLabs live adapter доказан ROOM 917; второй provider не доказан и не нужен как v1.0 blocker.

**DECISION:** PARTIAL / v1.x EXTENSION.

## 14 — MINIMAL PAID LIVE CANARY
**PROMPT:** Разработай минимальный paid canary, который проверяет максимум pipeline при минимальной стоимости.

**EXECUTION / RESULT:** Для LESSON ZERO выбран canary из **3 request blocks / 36 spoken units / 2163 characters / 3 voices: Narrator, Ethan, Aoife**. Он проверяет TTD, isolated narrator TTS, pronunciation, real alignment, ambience/Foley/diegetic sound и protected silence при минимальном spend.

**DECISION:** READY_FOR_LIVE.

## 15 — ALIGNMENT CONTRACT
**PROMPT:** Определи alignment contract от provider timestamps до normalized alignment и resolved sample timeline.

**EXECUTION / RESULT:** До render разрешены только semantic anchors. После accepted take: `RAW_ALIGNMENT → NORMALIZED_ALIGNMENT → RESOLVED_TIMELINE`. Synthetic fixture positions никогда не продвигаются в production timing. ROOM 917 P001/P002 показал критичность этого firewall.

**DECISION:** ACCEPTED.

## 16 — DEPENDENCY INVALIDATION / RESUME
**PROMPT:** Спроектируй dependency invalidation: что перестраивать после rerender одного блока и что нельзя трогать.

**EXECUTION / RESULT:** Изменение блока инвалидирует только зависимые anchors/cues/mix segments; независимые locked takes/assets сохраняются. DAG + hashes + checkpoints + `--resume` должны обеспечивать true selective rebuild.

**DECISION:** ACCEPTED.

## 17 — ACOUSTIC PASSPORT / POINT OF AUDITION
**PROMPT:** Разработай acoustic passport и listener point-of-audition, чтобы пространство было смысловым, а не постоянным stereo widening.

**EXECUTION / RESULT:** На сцену фиксируются room identity, listener position, sources, distance, orientation, occlusion, movement, stereo intent и mono-safe constraints. ROOM 917 доказал: высокая correlation сама по себе не дефект; узкость допустима для VO/telephone/intimacy, но не должна уничтожать authored spatial state changes.

**DECISION:** ACCEPTED.

## 18 — MICROPHONE CHOREOGRAPHY
**PROMPT:** Разработай microphone choreography: как proximity/body orientation/movement меняют performance, а не только gain/pan.

**EXECUTION / RESULT:** Close confidential, across-room, phone/media и moving speech требуют разных projection/breath/articulation/room relations. Неверную подачу нельзя правдоподобно исправить одним post gain.

**DECISION:** ACCEPTED.

## 19 — FOLEY CAUSALITY / BODY MICROTEXTURE
**PROMPT:** Разработай Foley causality + body microtexture, чтобы звук тела/объекта следовал действию и не становился декором.

**EXECUTION / RESULT:** Каждый cue требует cause/action/listener function/priority/space. Footsteps, cloth, touch, chair, breath, swallow, object handling существуют только если физически/драматургически заработаны. ROOM 917 Foley уже показал хороший spatial baseline; его следует расширять, не перестраивать.

**DECISION:** ACCEPTED.

## 20 — CLUE SOUND / ACOUSTIC IDENTITY
**PROMPT:** Разработай `CLUE_SOUND_REGISTRY + ACOUSTIC_IDENTITY_LEDGER` для доказательных звуков.

**EXECUTION / RESULT:** Clue получает immutable identity, provenance, mono-critical flag, masking immunity, order constraints и relation to music/media. ROOM 917 missing-fourth-note доказал: independently generated related sounds нельзя честно считать одной музыкальной уликой без общего pitch/identity system.

**DECISION:** ACCEPTED.

## 21 — AMBIENCE ARCHITECTURE
**PROMPT:** Разработай ambience architecture, которая предотвращает мёртвую пустоту, но не заполняет protected silence.

**EXECUTION / RESULT:** Ambience требует room/world identity, variation/loop strategy, movement/occlusion и explicit silence interaction. В полном ROOM 917 E01 исправленная Scene 3 имеет 0 s below -45 dBFS, а ранняя часть заметно более пустая; это кандидат на density/ambience repair, но не основание автоматически заполнять паузы.

**DECISION:** PROVEN_NEED.

## 22 — MUSIC DRAMATURGY
**PROMPT:** Разработай music dramaturgy: причины входа/выхода, no-music windows, motifs и связь с clue identity.

**EXECUTION / RESULT:** Каждый cue хранит function, entry cause, exit cause, motif, intensity, dialogue policy, negative implications. Wallpaper music запрещена. Если музыка участвует в clue inference, она должна ссылаться на общий musical/acoustic fact system.

**DECISION:** ACCEPTED.

## 23 — PROTECTED SILENCE
**PROMPT:** Определи protected silence как first-class mask и правила против auto-fill/auto-trim.

**EXECUTION / RESULT:** ROOM 917 содержит 6 protected-silence masks с суммарной авторской длительностью **2.94 s** в E01 intent/fixtures. Mask запрещает decorative fill, reverb-tail invasion и silence removal; допускаются только явно разрешённые baselines. Low RMS не доказывает dead air.

**DECISION:** PROVEN.

## 24 — CAUSAL OVERLAP / DENSITY
**PROMPT:** Разработай causal-overlap profile, чтобы сцена не звучала как «реплика — эффект — реплика».

**EXECUTION / RESULT:** Mix должен планировать earned overlaps между dialogue/body/ambience/SFX/music при сохранении focus owner. ROOM 917 v1.3E поднял top-level causal overlaps **1 → 8** и убрал прежний low-level провал без новых provider calls — сильное доказательство нужности layer.

**DECISION:** PROVEN.

## 25 — AUTOMIX AS ATTENTION CONTROL
**PROMPT:** Разработай AutoMix как attention controller, а не нормализатор.

**EXECUTION / RESULT:** AutoMix получает listener contract + attention state + cue priority и управляет ducking/focus/occlusion/stereo, сохраняя protected silence и clue immunity. Dialogue priority не означает вечный center-only mix.

**DECISION:** ACCEPTED.

## 26 — STEREO INTEGRITY / MONO MOBILE
**PROMPT:** Определи stereo-integrity QC: различай source stereo, stem processing и whole-master correlation; сохрани mono/mobile.

**EXECUTION / RESULT:** Whole-master correlation не может один решать PASS/FAIL. QC сравнивает source-vs-stem stereo, declared intent, phase/mono collapse и mobile translation. ROOM 917 выявил реальный mixer bug: MUSIC/CLUE_SFX были stereo в source, но downstream mixer forced mono.

**DECISION:** PROVEN.

## 27 — MASTERING VS ARTISTIC RELEASE
**PROMPT:** Определи mastering target и границу между техническим master PASS и художественным release PASS.

**EXECUTION / RESULT:** Sample rate/bit depth/loudness/true peak/clipping/LRA — необходимые, но недостаточные gates. ROOM 917 v1.2.2 был технически валиден и художественно NO-GO; следовательно technical master PASS не может сертифицировать acting/space/music/engagement.

**DECISION:** PROVEN.

## 28 — MACHINE QC FAIL-CLOSED
**PROMPT:** Собери fail-closed machine QC gates универсального build.

**EXECUTION / RESULT:** Mandatory: authority/source hash, branch contamination, unit accounting, exact text, voice binding, pronunciation, asset lock, unresolved anchors, clue order/audibility, protected silence, forbidden music, mono-critical cue flags, missing stems/assets, loudness/peak/clipping, alignment verification, repair register. Open FATAL => no `MASTER_LOCK`.

**DECISION:** ACCEPTED.

## 29 — HUMAN LISTEN GATE
**PROMPT:** Определи human-listen/blind-listener protocol, который нельзя заменить метриками.

**EXECUTION / RESULT:** Проверяются comprehension, believable performance, believable sound world, emotional result, AI distraction, role distinction, fatigue, headphones/mono/phone translation. Ни ROOM 917, ни engine v1.0 не получают release claim без фактического human evidence.

**DECISION:** OPEN_HUMAN_GATE.

## 30 — DEFECT ROUTER / EDIT BEFORE REGEN
**PROMPT:** Разработай defect router + edit-before-regenerate + selective repair policy.

**EXECUTION / RESULT:** Если exact words + voice identity + intention PASS, а дефект pause/spacing/crossfade/reaction placement — `EDIT_ONLY`. Performance/identity/text/provider failure → selective rerender. Whole-episode rerender запрещён по умолчанию. ROOM 917 v1.3E уже доказал zero-new-provider-call remix repair.

**DECISION:** PROVEN.

## 31 — ECONOMICS / COST PER ACCEPTED MINUTE
**PROMPT:** Разработай production economics: cost per accepted minute, reuse/cache, paid-call cascade и throughput metrics.

**EXECUTION / RESULT:** Считать provider characters/requests/assets, rejected takes, accepted minutes, manual minutes, reuse ratio, provider cost, repair cost и cost per accepted minute. Canary-first + edit-before-regen минимизируют spend. Пока LESSON ZERO live canary не выполнен, универсальная экономика остаётся **UNMEASURED**, а не предполагаемой.

**DECISION:** OPEN_MEASUREMENT.

## 32 — PORTABILITY / RELEASE READINESS VERDICT
**PROMPT:** Проведи финальный verdict по ROOM 917 + LESSON ZERO и определи, можно ли назвать движок законченным.

**EXECUTION / RESULT:** ROOM 917 доказал live dialogue/SFX/music provider execution, alignment, timeline/mix и selective repair. LESSON ZERO доказал second-project segmentation, **146/146 coverage**, 11 render/request blocks, pronunciation/voice-map structure, **14/14 sound cues** и fail-closed dry production. Значит архитектурная переносимость доказана.

Но `IVDIVO AUDIO NOVEL ENGINE v1.0 — PRODUCTION READY` пока преждевременно. Открыты пять доказательств:
1. LESSON ZERO 3-request live canary с реальными voice IDs.
2. Real alignment → resolved timeline → accepted mini-mix.
3. Human listen / AI-distraction / comprehension gate.
4. Cost per accepted minute + manual minutes + repair/reuse metrics.
5. One-command CLI / resume / selective rebuild regression.

**DECISION:** `RELEASE_CANDIDATE / LIVE_PORTABILITY_GATE_OPEN`.

---

# 32-RUN SCORECARD

- ACCEPTED / PROVEN / PROVEN_DRY: **26** work areas.
- READY_FOR_LIVE: pronunciation + low-cost portability canary.
- PARTIAL but non-blocking for v1.0: multi-provider abstraction beyond ElevenLabs.
- OPEN evidence gates: human listening, measured economics, live second-project portability, one-command orchestration regression.
- No evidence supports another generic architecture rewrite before these gates are run.