### ежедневная практика · daily practice

каждый день решаю задачу по sql или pandas на данных спортивного магазина. 30 задач по sql и 15 по pandas, от простых выборок до оконных функций и rfm-анализа, решения проверяются автоматически
*one sql or pandas task a day on a sports shop dataset: 30 sql and 15 pandas tasks, from simple selects to window functions and rfm, auto-checked*

`sql` `sqlite` `pandas` `python`

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nnearss/daily-practice/blob/main/playground.ipynb)

---

**задачи** · *tasks*: [sql](sql/TASKS.md) · [pandas](pandas/TASKS.md)

**данные** · *data*: магазин спорттоваров за 2025 год. 200 клиентов, 40 товаров в 6 категориях, 1500 заказов
*a sports shop in 2025: 200 customers, 40 products, 1,500 orders*

```
customers   (id, name, city, signup_date)
products    (id, name, category, price)
orders      (id, customer_id, order_date, status)      -- delivered / cancelled / processing
order_items (order_id, product_id, quantity)
```

база sqlite в `data/shop.db`, те же таблицы в csv рядом
*sqlite database in `data/shop.db`, the same tables as csv*

---

**как решать** · *workflow*

1. открой [песочницу в colab](https://colab.research.google.com/github/nnearss/daily-practice/blob/main/playground.ipynb) и пробуй запрос, пока не получится
2. на github зайди в папку `sql` или `pandas` → **add file → create new file**, назови по номеру задачи: `07.sql` или `03.py`
3. вставь решение и нажми **commit changes**
4. в песочнице запусти последнюю ячейку: ✅ значит верно, ❌ подскажет, что не так

для pandas ответ кладётся в переменную `result`. подсмотреть правильные ответы нельзя: в `answers.json` лежат только их хеши
*for pandas, put the answer in `result`. answers are stored as hashes, so you can check but not peek*

локально · *locally*: `python checker.py` проверит всё, `python checker.py sql 07` одну задачу

---

**прогресс** · *progress*

sql: ▢▢▢▢▢▢▢▢▢▢ ▢▢▢▢▢▢▢▢▢▢ ▢▢▢▢▢▢▢▢▢▢
pandas: ▢▢▢▢▢▢▢▢▢▢ ▢▢▢▢▢

*заменяй ▢ на ✅ по мере решения · replace ▢ with ✅ as you go*
