# OBJECTIVE_CARDS_EXPORTS_MANIFEST_v0.1

Статус: DRAFT / EXPORT MANIFEST  
Дата: 2026-07-22  
Связанный модуль: `OBJECTIVE_CARDS_v0.1_DRAFT`

## Назначение

Этот файл фиксирует полный набор локально созданных экспортов для модуля карт целей. Полная рабочая таблица также сохранена как нативная Google Sheet:

https://docs.google.com/spreadsheets/d/1b1wTzRAfhsjjexfhSNI4XibNYXLPrqlMjODNj2QoP38/edit

## Экспорты

| Файл | Размер | SHA-256 | Статус |
|---|---:|---|---|
| `IVDIVO_objective_cards_v0_1_DRAFT.xlsx` | 39,889 bytes | `4e0306c4ed79ecc2efae41a45d44a9c8e9cd207671f2e656144bbcc421bb14eb` | создан локально; бинарный XLSX |
| `IVDIVO_objective_cards_v0_1_DRAFT.csv` | 45,947 bytes | `78a9b40368d6a11c24a5137674a222da020d1fe690a25ce017575b3f8f9270d8` | создан локально; UTF-8 CSV |
| `OBJECTIVE_CARDS_v0.1_DRAFT.md` | 48,934 bytes | `7dfaaf521f588a6a093faf6c8a02883eb295113df8c3cbf4d88854dedf576e4a` | создан локально; полный Markdown |
| `objective_cards_preview.png` | 242,409 bytes | `a2fe8012b16ae4c5206e1bbfce07e3843b259a31061074f934372f20379f3a7c` | создан локально; preview PNG |

## Ограничение коннектора

GitHub connector in this environment writes UTF-8 repository text files through `create_file` / `update_file`. It does not expose a direct local-file upload parameter for binary `.xlsx` / `.png` files. Therefore the authoritative editable spreadsheet is the Google Sheet above, while this manifest records local export names, sizes, and checksums.

## Что уже находится в GitHub

- `docs/04_CARDS_AND_COMPONENTS/OBJECTIVE_CARDS_v0.1_DRAFT.md` — GitHub Markdown specification of the objective-card module.
- `docs/04_CARDS_AND_COMPONENTS/OBJECTIVE_CARDS_EXPORTS_MANIFEST_v0.1.md` — this export manifest.
- `CHANGELOG.md`, `MASTER_INDEX.md`, `OPEN_QUESTIONS.md` — updated navigation and project tracking.

## Governance

- Status remains DRAFT / TO-VERIFY.
- No APPROVED decision is created by these exports.
- Personal goals remain cooperative and must not become hidden betrayal mechanics.