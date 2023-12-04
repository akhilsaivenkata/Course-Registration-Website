/*document.getElementById('view-plan-btn').addEventListener('click', function() {
    fetch('/view_degree_plan').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});*/

document.getElementById('modify-plan-btn').addEventListener('click', function() {
    loadContent('Modify Degree Plan');
});

document.getElementById('submit-request-btn').addEventListener('click', function() {
    fetch('/submit_degree_plan').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});

document.getElementById('view-schedule-btn').addEventListener('click', function() {
    loadContent('View Semester Schedule');
});

document.getElementById('select-section-btn').addEventListener('click', function() {
    loadContent('Select Course Sections');
});

function loadContent(content) {
    document.getElementById('content-area').textContent = content + ' content loading...';
    // Here you would typically make an AJAX call to the server to load the content.
    // For now, we are just changing the text.
}

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

