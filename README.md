# 🚀 Todo API — FastAPI CRUD with SQLite Persistence

A RESTful Todo API built with **FastAPI**, developed in two stages: first as an in-memory CRUD service (Assignment 1), then upgraded to a **SQLite**-backed API with permanent data storage (Assignment 2). The project covers request validation, filtering, searching, task statistics, and interactive Swagger documentation.

---

## 🛠️ Tech Stack

- Python 3
- FastAPI
- Uvicorn
- Pydantic
- SQLite3 (Assignment 2)
- DB Browser for SQLite (Assignment 2)

---

## 📁 Project Structure

```text
todo-api/
│
├── main.py
├── tasks.db
├── README.md
├── .gitignore
└── screenshots/
    ├── swagger-ui.png
    ├── sql-count-query.png
    └── sql-completed-tasks.png
```

> `tasks.db` is typically excluded via `.gitignore` so every fresh clone starts with a clean, auto-generated database.

---

## 📦 Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/Abdul-Ahad11/todo-api.git
cd todo-api

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install fastapi uvicorn pydantic

# 4. Run the server
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `/docs` (Swagger UI) and `/redoc` (ReDoc).

---
---

# 📌 Assignment 1 — In-Memory CRUD API

## Overview

The first version of the API implements full CRUD (Create, Read, Update, Delete) functionality using an **in-memory Python list** as temporary storage. It also adds filtering, searching, and basic statistics on top of the core endpoints.

## ✨ Features

- Create, read, update, and delete tasks
- Filter tasks by completion status
- Search tasks by title (case-insensitive)
- Combine filtering and search in a single request
- Task statistics summary
- Request validation with Pydantic
- Auto-generated Swagger UI documentation

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home endpoint |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/stats` | Get task statistics |

**Filtering & search examples:**

```http
GET /tasks?done=true              # completed tasks only
GET /tasks?search=python          # title contains "python"
GET /tasks?done=true&search=git   # combine both filters
```

## 📝 Example Requests

**Create a task**
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI"}'
```
→ `201 Created` with the new task, including its assigned `id`.

**Update a task**
```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn AI","done":true}'
```

**Delete a task**
```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```
→ `204 No Content`

## 📷 Swagger UI

FastAPI automatically generates interactive documentation for every endpoint.

![Swagger UI showing all Todo API endpoints](screenshots/swagger-ui.png)

*Figure 1: Swagger UI listing the full set of CRUD endpoints — `/`, `/health`, `/tasks`, and `/tasks/{id}` — each tagged with its HTTP method.*

## 📈 Learning Outcomes

- FastAPI fundamentals and routing
- REST API design and CRUD operations
- Path and query parameters
- Request validation with Pydantic
- HTTP status codes (200, 201, 204, 404)
- Filtering, searching, and computed statistics
- Swagger UI / ReDoc
- Git and GitHub workflow

---
---

# 📌 Assignment 2 — SQLite Database Integration

## Overview

Assignment 2 upgrades the API's storage layer from an in-memory list to a persistent **SQLite** database. The API's routes and behavior stay identical — only the underlying storage changes, so tasks now survive a server restart instead of disappearing.

On startup, the app automatically creates `tasks.db`, creates the `tasks` table if missing, and seeds three sample tasks only when the table is empty.

## ✨ Features

- Automatic database and table creation
- One-time seeding of sample data
- Full CRUD implemented with parameterized SQL queries
- Data persists across server restarts
- Manual SQL exploration via DB Browser for SQLite

## 🗄️ Database Schema

**File:** `tasks.db`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-incrementing ID |
| title | TEXT | Task title |
| done | BOOLEAN | Completion status (0/1) |

## 🗃️ SQL Operations

```sql
-- Read all tasks
SELECT * FROM tasks;

-- Read one task
SELECT * FROM tasks WHERE id = ?;

-- Create a task
INSERT INTO tasks (title, done) VALUES (?, ?);

-- Update a task
UPDATE tasks SET title = ?, done = ? WHERE id = ?;

-- Delete a task
DELETE FROM tasks WHERE id = ?;
```

All queries use `?` placeholders instead of string concatenation, protecting against SQL injection.

## 🧪 Manual SQL Queries (DB Browser for SQLite)

To confirm the API and database stayed in sync, the following queries were run directly against `tasks.db`:

**Count total tasks**
```sql
SELECT COUNT(*) FROM tasks;
```
![COUNT query result showing 4 tasks in the database](screenshots/sql-count-query.png)

*Figure 2: Running `SELECT COUNT(*) FROM tasks;` in DB Browser returns a total of 4 tasks stored in the database.*

**View completed tasks**
```sql
SELECT * FROM tasks WHERE done = 1;
```
![Query result showing completed tasks](screenshots/sql-completed-tasks.png)

*Figure 3: Running `SELECT * FROM tasks WHERE done = 1;` returns only the completed tasks — confirming the database and the `/tasks` API endpoint reflect the same data.*

## 💾 Data Persistence

Any task created, updated, or deleted through the API remains in `tasks.db` after the server restarts — a key difference from Assignment 1, where all data lived only in memory.

## 📚 Learning Outcomes

- Connecting FastAPI to a SQLite database
- Automatic database and table initialization
- Seeding sample data safely (once, not on every run)
- Parameterized SQL queries for CRUD operations
- Verifying data persistence across restarts
- Executing and interpreting SQL manually with DB Browser
- Publishing a database-backed FastAPI project

---

## 🚀 Future Improvements

- Migrate from SQLite to PostgreSQL for production use
- Add user authentication
- Implement pagination and sorting
- Add automated unit tests
- Deploy the API to the cloud

---

## 👨‍💻 Author

**Abdul Ahad**
GitHub: [github.com/Abdul-Ahad11](https://github.com/Abdul-Ahad11)

⭐ If you found this project helpful, consider giving it a star on GitHub!
