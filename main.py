from fastapi import FastAPI , HTTPException

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
def task(id:int):
    for t in tasks:
        if t["id"] == id :
            return t

    raise HTTPException(
        status_code=404,
        detail="task not found"
    )


