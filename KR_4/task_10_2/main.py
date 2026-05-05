from typing import Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, conint, constr


app = FastAPI(title="KR_4 Task 10.2")


class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


class ValidationErrorItem(BaseModel):
    field: str
    message: str


class ValidationErrorResponse(BaseModel):
    message: str
    errors: list[ValidationErrorItem]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field_path = [str(item) for item in err["loc"] if item != "body"]
        errors.append(
            ValidationErrorItem(
                field=".".join(field_path),
                message=err["msg"],
            )
        )

    payload = ValidationErrorResponse(
        message="Validation failed",
        errors=errors,
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.post("/users/validate")
def validate_user(user: User):
    return {
        "message": "User data is valid",
        "user": user.model_dump(),
    }
