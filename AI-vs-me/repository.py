import os
from datetime import datetime

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

connection = psycopg.connect(DATABASE_URL)
connection.autocommit = True


def init_db():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
            """
        )

        cursor.execute(
            "SELECT COUNT(*) FROM tasks"
        )

        count = cursor.fetchone()[0]

        if count == 0:
            now = datetime.now()

            cursor.executemany(
                """
                INSERT INTO tasks
                (title, done, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
                """,
                [
                    ("Learn FastAPI", False, now, now),
                    ("Complete Internship Assignment", False, now, now),
                    ("Push Code To GitHub", True, now, now),
                ],
            )


init_db()


def get_all_tasks(task_id=None, done=None, search=None):

    query = """
        SELECT id, title, done, created_at, updated_at
        FROM tasks
        WHERE 1=1
    """

    params = []

    if task_id is not None:
        query += " AND id = %s"
        params.append(task_id)

    if done is not None:
        query += " AND done = %s"
        params.append(done)

    if search:
        query += " AND title ILIKE %s"
        params.append(f"%{search}%")

    query += " ORDER BY id"

    with connection.cursor() as cursor:
        cursor.execute(query, params)

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "done": row[2],
                "created_at": row[3],
                "updated_at": row[4],
            }
            for row in rows
        ]


def get_task_by_id(task_id):

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, done, created_at, updated_at
            FROM tasks
            WHERE id = %s
            """,
            (task_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "done": row[2],
            "created_at": row[3],
            "updated_at": row[4],
        }
def create_task(title, done):

    now = datetime.now()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO tasks
            (title, done, created_at, updated_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, done, created_at, updated_at
            """,
            (
                title,
                done,
                now,
                now,
            ),
        )
        row = cursor.fetchone()
        return {
            "id": row[0],
            "title": row[1],
            "done": row[2],
            "created_at": row[3],
            "updated_at": row[4],
        }

def update_task(task_id, title, done):

    now = datetime.now()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE tasks
            SET
                title = %s,
                done = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING id, title, done, created_at, updated_at
            """,
            (
                title,
                done,
                now,
                task_id,
            ),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "done": row[2],
            "created_at": row[3],
            "updated_at": row[4],
        }


def delete_task(task_id):

    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s
            RETURNING id
            """,
            (task_id,),
        )

        row = cursor.fetchone()

        return row is not None


def get_stats():

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            """
        )

        total = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE done = TRUE
            """
        )

        completed = cursor.fetchone()[0]

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "open_tasks": total - completed,
        }