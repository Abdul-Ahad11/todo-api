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
    results=tasks
    if done is not None:
        filtered_tasks = []
        for t in results:
            if t["done"]==done:
                filtered_tasks.append(t)
        results=filtered_tasks

    if search is not None:
        searched_tasks=[]
        for t in results:
            if search.lower() in t["title"].lower():
                searched_tasks.append(t)
            results=searched_tasks
    return results




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

@app.put('/tasks/{id}')
def update_tasks(id: int ,  update_task :UpdateTask):
    for t in tasks:
        if t["id"]==id:
            t["title"] = update_task.title
            t["done"] = update_task.done
            return t
    raise HTTPException(
        status_code=404,
        detail="not found"
    )

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for t in tasks:
        if t["id"]==id:
            tasks.remove(t)
            return None
    raise HTTPException(
        status_code=404,
        detail="not found"
    )

@app.get('/stats')
def get_stats():
    total=len(tasks)
    done=0
    open_task=0
    for t in tasks:
        if t["done"]:
            done +=1
        else:
            open_task +=1

    return {
        "total": total ,
        "done":done ,
        "open_task":open_task
    }