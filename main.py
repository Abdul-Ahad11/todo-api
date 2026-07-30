import sqlite3
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field

app=FastAPI()

connection = sqlite3.connect("tasks.db" , check_same_thread=False)
cursor=connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY, 
title TEXT NOT NULL, 
done BOOLEAN NOT NULL
)
"""  )

connection.commit()
cursor.execute("SELECT COUNT(*) FROM tasks")
count=cursor.fetchone()[0]
if count==0:
    seed_task=[
        ("learn fast api", False),
        ("complete internship assignment", False),
        ("push code to git hub", True)
    ]
    cursor.executemany(
        "INSERT INTO tasks (title , done) VALUES (?,?)", seed_task
    )
    connection.commit()
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
    cursor.execute("SELECT * FROM tasks")
    rows=cursor.fetchall()
    result=[]
    for row in rows:
        result.append({
            "id":row[0],
            "title":row[1],
            "done":bool(row[2])
        })
    if done is not None:
        filtered_tasks = []
        for t in result:
            if t["done"]==done:
                filtered_tasks.append(t)
        result=filtered_tasks

    if search is not None:
        searched_tasks=[]
        for t in result:
            if search.lower() in t["title"].lower():
                searched_tasks.append(t)
        result=searched_tasks
    return result




@app.get('/tasks/{id}')
def task_byid(id:int):
    cursor.execute("SELECT * FROM tasks WHERE id = ?" , (id,))

    row = cursor.fetchone()
    if row is None:
        raise HTTPException(
            status_code=404,
            detail="task not found"
        )
    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }
@app.post('/tasks', status_code=201)
def create_task(task : TaskCreate):
    cursor.execute("INSERT INTO tasks (title , done) VALUES (? , ?)" , (task.title , False) )

    connection.commit()
    new_id =cursor.lastrowid

    return {
        "id":new_id,
        "title":task.title,
        "done":False
    }

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