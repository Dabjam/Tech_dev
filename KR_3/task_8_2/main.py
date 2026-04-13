from fastapi import FastAPI, HTTPException, status

from database import get_db_connection, init_db
from models import Todo, TodoCreate, TodoUpdate

app = FastAPI(title="KR 3 - Task 8.2")
init_db()


def row_to_todo(row) -> Todo:
    return Todo(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        completed=bool(row["completed"]),
    )


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate) -> Todo:
    connection = get_db_connection()
    cursor = connection.execute(
        "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
        (todo.title, todo.description, 0),
    )
    connection.commit()
    todo_id = cursor.lastrowid
    row = connection.execute(
        "SELECT id, title, description, completed FROM todos WHERE id = ?",
        (todo_id,),
    ).fetchone()
    connection.close()
    return row_to_todo(row)


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    connection = get_db_connection()
    row = connection.execute(
        "SELECT id, title, description, completed FROM todos WHERE id = ?",
        (todo_id,),
    ).fetchone()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    return row_to_todo(row)


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate) -> Todo:
    connection = get_db_connection()
    updated = connection.execute(
        """
        UPDATE todos
        SET title = ?, description = ?, completed = ?
        WHERE id = ?
        """,
        (todo.title, todo.description, int(todo.completed), todo_id),
    )
    connection.commit()

    if updated.rowcount == 0:
        connection.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    row = connection.execute(
        "SELECT id, title, description, completed FROM todos WHERE id = ?",
        (todo_id,),
    ).fetchone()
    connection.close()
    return row_to_todo(row)


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int) -> dict[str, str]:
    connection = get_db_connection()
    deleted = connection.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    connection.commit()
    connection.close()

    if deleted.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return {"message": "Todo deleted successfully"}
