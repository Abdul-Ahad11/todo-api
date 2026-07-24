# 🚀 Todo API (FastAPI)

A simple RESTful Todo API built with **FastAPI**. This project demonstrates the complete CRUD (Create, Read, Update, Delete) operations using an in-memory list and automatic API documentation with Swagger UI.

## ✨ Features

- Create a new task
- Get all tasks
- Get a task by ID
- Update an existing task
- Delete a task
- Automatic Swagger UI documentation
- Input validation using Pydantic

---

## 🛠️ Technologies Used

- Python 3
- FastAPI
- Uvicorn
- Pydantic

---

## 📁 Project Structure

```
todo-api/
│
├── main.py
├── .gitignore
├── README.md
└── Swagger UI screenshot/
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Abdul-Ahad11/todo-api.git
```

### 2. Navigate to the project

```bash
cd todo-api
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the virtual environment

**macOS/Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

---

## ▶️ Run the API

```bash
uvicorn main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

## 📚 Swagger Documentation

Open your browser and visit:

```
http://127.0.0.1:8000/docs
```

Swagger UI allows you to test every API endpoint directly from the browser.

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

---

# 📝 Request Examples

## Create Task

**POST** `/tasks`

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

```json
{
  "title": "Learn AI",
  "done": true
}
```

---

## Delete Task

**DELETE** `/tasks/1`

Response Status:

```
204 No Content
```

---

# 📷 Swagger UI Screenshot

Add your Swagger UI screenshot here.

Example:

```
Swagger UI screenshot/
    swagger.png
```

Then display it like this:

```markdown
![Swagger UI](Swagger%20UI%20screenshot/swagger.png)
```

---

# 🧪 Example cURL Command

```bash
curl -X GET http://127.0.0.1:8000/tasks
```

---

# 📈 Learning Outcomes

This project helped me learn:

- REST API fundamentals
- FastAPI routing
- Path parameters
- Request body validation using Pydantic
- CRUD operations
- HTTP status codes (200, 201, 204, 404)
- Swagger UI documentation
- Git and GitHub workflow

---

# 👨‍💻 Author

**Abdul Ahad**

GitHub:
https://github.com/Abdul-Ahad11