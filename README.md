# 🚀 Todo API (FastAPI)

A simple RESTful Todo API built with **FastAPI**. This project demonstrates CRUD (Create, Read, Update, Delete) operations using an in-memory list. It also includes filtering, searching, task statistics, request validation with Pydantic, and interactive API documentation using Swagger UI.

---

# ✨ Features

- ✅ Create a new task
- ✅ Get all tasks
- ✅ Get a task by ID
- ✅ Update a task
- ✅ Delete a task
- ✅ Filter tasks by completion status
- ✅ Search tasks by title
- ✅ View task statistics
- ✅ Request validation using Pydantic
- ✅ Automatic Swagger UI documentation

---

# 🛠️ Technologies Used

- Python 3
- FastAPI
- Uvicorn
- Pydantic

---

# 📁 Project Structure

```text
todo-api/
│
├── main.py
├── README.md
├── .gitignore
└── screenshots/
    └── swagger-ui.png
```

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/Abdul-Ahad11/todo-api.git
```

## 2. Navigate to the project

```bash
cd todo-api
```

## 3. Create a virtual environment

```bash
python3 -m venv .venv
```

## 4. Activate the virtual environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## 5. Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

---

# ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 📌 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Home endpoint |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/stats` | Get task statistics |

---

# 🔍 Filter Tasks

Retrieve tasks based on their completion status.

### Get completed tasks

```http
GET /tasks?done=true
```

### Get incomplete tasks

```http
GET /tasks?done=false
```

---

# 🔎 Search Tasks

Search tasks by title.

Example:

```http
GET /tasks?search=python
```

Search is **case-insensitive**, so the following all work:

```
python
Python
PYTHON
```

---

# 🔀 Combine Filtering and Search

Both query parameters can be used together.

Example:

```http
GET /tasks?done=true&search=git
```

This returns only completed tasks whose title contains **git**.

---

# 📊 Task Statistics

Get a summary of your tasks.

```http
GET /stats
```

Example Response

```json
{
    "total": 5,
    "done": 2,
    "open": 3
}
```

---

# 📝 Request Examples

## Create Task

**POST** `/tasks`

Request

```json
{
    "title": "Learn FastAPI"
}
```

Response

```json
{
    "id": 4,
    "title": "Learn FastAPI",
    "done": false
}
```

---

## Update Task

**PUT** `/tasks/1`

Request

```json
{
    "title": "Learn AI",
    "done": true
}
```

Response

```json
{
    "id": 1,
    "title": "Learn AI",
    "done": true
}
```

---

## Delete Task

**DELETE** `/tasks/1`

Response Status

```
204 No Content
```

---

# 📷 Swagger UI

Add a screenshot of your Swagger UI inside the **screenshots** folder.

Project structure:

```text
screenshots/
    └── swagger-ui.png
```

Display it in the README:

```markdown
![Swagger UI](screenshots/swagger-ui.png)
```

---

# 🧪 Example cURL Commands

### Get all tasks

```bash
curl http://127.0.0.1:8000/tasks
```

### Create a task

```bash
curl -X POST http://127.0.0.1:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Study FastAPI"}'
```

### Update a task

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
-H "Content-Type: application/json" \
-d '{"title":"Study AI","done":true}'
```

### Delete a task

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

---

# 📈 Learning Outcomes

Through this project, I learned:

- FastAPI fundamentals
- REST API development
- CRUD operations
- Path parameters
- Query parameters
- Request validation using Pydantic
- HTTP status codes (200, 201, 204, 404)
- Filtering API responses
- Searching with query parameters
- Generating task statistics
- Swagger UI and ReDoc
- Git and GitHub workflow
- Writing project documentation

---

# 🚀 Future Improvements

- Store data in SQLite or PostgreSQL instead of memory
- Add user authentication
- Implement pagination
- Add sorting
- Add unit tests
- Deploy the API to the cloud

---

# 👨‍💻 Author

**Abdul Ahad**

GitHub: **https://github.com/Abdul-Ahad11**

---

## ⭐ If you found this project helpful, consider giving it a star on GitHub!
