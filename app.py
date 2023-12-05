from flask import Flask, render_template, jsonify, request, redirect, url_for, session,flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret'
# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mcis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

core_courses = [
    {'course_code': 'MCIS5103', 'title': 'Advanced Programming Concepts', 'description': 'Advanced concepts in programming.'},
    {'course_code': 'MCIS5133', 'title': 'Database Management Systems', 'description': 'In-depth study of database systems.'},
    {'course_code': 'MCIS6163', 'title': 'Computer Networking', 'description': 'Study of computer networking principles.'},
    {'course_code': 'MCIS6173', 'title': 'Information & Networking Security', 'description': 'Security in networking and information systems.'}
]

elective_courses = [
    {'course_code': 'MCIS5003', 'title': 'Survey of Information Technology', 'description': 'Comprehensive overview of Information Technology'},
    {'course_code': 'MCIS5013', 'title': 'UNIX Operating System', 'description': 'In-depth study of the UNIX operating system'},
    {'course_code': 'MCIS5113', 'title': 'Web Programming: Client Side', 'description': 'Client-side programming for web applications'},
    {'course_code': 'MCIS5313', 'title': 'Data Structures and Algorithms', 'description': 'Advanced data structures and algorithms'},
    {'course_code': 'MCIS5413', 'title': 'Web Programming: Server Side', 'description': 'Server-side programming for web applications'},
    {'course_code': 'MCIS6123', 'title': 'Decision Science', 'description': 'Decision-making processes in business'},
    {'course_code': 'MCIS6133', 'title': 'User Interface Design', 'description': 'Principles and practices of user interface design'},
    {'course_code': 'MCIS6153', 'title': 'Software Engineering', 'description': 'Software development life cycle and methodologies'},
    {'course_code': 'MCIS6183', 'title': 'Special Topics in Computer Science', 'description': 'Various current topics in computer science'},
    {'course_code': 'MCIS6193', 'title': 'Special Topics in Information Systems', 'description': 'Various current topics in information systems'},
    {'course_code': 'MCIS6201-6', 'title': 'Special Topics Seminar', 'description': 'Seminars on special topics in computer science and information systems'},
    {'course_code': 'MCIS6213', 'title': 'Applied Cryptography', 'description': 'Practical aspects of cryptography'},
    {'course_code': 'MCIS6223', 'title': 'Vulnerability and Risk Assessment', 'description': 'Assessing and managing vulnerabilities and risks in systems'},
    {'course_code': 'MCIS6233', 'title': 'Traceable Systems and Computer Forensics', 'description': 'Forensic analysis of computer systems'},
    {'course_code': 'MCIS6243', 'title': 'Wireless and Mobile Security', 'description': 'Security issues in wireless and mobile networks'},
    {'course_code': 'MCIS6253', 'title': 'Privacy Compliant Systems Design', 'description': 'Designing systems that comply with privacy laws and regulations'},
    {'course_code': 'MCIS6263', 'title': 'Big Data', 'description': 'Technologies and methodologies for handling big data'},
    {'course_code': 'MCIS6273', 'title': 'Data Mining', 'description': 'Methods for extracting useful information from large datasets'},
    {'course_code': 'MCIS6283', 'title': 'Machine Learning', 'description': 'Algorithms and techniques in machine learning'},
    {'course_code': 'MCIS6293', 'title': 'Special Topics in Cybersecurity', 'description': 'Various current topics in cybersecurity'},
    {'course_code': 'MCIS6983', 'title': 'Internship in Computer and Information Science', 'description': 'Practical work experience in computer and information science'},
    {'course_code': 'MCIS6911-6', 'title': 'Thesis', 'description': 'Research project in computer and information science'}
]

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), nullable=False)  # 'student', 'advisor', or 'admin'
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_core = db.Column(db.Boolean, default=False)
    sections = db.relationship('Section', backref='course', lazy=True)

class DegreePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_code = db.Column(db.Integer, db.ForeignKey('course.course_code'), nullable=False)
    approved = db.Column(db.Boolean, default=False)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(100), unique=True, nullable=False)
    course_code = db.Column(db.Integer, db.ForeignKey('course.course_code'), nullable=False)
    semester = db.Column(db.String(20))
    meeting_time = db.Column(db.String(100))  # Example format: "MWF 10-11 AM"
    location = db.Column(db.String(100))      # Example: "Building A, Room 101"
    instructor = db.Column(db.String(100))    # Name of the instructor
    capacity = db.Column(db.Integer, default=15)
    current_enrollment = db.Column(db.Integer, default=0)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

class UserActionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "action": self.action
        }


class ChangeRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    degree_plan_id = db.Column(db.Integer, db.ForeignKey('degree_plan.id'), nullable=False)
    requested_changes = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending')  # e.g., 'pending', 'approved', 'denied'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "degree_plan_id": self.degree_plan_id,
            "requested_changes": self.requested_changes,
            "status": self.status,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
##class Schedule(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
##    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
#    
#
#    # Establish a relationship with the Section model
#    section = db.relationship('Section', back_populates='schedule')*/


def initialize_courses():
    existing_courses = Course.query.count()
    if existing_courses == 0:
        for course_data in core_courses:
            course = Course(**course_data, is_core=True)
            db.session.add(course)

        for course_data in elective_courses:
            course = Course(**course_data, is_core=False)
            db.session.add(course)

        db.session.commit()
        print("Courses initialized in the database.")
    else:
        print("Courses are already initialized.")

# Create the database tables
#@app.before_first_request
#def create_tables():
with app.app_context():
    db.create_all()
    initialize_courses()

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.password_hash == password:
        session['username'] = user.username
        session['role'] = user.role
        return redirect(url_for('index'))
    flash('Invalid username or password')
    return redirect(url_for('login_form'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login_form'))

# Routes for the student interface
@app.route('/')
def index():
    return render_template('studentInterface.html')

@app.route('/view_degree_plan', methods=['GET'])
def view_degree_plan():
    # Placeholder for actual database query
    # degree_plan = DegreePlan.query.filter_by(student_id=session['user_id']).first()
    # return jsonify(degree_plan.to_dict())
    if 'username' not in session:
        return redirect(url_for('login_form'))

    student_id = User.query.filter_by(username=session['username']).first().id
    print(student_id)
    #degree_plans = DegreePlan.query.filter_by(student_id=student_id).all()

    #print(degree_plans)
    plan_data = []
    degree_plans = DegreePlan.query.filter_by(student_id=student_id).all()
    print("Degree Plans:", degree_plans)

    for plan in degree_plans:
        course_details = Course.query.filter_by(course_code=plan.course_code).first()
        if course_details:
            plan_data.append({
                "course_id": course_details.id,
                "course_code": course_details.course_code,
                "title": course_details.title,
                "description": course_details.description,
                "is_core": course_details.is_core,
                "approved": plan.approved  # Assuming this field is part of the DegreePlan model
            })
        else:
            print(f"No course found with code: {plan.course_code}")       
    print(plan_data)
    return jsonify(plan_data)
    #return jsonify({"courses": ["Course 1", "Course 2", "Course 3"]})

#@app.route('/submit_degree_plan', methods=['POST'])
#def submit_degree_plan():
#    # Placeholder for saving data to the database
#    # degree_plan = request.json
#    # Save the degree_plan to the database
#    return jsonify({"success": True, "message": "Degree plan submitted"})


def generate_new_section_number(course_id, semester):
    last_section = Section.query.filter_by(course_id=course_id, semester=semester).order_by(Section.section_number.desc()).first()
    if last_section:
        return str(int(last_section.section_number) + 1)
    else:
        return "1"

@app.route('/student/add_degree_plan', methods=['POST'])
def add_degree_plan_student():
    student_id = request.form['student_id']
    course_code = request.form['course_code']
    new_plan = DegreePlan(student_id=student_id, course_code=course_code)
    db.session.add(new_plan)
    db.session.commit()
    log_action("Added a degree plan by Student with id: "+str(student_id))
    return jsonify({"message": "Degree plan added successfully"})
    

@app.route('/student/submit_change_request', methods=['POST'])
def submit_change_request():
    print("Received POST request for /submit_change_request")
    if 'username' not in session:
        return jsonify({"message": "Not logged in"}), 401

    student = User.query.filter_by(username=session['username']).first()
    if not student:
        return jsonify({"message": "Student not found"}), 404

    # Extract the degree plan ID and requested changes from the request
    degree_plan_id = request.json.get('degree_plan_id')
    requested_changes = request.json.get('requested_changes')

    if not degree_plan_id or not requested_changes:
        return jsonify({"message": "Degree plan ID and requested changes are required"}), 400

    # Create a new change request record
    change_request = ChangeRequest(
        student_id=student.id,
        degree_plan_id=degree_plan_id,
        requested_changes=requested_changes
    )
    db.session.add(change_request)
    db.session.commit()
    log_action("Change request for degree plan id: "+str(degree_plan_id)+" by a student")
    return jsonify({"message": "Change request submitted successfully", "id": change_request.id})


@app.route('/student/view_requests', methods=['GET'])
def view_student_requests():
    if 'username' not in session:
        return jsonify({"message": "User not logged in"}), 401
    
    student = User.query.filter_by(username=session['username']).first()
    if not student:
        return jsonify({"message": "Student not found"}), 404
    
    requests = ChangeRequest.query.filter_by(student_id=student.id).all()
    return jsonify([r.to_dict() for r in requests])


@app.route('/student/view_semester_schedule', methods=['GET'])
def view_semester_schedule():
    if 'username' not in session:
        return jsonify({"message": "User not logged in"}), 401
    
    # Optionally, filter by the current semester
    # current_semester = 'Spring 2023' # Example, you can determine this dynamically
    # sections = Section.query.filter_by(semester=current_semester).all()
    
    sections = Section.query.all()
    sections_data = [
        {
            "id": section.id,
            "section_name": section.section_name,
            "course_code": section.course_code,
            "semester": section.semester,
            "meeting_time": section.meeting_time,
            "location": section.location,
            "instructor": section.instructor,
            "capacity": section.capacity,
            "current_enrollment": section.current_enrollment
        } for section in sections
    ]

    return jsonify(sections_data)
'''
@app.route('/student/select_sections', methods=['GET'])
def select_sections():
    if 'username' not in session:
        return jsonify({"message": "Not logged in"}), 401

    student = User.query.filter_by(username=session['username']).first()
    if not student:
        return jsonify({"message": "Student not found"}), 404

    # Get approved degree plans for the student
    approved_plans = DegreePlan.query.filter_by(student_id=student.id, approved=True).all()
    approved_course_codes = [plan.course_code for plan in approved_plans]

    # Get sections for the approved courses
    available_sections = Section.query.filter(Section.course_code.in_(approved_course_codes)).all()

    # Convert sections to a dictionary
    sections_data = [
        {
            "id": section.id,
            "section_name": section.section_name,
            "course_code": section.course_code,
            "semester": section.semester,
            "meeting_time": section.meeting_time,
            "location": section.location,
            "instructor": section.instructor,
            "capacity": section.capacity,
            "current_enrollment": section.current_enrollment
        } for section in available_sections
    ]

    return jsonify(sections_data)
'''

@app.route('/student/select_sections', methods=['GET'])
def select_sections():
    if 'username' not in session:
        return jsonify({"message": "Not logged in"}), 401

    student = User.query.filter_by(username=session['username']).first()
    if not student:
        return jsonify({"message": "Student not found"}), 404

    # Get approved degree plans for the student
    approved_plans = DegreePlan.query.filter_by(student_id=student.id, approved=True).all()
    approved_course_codes = [plan.course_code for plan in approved_plans]

    # Get sections for the approved courses
    all_sections = Section.query.filter(Section.course_code.in_(approved_course_codes)).all()

    # Filter out sections where the student is already enrolled
    available_sections = []
    for section in all_sections:
        existing_enrollment = Enrollment.query.filter_by(student_id=student.id, section_id=section.id).first()
        if not existing_enrollment:
            available_sections.append(section)

    # Convert sections to a dictionary
    sections_data = [
        {
            "id": section.id,
            "section_name": section.section_name,
            "course_code": section.course_code,
            "semester": section.semester,
            "meeting_time": section.meeting_time,
            "location": section.location,
            "instructor": section.instructor,
            "capacity": section.capacity,
            "current_enrollment": section.current_enrollment
        } for section in available_sections
    ]

    return jsonify(sections_data)

@app.route('/student/enroll_in_section', methods=['POST'])
def enroll_in_section():
    if 'username' not in session:
        return jsonify({"message": "Not logged in"}), 401

    student = User.query.filter_by(username=session['username']).first()
    if not student:
        return jsonify({"message": "Student not found"}), 404

    section_id = request.json.get('section_id')

    # Check if the section exists and has capacity
    section = Section.query.get(section_id)
    if not section or section.current_enrollment >= section.capacity:
        return jsonify({"message": "Section not found or full"}), 400

    # Check if student is already enrolled
    if Enrollment.query.filter_by(student_id=student.id, section_id=section_id).first():
        return jsonify({"message": "Already enrolled"}), 400

    # Enroll the student
    new_enrollment = Enrollment(student_id=student.id, section_id=section_id)
    db.session.add(new_enrollment)

    # Increment current enrollment
    section.current_enrollment += 1
    db.session.commit()

    return jsonify({"message": "Enrollment successful"})

@app.route('/student/view_enrollments', methods=['GET'])
def view_enrollments():
    if 'username' not in session:
        return jsonify({"message": "Not logged in"}), 401

    student = User.query.filter_by(username=session['username']).first()
    if not student:
        return jsonify({"message": "Student not found"}), 404

    # Fetch enrollments for the student
    enrollments = Enrollment.query.filter_by(student_id=student.id).all()

    # Join with the Section table to get detailed information
    enrollments_data = []
    for enrollment in enrollments:
        section = Section.query.get(enrollment.section_id)
        if section:
            enrollments_data.append({
                "id": section.id,
                "section_name": section.section_name,
                "course_code": section.course_code,
                "semester": section.semester,
                "meeting_time": section.meeting_time,
                "location": section.location,
                "instructor": section.instructor
            })

    return jsonify(enrollments_data)

# Advisor Routes
@app.route('/advisor/')
def advisor_index():
    return render_template('advisorInterface.html')

@app.route('/advisor/view_all_enrollments', methods=['GET'])
def view_all_enrollments():
    enrollments = db.session.query(
        Enrollment.id,
        Enrollment.student_id,
        Section.section_name,
        Section.course_code
    ).join(Section, Enrollment.section_id == Section.id).all()

    enrollments_data = [
        {
            "id": enrollment.id,
            "student_id": enrollment.student_id,
            "section_name": enrollment.section_name,
            "course_code": enrollment.course_code
        } for enrollment in enrollments
    ]

    return jsonify(enrollments_data)

# Routes for the advisor interface
@app.route('/advisor/view_change_requests', methods=['GET'])
def view_change_requests():
    change_requests = ChangeRequest.query.all()
    requests_data = [request.to_dict() for request in change_requests]
    return jsonify(requests_data)


@app.route('/advisor/edit_request', methods=['POST'])
def edit_request():
    # Assuming you have authentication and authorization set up
    # Ensure the user is authorized to perform this action

    request_id = request.form.get('request_id')
    requested_changes = request.form.get('requested_changes')
    status = request.form.get('status')

    # Validate input data as necessary

    # Find the request in the database
    change_request = ChangeRequest.query.get(request_id)
    if not change_request:
        return jsonify({"message": "Change request not found"}), 404

    # Update the request
    change_request.requested_changes = requested_changes
    change_request.status = status

    # Save changes to the database
    db.session.commit()

    return jsonify({"message": "Change request updated successfully"})

@app.route('/advisor/get_request/<int:request_id>', methods=['GET'])
def get_request(request_id):
    # Assuming you have authentication and authorization set up
    # Ensure the user is authorized to perform this action

    # Find the request in the database
    change_request = ChangeRequest.query.get(request_id)
    if not change_request:
        return jsonify({"message": "Change request not found"}), 404

    # Convert the request to a dictionary (or similar structure)
    request_data = {
        "id": change_request.id,
        "student_id": change_request.student_id,
        "degree_plan_id": change_request.degree_plan_id,
        "requested_changes": change_request.requested_changes,
        "status": change_request.status,
        "timestamp": change_request.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(request_data)

@app.route('/advisor/add_degree_plan', methods=['POST'])
def add_degree_plan_advisor():
    student_id = request.form['student_id']
    course_code = request.form['course_code']
    new_plan = DegreePlan(student_id=student_id, course_code=course_code)
    db.session.add(new_plan)
    db.session.commit()
    log_action("Added a degree plan of a student with id: "+str(student_id)+" by advisor")
    return jsonify({"message": "Degree plan added successfully"})

@app.route('/advisor/edit_degree_plan', methods=['POST'])
def edit_degree_plan_advisor():
    plan_id = request.form['plan_id']
    student_id = request.form['student_id']
    course_code = request.form['course_code']
    approved = 'approved' in request.form

    plan = DegreePlan.query.get(plan_id)
    if plan:
        plan.student_id = student_id
        plan.course_code = course_code
        plan.approved = approved
        db.session.commit()
        log_action("Edited a degree plan of a student with id "+str(plan.student_id)+" by advisor")
        return jsonify({"message": "Degree plan updated successfully"})
    return jsonify({"message": "Degree plan not found"}), 404

@app.route('/advisor/delete_degree_plan/<int:plan_id>', methods=['DELETE'])
def delete_degree_plan_advisor(plan_id):
    plan = DegreePlan.query.get(plan_id)
    if plan:
        db.session.delete(plan)
        db.session.commit()
        log_action("Deleted a degree plan by advisor")
        return jsonify({"message": "Degree plan deleted successfully"})
    return jsonify({"message": "Degree plan not found"}), 404

# Admin Routes
@app.route('/admin/')
def admin_index():
    return render_template('adminInterface.html')


@app.route('/admin/manage_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_data = [{"id": user.id, "username": user.username, "role": user.role} for user in users]

    # Log the user data
    print("Sending user data:", user_data)

    return jsonify(user_data)
    #return jsonify([{"username": user.username, "role": user.role} for user in users])

@app.route('/admin/manage_users/add', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password_hash = request.form['password']
    role = request.form['role']
    new_user = User(username=username, email=email, password_hash=password_hash, role=role)
    db.session.add(new_user)
    db.session.commit()
    log_action("Added a user with name: "+username+" by admin")
    return jsonify({"message": "User added successfully"})

@app.route('/admin/manage_users/delete', methods=['POST'])
def delete_user():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        log_action("Deleted an user with username: "+username+" by admin")
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "User not found"})



@app.route('/admin/manage_courses/add', methods=['POST'])
def add_course():
    course_code = request.form['course_code']
    title = request.form['title']
    description = request.form['description']
    is_core = 'is_core' in request.form
    new_course = Course(course_code=course_code, title=title, description=description, is_core=is_core)
    db.session.add(new_course)
    db.session.commit()
    log_action("Added a course with code: "+course_code+" by admin")
    return jsonify({"message": "Course added successfully"})

# Admin: Manage Courses - Delete a Course
@app.route('/admin/manage_courses/delete', methods=['POST'])
def delete_course():
    course_code = request.form['course_code']
    course = Course.query.filter_by(course_code=course_code).first()
    if course:
        db.session.delete(course)
        db.session.commit()
        log_action("Deleted Course with code: "+course_code+" by admin")
        return jsonify({"message": "Course deleted successfully"})
    return jsonify({"message": "Course not found"})

@app.route('/admin/manage_courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{"course_code": course.course_code, "title": course.title} for course in courses])

@app.route('/admin/manage_degree_plans', methods=['GET'])
def manage_degree_plans():
    degree_plans = DegreePlan.query.all()
    plans_data = [
        {
            "id": plan.id,
            "student_id": plan.student_id,
            "course_code": plan.course_code,
            "approved": plan.approved
        } 
        for plan in degree_plans
    ]
    return jsonify(plans_data)

@app.route('/admin/add_degree_plan', methods=['POST'])
def add_degree_plan():
    student_id = request.form['student_id']
    course_code = request.form['course_code']
    new_plan = DegreePlan(student_id=student_id, course_code=course_code)
    db.session.add(new_plan)
    db.session.commit()
    log_action("Added a degree plan of a student with id: "+str(student_id)+" by admin")
    return jsonify({"message": "Degree plan added successfully"})

@app.route('/admin/get_degree_plan/<int:plan_id>', methods=['GET'])
def get_degree_plan(plan_id):
    plan = DegreePlan.query.get(plan_id)
    if plan:
        return jsonify({
            "id": plan.id,
            "student_id": plan.student_id,
            "course_code": plan.course_code,
            "approved": plan.approved
        })
    return jsonify({"message": "Degree plan not found"}), 404

@app.route('/admin/edit_degree_plan', methods=['POST'])
def edit_degree_plan():
    plan_id = request.form['plan_id']
    student_id = request.form['student_id']
    course_code = request.form['course_code']
    approved = 'approved' in request.form

    plan = DegreePlan.query.get(plan_id)
    if plan:
        plan.student_id = student_id
        plan.course_code = course_code
        plan.approved = approved
        db.session.commit()
        log_action("Edited a degree plan of a student with id "+str(plan.student_id)+" by admin")
        return jsonify({"message": "Degree plan updated successfully"})
    return jsonify({"message": "Degree plan not found"}), 404

@app.route('/admin/delete_degree_plan/<int:plan_id>', methods=['DELETE'])
def delete_degree_plan(plan_id):
    plan = DegreePlan.query.get(plan_id)
    if plan:
        db.session.delete(plan)
        db.session.commit()
        log_action("Deleted a degree plan by admin")
        return jsonify({"message": "Degree plan deleted successfully"})
    return jsonify({"message": "Degree plan not found"}), 404

#@app.route('/admin/manage_degree_plans', methods=['GET'])
#def manage_degree_plans():
#    degree_plans = DegreePlan.query.all()
#    return jsonify([{"id": plan.id, "student_id": plan.student_id, "course_id": plan.course_id, "approved": plan.approved} for plan in degree_plans])

def log_action(action):
    log_entry = UserActionLog(action=action)
    db.session.add(log_entry)
    db.session.commit()

@app.route('/admin/view_logs', methods=['GET'])
def view_logs():
    logs = UserActionLog.query.order_by(UserActionLog.timestamp.desc()).all()
    return jsonify([log.to_dict() for log in logs])

@app.route('/admin/get_section/<int:id>', methods=['GET'])
def get_section(id):
    section = Section.query.get(id)
    if not section:
        return jsonify({"message": "Section not found"}), 404

    section_data = {
        "id": section.id,
        "course_code": section.course_code,
        "semester": section.semester,
        "meeting_time": section.meeting_time,
        "location": section.location,
        "instructor": section.instructor,
        "capacity": section.capacity,
        "current_enrollment": section.current_enrollment
    }

    return jsonify(section_data)

@app.route('/admin/edit_section/<int:id>', methods=['POST'])
def edit_section(id):
    section = Section.query.get(id)
    if not section:
        return jsonify({"message": "Section not found"}), 404

    section.section_name = request.form.get('section_name', section.section_name)
    section.course_code = request.form.get('course_code', section.course_code)
    section.semester = request.form.get('semester', section.semester)
    section.meeting_time = request.form.get('meeting_time', section.meeting_time)
    section.location = request.form.get('location', section.location)
    section.instructor = request.form.get('instructor', section.instructor)
    section.capacity = request.form.get('capacity', section.capacity, type=int)

    # Optionally, add validation for course_code or other fields if needed

    db.session.commit()
    log_action("Edited "+section.course_code+" section by admin")
    return jsonify({"message": "Section updated successfully"})

@app.route('/admin/add_section', methods=['POST'])
def add_section():
    section_name = request.form.get('section_name')
    course_code = request.form.get('course_code')
    semester = request.form.get('semester')
    meeting_time = request.form.get('meeting_time')
    location = request.form.get('location')
    instructor = request.form.get('instructor')
    capacity = request.form.get('capacity', 15, type=int)

    # Check if section_name already exists
    if Section.query.filter_by(section_name=section_name).first():
        return jsonify({"message": "Section name already exists"}), 400

    # Check if course with the given course_code exists
    course_exists = Course.query.filter_by(course_code=course_code).first()
    if not course_exists:
        return jsonify({"message": "Course code not found"}), 404

    new_section = Section(
        section_name=section_name,
        course_code=course_code,
        semester=semester,
        meeting_time=meeting_time,
        location=location,
        instructor=instructor,
        capacity=capacity
    )

    db.session.add(new_section)
    db.session.commit()
    log_action("Added "+section_name+" section by admin")
    return jsonify({"message": "Section added successfully"})

@app.route('/admin/delete_section/<int:id>', methods=['DELETE'])
def delete_section(id):
    section = Section.query.get(id)
    if not section:
        return jsonify({"message": "Section not found"}), 404

    db.session.delete(section)
    db.session.commit()
    log_action("Deleted a section by admin")
    return jsonify({"message": "Section deleted successfully"})

@app.route('/admin/get_sections', methods=['GET'])
def get_sections():
    sections = Section.query.all()
    sections_data = [
        {
            "id": section.id,
            "section_name": section.section_name,
            "course_code": section.course_code,
            "semester": section.semester,
            "meeting_time": section.meeting_time,
            "location": section.location,
            "instructor": section.instructor,
            "capacity": section.capacity,
            "current_enrollment": section.current_enrollment
        } for section in sections
    ]

    return jsonify(sections_data)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
