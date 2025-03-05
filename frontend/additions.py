
@app.route('/open', methods=['GET'])
def open():
    courses = Course.query.all()
    courses = [{"id": course.id, "name": course.name} for course in courses]
    return jsonify({"message": "Anyone can view this page", "courses":courses}), 200  

##############################################################################################################

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
        content_id = existing_content.id
        new_content=False
    else:
        new_content = CourseContent(course_id=course_id, week=week, title=title, description=description, video_link=video_link)
        db.session.add(new_content)
        message = "Course content added successfully."
        content_id = new_content.id
 #       extract_video_transcripts.delay(content_id)
#        message += " Transcript extraction started."
    db.session.commit()
    return jsonify({"message": message}), 200

##############################################################################################################
@app.route('/dashboard/admin', methods=['GET'], endpoint="admin_dashboard")
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    if user.role != 'admin':
        return jsonify({"error": "Unauthorized request. Only admin can access this path."}), 403    
    courses = Course.query.all()
    courses = [{"id": course.id, "name": course.name , "prof": course.prof} for course in courses]
    pendingApprovals = db.session.query(User, Course).join(SupportStaff, User.id == SupportStaff.staff_id).join(Course, Course.id == SupportStaff.course_id).filter(SupportStaff.approved == False).all()
    pendingApprovals = [{"staff_id": staff.id, "staff_name": staff.name, "staff_email": staff.email , "course_id": course.id, "course_name": course.name} for staff, course in pendingApprovals]
    pendingEnrollments = db.session.query(User, Course).join(StudentEnrollment, User.id == StudentEnrollment.student_id).join(Course, Course.id == StudentEnrollment.course_id).filter(StudentEnrollment.approved == False).all()
    pendingEnrollments = [{"student_id": student.id, "student_name": student.name, "student_email": student.email, "course_id": course.id, "course_name": course.name} for student, course in pendingEnrollments]
    return jsonify({"courses": courses, "pendingApprovals": pendingApprovals, "pendingEnrollments": pendingEnrollments}), 200

##############################################################################################################

app.app_context().push()
db.create_all()