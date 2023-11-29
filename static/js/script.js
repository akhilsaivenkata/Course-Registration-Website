document.getElementById('view-plan-btn').addEventListener('click', function() {
    loadContent('View Degree Plan');
});

document.getElementById('modify-plan-btn').addEventListener('click', function() {
    loadContent('Modify Degree Plan');
});

document.getElementById('submit-request-btn').addEventListener('click', function() {
    loadContent('Submit Change Request');
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
