from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: str


class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool


class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
