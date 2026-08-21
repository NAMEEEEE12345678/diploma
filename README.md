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



<img width="1536" height="1024" alt="34e29086-dc02-46a4-9de5-b37da448e566" src="https://github.com/user-attachments/assets/9b1b708c-a97e-47f0-8f74-a198634bd4f6" />





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
И будет видна такая работа:


<img width="1885" height="900" alt="Снимок экрана (165)" src="https://github.com/user-attachments/assets/eeadb971-fb86-4c1a-95a6-46d85eb5533d" />
<img width="1896" height="906" alt="Снимок экрана (166)" src="https://github.com/user-attachments/assets/f85a2551-3e72-4edf-b31d-2a66f1b7e58c" />
<img width="1900" height="899" alt="Снимок экрана (167)" src="https://github.com/user-attachments/assets/e2e51c53-5453-41c8-81d2-69428826b531" />
<img width="1897" height="898" alt="Снимок экрана (168)" src="https://github.com/user-attachments/assets/c94faf61-6783-4bd6-a2e5-eecdd07175e1" />
<img width="1896" height="907" alt="Снимок экрана (169)" src="https://github.com/user-attachments/assets/6022b8dd-83d0-41cd-ad25-139f6edbc3e2" />
<img width="1892" height="897" alt="Снимок экрана (170)" src="https://github.com/user-attachments/assets/2a859422-2e62-49f0-a9c0-ae0d2f4870ba" />
<img width="1897" height="912" alt="Снимок экрана (171)" src="https://github.com/user-attachments/assets/561679ad-d864-4e62-901b-f154527d4f79" />
<img width="1900" height="888" alt="Снимок экрана (172)" src="https://github.com/user-attachments/assets/8ad5cefb-a20e-477d-a57d-d2f5e8464cfa" />
<img width="1895" height="885" alt="Снимок экрана (173)" src="https://github.com/user-attachments/assets/9e3a1590-d994-41c5-88f2-d418c9a9023b" />
<img width="1897" height="901" alt="Снимок экрана (174)" src="https://github.com/user-attachments/assets/97f2be5c-5854-4b5c-947c-1ed2b5e5ae52" />
<img width="1899" height="892" alt="Снимок экрана (175)" src="https://github.com/user-attachments/assets/266b5b9f-390f-427a-bb2b-ddd9b591c4a6" />
<img width="1899" height="900" alt="Снимок экрана (176)" src="https://github.com/user-attachments/assets/e953de44-213b-4a02-b2b0-d4b76baae39e" />
<img width="1899" height="892" alt="Снимок экрана (177)" src="https://github.com/user-attachments/assets/95e1f8de-051a-4917-b4bc-138a63c082c3" />
<img width="1915" height="907" alt="Снимок экрана (178)" src="https://github.com/user-attachments/assets/02284b09-05a1-47fb-8dd1-f963f8d0f096" />




