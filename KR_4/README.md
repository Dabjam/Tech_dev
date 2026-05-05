# Контрольная работа №4

В папке `KR_4` собраны решения заданий `9.1`, `10.1`, `10.2`, `11.1` и `11.2`

## Структура

- `task_9_1` - миграции Alembic для таблицы `products` в SQLite
- `task_10_1` - пользовательские классы исключений и обработчики ошибок
- `task_10_2` - валидация JSON и собственная обработка ошибок валидации
- `task_11_1` - синхронные тесты FastAPI через `TestClient`
- `task_11_2` - асинхронные тесты через `pytest-asyncio`, `httpx.AsyncClient`, `ASGITransport` и `Faker`

## Установка

Из корня папки `KR_4`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Запуск заданий

### Задание 9.1

```powershell
cd task_9_1
alembic upgrade 8c1d2f31a5b1
python seed_initial_products.py
alembic upgrade head
uvicorn app.main:app --reload
```

Проверка:

```powershell
curl http://127.0.0.1:8000/products
curl http://127.0.0.1:8000/products/1
```

Что получится:

- первая миграция создаёт таблицу `products`;
- затем в таблицу добавляются две записи;
- вторая миграция добавляет обязательное поле `description`;
- после этого API показывает уже обновлённую схему.

### Задание 10.1

```powershell
cd task_10_1
uvicorn main:app --reload
```

Проверка:

```powershell
curl "http://127.0.0.1:8000/demo/limit?count=15"
curl http://127.0.0.1:8000/demo/product/100
curl http://127.0.0.1:8000/demo/product/1
```

### Задание 10.2

```powershell
cd task_10_2
uvicorn main:app --reload
```

Проверка:

```powershell
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"student\",\"age\":20,\"email\":\"student@example.com\",\"password\":\"password1\"}" http://127.0.0.1:8000/users/validate
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"student\",\"age\":17,\"email\":\"wrong\",\"password\":\"123\"}" http://127.0.0.1:8000/users/validate
```

### Задание 11.1

Запуск тестов:

```powershell
pytest task_11_1/tests -v
```

### Задание 11.2

Запуск асинхронных тестов:

```powershell
pytest task_11_2/tests -v
```

### Все тесты сразу

```powershell
pytest -v
```

## Краткое описание реализации

- В `task_9_1` использованы `SQLAlchemy`, `Alembic` и `SQLite`.
- В `task_10_1` сделаны два собственных исключения с разными статус-кодами и единым форматом ответа.
- В `task_10_2` добавлена Pydantic-модель пользователя и свой обработчик `RequestValidationError`.
- В `task_11_1` есть тесты успешных и ошибочных сценариев для простого приложения с пользователями.
- В `task_11_2` тесты полностью асинхронные и не требуют запуска `uvicorn`, так как работают через `ASGITransport`.
