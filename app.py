from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mcis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    approved = db.Column(db.Boolean, default=False)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    section_number = db.Column(db.String(10))
    semester = db.Column(db.String(20))
    capacity = db.Column(db.Integer, default=15)
    current_enrollment = db.Column(db.Integer, default=0)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

# Create the database tables
#@app.before_first_request
#def create_tables():
with app.app_context():
    db.create_all()

# Routes for the student interface
@app.route('/')
def index():
    return render_template('studentInterface.html')

@app.route('/view_degree_plan', methods=['GET'])
def view_degree_plan():
    # Placeholder for actual database query
    # degree_plan = DegreePlan.query.filter_by(student_id=session['user_id']).first()
    # return jsonify(degree_plan.to_dict())
    return jsonify({"courses": ["Course 1", "Course 2", "Course 3"]})

@app.route('/submit_degree_plan', methods=['POST'])
def submit_degree_plan():
    # Placeholder for saving data to the database
    # degree_plan = request.json
    # Save the degree_plan to the database
    return jsonify({"success": True, "message": "Degree plan submitted"})

@app.route('/enroll_in_section', methods=['POST'])
def enroll_in_section():
    student_id = request.form.get('student_id')
    course_id = request.form.get('course_id')
    semester = request.form.get('semester')

    # Find or create a section
    #section = Section.query.filter_by(course_id=course_id, semester=semester, current_enrollment < Section.capacity).first()
    section = Section.query.filter(
    Section.course_id == course_id,
    Section.semester == semester,
    Section.current_enrollment < Section.capacity).first()
    if not section:
        section_number = generate_new_section_number(course_id, semester)
        section = Section(course_id=course_id, semester=semester, section_number=section_number)
        db.session.add(section)
        db.session.commit()

    # Check if student is already enrolled
    existing_enrollment = Enrollment.query.filter_by(student_id=student_id, section_id=section.id).first()
    if existing_enrollment:
        return jsonify({"success": False, "message": "Already enrolled in this course section."})

    # Enroll the student
    enrollment = Enrollment(student_id=student_id, section_id=section.id)
    db.session.add(enrollment)
    section.current_enrollment += 1
    db.session.commit()

    return jsonify({"success": True, "message": f"Enrolled in section {section.section_number}."})

def generate_new_section_number(course_id, semester):
    last_section = Section.query.filter_by(course_id=course_id, semester=semester).order_by(Section.section_number.desc()).first()
    if last_section:
        return str(int(last_section.section_number) + 1)
    else:
        return "1"
    
# Advisor Routes
@app.route('/advisor/')
def advisor_index():
    return render_template('advisorInterface.html')

# Routes for the advisor interface
@app.route('/advisor/review_plans', methods=['GET'])
def review_plans():
    # Placeholder for fetching degree plans for review
    # plans = DegreePlan.query.all()
    # return jsonify([plan.to_dict() for plan in plans])
    return jsonify({"degree_plans": ["Plan 1", "Plan 2"]})

@app.route('/advisor/finalize_plan', methods=['POST'])
def finalize_plan():
    # Placeholder for updating the degree plan status in the database
    # degree_plan_id = request.json.get('plan_id')
    # Update the degree plan status to 'finalized'
    return jsonify({"success": True, "message": "Degree plan finalized"})

# Admin Routes
@app.route('/admin/')
def admin_index():
    return render_template('adminInterface.html')

# Routes for the administrative interface
@app.route('/admin/manage_users', methods=['GET', 'POST'])
def manage_users():
    # Logic to manage user accounts
    return jsonify({"users": ["User 1", "User 2"]})

@app.route('/admin/manage_courses', methods=['GET', 'POST'])
def manage_courses():
    # Logic to manage course offerings
    return jsonify({"courses": ["Course 1", "Course 2"]})

@app.route('/admin/manage_degree_plans', methods=['GET', 'POST'])
def manage_degree_plans():
    # Logic to manage degree plans
    return jsonify({"degree_plans": ["Plan 1", "Plan 2"]})

@app.route('/admin/manage_schedules', methods=['GET', 'POST'])
def manage_schedules():
    # Logic to manage schedules
    return jsonify({"schedules": ["Schedule 1", "Schedule 2"]})

@app.route('/admin/view_logs', methods=['GET'])
def view_logs():
    # Logic to view change logs
    return jsonify({"logs": ["Log 1", "Log 2"]})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
