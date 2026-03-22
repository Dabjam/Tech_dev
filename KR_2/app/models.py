from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int | None = Field(gt=0, le=100)
    is_subscribed: bool | None = None
