#!/usr/bin/env python3
"""Проверка реестра карт на совпадения параметров."""
import csv, collections, sys

KEY = ['yarus','stavka','domen','registr','sreda','instrument','konfiguraciya','moment','kadr']

rows = [r for r in csv.DictReader(open('REESTR.csv', encoding='utf-8'))
        if r['status'] != 'pending']

if not rows:
    print('Реестр пуст.'); sys.exit()

print(f'Карт в реестре: {len(rows)}\n')

# полные совпадения ключа
c = collections.Counter(tuple(r[k] for k in KEY) for r in rows)
dupes = {k: n for k, n in c.items() if n > 1}
if dupes:
    print('ПОЛНЫЕ СОВПАДЕНИЯ КЛЮЧА:')
    for k, n in dupes.items():
        who = [r['nomer'] for r in rows if tuple(r[x] for x in KEY) == k]
        print(f'  {n} карт: {", ".join(who)}')
else:
    print('Полных совпадений ключа нет.')

# повтор параметра в трёх подряд
print('\nПОВТОР В ТРЁХ ПОДРЯД:')
srt = sorted(rows, key=lambda r: r['nomer'])
found = False
for i in range(len(srt) - 2):
    a, b, cc = srt[i], srt[i+1], srt[i+2]
    for k in KEY:
        if a[k] == b[k] == cc[k] and a[k]:
            print(f'  {k}="{a[k]}" в картах {a["nomer"]}, {b["nomer"]}, {cc["nomer"]}')
            found = True
if not found:
    print('  нет')

# распределение по осям
print('\nРАСПРЕДЕЛЕНИЕ:')
for k in KEY:
    d = collections.Counter(r[k] for r in rows if r[k])
    if d:
        top = ', '.join(f'{v}×{n}' for v, n in d.most_common(4))
        print(f'  {k:16} {top}')
