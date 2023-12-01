document.getElementById('manage-users-btn').addEventListener('click', function() {
    fetch('/admin/manage_users').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});

document.getElementById('manage-courses-btn').addEventListener('click', function() {
    fetch('/admin/manage_courses').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});

document.getElementById('manage-degree-plans-btn').addEventListener('click', function() {
    fetch('/admin/manage_degree_plans').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});
3
document.getElementById('manage-schedules-btn').addEventListener('click', function() {
    fetch('/admin/manage_schedules').then(response => response.json()).then(data => {
        document.getElementById('content-area').textContent = JSON.stringify(data);
    });
});

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
