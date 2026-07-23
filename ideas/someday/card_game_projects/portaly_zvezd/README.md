# Порталы Звёзд

Семейная карточная игра о порталах между мирами. 2–5 игроков, 30–40 минут,
вес 1.8–2.0. Дочерний проект относительно IVDIVO GAME MASTER — не
использует терминологию ИВДИВО (терминологический файрвол соблюдён),
рассматривается как возможный стратегический разгонный тайтл перед
основной игрой (см. kickstarter/23_prelaunch_strategy.md).

**Статус документов:** всё ниже — PROPOSED. Ничего не имеет статуса
Approved — это решение только Ярослава.

## Структура

```
data/                     — единый источник правды (CSV), кормит и
                             симулятор, и генератор печати
  portal_cards.csv         24 карты Порталов
  adventure_cards.csv      24 карты Приключений
  action_cards.csv         18 карт Действий
  secret_objectives.csv    24 тайные цели
  characters.csv           6 персонажей

design/
  05_plot_twists.md         12 неожиданных элементов
  09_irish_layer.md         ирландский слой + НАЙДЕНА И ИСПРАВЛЕНА
                             географическая ошибка (Шотландия vs Ирландия)
  10_rules_one_page.md      правила на 1 страницу

code/
  simulator/                 балансировочный симулятор — РЕАЛЬНО ЗАПУЩЕН
    engine.py, players.py, run_simulation.py, config.yaml
    results.csv               сырые данные 10 000 партий
    REPORT.md                 ГЛАВНЫЙ ФАЙЛ — читать первым: Проводник
                               сломан (51% винрейт), runaway-leader 48%,
                               баг зависания на 2 игроках
  web_prototype/
    portals_prototype.html    играбельный hot-seat прототип, откройте
                               в браузере, экспорт лога партии в JSON
  print_and_play/
    generate_pdf.py           CSV -> PDF за секунды при смене баланса

output_pdf/
  portals_print_and_play.pdf  готовый PDF, 24 карты Порталов
  adventures_print_and_play.pdf  24 карты Приключений

art/
  16_art_bible.md, 17_illustration_prompts.md, 19_iconography.md

playtest/
  20_playtest_protocol.md
  21_analysis_methodology.md
  22_gap_audit.md            9 честных находок по всему материалу —
                              включая 3 блокера перед печатью прототипа

kickstarter/
  23_prelaunch_strategy.md, 24_campaign_structure.md
```

## Что читать в первую очередь

1. `code/simulator/REPORT.md` — реальные цифры, не гипотезы
2. `playtest/22_gap_audit.md` — сведённый список того, что нужно решить
3. `design/09_irish_layer.md` — важная гео-правка для 481A

## Три блокера перед печатью физического прототипа (из gap-аудита)
1. Проводник структурно сильнее остальных персонажей — нужна правка
2. Runaway-leader 48% — выше комфортного порога вашего же приоритета
3. Партии на 2 игроках иногда зависают до потолка симулятора — не
   расследовано, требует отдельного технического разбора

## Как запустить симулятор заново после правок баланса
```
cd code/simulator
python3 run_simulation.py
```
Меняете числа в `config.yaml` или `../../data/*.csv` — прогоняете заново.

## Как обновить print-and-play после правок карт
```
cd code/print_and_play
python3 generate_pdf.py ../../data/portal_cards.csv ../../output_pdf/portals_print_and_play.pdf portal
```
