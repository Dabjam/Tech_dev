from os import name
from re import S
from sre_parse import SUCCESS
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()


users = [
    {
        "id": 1,
        "name": "Вова",
        "age": 25,
    }
]

@app.get("/", summary="Рычач", tags=["Оснвын функции"])
def root():
    return("Hell, world!")

@app.get("/users", summary="Все пользователи", tags=["Пользователи"])
def show_users():
    return users

@app.get("/users/{user_id}", summary="Найти пользователя", tags=["Пользователи"])
def search_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    
    raise HTTPException(status_code=404, default="Пользователь не найден")


class NewUser(BaseModel):
    name: str
    age: int


@app.post("/users", tags=["Добавить пользователя"])
def create_user(new_user, NewUser):
    users.append({
        "id": len(users) + 1,
        "name": new_user.name,
        "age": new_user.age,
    })
    return {"success": True, "message": "Пользователь добавлен"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)