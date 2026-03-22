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
