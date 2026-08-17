# Маршрут — конструктор путешествий

Полноценный веб-сервис для планирования поездок: пользователь выбирает город и даты, собирает маршрут вручную или получает автоматический план по интересам и бюджету. В маршруте доступны избранное, интерактивная карта и сохранение поездок.

## Возможности

- Регистрация, вход и JWT-защита личных данных.
- Каталог стран, городов и реальных достопримечательностей с поиском и фильтрами.
- Личное избранное мест.
- Создание, изменение и удаление поездок.
- Ручное добавление мест, времени и заметок в маршрут.
- Автоматическое формирование маршрута по датам, интересам и бюджету.
- Карта Leaflet + OpenStreetMap с маршрутом и фильтром по дням.
- Адаптивный React-интерфейс для desktop и mobile.

## Технологии

Backend: Python, FastAPI, SQLAlchemy 2, Pydantic, Alembic, PostgreSQL, PyJWT, Argon2.

Frontend: React, JavaScript, Vite, React Router, Leaflet, React Leaflet, CSS.

## Структура

```text
.
├── backend/
│   ├── alembic/              # миграции PostgreSQL
│   ├── app/
│   │   ├── api/v1/           # REST endpoints
│   │   ├── core/             # настройки, БД, безопасность
│   │   ├── models/           # SQLAlchemy-модели
│   │   ├── schemas/          # Pydantic-схемы
│   │   ├── seed.py           # начальные страны, города и места
│   │   └── main.py           # FastAPI-приложение
│   ├── tests/
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/              # API-клиент
    │   ├── auth/             # сессия и защищённые маршруты
    │   ├── components/       # layout, карта, уведомления
    │   └── pages/            # страницы приложения
    └── package.json
```

## Требования

- Python 3.11+ (проект проверен с Python 3.13).
- PostgreSQL 15+.
- Node.js 20+ и npm.

## PostgreSQL и backend

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE trip_constructor;
```

В корне проекта создайте и активируйте виртуальное окружение:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Создайте `backend/.env` на основе `backend/.env.example`. Задайте актуальные пароль PostgreSQL и длинный случайный `TRIP_JWT_SECRET_KEY`:

```env
TRIP_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/trip_constructor
TRIP_JWT_SECRET_KEY=replace-with-a-long-random-secret
TRIP_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Установите зависимости, примените миграции и загрузите стартовые данные:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m alembic upgrade head
..\.venv\Scripts\python.exe -m app.seed
```

Запустите FastAPI:

```powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend доступен по адресу `http://127.0.0.1:8000`, Swagger UI — `http://127.0.0.1:8000/docs`, health-check — `http://127.0.0.1:8000/api/v1/health`.

## Frontend

Создайте `frontend/.env` на основе `frontend/.env.example`:

```env
VITE_API_URL=http://localhost:8000
```

Установите зависимости и запустите Vite в отдельном терминале:

```powershell
cd frontend
npm install
npm run dev
```

Приложение будет доступно по адресу `http://localhost:5173`.

Production-сборка frontend:

```powershell
cd frontend
npm run build
```

## Проверки

Запуск backend-тестов:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q
```

Проверка согласованности моделей и миграций Alembic:

```powershell
cd backend
..\.venv\Scripts\python.exe -m alembic check
```

Перед демонстрацией проекта рекомендуется выполнить последовательно `alembic upgrade head`, `python -m app.seed`, `pytest -q` и `npm run build`.
