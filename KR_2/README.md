### Отчет по контрольной работе

## Задание 3.1

# main.py

```python
from fastapi import APIRouter, FastAPI
from models import UserCreate

app = FastAPI()

@app.post("/create_user", response_model=UserCreate, summary="Создание пользователя")
def create_user(user: UserCreate):
    return user
```

# models.py

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int | None = Field(gt=0, le=100)
    is_subscribed: bool | None = None
```

# Результат

![1774182948267](image/README/1774182948267.png)

## Задание 3.2

# main.py

```python
from fastapi import  FastAPI, HTTPException
from models import UserCreate, Product

app = FastAPI()

products = [
    {
        "product_id": 123,
        "name": "Smartphone",
        "category": "Electronics",
        "price": 599.99
    },

    {
        "product_id": 456,
        "name": "Phone Case",
        "category": "Accessories",
        "price": 19.99
    },
    {
        "product_id": 789,
        "name": "Iphone",
        "category": "Electronics",
        "price": 1299.99
    },
    {
        "product_id": 101,
        "name": "Headphones",
        "category": "Accessories",
        "price": 99.99
    },
    {
        "product_id": 202,
        "name": "Smartwatch",
        "category": "Electronics",
        "price": 299.99
    },
]

@app.post("/create_user", response_model=UserCreate, summary="Создание пользователя")
def create_user(user: UserCreate):
    return user

@app.get("/product/{product_id}", response_model=Product, summary="Получение продукта")
def get_product(product_id: int):
    for product in products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Продукт не найден")

@app.get("/products/search", response_model=list[Product], summary="Поиск продуктов")
def search_products(keyword: str, category: str = None, limit: int = 10):
    results = []
    for product in products:
        if keyword.lower() in product["name"].lower():
            if category is None or product["category"] == category:
                results.append(product)
    return results[:limit]
```

# models.py

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int | None = Field(gt=0, le=100)
    is_subscribed: bool | None = None

class Product(BaseModel):
    product_id: int = Field(ge=1, le=1000)
    name: str = Field(min_length=2, max_length=50)
    category: str = Field(min_length=2, max_length=50)
    price: float = Field(ge=0, le=1000000)
```

# результат

![1774210154028](image/README/1774210154028.png)
![1774210171962](image/README/1774210171962.png)

## Задание 5.1

# main.py

```python
from fastapi import  FastAPI, HTTPException, Cookie, Header, Response, Form
from models import UserCreate, Product
from typing import Annotated, Optional

import uuid

app = FastAPI()

sessions = {}

@app.post("/login", summary="Вход в систему")
def logint(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    session_id = str(uuid.uuid4())
    sessions[session_id] = username

    response.set_cookie(key="session_token", value=session_id, httponly=True)

    return {"message": "Успешный вход", "session_id": session_id}

@app.get("/user", summary="Проверка авторизации через Cookie")
def get_user(session_token: Optional[str]= Cookie(None)):
    if not session_token or session_token not in sessions:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован (отсутствует session_token)")

    username = sessions[session_token]
    return {"message": f"Успешный вход пользователя {username}!"}

```

# результат

![1774285836189](image/README/1774285836189.png)
![1774285857644](image/README/1774285857644.png)

## Задание 5.2

# main.py

```python
SECRET_KEY = "my-super-secret-key-123"

signer = TimestampSigner(SECRET_KEY)

users_db = {"admin": "12345"}
sessions_db = {}

@app.post("/login", summary="Вход с подписанной Cookie")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    if username not in users_db or users_db[username] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(uuid.uuid4())
    sessions_db[user_id] = username
    signed_token = signer.sign(user_id).decode('utf-8')

    response.set_cookie(
        key="session_token",
        value=signed_token,
        httponly=True,
        max_age=3600
    )

    return {"message": "Успешный вход", "user_id": user_id}

@app.get("/profile", summary="Защищенный профиль с проверкой подписи")
def get_profile(session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail="Unauthorized: No cookie")

    try:
        user_id = signer.unsign(session_token, max_age=3600).decode('utf-8')

        if user_id not in sessions_db:
            raise HTTPException(status_code=401, detail="Unauthorized: Session expired")

        return {
            "message": "Welcome to your profile",
            "user_id": user_id,
            "username": sessions_db[user_id]
        }

    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or tampered signature")
```

![1774290315924](image/README/1774290315924.png)
![1774290335433](image/README/1774290335433.png)

## Задание 5.3
