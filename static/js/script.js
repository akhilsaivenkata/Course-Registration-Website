document.getElementById('view-plan-btn').addEventListener('click', function() {
    fetch('/view_degree_plan').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});

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
