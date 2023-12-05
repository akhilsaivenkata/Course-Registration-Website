/*document.getElementById('view-plan-btn').addEventListener('click', function() {
    fetch('/view_degree_plan').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});*/
document.getElementById('view-courses-btn').addEventListener('click', function() {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = `
        <h2>Available Courses</h2>
        <div id="courses-list"></div>
    `;


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


document.getElementById('view-plan-btn').addEventListener('click', function() {
    fetch('/view_degree_plan')
        .then(response => response.json())
        .then(degreePlans => {
            const contentArea = document.getElementById('content-area');
            contentArea.innerHTML = ''; // Clear existing content

            if (degreePlans.length === 0) {
                contentArea.innerHTML = '<p>No degree plan found for this student.</p>';
                return;
            }

            // Create a table to display degree plans
            const table = document.createElement('table');
            table.innerHTML = `
                <tr>
                    <th>Course Code</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Is Core</th>
                    <th>Approved</th>
                </tr>
            `;

            // Populate the table with degree plan data
            degreePlans.forEach(plan => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${plan.course_code}</td>
                    <td>${plan.title}</td>
                    <td>${plan.description}</td>
                    <td>${plan.is_core ? 'Yes' : 'No'}</td>
                    <td>${plan.approved ? 'Yes' : 'No'}</td>
                `;
                table.appendChild(row);
            });

            contentArea.appendChild(table);
        })
        .catch(error => {
            console.error('Error fetching degree plan:', error);
            document.getElementById('content-area').innerHTML = '<p>Error loading degree plan.</p>';
        });
});


/*document.getElementById('modify-plan-btn').addEventListener('click', function() {
    loadContent('Modify Degree Plan');
});*/

document.getElementById('submit-request-btn').addEventListener('click', function() {
    const contentArea = document.getElementById('content-area');

    // new request form
    // Form for submitting a change request
    const submitRequestFormHTML = `
        <h3>Submit Change Request</h3>
        <form id="submit-change-request-form">
            <input type="text" name="degree_plan_id" placeholder="Degree Plan ID" required>
            <textarea name="requested_changes" placeholder="Describe your requested changes" required></textarea>
            <button type="submit">Submit Request</button>
        </form>
        <hr>
        <p>If you cannot find the plan you want, please add it here and then submit the request.</p>
    `;

    // Form for adding a new degree plan
    const addFormHTML = `
        <h3>Add New Degree Plan</h3>
        <form id="add-degree-plan-form">
            <input type="text" name="student_id" placeholder="Student ID" required>
            <input type="text" name="course_code" placeholder="Course Code" required>
            <button type="submit">Add Plan</button>
        </form>
    `;
    contentArea.innerHTML = submitRequestFormHTML;
    
    

    contentArea.innerHTML += addFormHTML;

    // Load existing degree plans
    loadDegreePlans();
    console.log('Form submission reached');
    document.getElementById('submit-change-request-form').addEventListener('submit', function(event) {
        event.preventDefault();
        console.log('Form submission prevented.');
        const formData = new FormData(event.target);
        const degreePlanId = event.target.elements.degree_plan_id.value;
        const requestedChanges = event.target.elements.requested_changes.value;

        fetch('/student/submit_change_request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  // Specify that you're sending JSON data
            },
            body: JSON.stringify({
                degree_plan_id: degreePlanId,
                requested_changes: requestedChanges
            })
        }).then(response => response.json()).then(data => {
            alert(data.message);
        });
        
    });

    // Event listener for adding a new degree plan
    document.getElementById('add-degree-plan-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/student/add_degree_plan', {
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
            `;
            list.appendChild(listItem);
        });
        contentArea.appendChild(list);
    });
}
/*
        const formData = new FormData(event.target);
        const degreePlanId = event.target.elements.degree_plan_id.value;
        const requestedChanges = event.target.elements.requested_changes.value;

        fetch('/student/submit_change_request', {
            method: 'POST',
            body: formData
        }).then(response => response.json()).then(data => {
            alert(data.message);
        });
*/


document.getElementById('view-request-btn').addEventListener('click', function() {
    const contentArea = document.getElementById('content-area');
    
    fetch('/student/view_requests')
        .then(response => response.json())
        .then(requests => {
            contentArea.innerHTML = '';  // Clear the content area
            if (requests.length === 0) {
                contentArea.innerHTML = '<p>No requests found.</p>';
                return;
            }
            
            // Create and populate the table with requests
            const table = document.createElement('table');
            table.innerHTML = `
                <tr>
                    <th>Request ID</th>
                    <th>Requested Changes</th>
                    <th>Status</th>
                    <th>Timestamp</th>
                </tr>
            `;
            requests.forEach(request => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${request.id}</td>
                    <td>${request.requested_changes}</td>
                    <td>${request.status}</td>
                    <td>${request.timestamp}</td>
                `;
                table.appendChild(row);
            });
            
            contentArea.appendChild(table);
        })
        .catch(error => {
            console.error('Error fetching requests:', error);
            contentArea.innerHTML = '<p>Error loading requests.</p>';
        });
});

document.getElementById('view-schedule-btn').addEventListener('click', function() {
    const contentArea = document.getElementById('content-area');
    
    fetch('/student/view_semester_schedule')
        .then(response => response.json())
        .then(sections => {
            contentArea.innerHTML = '';  // Clear the content area
            if (sections.length === 0) {
                contentArea.innerHTML = '<p>No schedules found for this semester.</p>';
                return;
            }

            // Create and populate the table with semester schedules
            const table = document.createElement('table');
            table.innerHTML = `
                <tr>
                    <th>Section Name</th>
                    <th>Course Code</th>
                    <th>Semester</th>
                    <th>Meeting Time</th>
                    <th>Location</th>
                    <th>Instructor</th>
                    <th>Capacity</th>
                    <th>Current Enrollment</th>
                </tr>
            `;
            sections.forEach(section => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${section.section_name}</td>
                    <td>${section.course_code}</td>
                    <td>${section.semester}</td>
                    <td>${section.meeting_time}</td>
                    <td>${section.location}</td>
                    <td>${section.instructor}</td>
                    <td>${section.capacity}</td>
                    <td>${section.current_enrollment}</td>
                `;
                table.appendChild(row);
            });

            contentArea.appendChild(table);
        })
        .catch(error => {
            console.error('Error fetching semester schedule:', error);
            contentArea.innerHTML = '<p>Error loading schedules.</p>';
        });
});



/*document.getElementById('submit-request-btn').addEventListener('click', function() {
    fetch('/submit_degree_plan').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});*/

//<button onclick="deleteDegreePlan(${plan.id})">Delete</button>

/*document.getElementById('view-schedule-btn').addEventListener('click', function() {
    //loadContent('View Semester Schedule');
});
*/
document.getElementById('select-section-btn').addEventListener('click', function() {
    //loadContent('Select Course Sections');
});

function loadContent(content) {
    document.getElementById('content-area').textContent = content + ' content loading...';
    // Here you would typically make an AJAX call to the server to load the content.
    // For now, we are just changing the text.
}


