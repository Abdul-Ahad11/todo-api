import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger("todo-api")

app = FastAPI()
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


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)


class UpdateTask(BaseModel):
    title: str = Field(..., min_length=1)
    done: bool


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.warning(
        "%s %s failed with %s: %s",
        request.method, request.url.path, exc.status_code, exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"status": exc.status_code, "detail": exc.detail}},
        headers=exc.headers
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning(
        "%s %s failed validation: %s",
        request.method, request.url.path, exc.errors()
    )
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "status": 422,
                "detail": "request validation failed",
                "errors": jsonable_encoder(exc.errors())
            }
        }
    )


@app.exception_handler(Exception)
def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "unhandled error while handling %s %s",
        request.method, request.url.path, exc_info=exc
    )
    return JSONResponse(
        status_code=500,
        content={"error": {"status": 500, "detail": "internal server error"}}
    )


def find_task(id: int) -> dict:
    for t in tasks:
        if t["id"] == id:
            return t
    raise HTTPException(status_code=404, detail=f"task {id} not found")


def next_id() -> int:
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


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
def task(done: bool | None = None, search: str | None = None):
    results = list(tasks)
    if done is not None:
        results = [t for t in results if t["done"] == done]

    if search is not None:
        results = [t for t in results if search.lower() in t["title"].lower()]

    return results


@app.get('/tasks/{id}')
def task_byid(id: int):
    return find_task(id)


@app.post('/tasks', status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": next_id(),
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task


@app.put('/tasks/{id}')
def update_tasks(id: int, update_task: UpdateTask):
    existing = find_task(id)
    existing["title"] = update_task.title
    existing["done"] = update_task.done
    return existing


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    tasks.remove(find_task(id))
    return None


@app.get('/stats')
def get_stats():
    done = sum(1 for t in tasks if t["done"])
    return {
        "total": len(tasks),
        "done": done,
        "open_task": len(tasks) - done
    }
