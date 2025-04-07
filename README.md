
---

# 🧪 Project Setup and Instructions

## 🚀 Installation and Running Instructions

### ✅ Step 1: Install Python
Make sure Python is installed on your system.  
📥 [Download Python](https://www.python.org/downloads/)

---

### ✅ Step 2: Create a Virtual Environment
```sh
python -m venv venv
```

---

### ✅ Step 3: Activate the Virtual Environment

**Windows:**
```sh
.\venv\Scripts\activate
```

**macOS/Linux/WSL:**
```sh
source venv/bin/activate
```

---

### ✅ Step 4: Install Required Dependencies
```sh
pip install -r backend/requirements.txt
```

---

### ⚠️ Step 5: **Run Redis Server**

**Redis is required before running Celery.**  
In a new terminal (or WSL terminal), start Redis:
```sh
redis-server
```

📌 **Ensure `redis-server` is installed**. If not, install via:

- **Ubuntu/WSL:**
  ```sh
  sudo apt update
  sudo apt install redis-server
  ```

- **macOS (Homebrew):**
  ```sh
  brew install redis
  ```

- **Windows:** Use Redis via WSL or install it using [Memurai](https://www.memurai.com/) or [Docker](https://hub.docker.com/_/redis).

---

### ✅ Step 6: Run Celery (with Beat)

In **another new terminal**, run:
```sh
celery -A app.celery worker --beat --loglevel=info
```

📌 Make sure Redis is running before starting Celery.

---

### ✅ Step 7: Run the Main Application

In the project root, run:
```sh
./run
```

---

### ✅ Step 8: Access the Application

- Backend: [http://localhost:5000](http://localhost:5000)
- Frontend: Open a terminal, go to `frontend/`, and run:
  ```sh
  npm install
  npm run dev
  ```
  Then open [http://localhost:5173](http://localhost:5173)

---

## 👥 User Login Details

| Role          | Email              | Password  |
|---------------|--------------------|-----------|
| **Admin**     | admin@app.com      | Pass@123  |
| **Student**   | student@app.com    | Pass@123  |
| **Support**   | support@app.com    | Pass@123  |

You may also register as a new student or support staff.

---

## 🔐 User Roles and Permissions

### 👑 Admin
- Add new courses
- Approve course enrollments and support staff
- View course contents
- Add course materials

### 🛠️ Support Staff
- Approve student enrollments
- View course content
- Apply for support roles in other courses
- Profile management

### 🎓 Students
- Enroll in courses
- View enrolled course content
- AI-powered chat support

---

## 🛠️ Troubleshooting & Precautions

- ❗**Redis not found?**
  - Check installation using `redis-server --version`
  - Use `sudo service redis-server start` (Linux) or run manually if installed via Homebrew

- ❗**Celery fails to connect to Redis?**
  - Ensure Redis is running (`redis-cli ping` → should return `PONG`)
  - Check `CELERY_BROKER_URL` in your config (`redis://localhost:6379/0`)

- 🔁 **Always open new terminals** for:
  - Redis server
  - Celery + Beat
  - Main backend server
  - Frontend dev server

- 🔒 **Permissions:**
  - Use `chmod +x run` if `./run` is not executable
  - Use virtual environment to avoid conflicts

---
