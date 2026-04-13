from fastapi import FastAPI

from database import get_db_connection, init_db
from models import User

app = FastAPI(title="KR 3 - Task 8.1")
init_db()


@app.post("/register")
def register(user: User) -> dict[str, str]:
    connection = get_db_connection()
    connection.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (user.username, user.password),
    )
    connection.commit()
    connection.close()
    return {"message": "User registered successfully!"}
