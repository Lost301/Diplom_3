# Diplom_3 — UI-автотесты для Stellar Burgers

UI-автотесты веб-приложения [Stellar Burgers](https://stellarburgers.education-services.ru/)
на Python + Selenium + pytest с отчётом Allure. Используется паттерн Page Object.

## Что покрыто

**Основная функциональность (раздел «Конструктор»):**
1. Переход по клику на «Конструктор» из другого раздела (лента заказов).
2. Переход по клику на раздел «Лента заказов».
3. Клик на ингредиент открывает всплывающее окно с деталями.
4. Всплывающее окно закрывается кликом по крестику.
5. При добавлении ингредиента в заказ счётчик ингредиента увеличивается.

**Раздел «Лента заказов» (требуется авторизация):**
6. При создании нового заказа счётчик «Выполнено за всё время» увеличивается.
7. При создании нового заказа счётчик «Выполнено за сегодня» увеличивается.
8. После оформления заказа его номер появляется в разделе «В работе».

## Стек

- Python 3.14
- selenium 4.47.0
- pytest 9.1.1
- allure-pytest 2.16.0
- requests 2.34.2 (создание/удаление тестовых пользователей через API)

## Запуск

```bash
pip install -r requirements.txt

# Chrome (по умолчанию), headless
python -m pytest tests/ -v

# с указанием браузера
python -m pytest tests/ --browser chrome -v
python -m pytest tests/ --browser firefox -v   # требуется установленный Firefox

# с формированием результатов Allure
python -m pytest tests/ --alluredir=allure-results -v
```

## Отчёт Allure

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

## Структура проекта

```
.
├── conftest.py          # фикстуры: driver (параметр --browser), открытие страниц, пользователь через API
├── data.py              # URL-ы приложения и API
├── helpers.py           # генерация тестовых данных (uuid)
├── locators.py          # селекторы страниц
├── pages/
│   ├── __init__.py
│   ├── base_page.py     # базовый класс Page Object
│   ├── main_page.py     # главная / конструктор
│   └── feed_page.py     # лента заказов
├── tests/
│   ├── __init__.py
│   ├── test_constructor.py  # тесты 1–5
│   └── test_feed.py         # тесты 6–8
├── requirements.txt
└── README.md
```

## Особенности

- Авторизация в UI-тестах выполняется через инъекцию токенов (`accessToken` /
  `refreshToken`) в `localStorage` с последующим `driver.refresh()` — тестовый
  пользователь предварительно создаётся через API (`POST /api/auth/register`)
  и удаляется после теста (`DELETE /api/auth/user`).
- Добавление ингредиента в конструктор выполняется через JS-симуляцию событий
  HTML5 drag&drop (`dragstart`/`dragover`/`drop`), так как стандартный
  `ActionChains` не работает с React DnD.
- Параметризация браузера: `--browser chrome|firefox` (по умолчанию `chrome`).
  Firefox готов к запуску, но на машине разработки не установлен.
