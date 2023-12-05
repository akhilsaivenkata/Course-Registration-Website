document.getElementById('finalize-plans-btn').addEventListener('click', function() {
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

    console.log("reached 1");

    // Load existing degree plans
    loadDegreePlans();

    // Event listener for adding a new degree plan
    document.getElementById('add-degree-plan-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/advisor/add_degree_plan', {
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
        console.log("reached load degree plans");
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
        fetch(`/advisor/delete_degree_plan/${planId}`, { method: 'DELETE' })
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
            fetch('/advisor/edit_degree_plan', {
                method: 'POST',
                body: formData
            }).then(response => response.json()).then(data => {
                alert(data.message);
                loadDegreePlans();  // Reload the degree plans list
            });
        });
    });
}




document.getElementById('change-requests-btn').addEventListener('click', function() {
    const contentArea = document.getElementById('content-area');

    // Load existing requests
    loadRequests();

    function loadRequests() {
        fetch('/advisor/view_change_requests')
            .then(response => response.json())
            .then(requests => {
                const list = document.createElement('ul');
                requests.forEach(request => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `
                        Request ID: ${request.id}, Student ID: ${request.student_id}, Degree Plan ID: ${request.degree_plan_id}, Requested Changes: ${request.requested_changes}, Status: ${request.status}
                        <button onclick="editRequest(${request.id})">Edit</button>
                    `;
                    list.appendChild(listItem);
                });
                contentArea.innerHTML = '';
                contentArea.appendChild(list);
            })
            .catch(error => console.error('Error:', error));
    }
});



function editRequest(requestId) {
    fetch(`/advisor/get_request/${requestId}`)
        .then(response => response.json())
        .then(requestData => {
            const contentArea = document.getElementById('content-area');
            contentArea.innerHTML = `
                <h2>Edit Request</h2>
                <form id="edit-request-form">
                    <input type="hidden" name="request_id" value="${requestId}">
                    <textarea name="requested_changes" placeholder="Requested Changes">${requestData.requested_changes}</textarea>
                    <select name="status">
                        <option value="pending" ${requestData.status === 'pending' ? 'selected' : ''}>Pending</option>
                        <option value="approved" ${requestData.status === 'approved' ? 'selected' : ''}>Approved</option>
                        <option value="denied" ${requestData.status === 'denied' ? 'selected' : ''}>Denied</option>
                    </select>
                    <button type="submit">Update Request</button>
                </form>
            `;

            document.getElementById('edit-request-form').addEventListener('submit', function(event) {
                event.preventDefault();
                const formData = new FormData(event.target);
                fetch('/advisor/edit_request', {
                    method: 'POST',
                    body: formData
                }).then(response => response.json()).then(data => {
                    alert(data.message);
                    loadRequests();  // Reload the requests list
                });
            });
        });
}


document.getElementById('section-management-btn').addEventListener('click', function() {
    const contentArea = document.getElementById('content-area');
    
    fetch('/advisor/view_all_enrollments')
        .then(response => response.json())
        .then(enrollments => {
            contentArea.innerHTML = '';  // Clear the content area
            if (enrollments.length === 0) {
                contentArea.innerHTML = '<p>No enrollments found.</p>';
                return;
            }

            // Create and populate the table with enrollments
            const table = document.createElement('table');
            table.innerHTML = `
                <tr>
                    <th>Enrollment ID</th>
                    <th>Student ID</th>
                    <th>Section Name</th>
                    <th>Course Code</th>
                    <th>Action</th>
                </tr>
            `;
            enrollments.forEach(enrollment => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${enrollment.id}</td>
                    <td>${enrollment.student_id}</td>
                    <td>${enrollment.section_name}</td>
                    <td>${enrollment.course_code}</td>
                    <td><button onclick="removeEnrollment(${enrollment.id})">Remove</button></td>
                `;
                table.appendChild(row);
            });

            contentArea.appendChild(table);
        })
        .catch(error => {
            console.error('Error fetching enrollments:', error);
            contentArea.innerHTML = '<p>Error loading enrollments.</p>';
        });
});

// Placeholder function for removing an enrollment
function removeEnrollment(enrollmentId) {
    if(confirm(`Are you sure you want to remove enrollment ID: ${enrollmentId}?`)) {
        fetch(`/advisor/remove_enrollment/${enrollmentId}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                // Optionally, refresh the enrollments list
                document.getElementById('section-management-btn').click();
            })
            .catch(error => {
                console.error('Error removing enrollment:', error);
                alert('Error removing enrollment.');
            });
    }
}


function loadContent(content) {
    document.getElementById('content-area').textContent = content + ' content loading...';
    // Here you would typically make an AJAX call to the server to load the content.
    // For now, we are just changing the text.
}
