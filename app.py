from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mcis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# TODO: Define your models (tables) here
# class User(db.Model):
#     ...
# class Course(db.Model):
#     ...
# class DegreePlan(db.Model):
#     ...

# Routes for the student interface
@app.route('/')
def index():
    return render_template('student_interface.html')

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
