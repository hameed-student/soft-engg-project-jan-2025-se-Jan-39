
# Project Setup and Instructions

## Installation and running Instructions

### Step 1: Install Python
Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Step 2: Create a Virtual Environment
Navigate to your project directory and create a virtual environment using the following command:
```sh
python -m venv venv

Step 3: Activate the Virtual Environment
Activate the virtual environment using the command below:

On Windows:
.\venv\Scripts\activate

On macOS and Linux:
source venv/bin/activate

Step 4: Install Required Libraries
Install the required Python libraries by running:
pip install -r backend/requirements.txt


### **important** ###
Step 5: Run the Application
Start the application by running these commands inside the backend directory in the following order:
flask db init
flask db migrate
flask db upgrade
python admin.py
python app.py

Step 6: Access the Application
Open your web browser and go to http://localhost:5000 to access the application.
alternatively you can access via localhost:5173 after running npm run dev inside frontend directory

Additional Notes
Ensure that you have the necessary permissions to install and run Python applications on your system.
If you encounter any issues, refer to the documentation or seek help from the community.


## User Login Details
You can login to 3 types of users using the details below:
- **Admin**
  - Email: admin@app.com
  - Password: Pass@123
  - Role: admin
- **Student**
  - Email: student@app.com
  - Password: Pass@123
  - Role: student
- **Support Staff**
  - Email: support@app.com
  - Password: Pass@123
  - Role: support staff

Alternatively, you can also register as a new student or support staff.

## User Roles and Permissions
- **Admins**: Can add new courses, approve new course enrollments and support staff, and view course contents. In future updates, they will be able to add course contents.
- **Support Staff**: Can approve enrollments of students into courses, view course contents, and apply for other courses as support staff. In future updates, they will be able to update their profile.
- **Students**: Can view course contents and enroll in new courses. In future updates, they will be able to chat with AI using the bottom right chat icon.