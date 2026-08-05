import os
import psycopg
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
DATABASE_URL= os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise Exception("DATABASE_URL is missing")
connection=psycopg.connect(DATABASE_URL)
cursor=connection.cursor()

#create the table
now = datetime.now().isoformat()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id SERIAL PRIMARY KEY,
title TEXT NOT NULL,
done BOOLEAN NOT NULL,
created_at TEXT,
updated_at TEXT
)
""")
connection.commit()

# Seeding tasks
cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]
if count == 0:
    seed_tasks = [
        ("learn fast api", False ,now , now),
        ("complete internship assignment", False , now , now),
        ("push code to git hub", True,now,now)
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, done , created_at , updated_at) VALUES (%s, %s , %s , %s)",
        seed_tasks
    )
    connection.commit()


def get_all_tasks(done: bool |None=None , search : str |None=None):
    query="SELECT * FROM tasks WHERE 1=1"
    params=[]

    if done is not None:
        query += " AND done=%s"
        params.append(done)

    if search is not None:
        query+=" AND title ILIKE %s"
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

def get_task_by_id(id: int):
    cursor.execute(
        "SELECT * FROM tasks WHERE id=%s",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        return None
    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2]),
        "created_at": row[3],
        "updated_at": row[4]
    }

#post
def create_task_repository(title: str):
    now = datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO tasks
        (title, done, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (title, False, now, now)
    )
    new_id = cursor.fetchone()[0]
    connection.commit()
    return {
        "id": new_id,
        "title": title,
        "done": False,
        "created_at": now,
        "updated_at": now
    }

#put
def update_task(id: int, title: str, done: bool):
    now = datetime.now().isoformat()

    cursor.execute(
        """
        UPDATE tasks
        SET title=%s, done=%s, updated_at=%s
        WHERE id=%s
        """,
        (title, done, now, id)
    )
    connection.commit()

    if cursor.rowcount == 0:
        return None
    return {
        "id": id,
        "title": title,
        "done": done,
        "updated_at": now
    }

#delete
def delete_task(id: int):
    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (id,)
    )
    connection.commit()
    if cursor.rowcount == 0:
        return False
    return True

#stats
def get_stats():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done=true")
    done = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done=false")
    open_task = cursor.fetchone()[0]

    return {
        "total": total,
        "done": done,
        "open_task": open_task
    }