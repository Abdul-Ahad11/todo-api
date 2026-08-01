from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("tasks.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# -----------------------------
# Create Table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
)
""")
conn.commit()

# -----------------------------
# Seed Data (only if empty)
# -----------------------------
cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    sample_tasks = [
        ("Learn FastAPI", False),
        ("Complete internship assignment", False),
        ("Push code to GitHub", True)
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        sample_tasks
    )
    conn.commit()


# -----------------------------
# Pydantic Models
# -----------------------------
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


# -----------------------------
# Helper Function
# -----------------------------
def row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


# -----------------------------
# GET /tasks
# -----------------------------
@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks ORDER BY id")
    rows = cursor.fetchall()
    return [row_to_dict(row) for row in rows]


# -----------------------------
# GET /tasks/{id}
# -----------------------------
@app.get("/tasks/{id}")
def get_task(id: int):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return row_to_dict(row)


# -----------------------------
# POST /tasks
# -----------------------------
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    cursor.execute(
        "INSERT INTO tasks(title, done) VALUES(?, ?)",
        (task.title, False)
    )
    conn.commit()

    task_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    return row_to_dict(cursor.fetchone())


# -----------------------------
# PUT /tasks/{id}
# -----------------------------
@app.put("/tasks/{id}")
def update_task(id: int, task: TaskUpdate):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (task.title, task.done, id)
    )
    conn.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    return row_to_dict(cursor.fetchone())


# -----------------------------
# DELETE /tasks/{id}
# -----------------------------
@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )
    conn.commit()


# -----------------------------
# GET /health
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -----------------------------
# GET /stats
# -----------------------------
@app.get("/stats")
def stats():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = ?", (True,))
    completed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = ?", (False,))
    pending = cursor.fetchone()[0]

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }