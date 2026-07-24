from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field

app=FastAPI()
tasks=[
    {
        "id":1,
        "title":"learn fast api",
        "done":False
    },
    {
        "id":2,
        "title":"complete internship assignment",
        "done":False
    },
    {
        "id":3,
        "title":"push code to git hub",
        "done":True
    }
]

class TaskCreate(BaseModel):
    title:str = Field(...,min_length=1)

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
def task():
    return tasks

@app.get('/tasks/{id}')
def task_byid(id:int):
    for t in tasks:
        if t["id"] == id :
            return t

    raise HTTPException(
        status_code=404,
        detail="task not found"
    )
@app.post('/tasks', status_code=201)
def create_task(task : TaskCreate):
    new_id=len(tasks)+1
    new_task={
        "id":new_id,
        "title": task.title ,
        "done":False
    }
    tasks.append(new_task)
    return new_task