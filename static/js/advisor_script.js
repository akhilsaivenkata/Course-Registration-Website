document.getElementById('review-plans-btn').addEventListener('click', function() {
    loadContent('Review Degree Plans');
});

document.getElementById('finalize-plans-btn').addEventListener('click', function() {
    loadContent('Finalize Degree Plans');
});

document.getElementById('change-requests-btn').addEventListener('click', function() {
    loadContent('View Change Requests');
});

document.getElementById('schedule-management-btn').addEventListener('click', function() {
    loadContent('Manage Schedules');
});

function loadContent(content) {
    document.getElementById('content-area').textContent = content + ' content loading...';
    // Here you would typically make an AJAX call to the server to load the content.
    // For now, we are just changing the text.
}
