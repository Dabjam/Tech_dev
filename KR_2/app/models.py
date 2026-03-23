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


# class Login(BaseModel):
#     username: str = Field(min_length=2, max_length=50)
#     password: str = Field(min_length=8, max_length=50)