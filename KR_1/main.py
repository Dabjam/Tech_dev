from fastapi import FastAPI
from fastapi.responses import FileResponse

from models import Feedback, User, UserAge


app = FastAPI()

current_user = User(name="Ваше Имя и Фамилия", id=1)

feedbacks = []

@app.get("/", summary="Задание 1.2", tags=["html страница"])
def show_html():
    return FileResponse("index.html")

@app.post("/calculate", summary="Задание 1.3", tags=["Калькулятор"])
def show_sum_digits(num1: int, num2: int):
    return {"result": f"num1 + num2 = {num1 + num2}"}

@app.get("/users", summary="Информация о пользователе")
def get_user():
    return current_user


@app.post("/user", summary="Проверка возраста")
def check_age(user: UserAge):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18,
    }

@app.post("/feedback", summary="Отзыв", tags=["Отзывы"])
def create_feedback(fb: Feedback): 
    feedbacks.append(fb)
    return {"message": f"Спасибо, {fb.name}! Ваш отзыв сохранён."}

@app.get("/feedback", summary="Просмотр отзывов", tags=["Отзывы"])
def list_feedbacks(): 
    return feedbacks




