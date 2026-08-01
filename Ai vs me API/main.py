from datetime import datetime
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
done BOOLEAN NOT NULL, 
created_at TEXT , 
updated_at TEXT
)
"""  )

connection.commit()

cursor.execute("SELECT COUNT(*) FROM tasks")
count=cursor.fetchone()[0]
if count==0:
    now = datetime.now().isoformat()
    seed_task=[
        ("learn fast api", False , now , now),
        ("complete internship assignment", False , now , now),
        ("push code to git hub", True , now, now)
    ]
    cursor.executemany(
        "INSERT INTO tasks (title , done ,created_at , updated_at) VALUES (?,?,?,?)", seed_task
    )
    connection.commit()

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
    query="SELECT * FROM tasks WHERE 1=1"
    params=[]

    if done is not None:
        query += " AND done=?"
        params.append(done)

    if search is not None:
        query+=" AND title LIKE ?"
        params.append(f"%{search}%")

    query+=" ORDER BY title"

    cursor.execute(query , params)
    rows=cursor.fetchall()
    result=[]
    for row in rows:
        result.append({
            "id":row[0],
            "title":row[1],
            "done":bool(row[2]),
            "created_at":row[3],
            "updated_at":row[4]
        })
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
        "done": bool(row[2]),
        "created_at": row[3],
        "updated_at": row[4]
    }
@app.post('/tasks', status_code=201)
def create_task(task : TaskCreate):

    now=datetime.now().isoformat()
    cursor.execute("INSERT INTO tasks (title , done , created_at , updated_at) VALUES (?,?,?,?)" ,
                   (task.title , False ,now , now) )

    connection.commit()
    new_id =cursor.lastrowid

    return {
        "id":new_id,
        "title":task.title,
        "done":False,
        "created_at": now,
        "updated_at": now
    }

@app.put('/tasks/{id}')
def update_tasks(id: int ,  update_task :UpdateTask):

    now=datetime.now().isoformat()

    cursor.execute("UPDATE tasks SET title=? , done=? , updated_at=?  WHERE id=?" ,
                   (update_task.title , update_task.done ,now , id))
    connection.commit()

    if cursor.rowcount==0:
        raise HTTPException(
        status_code=404,
        detail="not found"
    )
    return {
        "id": id,
        "title": update_task.title,
        "done": update_task.done ,
        "updated_at":now
    }


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )
    connection.commit()
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return None


@app.get('/stats')
def get_stats():
    cursor.execute("SELECT COUNT(*) FROM tasks ")
    total=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done=1")
    done=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done=0")
    open_task=cursor.fetchone()[0]

    return {
        "total": total ,
        "done":done ,
        "open_task":open_task
    }