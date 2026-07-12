# PROMPT EXECUTION MASTER 100 v0.2 DRAFT

Версия: v0.2  
Дата: 2026-07-12  
Статус: DRAFT / CANON ARCHITECTURE RESOLVED  
Код: AI-100  
Ветка: `agent/execute-100-game-workstreams`

## Назначение

Документ переводит библиотеку из 100 промтов в управляемую производственную систему. Все задачи получили целевой результат, зависимости, статус и критерий завершения. Архитектура миров зафиксирована DEC-015, однако числа, баланс, тексты карт, финальный лор, визуал и производство остаются DRAFT до тестов и отдельных решений.

## Утверждённая архитектурная опора

[APPROVED / FOUNDER-DECISION]

- Пять вертикальных миров: Физический → Тонкий → Метагалактический → Огненный → Синтезный.
- Параллельные миры являются орбиталями относительно вертикальной оси.
- Известные орбитали: Ад, Рай, Аидия, Демонский и Омарный миры.
- Орбитали не являются обязательными ступенями восхождения.
- DEC-003 и восьмимировая вертикаль имеют статус SUPERSEDED.
- Источник истины: `WORLD_ARCHITECTURE_v0.2_APPROVED.md`, DEC-015.

## Продуктовое направление

[WORKING HYPOTHESIS / FOUNDER DIRECTION]

- Базовая коробка является законченной самостоятельной игрой.
- Она подробно раскрывает Физический мир, Убежище, территорию, Корневую угрозу, портал, четыре роли и первое малое восхождение.
- Полноценные Тонкий, Метагалактический, Огненный и Синтезный миры рассматриваются как крупные дополнения после освоения базы.
- Орбитали рассматриваются как модульные кампании, фракционные наборы, кольца, антигерои или мини-дополнения.
- Порядок выпуска остаётся REVIEW и не является частью DEC-015.

## Статусы

- `INITIAL DRAFT COMPLETE` — создана исходная архитектура и критерии; требуется детализация или тест.
- `CANON GROUNDED` — задача имеет утверждённую архитектурную основу, но содержимое ещё не финализировано.
- `TO-VERIFY` — необходим источник, решение, тест или карта связей.
- `REQUIRES PLAYTEST` — числа и UX нельзя утверждать аналитически.
- `DEFERRED` — задача не должна опережать доказательство core loop.

## Карта 100 задач

### Блок 1 — архитектура проекта и GitHub

1. Аудит репозитория — INITIAL DRAFT COMPLETE.
2. Финальная структура папок — INITIAL DRAFT COMPLETE.
3. Коды документов — INITIAL DRAFT COMPLETE.
4. Карта источников истины — INITIAL DRAFT COMPLETE; обновлена DEC-015.
5. Граф зависимостей — INITIAL DRAFT COMPLETE.
6. Аудит журнала решений — INITIAL DRAFT COMPLETE; DEC-003 superseded, DEC-015 added.
7. Гейты разработки — INITIAL DRAFT COMPLETE.
8. Единый словарь — CANON GROUNDED / player-facing terminology TO-VERIFY.
9. Формы документов — INITIAL DRAFT COMPLETE.
10. Дорожная карта — INITIAL DRAFT COMPLETE.

Результат: `blocks/BLOCK_01_PROJECT_AND_GITHUB_v0.1_DRAFT.md` плюс DEC-015/WORLD-002.

### Блок 2 — первая базовая игра

11. Однострочник и обещание — INITIAL DRAFT COMPLETE.
12. Границы первой коробки — INITIAL DRAFT COMPLETE.
13. Фантазия роли игрока — INITIAL DRAFT COMPLETE.
14. Core loop — REQUIRES PLAYTEST.
15. Три слоя Корневой угрозы — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
16. Портал базовой игры — REQUIRES PLAYTEST.
17. Четыре роли — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
18. Экономика базовой игры — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
19. Кампания первой коробки — INITIAL DRAFT COMPLETE.
20. Состав коробки — INITIAL DRAFT COMPLETE / production TO-VERIFY.

Результат: `blocks/BLOCK_02_BASE_GAME_v0.1_DRAFT.md`.

### Блок 3 — миры как дополнения

21. Мастер-форма дополнения — INITIAL DRAFT COMPLETE.
22. Тонкий мир — CANON GROUNDED / MECHANICS DRAFT.
23. Метагалактический мир — CANON GROUNDED / MECHANICS DRAFT.
24. Огненный мир — CANON GROUNDED / MECHANICS DRAFT.
25. Синтезный мир — CANON GROUNDED / MECHANICS DRAFT.
26. Орбитальные миры — CANON GROUNDED / ORBIT MAP TO-VERIFY.
27. Наборы антигероев — INITIAL DRAFT COMPLETE.
28. Совместимость дополнений — INITIAL DRAFT COMPLETE.
29. Междополнительная прогрессия — INITIAL DRAFT COMPLETE.
30. Великая Конъюнкция — INITIAL DRAFT COMPLETE / DEFERRED.

Результат: `blocks/BLOCK_03_WORLD_EXPANSIONS_v0.2_DRAFT.md`.

### Блок 4 — сюжет и кампании

31. Сюжетная грамматика — INITIAL DRAFT COMPLETE.
32. Форма сценария — INITIAL DRAFT COMPLETE.
33. Обучающий сценарий — INITIAL DRAFT COMPLETE.
34. Первый сценарий с Корнем — INITIAL DRAFT COMPLETE.
35. Эмоциональная дуга — INITIAL DRAFT COMPLETE.
36. Ветвления — INITIAL DRAFT COMPLETE.
37. Диалоговая система — INITIAL DRAFT COMPLETE.
38. Социальные сцены — INITIAL DRAFT COMPLETE.
39. Система финалов — INITIAL DRAFT COMPLETE.
40. Процедурные миссии — INITIAL DRAFT COMPLETE / REQUIRES CONTENT TEST.

Результат: `blocks/BLOCK_04_STORY_AND_CAMPAIGNS_v0.1_DRAFT.md`.

### Блок 5 — персонажи, фракции и антигерои

41. Паспорт персонажа — INITIAL DRAFT COMPLETE.
42. Четыре героя — INITIAL DRAFT COMPLETE / names TO-VERIFY.
43. Личные дуги — CANON GROUNDED / CONTENT DRAFT.
44. Колоды ролей — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
45. Главный антигерой — INITIAL DRAFT COMPLETE / lore TO-VERIFY.
46. Трагический союзник — INITIAL DRAFT COMPLETE.
47. Фракции территории — INITIAL DRAFT COMPLETE.
48. Система отношений — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
49. Жители миров — CANON GROUNDED / INDIVIDUAL PASSPORTS TO-VERIFY.
50. Боссы и Проявления — INITIAL DRAFT COMPLETE.

Результат: `blocks/BLOCK_05_CHARACTERS_AND_FACTIONS_v0.1_DRAFT.md`.

### Блок 6 — карты, Инструменты и экономика

51. Таксономия карт — INITIAL DRAFT COMPLETE.
52. Шаблон карты — INITIAL DRAFT COMPLETE.
53. Карты вспоминания — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
54. Система Инструментов — INITIAL DRAFT COMPLETE.
55. 30 Инструментов — INITIAL DRAFT COMPLETE / balance TO-VERIFY.
56. Карты законов — INITIAL DRAFT COMPLETE.
57. Карты условий — INITIAL DRAFT COMPLETE.
58. Колода угроз — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
59. Награды и открытия — INITIAL DRAFT COMPLETE.
60. Математическая модель карт — REQUIRES PLAYTEST DATA.

Результат: `blocks/BLOCK_06_CARDS_TOOLS_ECONOMY_v0.1_DRAFT.md`.

### Блок 7 — поля, компоненты и интерфейс

61. Базовое поле — INITIAL DRAFT COMPLETE.
62. Кольца и орбитали — CANON GROUNDED / production TO-VERIFY.
63. Зоны и накладки — INITIAL DRAFT COMPLETE.
64. Центральный портал — INITIAL DRAFT COMPLETE / REQUIRES UX TEST.
65. Планшеты игроков — INITIAL DRAFT COMPLETE.
66. Убежище — INITIAL DRAFT COMPLETE.
67. Поля дополнений — CANON GROUNDED / DESIGN DRAFT.
68. Иконографика — INITIAL DRAFT COMPLETE / visual TO-VERIFY.
69. PnP — INITIAL DRAFT COMPLETE.
70. Стоимость компонентов — DEFERRED UNTIL PROTOTYPE.

Результат: `blocks/BLOCK_07_BOARDS_COMPONENTS_UI_v0.1_DRAFT.md`.

### Блок 8 — правила, баланс и тестирование

71. Структура правил — INITIAL DRAFT COMPLETE.
72. Обучение — INITIAL DRAFT COMPLETE.
73. Памятки — INITIAL DRAFT COMPLETE.
74. Setup/teardown — INITIAL DRAFT COMPLETE / REQUIRES PHYSICAL TEST.
75. Доступность — INITIAL DRAFT COMPLETE.
76. Соло и дуо — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
77. Защита от альфа-игрока — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
78. Математический баланс — REQUIRES DATA.
79. Мастер-протокол тестов — INITIAL DRAFT COMPLETE.
80. Форма партии — INITIAL DRAFT COMPLETE.

Результат: `blocks/BLOCK_08_RULES_BALANCE_TESTING_v0.1_DRAFT.md`.

### Блок 9 — эмоции, азарт и социальный опыт

81. Эмоциональная карта партии — INITIAL DRAFT COMPLETE.
82. Ритм наград — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
83. Опыт победы — INITIAL DRAFT COMPLETE.
84. Интересное поражение — INITIAL DRAFT COMPLETE.
85. Push-your-luck — INITIAL DRAFT COMPLETE / REQUIRES PLAYTEST.
86. Разговоры за столом — INITIAL DRAFT COMPLETE.
87. Памятные истории — INITIAL DRAFT COMPLETE.
88. Юмор и отдых — INITIAL DRAFT COMPLETE.
89. Реиграбельность — INITIAL DRAFT COMPLETE / REQUIRES REPEAT TESTS.
90. Слепой эмоциональный тест — INITIAL DRAFT COMPLETE.

Результат: `blocks/BLOCK_09_EMOTION_RISK_SOCIAL_v0.1_DRAFT.md`.

### Блок 10 — визуал, производство, Kickstarter и цифровой слой

91. Визуальная библия — INITIAL DRAFT COMPLETE / art TO-VERIFY.
92. Коды пяти вертикальных миров и орбиталей — CANON GROUNDED / ART DRAFT.
93. Art brief — INITIAL DRAFT COMPLETE.
94. 50 art briefs — DEFERRED UNTIL COMPONENT LOCK.
95. Производственная спецификация — DEFERRED UNTIL PROTOTYPE.
96. Kickstarter — DEFERRED UNTIL BLIND TESTS.
97. Пятилетняя линейка — INITIAL DRAFT COMPLETE / business TO-VERIFY.
98. Цифровой компаньон — INITIAL DRAFT COMPLETE.
99. Локализация — INITIAL DRAFT COMPLETE.
100. Интеграционный аудит — INITIAL DRAFT COMPLETE; повторить после тестов.

Результат: `blocks/BLOCK_10_VISUAL_PRODUCTION_MARKET_v0.1_DRAFT.md`.

## Обновлённый критический путь

1. **Выполнено:** разрешена каноническая коллизия миров — DEC-015/WORLD-002.
2. Зафиксировать окончательный scope первой коробки.
3. Сделать один работающий core loop.
4. Проверить Корневую угрозу.
5. Проверить кольца, орбитали и качество переходов.
6. Проверить одно малое открытие после победы.
7. Создать карту привязки орбиталей к вертикальным мирам.
8. Только затем расширять кампанию и дополнения.

## Запрет на ложную завершённость

Решение канона не доказывает играбельность. Документы ветки не подтверждают баланс, эмоциональный эффект, стоимость производства или коммерческий успех без бумажных и слепых тестов.
