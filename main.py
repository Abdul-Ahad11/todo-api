from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field
from repository import get_all_tasks, get_task_by_id, create_task_repository,update_task,delete_task,get_stats

app=FastAPI()


class TaskCreate(BaseModel):
    title:str = Field(...,min_length=1)

class UpdateTask(BaseModel):
    title:str =Field(...,min_length=1)
    done:bool

@app.get('/health')
def health():
    return {'status':'ok'}

@app.get('/tasks')
def task(done: bool | None = None, search: str | None = None):
    return get_all_tasks(done , search)

@app.get('/tasks/{id}')
def task_byid(id:int):
    task = get_task_by_id(id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="task not found"
        )
    return task

@app.post('/tasks', status_code=201)
def create_task(task : TaskCreate):
    return create_task_repository(task.title)

@app.put('/tasks/{id}')
def update_tasks(id: int, update_data: UpdateTask):

    task = update_task(
        id,
        update_data.title,
        update_data.done
    )
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="not found"
        )
    return task

@app.delete("/tasks/{id}", status_code=204)
def delete_task_route(id: int):
    deleted = delete_task(id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return None

@app.get('/stats')
def stats():
    return get_stats()