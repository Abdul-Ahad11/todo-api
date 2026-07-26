from fastapi import FastAPI
from pydantic import BaseModel , Field

from utils import (
    build_task,
    filter_tasks,
    find_task_or_404,
    next_task_id,
    task_stats,
)

app=FastAPI()
tasks=[
    build_task(1, "learn fast api"),
    build_task(2, "complete internship assignment"),
    build_task(3, "push code to git hub", True),
]

class TaskCreate(BaseModel):
    title:str = Field(...,min_length=1)

class UpdateTask(BaseModel):
    title:str =Field(...,min_length=1)
    done:bool

@app.get('/')
def home():
    return {
        "name":"Task API",
        "version":"1.0",
        "endpoints":["/tasks"]
    }

@app.get('/health')
def health():
    return {'status':'ok'}

@app.get('/tasks')
def task(done: bool |None=None , search : str |None=None):
    return filter_tasks(tasks, done=done, search=search)

@app.get('/tasks/{id}')
def task_byid(id:int):
    return find_task_or_404(tasks, id)

@app.post('/tasks', status_code=201)
def create_task(task : TaskCreate):
    new_task=build_task(next_task_id(tasks), task.title)
    tasks.append(new_task)
    return new_task

@app.put('/tasks/{id}')
def update_tasks(id: int ,  update_task :UpdateTask):
    t=find_task_or_404(tasks, id)
    t["title"] = update_task.title
    t["done"] = update_task.done
    return t

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    t=find_task_or_404(tasks, id)
    tasks.remove(t)
    return None

@app.get('/stats')
def get_stats():
    return task_stats(tasks)
