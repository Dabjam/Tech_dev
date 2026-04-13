# Контрольная работа №3

В папке `KR_3` собраны решения заданий из PDF по темам `6.1-8.2`.
Каждое задание оформлено как отдельное мини-приложение FastAPI, чтобы их было удобно запускать и проверять независимо друг от друга.

## Структура

- `task_6_1` - базовая HTTP Basic аутентификация для `GET /login`
- `task_6_2` - регистрация и логин с хешированием паролей через `passlib`
- `task_6_3` - управление Swagger/OpenAPI в режимах `DEV` и `PROD`
- `task_6_4` - JWT-аутентификация и защищенный ресурс
- `task_6_5` - регистрация, JWT и ограничение запросов
- `task_7_1` - RBAC: роли `admin`, `user`, `guest`
- `task_8_1` - регистрация пользователя в SQLite без SQLAlchemy
- `task_8_2` - CRUD для `Todo` c SQLite без SQLAlchemy

## Установка

Из корня папки `KR_3`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Переменные окружения

Файл `.env.example` содержит пример:

```env
MODE=DEV
DOCS_USER=docs_admin
DOCS_PASSWORD=docs_password
JWT_SECRET_KEY=change_me
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

Файл `.env` не должен публиковаться в репозиторий.

## Запуск заданий

Запуск любого задания выполняется одинаково: нужно перейти в соответствующую папку и поднять `uvicorn`.

### Задание 6.1

```bash
cd task_6_1
uvicorn main:app --reload
```

Проверка:

```bash
curl -u admin:admin123 http://127.0.0.1:8000/login
curl -u admin:wrong http://127.0.0.1:8000/login
```

### Задание 6.2

```bash
cd task_6_2
uvicorn main:app --reload
```

Проверка:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"user1\",\"password\":\"correctpass\"}" http://127.0.0.1:8000/register
curl -u user1:correctpass http://127.0.0.1:8000/login
curl -u user1:wrongpass http://127.0.0.1:8000/login
```

### Задание 6.3

```bash
cd task_6_3
uvicorn main:app --reload
```

Проверка в `DEV`:

```bash
curl -u docs_admin:docs_password http://127.0.0.1:8000/docs
curl -u docs_admin:docs_password http://127.0.0.1:8000/openapi.json
curl http://127.0.0.1:8000/redoc
```

Проверка в `PROD`:

```powershell
$env:MODE="PROD"
uvicorn main:app --reload
curl http://127.0.0.1:8000/docs
curl http://127.0.0.1:8000/openapi.json
```

### Задание 6.4

```bash
cd task_6_4
uvicorn main:app --reload
```

Проверка:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"john_doe\",\"password\":\"securepassword123\"}" http://127.0.0.1:8000/login
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/protected_resource
```

### Задание 6.5

```bash
cd task_6_5
uvicorn main:app --reload
```

Проверка:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"alice\",\"password\":\"qwerty123\"}" http://127.0.0.1:8000/register
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"alice\",\"password\":\"qwerty123\"}" http://127.0.0.1:8000/login
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/protected_resource
```

### Задание 7.1

```bash
cd task_7_1
uvicorn main:app --reload
```

Проверка:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"root\",\"password\":\"rootpass\",\"role\":\"admin\"}" http://127.0.0.1:8000/register
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"root\",\"password\":\"rootpass\"}" http://127.0.0.1:8000/login
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/protected_resource
curl -X POST -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/admin/resource
curl -X DELETE -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/admin/resource
```

### Задание 8.1

```bash
cd task_8_1
python init_db.py
uvicorn main:app --reload
```

Проверка:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"test_user\",\"password\":\"12345\"}" http://127.0.0.1:8000/register
```

После запроса в папке задания появится файл `users.db`.

### Задание 8.2

```bash
cd task_8_2
uvicorn main:app --reload
```

Проверка:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"Buy groceries\",\"description\":\"Milk, eggs, bread\"}" http://127.0.0.1:8000/todos
curl http://127.0.0.1:8000/todos/1
curl -X PUT -H "Content-Type: application/json" -d "{\"title\":\"Buy groceries\",\"description\":\"Milk, eggs, bread\",\"completed\":true}" http://127.0.0.1:8000/todos/1
curl -X DELETE http://127.0.0.1:8000/todos/1
```

## Краткое описание реализации

- В заданиях `6.1-6.3` использована базовая аутентификация и защита от тайминг-атак через `secrets.compare_digest`.
- В заданиях `6.2`, `6.5` и `7.1` пароли хранятся в виде хеша через `passlib` и `bcrypt`.
- В заданиях `6.4`, `6.5` и `7.1` применяются JWT-токены.
- В заданиях `8.1` и `8.2` используется `SQLite` и `sqlite3` без `SQLAlchemy`, как требуется по условию.
