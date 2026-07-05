# Портфолио Даниила Бритова

Центральный сайт с девятью проверяемыми проектами: пятью web-кейсами и четырьмя Python-системами. Каталог хранится в `assets/data/projects.json` и фильтруется без фреймворков.

## Локальный запуск

```bash
python3 -m http.server 8000
```

Откройте `http://localhost:8000`. Не открывайте `index.html` напрямую через `file://`: браузер блокирует `fetch()` к JSON-каталогу.

## Проверка

```bash
python3 -m pytest tests -v
PYTHONPATH=. python3 scripts/check_static_site.py . --portfolio
python3 scripts/audit_portfolio.py .
node --test tests/portfolio-state.test.js
node --check assets/js/portfolio-state.js
node --check assets/js/main.js
```

В каталоге `resume/` лежат публичные PDF- и DOCX-версии резюме; ссылки на них доступны в блоке контактов. Публичные URL каталога проверяются скриптом аудита.

---

# Бритов Даниил

Python-разработчик: Telegram-боты, AI-интеграции, API, автоматизация и сайты для малого бизнеса.

Собираю системы, которые принимают заявки, записывают клиентов, отвечают по базе знаний, связывают веб-интерфейс с базой данных и снимают ручную работу. Для кейсов подготовлены код, инструкции запуска и автотесты.

**Открыт к новым проектам.**

[Портфолио](https://brtvd07.github.io) · [Telegram @brtvd_07](https://t.me/brtvd_07) · [Email](mailto:danechkabritov@yandex.ru)

## Чем могу помочь

- Telegram-бот для заявок, записи, уведомлений и отчётов.
- AI-помощник с поиском ответа в базе знаний.
- API и бизнес-логика для веб-интерфейса, бота и внешних сервисов.
- Адаптивный сайт, каталог, калькулятор или личный кабинет.

## Технологии

`Python` · `FastAPI` · `Telegram Bot API` · `SQLite` · `HTML` · `CSS` · `JavaScript` · `pytest` · `Docker` · `GitHub Actions`

## Избранные проекты

<!-- featured-project -->
### [Telegram Freelance Agent](https://github.com/brtvd07/telegram-freelance-agent)

Поиск и фильтрация технических заказов, Telegram-управление и локальный порядок обработки заказа.

<!-- featured-project -->
### [AI Support Bot](https://github.com/brtvd07/ai-support-bot)

FastAPI и Telegram-адаптер с поиском релевантного контекста, grounded-ответами и офлайн-демо.

<!-- featured-project -->
### [Booking CRM Bot](https://github.com/brtvd07/booking-crm-bot)

Запись по слотам без дублей, отмена, уведомления, API и демонстрационная CRM-панель.

<!-- featured-project -->
### [NordMarket](https://github.com/brtvd07/nordmarket)

Демонстрационный интернет-магазин: поиск, фильтры, сортировка, корзина, промокод и безопасный сценарий оформления.

<!-- featured-project -->
### [СтройРасчёт](https://github.com/brtvd07/stroyraschet)

Демонстрационный сайт услуг с пошаговым калькулятором, детализацией сметы и переходом в Telegram.

<!-- featured-project -->
### [FlowDesk](https://github.com/brtvd07/flowdesk)

Демонстрационная B2B-панель: заявки, статусы, поиск, фильтры, адаптивные таблицы и графики.

## Связаться

Быстрее всего — [написать в Telegram](https://t.me/brtvd_07). Для подробного описания можно использовать [email](mailto:danechkabritov@yandex.ru).
