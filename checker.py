"""
Проверка решений.

    python checker.py           # проверить всё, что уже решено
    python checker.py sql 07    # одну задачу

Правильные ответы хранятся в answers.json в виде хешей: подсмотреть их нельзя,
но можно узнать, совпал ли твой результат.
"""

import hashlib
import json
import math
import runpy
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


# ---------- приведение результата к общему виду ----------

def _value(v):
    if v is None:
        return None
    if hasattr(v, 'item') and not isinstance(v, (str, bytes)):   # numpy-числа
        v = v.item()
    if hasattr(v, 'isoformat'):                                  # даты
        return v.isoformat()[:10]
    if isinstance(v, bool):
        v = int(v)
    if isinstance(v, (int, float)):
        if isinstance(v, float) and math.isnan(v):
            return None
        return f'{round(float(v), 2):.2f}'
    return str(v).strip()


def _rows_from_pandas(obj):
    import pandas as pd
    if isinstance(obj, pd.Series):
        obj = obj.to_frame()
    if isinstance(obj, pd.DataFrame):
        unnamed = all(n is None for n in obj.index.names)
        obj = obj.reset_index(drop=unnamed)   # именованный индекс (после groupby) — это данные
        return [tuple(r) for r in obj.itertuples(index=False, name=None)]
    if isinstance(obj, (pd.Index, list, tuple)) or type(obj).__name__ == 'ndarray':
        return [(v,) for v in list(obj)]
    return [(obj,)]


def normalize(result, ordered=False):
    if isinstance(result, list) and result and isinstance(result[0], tuple):
        rows = result                                     # строки из SQL
    elif isinstance(result, list) and not result:
        rows = []
    else:
        rows = _rows_from_pandas(result)
    rows = [[_value(v) for v in r] for r in rows]
    return rows if ordered else sorted(rows, key=lambda r: json.dumps(r, ensure_ascii=False))


def fingerprint(rows):
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False).encode()).hexdigest()


# ---------- запуск решений ----------

def run_sql(path):
    con = sqlite3.connect(ROOT / 'data' / 'shop.db')
    return con.execute(path.read_text(encoding='utf-8')).fetchall()


def run_pandas(path):
    ns = runpy.run_path(str(path))
    if 'result' not in ns:
        raise ValueError('в файле нет переменной result')
    return ns['result']


def check(kind, num, answers):
    ext = 'sql' if kind == 'sql' else 'py'
    path = ROOT / kind / f'{num}.{ext}'
    if not path.exists():
        return None, ''
    expected = answers[kind][num]
    try:
        raw = run_sql(path) if kind == 'sql' else run_pandas(path)
        rows = normalize(raw, expected['ordered'])
    except Exception as e:
        return False, f'ошибка: {e}'
    if fingerprint(rows) == expected['hash']:
        return True, ''
    hint = f"строк {len(rows)}, ожидалось {expected['rows']}" if len(rows) != expected['rows'] else 'значения не совпали'
    if expected['ordered']:
        hint += ', важен порядок строк'
    return False, hint


def main():
    import os
    os.chdir(ROOT)
    answers = json.loads((ROOT / 'answers.json').read_text(encoding='utf-8'))
    targets = [(sys.argv[1], sys.argv[2].zfill(2))] if len(sys.argv) == 3 else \
        [(k, n) for k in ('sql', 'pandas') for n in answers[k]]
    solved = total = 0
    for kind, num in targets:
        ok, msg = check(kind, num, answers)
        if ok is None:
            continue
        total += 1
        solved += ok
        print(f"{'✅' if ok else '❌'} {kind} {num}  {msg}")
    all_tasks = sum(len(v) for v in answers.values())
    if total == 0:
        print('пока нет решений: создай файл, например sql/01.sql')
    else:
        print(f'\nрешено верно: {solved} из {total} проверенных · всего задач: {all_tasks}')


if __name__ == '__main__':
    main()
