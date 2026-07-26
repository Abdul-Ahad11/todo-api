import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, Query, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict, Field

API_KEY_ENV = "TODO_API_KEY"
MAX_TITLE_LENGTH = 200
MAX_SEARCH_LENGTH = 100
MAX_TASKS = 1000

DOCS_ENABLED = os.environ.get("ENABLE_DOCS", "true").lower() in ("1", "true", "yes")

app = FastAPI(
    title="Task API",
    version="1.0",
    docs_url="/docs" if DOCS_ENABLED else None,
    redoc_url="/redoc" if DOCS_ENABLED else None,
    openapi_url="/openapi.json" if DOCS_ENABLED else None,
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(provided_key: str | None = Security(api_key_header)) -> None:
    expected_key = os.environ.get(API_KEY_ENV)
    if not expected_key:
        raise HTTPException(
            status_code=503,
            detail=f"write access is disabled because {API_KEY_ENV} is not configured",
        )
    if provided_key is None or not secrets.compare_digest(provided_key, expected_key):
        raise HTTPException(status_code=401, detail="invalid or missing API key")


tasks = [
    {
        "id": 1,
        "title": "learn fast api",
        "done": False
    },
    {
        "id": 2,
        "title": "complete internship assignment",
        "done": False
    },
    {
        "id": 3,
        "title": "push code to git hub",
        "done": True
    }
]

next_id = len(tasks) + 1


class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(..., min_length=1, max_length=MAX_TITLE_LENGTH)


class UpdateTask(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(..., min_length=1, max_length=MAX_TITLE_LENGTH)
    done: bool


@app.get('/')
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/tasks')
def task(
    done: bool | None = None,
    search: str | None = Query(default=None, max_length=MAX_SEARCH_LENGTH),
):
    results = tasks
    if done is not None:
        results = [t for t in results if t["done"] == done]

    if search is not None:
        results = [t for t in results if search.lower() in t["title"].lower()]

    return results


@app.get('/tasks/{id}')
def task_byid(id: int):
    for t in tasks:
        if t["id"] == id:
            return t

    raise HTTPException(
        status_code=404,
        detail="task not found"
    )


@app.post('/tasks', status_code=201, dependencies=[Depends(require_api_key)])
def create_task(task: TaskCreate):
    global next_id
    if len(tasks) >= MAX_TASKS:
        raise HTTPException(
            status_code=507,
            detail=f"task limit of {MAX_TASKS} reached"
        )
    new_task = {
        "id": next_id,
        "title": task.title,
        "done": False
    }
    next_id += 1
    tasks.append(new_task)
    return new_task


@app.put('/tasks/{id}', dependencies=[Depends(require_api_key)])
def update_tasks(id: int, update_task: UpdateTask):
    for t in tasks:
        if t["id"] == id:
            t["title"] = update_task.title
            t["done"] = update_task.done
            return t
    raise HTTPException(
        status_code=404,
        detail="not found"
    )


@app.delete("/tasks/{id}", status_code=204, dependencies=[Depends(require_api_key)])
def delete_task(id: int):
    for t in tasks:
        if t["id"] == id:
            tasks.remove(t)
            return None
    raise HTTPException(
        status_code=404,
        detail="not found"
    )


@app.get('/stats')
def get_stats():
    total = len(tasks)
    done = 0
    open_task = 0
    for t in tasks:
        if t["done"]:
            done += 1
        else:
            open_task += 1

    return {
        "total": total,
        "done": done,
        "open_task": open_task
    }
