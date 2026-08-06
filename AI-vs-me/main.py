from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

from repository import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    get_stats,
)

app = FastAPI(
    title="Todo API",
    version="1.0.0",
)


# ----------------------------
# Request Models
# ----------------------------

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    done: bool


class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    done: bool


# ----------------------------
# Health Check
# ----------------------------

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "status": "ok",
        "message": "API is running"
    }


# ----------------------------
# Statistics
# ----------------------------

@app.get("/stats", status_code=status.HTTP_200_OK)
def stats():
    return get_stats()


# ----------------------------
# Get All Tasks
# Optional filters:
# /tasks
# /tasks?id=1
# /tasks?done=true
# /tasks?search=learn
# ----------------------------

@app.get("/tasks", status_code=status.HTTP_200_OK)
def read_tasks(
    id: int | None = Query(default=None),
    done: bool | None = Query(default=None),
    search: str | None = Query(default=None),
):
    return get_all_tasks(
        task_id=id,
        done=done,
        search=search,
    )


# ----------------------------
# Get Task By ID
# ----------------------------

@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def read_task(task_id: int):

    task = get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


# ----------------------------
# Create Task
# ----------------------------

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def add_task(task: TaskCreate):

    return create_task(
        title=task.title,
        done=task.done,
    )


# ----------------------------
# Update Task
# ----------------------------

@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def edit_task(task_id: int, task: TaskUpdate):

    updated = update_task(
        task_id=task_id,
        title=task.title,
        done=task.done,
    )

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return updated


# ----------------------------
# Delete Task
# ----------------------------

@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def remove_task(task_id: int):

    deleted = delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return {
        "message": "Task deleted successfully"
    }