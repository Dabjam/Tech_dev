from fastapi import APIRouter, FastAPI
from models import UserCreate

app = FastAPI()

@app.post("/create_user", response_model=UserCreate, summary="Создание пользователя")
def create_user(user: UserCreate):
    return user