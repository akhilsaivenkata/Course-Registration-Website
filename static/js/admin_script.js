document.getElementById('view-logs-btn').addEventListener('click', function() {
    fetch('/admin/view_logs').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});

function loadContent(content) {
    document.getElementById('content-area').textContent = content + ' content loading...';
    // Typically, you would make an AJAX call to the server to load the content dynamically
    // For this template, we are simply changing the text content as a placeholder
}

document.getElementById('manage-users-btn').addEventListener('click', function() {
    // Display forms for adding and deleting users and a section to display user data
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <h2>Manage Users</h2>
        <form id="add-user-form">
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <select name="role" required>
                <option value="student">Student</option>
                <option value="advisor">Advisor</option>
                <option value="admin">Admin</option>
            </select>
            <button type="submit">Add User</button>
        </form>
        <form id="delete-user-form">
            <input type="text" name="username" placeholder="Username to delete" required>
            <button type="submit">Delete User</button>
        </form>
        <div id="users-list"></div>
    `;

    // Event listener for adding a user
    document.getElementById('add-user-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/admin/manage_users/add', {
            method: 'POST',
            body: formData
        }).then(response => response.json()).then(data => {
            alert(data.message);
            loadUsers();  // Reload the user list
        });
    });

    // Event listener for deleting a user
    document.getElementById('delete-user-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/admin/manage_users/delete', {
            method: 'POST',
            body: formData
        }).then(response => response.json()).then(data => {
            alert(data.message);
            loadUsers();  // Reload the user list
        });
    });

    // Function to load and display users
    function loadUsers() {
        fetch('/admin/manage_users')
            .then(response => response.json())
            .then(users => {
                console.log("Received user data:", users);
                const usersList = document.getElementById('users-list');
                usersList.innerHTML = '<h3>Users:</h3>';
                users.forEach(user => {
                    usersList.innerHTML += `<p>id: ${user.id} ${user.username} [${user.role}]</p>`;
                });
            });
            
    }

    // Load users initially
    loadUsers();
});

//Manage courses

document.getElementById('manage-courses-btn').addEventListener('click', function() {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <h2>Manage Courses</h2>
        <form id="add-course-form">
            <input type="text" name="course_code" placeholder="Course Code" required>
            <input type="text" name="title" placeholder="Course Title" required>
            <textarea name="description" placeholder="Course Description"></textarea>
            <label><input type="checkbox" name="is_core"> Is Core Course</label>
            <button type="submit">Add Course</button>
        </form>
        <form id="delete-course-form">
            <input type="text" name="course_code" placeholder="Course Code to delete" required>
            <button type="submit">Delete Course</button>
        </form>
        <div id="courses-list"></div>
    `;

    // Event listener for adding a course
    document.getElementById('add-course-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/admin/manage_courses/add', {
            method: 'POST',
            body: formData
        }).then(response => response.json()).then(data => {
            alert(data.message);
            loadCourses();  // Reload the course list
        });
    });

    // Event listener for deleting a course
    document.getElementById('delete-course-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/admin/manage_courses/delete', {
            method: 'POST',
            body: formData
        }).then(response => response.json()).then(data => {
            alert(data.message);
            loadCourses();  // Reload the course list
        });
    });

    // Function to load and display courses
    function loadCourses() {
        fetch('/admin/manage_courses')
            .then(response => response.json())
            .then(courses => {
                const coursesList = document.getElementById('courses-list');
                coursesList.innerHTML = '<h3>Courses:</h3>';
                courses.forEach(course => {
                    coursesList.innerHTML += `<p>${course.course_code}: ${course.title}</p>`;
                });
            });
    }

    // Load courses initially
    loadCourses();
});

// Manage Degree plans

document.getElementById('manage-degree-plans-btn').addEventListener('click', function() {
    const contentArea = document.getElementById('content-area');

    // Form for adding a new degree plan
    const addFormHTML = `
        <h3>Add New Degree Plan</h3>
        <form id="add-degree-plan-form">
            <input type="text" name="student_id" placeholder="Student ID" required>
            <input type="text" name="course_code" placeholder="Course Code" required>
            <button type="submit">Add Plan</button>
        </form>
    `;
    contentArea.innerHTML = addFormHTML;

    // Load existing degree plans
    loadDegreePlans();

    // Event listener for adding a new degree plan
    document.getElementById('add-degree-plan-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/admin/add_degree_plan', {
            method: 'POST',
            body: formData
        }).then(response => response.json()).then(data => {
            alert(data.message);
            loadDegreePlans();  // Reload the degree plans list
        });
    });
});

function loadDegreePlans() {
    fetch('/admin/manage_degree_plans').then(response => response.json()).then(degreePlans => {
        const contentArea = document.getElementById('content-area');
        const list = document.createElement('ul');
        degreePlans.forEach(plan => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                Degree Plan ID: ${plan.id}, Student ID: ${plan.student_id}, Course Code: ${plan.course_code}, Approved: ${plan.approved}
                <button onclick="editDegreePlan(${plan.id})">Edit</button>
                <button onclick="deleteDegreePlan(${plan.id})">Delete</button>
            `;
            list.appendChild(listItem);
        });
        contentArea.appendChild(list);
    });
}

function deleteDegreePlan(planId) {
    // Confirm deletion
    if (confirm("Are you sure you want to delete this degree plan?")) {
        fetch(`/admin/delete_degree_plan/${planId}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            loadDegreePlans();  // Reload the degree plans list
        });
    }
}


function editDegreePlan(planId) {
    fetch(`/admin/get_degree_plan/${planId}`).then(response => response.json()).then(planData => {
        const contentArea = document.getElementById('content-area');
        contentArea.innerHTML = `
            <h2>Edit Degree Plan</h2>
            <form id="edit-degree-plan-form">
                <input type="hidden" name="plan_id" value="${planId}">
                <input type="text" name="student_id" placeholder="Student ID" value="${planData.student_id}" required>
                <input type="text" name="course_code" placeholder="Course Code" value="${planData.course_code}" required>
                <label>
                    Approved:
                    <input type="checkbox" name="approved" ${planData.approved ? 'checked' : ''}>
                </label>
                <button type="submit">Update Plan</button>
            </form>
        `;

        document.getElementById('edit-degree-plan-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            fetch('/admin/edit_degree_plan', {
                method: 'POST',
                body: formData
            }).then(response => response.json()).then(data => {
                alert(data.message);
                loadDegreePlans();  // Reload the degree plans list
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('manage-sections-btn').addEventListener('click', function() {
        const contentArea = document.getElementById('content-area');

        // Clear existing content and add the new section form
        contentArea.innerHTML = `
            <h3>Add New Section</h3>
            <form id="add-section-form">
                <input type="text" name="section_name" placeholder="Section Name" required>
                <input type="text" name="course_code" placeholder="Course Code" required>
                <input type="text" name="semester" placeholder="Semester" required>
                <input type="text" name="meeting_time" placeholder="Meeting Time" required>
                <input type="text" name="location" placeholder="Location" required>
                <input type="text" name="instructor" placeholder="Instructor" required>
                <input type="number" name="capacity" placeholder="Capacity" required>
                <button type="submit">Add Section</button>
            </form>
            <div id="sections-list"></div>
        `;

        loadSections();

        // Event listener for adding a new section
        document.getElementById('add-section-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            fetch('/admin/add_section', {
                method: 'POST',
                body: formData
            }).then(response => response.json()).then(data => {
                alert(data.message);
                loadSections();  // Reload the sections list
            });
        });
    });
});


function loadSections() {
    fetch('/admin/get_sections')
        .then(response => response.json())
        .then(sections => {
            const sectionsList = document.getElementById('sections-list');
            sectionsList.innerHTML = ''; // Clear existing content

            sections.forEach(section => {
                sectionsList.innerHTML += `
                    <div id="section-${section.id}">
                        <p>Section Name: ${section.section_name}</p>
                        <p>Course Code: ${section.course_code}</p>
                        <p>Semester: ${section.semester}</p>
                        <p>Meeting Time: ${section.meeting_time}</p>
                        <p>Location: ${section.location}</p>
                        <p>Instructor: ${section.instructor}</p>
                        <p>Capacity: ${section.capacity}</p>
                        <p>Current Enrollment: ${section.current_enrollment}</p>
                        <button onclick="editSection(${section.id})">Edit</button>
                        <button onclick="deleteSection(${section.id})">Delete</button>
                    </div>
                `;
            });
        });
}


function editSection(sectionId) {
    // Fetch the section details
    fetch(`/admin/get_section/${sectionId}`)
        .then(response => response.json())
        .then(section => {
            // Populate the edit form fields
            const contentArea = document.getElementById('content-area');
            contentArea.innerHTML = `
                <h3>Edit Section</h3>
                <form id="edit-section-form">
                    <input type="hidden" name="id" value="${section.id}">
                    <input type="text" name="section_name" placeholder="Section Name" value="${section.section_name}" required>
                    <input type="text" name="course_code" placeholder="Course Code" value="${section.course_code}" required>
                    <input type="text" name="semester" value="${section.semester}" required>
                    <input type="text" name="meeting_time" value="${section.meeting_time}" required>
                    <input type="text" name="location" value="${section.location}" required>
                    <input type="text" name="instructor" value="${section.instructor}" required>
                    <input type="number" name="capacity" value="${section.capacity}" required>
                    <button type="submit">Update Section</button>
                </form>
            `;

            // Event listener for submitting the edit form
            document.getElementById('edit-section-form').addEventListener('submit', function(event) {
                event.preventDefault();
                const formData = new FormData(event.target);
                fetch(`/admin/edit_section/${sectionId}`, {
                    method: 'POST',
                    body: formData
                }).then(response => response.json()).then(data => {
                    alert(data.message);
                    loadSections();  // Reload the sections list
                });
            });
        });
}

function deleteSection(sectionId) {
    if (confirm('Are you sure you want to delete this section?')) {
        fetch(`/admin/delete_section/${sectionId}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                loadSections();  // Reload the sections list
            });
    }
}
/*
// Function to handle the editing of schedules
function editSchedule(sectionId) {
    console.log("Editing schedule for Section ID:", sectionId);
    // Here, you need to implement the logic to fetch the current schedule data,
    // display it in a form for editing, and submit the updated data.
}

// Function to handle the deletion of schedules
function deleteSchedule(sectionId) {
    console.log("Deleting schedule for Section ID:", sectionId);
    // Implement the logic to send a DELETE request to your Flask backend
    // to delete the schedule associated with the given sectionId.
    // After successful deletion, you might want to reload the schedules list.
}*/
