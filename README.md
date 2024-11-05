# MCIS Course Registration System

### Overview
The **MCIS Course Registration System** is a web application that allows students, advisors, and administrators to manage and participate in course registration for the MCIS program. Built with **Flask** and **SQLAlchemy**, this platform provides role-based access to different functionalities, including degree plan management, course enrollment, and administrative controls. 

### Key Features
- **Role-Based Access Control**: Supports separate interfaces for students, advisors, and administrators, each with distinct functionality.
- **Course Enrollment and Management**: Students can register for classes, view schedules, and modify their degree plans. Advisors can review and approve degree plans, while administrators manage course offerings and sections.
- **Change Requests**: Students can request changes to their degree plans, which advisors review and either approve or suggest modifications.
- **Logging and Auditing**: Tracks and logs user actions, allowing admins to monitor platform usage and changes.
- **Database-Driven**: Structured data storage using SQLAlchemy ORM, with tables for users, courses, sections, enrollments, and action logs.

### Technology Stack
- **Backend**: Flask (Python)
- **Database**: SQLite using SQLAlchemy ORM
- **Frontend**: HTML, CSS, and JavaScript
- **Authentication**: Flask sessions with role-based access

### Database Structure
The database schema includes:
- **User**: Holds student, advisor, and admin information.
- **Course**: Stores course details such as course code, title, and description.
- **Section**: Manages course sections, with attributes for instructor, meeting times, and capacity.
- **DegreePlan**: Links students to their approved degree plans.
- **Enrollment**: Tracks students' course registrations.
- **UserActionLog** and **ChangeRequest**: Logs actions and handles requests for plan changes.
### Getting Started

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd course-registration-system
   ```
2. **Install Dependencie**:
   ```bash
    pip install -r requirements.txt
   ```
3. **Set Up the Database**:
  ```bash
    flask db init
    flask db migrate
    flask db upgrade
  ```
### Usage

- **Students**: 
   - Log in to view available courses, enroll in sections, and submit degree plans for advisor review.
   - View approved degree plans, semester schedules, and manage change requests.
   
- **Advisors**: 
   - Review and approve degree plans, manage student change requests, and view enrollment data.
   
- **Administrators**: 
   - Manage course offerings, add or edit course sections, and monitor platform usage through activity logs.

### Routes Overview
- **Student Routes**: `/view_degree_plan`, `/student/enroll_in_section`, `/student/submit_change_request`, etc.
- **Advisor Routes**: `/advisor/view_all_enrollments`, `/advisor/edit_request`, `/advisor/view_change_requests`, etc.
- **Admin Routes**: `/admin/manage_users`, `/admin/add_course`, `/admin/delete_course`, `/admin/view_logs`, etc.

### Future Enhancements
- **Enhanced Authentication**: Implement secure password hashing and session handling.
- **Real-Time Notifications**: Add alert notifications for important actions, such as enrollment deadlines.
- **UI Improvements**: Enhance front-end usability with more interactive features and AJAX for smooth loading.

### Contribution Guidelines
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a detailed description.

### License
This project is licensed under the Apache License 2.0.
