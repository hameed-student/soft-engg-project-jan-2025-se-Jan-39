from flask import Flask, send_from_directory, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt, get_jwt_identity, create_access_token, create_refresh_token
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import os, re, io, csv


app = Flask(__name__, static_folder='dist')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_tutor.db'
app.config['JWT_SECRET_KEY'] = 'SE_Project_T-39'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # student, support_staff, admin, manager, developer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    enrollments = db.relationship('StudentEnrollment', back_populates='student', cascade="all, delete-orphan")
    support_courses = db.relationship('SupportStaff', back_populates='staff', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_access_token(self):
        return create_access_token(identity={"id": self.id, "role": self.role}, expires_delta=timedelta(hours=24))
    
    def generate_refresh_token(self):
        return create_refresh_token(identity={"id": self.id, "role": self.role}, expires_delta=timedelta(hours=168))
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    prof = db.Column(db.String(100), nullable=False)
    
    contents = db.relationship('CourseContent', back_populates='course', cascade="all, delete-orphan")
    enrollments = db.relationship('StudentEnrollment', back_populates='course', cascade="all, delete-orphan")
    support_staff = db.relationship('SupportStaff', back_populates='course', cascade="all, delete-orphan")
    

class CourseContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    week = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    video_link = db.Column(db.String(200), nullable=False)

    course = db.relationship('Course', back_populates='contents')

class StudentEnrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)
    approved_at = db.Column(db.DateTime)
    
    student = db.relationship('User', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')
    
    
class SupportStaff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)
    approved_at =db.Column(db.DateTime)
    
    staff = db.relationship('User', back_populates='support_courses')
    course = db.relationship('Course', back_populates='support_staff')
    
class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(50), unique=True, nullable=False)
    token_type = db.Column(db.String(20), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=datetime.utcnow)
    

def is_token_blacklisted(jti):
    return TokenBlacklist.query.filter_by(jti=jti).first() is not None


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    return is_token_blacklisted(jwt_payload["jti"])


@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has been revoked"}), 401


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity().get("id")
    new_access_token = create_access_token(identity={"id": user_id})
    return jsonify({"access_token": new_access_token}), 200
    
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # If the request is for a static file (CSS/JS), serve it normally
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # For all other paths, serve the index.html so Vue Router can handle it
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = user.generate_access_token()
        refresh_token = user.generate_refresh_token()
        return jsonify({ "user": { "name": user.name, "email": user.email, "role": user.role }, "access_token": access_token, "refresh_token": refresh_token, "message": 'Login successful!'}), 200
    return jsonify({"error": "Invalid username or password."}), 401
    

def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None


def is_valid_password(password):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password) is not None


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('retypePassword')
    role = data.get('role')
    
    
    if not email or len(email) > 100 or not is_valid_email(email):
        return jsonify({"error": "Invalid or missing 'email'. Must be a valid email address and 100 characters or less."}), 400
    if not password or len(password) < 8 or not is_valid_password(password):
        return jsonify({"error": "Invalid or missing 'password'. Must be at least 8 characters long."}), 400
    if not password or len(confirm_password) < 8 or not is_valid_password(confirm_password):
        return jsonify({"error": "Invalid or missing 'password'. Must be at least 8 characters long."}), 400
    if not name or len(name) > 100:
        return jsonify({"error": "Invalid or missing 'name'. Must be 100 characters or less."}), 400
    if role not in ['student', 'support_staff', 'admin', 'manager', 'developer']:
        return jsonify({"error": "Invalid 'role'. Must be one of ['student', 'support_staff']."}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Username already exists."}), 400
    if password != confirm_password:
        return jsonify({"message": "Password and Confirm Password must be same."}), 400

    new_user = User(name=name, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    user = User.query.filter_by(email=email).first()
    access_token = user.generate_access_token()
    refresh_token = user.generate_refresh_token()    
    return jsonify({"user": { "name": user.name, "email": user.email, "role": user.role }, "access_token": access_token, "refresh_token": refresh_token, "message": "User registered successfully!"}), 201


@app.route('/logout_refresh', methods=['POST'], endpoint='loggig_out_user_refresh_token_invalidation')
@jwt_required(refresh=True)
def logout_refresh():
    jti = get_jwt()["jti"]
    token_type = get_jwt()["type"]
    expires = datetime.fromtimestamp(get_jwt()["exp"])
    if expires > datetime.now():
        revoked_token = TokenBlacklist(jti=jti, token_type=token_type, expires=expires)
        db.session.add(revoked_token)
        db.session.commit()          
    return jsonify({"message": "Refresh token revoked"}), 200

@app.route('/logout', methods=['POST'], endpoint='loggig_out_user_access_token_invalidation')
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    token_type = get_jwt()["type"]
    expires = datetime.fromtimestamp(get_jwt()["exp"])
    if expires > datetime.now():
        revoked_token = TokenBlacklist(jti=jti, token_type=token_type, expires=expires)
        db.session.add(revoked_token)
        db.session.commit()         
    return jsonify({"message": "Successfully logged out"}), 200


@app.route('/approve/support_staffs', methods=['PUT'], endpoint='approve_support_staffs')
@jwt_required()
def approve_staff():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role != 'admin':
        return jsonify({"error": "Unauthorized request denied."}), 403
    data = request.json
    staff_id = data.get('staff_id')
    course_id = data.get('course_id')
    action = data.get('action')
    if not staff_id or not course_id or action not in ["approve", "reject"]:
        return jsonify({"error": "staff_id, course_id, and valid action are required"}), 400
    instructor = SupportStaff.query.filter_by(staff_id=staff_id, course_id=course_id).first()  
    if not instructor:
        return jsonify({"error": "Support Staff not found"}), 404
    if action == "approve":
        instructor.approved = True
        instructor.approved_at = datetime.utcnow()
        message = "Support Staff approved successfully."
    else:
        db.session.delete(instructor)
        message = "Support Staff rejected successfully."
    db.session.commit()
    return jsonify({"message": message}), 200


@app.route('/apply/support_staff', methods=['POST'])
@jwt_required()
def apply_support_staff():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role != 'support_staff':
        return jsonify({"error": "Unauthorized request. Only staff can apply to assist courses."}), 403
    data = request.json
    course_id = data.get('course_id')
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400
    existing_application = SupportStaff.query.filter_by(staff_id=user_id, course_id=course_id).first()
    if existing_application:
        return jsonify({"error": "You have already applied to be support staff for this course."}), 400
    application = SupportStaff(staff_id=user_id, course_id=course_id, applied_at=datetime.utcnow(), approved=False)
    db.session.add(application)
    db.session.commit()
    return jsonify({"message": "Support staff application submitted successfully. Pending approval."}), 201


@app.route('/approve/course_enrollment', methods=['PUT'], endpoint='approve_course_enrollment')
@jwt_required()
def approve_enrollment():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role not in ['support_staff', 'admin']:
        return jsonify({"error": "Unauthorized request denied."}), 403
    data = request.json
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    action = data.get('action')
    if not student_id or not course_id or action not in ["approve", "reject"]:
        return jsonify({"error": "student_id, course_id, and valid action are required"}), 400
    enrollment = StudentEnrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if not enrollment:
        return jsonify({"error": "Student enrollment not found"}), 404
    if user.role == 'support_staff':
        is_assigned = SupportStaff.query.filter_by(staff_id=user_id, course_id=course_id, approved=True).first()
        if not is_assigned:
            return jsonify({"error": "You are not authorized to manage this enrollment."}), 403
    if action == "approve":
        enrollment.approved = True
        enrollment.approved_at = datetime.utcnow()
        message = "Student enrollment approved successfully."
    else:
        db.session.delete(enrollment)
        message = "Student enrollment rejected successfully."
    db.session.commit()
    return jsonify({"message": message}), 200



@app.route('/register/course', methods=['POST'])
@jwt_required()
def register_course():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role != 'student':
        return jsonify({"error": "Unauthorized request. Only students can register for courses."}), 403
    data = request.json
    course_id = data.get('course_id')
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400
    existing_enrollment = StudentEnrollment.query.filter_by(student_id=user_id, course_id=course_id).first()
    if existing_enrollment:
        return jsonify({"error": "You are already registered for this course."}), 400
    enrollment = StudentEnrollment(student_id=user_id, course_id=course_id, registered_at=datetime.utcnow(), approved=False)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({"message": "Course registration submitted successfully. Pending approval."}), 201


@app.route('/add/new_course', methods=['POST'])
@jwt_required()
def add_new_course():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role != 'admin':
        return jsonify({"error": "Unauthorized request. Only admin can add new courses."}), 403
    data = request.json
    name = data.get('name')
    prof = data.get('prof')
    if not name or len(name) > 100:
        return jsonify({"error": "Invalid or missing 'course name'. Must be 100 characters or less."}), 400
    if not prof or len(prof) > 100:
        return jsonify({"error": "Invalid or missing 'prof. name'. Must be 100 characters or less."}), 400    
    new_course = Course(name=name, prof=prof)
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"message": "New course added successfully..."}), 201
    
    
@app.route('/add_or_update/course_contents', methods=['POST'])
@jwt_required()
def add_or_update_course_contents():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role not in ['admin', 'support_staff']:
        return jsonify({"error": "Unauthorized request. Only admin or support staff can add course contents."}), 403
    data = request.json
    required_fields = ['course_id', 'week', 'title', 'description', 'video_link']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: course_id, week, title, description, video_link"}), 400
    course_id = data['course_id']
    week = data['week']
    title = data['title']
    description = data['description']
    video_link = data['video_link']
    
    if not isinstance(week, int) or week < 1 or week > 52:
        return jsonify({"error": "Invalid week. Must be an integer between 1 and 52."}), 400
    if not isinstance(title, str) or len(title) > 100:
        return jsonify({"error": "Invalid title. Must be a string with max 100 characters."}), 400
    if not isinstance(description, str) or len(description) > 200:
        return jsonify({"error": "Invalid description. Must be a string with max 200 characters."}), 400
    
    url_pattern = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be|vimeo\.com|drive\.google\.com)/.+')
    if not isinstance(video_link, str) or not re.match(url_pattern, video_link):
        return jsonify({"error": "Invalid video link. Must be a valid YouTube, Vimeo, or Google Drive link."}), 400

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found. Select another course."}), 404
    existing_content = CourseContent.query.filter_by(course_id=course_id, week=week, title=title).first()
    if existing_content:
        existing_content.title = title
        existing_content.description = description
        existing_content.video_link = video_link
        message = "Course content updated successfully."
    else:
        new_content = CourseContent(course_id=course_id, week=week, title=title, description=description, video_link=video_link)
        db.session.add(new_content)
        message = "Course content added successfully."
    db.session.commit()
    return jsonify({"message": message}), 200


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"csv"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_course_contents', methods=['POST'])
@jwt_required()
def upload_course_contents():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role not in ['admin', 'support_staff']:
        return jsonify({"error": "Unauthorized request. Only admin or support staff can upload course contents."}), 403
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Please upload a CSV file."}), 400

    try:
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        csv_reader = csv.DictReader(stream)
        required_columns = {"course_id", "week", "title", "description", "video_link"}
        if not required_columns.issubset(csv_reader.fieldnames):
            return jsonify({"error": "CSV file must contain columns: course_id, week, title, description, video_link"}), 400
        contents_to_add = []
        for row in csv_reader:
            try:
                course_id = int(row["course_id"])
                week = int(row["week"])
                title = row["title"].strip()
                description = row["description"].strip()
                video_link = row["video_link"].strip()
                
                course = Course.query.get(course_id)
                if not course:
                    return jsonify({"error": f"Course ID {course_id} not found."}), 404
                if week < 1 or week > 52:
                    return jsonify({"error": f"Invalid week {week}. Must be between 1 and 52."}), 400
                if len(title) > 100:
                    return jsonify({"error": f"Title too long for week {week}. Max 100 characters."}), 400
                if len(description) > 200:
                    return jsonify({"error": f"Description too long for week {week}. Max 200 characters."}), 400

                url_pattern = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be|vimeo\.com|drive\.google\.com)/.+')
                if not re.match(url_pattern, video_link):
                    return jsonify({"error": f"Invalid video link for week {week}. Must be YouTube, Vimeo, or Google Drive link."}), 400

                existing_content = CourseContent.query.filter_by(course_id=course_id, week=week, title=title).first()
                if existing_content:
                    existing_content.title = title
                    existing_content.description = description
                    existing_content.video_link = video_link
                else:
                    new_content = CourseContent(course_id=course_id, week=week, title=title, description=description, video_link=video_link)
                    contents_to_add.append(new_content)
            except ValueError:
                return jsonify({"error": "Invalid data format in CSV file."}), 400
        if contents_to_add:
            db.session.bulk_save_objects(contents_to_add)
        db.session.commit()
        return jsonify({"message": "Course contents uploaded successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"Error processing CSV file: {str(e)}"}), 500
    
    
@app.route('/delete_course_content', methods=['DELETE'])
@jwt_required()
def delete_course_content():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role not in ['admin', 'support_staff']:
        return jsonify({"error": "Unauthorized request. Only admin or support staff can delete course content."}), 403
    data = request.get_json()
    course_id = data.get("course_id")
    week = data.get("week")
    title = data.get("title")
    if not course_id or not week or not title:
        return jsonify({"error": "course_id and week are required."}), 400
    try:
        course_id = int(course_id)
        week = int(week)
        title = title.strip()
    except ValueError:
        return jsonify({"error": "course_id and week must be integers and title must be string."}), 400
    content = CourseContent.query.filter_by(course_id=course_id, week=week, title=title).first()
    if not content:
        return jsonify({"error": f"No content found for Course ID {course_id}, Week {week}, Title {title}."}), 404
    db.session.delete(content)
    db.session.commit()
    return jsonify({"message": f"Course content for Course ID {course_id}, Week {week}, Title {title} deleted successfully."}), 200


@app.route('/course_contents/<int:course_id>', methods=['GET'])
@jwt_required()
def course_contents(course_id):
    user_id = get_jwt_identity().get("id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404
    if user.role == 'student':
        course_enrollment = StudentEnrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
        if not course_enrollment or not course_enrollment.approved:
            return jsonify({"message": "You are not enrolled in this course."}), 403
    contents = CourseContent.query.filter_by(course_id=course_id).all()
    course_contents = []
    for content in contents:
        course_contents.append({
            "id": content.id,
            "week": content.week,
            "title": content.title,
            "description": content.description,
            "video_link": content.video_link
        })
    return jsonify({"course_contents": course_contents}), 200


@app.route('/dashboard/admin', methods=['GET'], endpoint="admin_dashboard")
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role != 'admin':
        return jsonify({"error": "Unauthorized request. Only admin can access this path."}), 403    
    courses = Course.query.all()
    courses = [{"id": course.id, "name": course.name} for course in courses]
    pendingApprovals = db.session.query(User, Course).join(SupportStaff, User.id == SupportStaff.staff_id).join(Course, Course.id == SupportStaff.course_id).filter(SupportStaff.approved == False).all()
    pendingApprovals = [{"staff_id": staff.id, "staff_name": staff.name, "staff_email": staff.email , "course_id": course.id, "course_name": course.name} for staff, course in pendingApprovals]
    pendingEnrollments = db.session.query(User, Course).join(StudentEnrollment, User.id == StudentEnrollment.student_id).join(Course, Course.id == StudentEnrollment.course_id).filter(StudentEnrollment.approved == False).all()
    pendingEnrollments = [{"student_id": student.id, "student_name": student.name, "student_email": student.email, "course_id": course.id, "course_name": course.name} for student, course in pendingEnrollments]
    return jsonify({"courses": courses, "pendingApprovals": pendingApprovals, "pendingEnrollments": pendingEnrollments}), 200


@app.route('/dashboard/support_staff', methods=['GET'], endpoint="support_staff_dashboard")
@jwt_required()
def support_staff_dashboard():
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role != 'support_staff':
        return jsonify({"error": "Unauthorized request. Only Support Staff can access this path."}), 403    
    courses = Course.query.all()
    courses = [{"id": course.id, "name": course.name} for course in courses]
    support_courses = db.session.query(Course).join(SupportStaff).filter(SupportStaff.staff_id == user.id, SupportStaff.approved == True).all()
    support_courses_ids = {course.id for course in support_courses} 
    support_courses = [{"id": course.id, "name": course.name} for course in support_courses]
    pendingEnrollments = db.session.query(User, Course).join(StudentEnrollment, User.id == StudentEnrollment.student_id).join(Course, Course.id == StudentEnrollment.course_id).filter(StudentEnrollment.approved == False, Course.id.in_(support_courses_ids)).all()
    pendingEnrollments = [{"student_id": student.id, "student_name": student.name, "student_email": student.email, "course_id": course.id, "course_name": course.name} for student, course in pendingEnrollments]
    return jsonify({"courses": courses, "support_courses": support_courses, "pendingEnrollments": pendingEnrollments}), 200


@app.route('/dashboard/student', methods=['GET'], endpoint="student_dashboard")
@jwt_required()
def student_dashboard(): 
    user_id = get_jwt_identity().get("id")
    user = User.query.get_or_404(user_id)
    if user.role != 'student':
        return jsonify({"error": "Unauthorized request. Only Student can access this path."}), 403    
    courses = Course.query.all()
    courses = [{"id": course.id, "name": course.name} for course in courses]
    enrolled_courses = db.session.query(Course).join(StudentEnrollment).filter(StudentEnrollment.student_id == user.id, StudentEnrollment.approved == True).all()
    enrolled_courses = [{"id": course.id, "name": course.name} for course in enrolled_courses]
    return jsonify({"courses": courses, "enrolled_courses": enrolled_courses}), 200


if __name__ == '__main__':
    app.run(debug=True)