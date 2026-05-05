from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field


app = FastAPI(title="KR_4 Task 11.1")

users_db: dict[str, dict] = {}


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(gt=18, le=100)


def reset_state() -> None:
    users_db.clear()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "errors": exc.errors(),
        },
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user.username] = user.model_dump()
    return users_db[user.username]


@app.get("/users/{username}")
def get_user(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[username]
