
---

# 🧪 Project Setup and Instructions

## 🚀 Installation and Running Instructions

### ✅ Step 1: Install Python
Make sure Python is installed on your system. You can download it from the official site:  
👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### ✅ Step 2: Create a Virtual Environment
Navigate to your project directory and run:
```sh
python -m venv venv
```

---

### ✅ Step 3: Activate the Virtual Environment

**On Windows:**
```sh
.\venv\Scripts\activate
```

**On macOS and Linux:**
```sh
source venv/bin/activate
```

---

### ✅ Step 4: Install Required Libraries
Install project dependencies:
```sh
pip install -r backend/requirements.txt
```

---

### ⚠️ **Important**  
### ✅ Step 5: Run the Application  
Inside the project root directory, execute:
```sh
./run
```

---

### ✅ Step 6: Access the Application

- Open [http://localhost:5000](http://localhost:5000)
- Alternatively, you can run the frontend by navigating to the `frontend` directory and using:
  ```sh
  npm run dev
  ```
  Then open [http://localhost:5173](http://localhost:5173)

---

## 👥 User Login Details

You can use the following credentials to log in:

### 🔐 Admin
- **Email:** `admin@app.com`  
- **Password:** `Pass@123`  
- **Role:** `admin`

### 🎓 Student
- **Email:** `student@app.com`  
- **Password:** `Pass@123`  
- **Role:** `student`

### 🛠️ Support Staff
- **Email:** `support@app.com`  
- **Password:** `Pass@123`  
- **Role:** `support staff`

You can also register as a new **student** or **support staff** from the app.

---

## 🔑 User Roles and Permissions

### 👑 Admin
- Add new courses
- Approve course enrollments and support staff
- View course contents
- *(Coming soon: Add course content)*

### 🛠️ Support Staff
- Approve student enrollments
- View course contents
- Apply for other courses as support staff
- *(Coming soon: Update profile)*

### 🎓 Students
- View course contents
- Enroll in new courses
- *(Coming soon: Chat with AI support)*

---

## 📌 Additional Notes
- Ensure you have permission to install and run Python applications.
- For issues, refer to project documentation or seek help from the community.

--- 
