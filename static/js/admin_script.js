document.getElementById('manage-users-btn').addEventListener('click', function() {
    loadContent('Manage Users');
});

document.getElementById('manage-courses-btn').addEventListener('click', function() {
    loadContent('Manage Courses');
});

document.getElementById('manage-degree-plans-btn').addEventListener('click', function() {
    loadContent('Manage Degree Plans');
});

document.getElementById('manage-schedules-btn').addEventListener('click', function() {
    loadContent('Manage Schedules');
});

document.getElementById('view-logs-btn').addEventListener('click', function() {
    loadContent('View Logs');
});

function loadContent(content) {
    document.getElementById('content-area').textContent = content + ' content loading...';
    // Typically, you would make an AJAX call to the server to load the content dynamically
    // For this template, we are simply changing the text content as a placeholder
}
