document.addEventListener('DOMContentLoaded', () => {
    if (!isLoggedIn()) {
        window.location.href = 'index.html';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id');

    if (!courseId) {
        document.getElementById('course-details-container').innerHTML = '<p class="text-danger">Invalid course ID.</p>';
        return;
    }

    loadCourseDetails(courseId);
});

async function loadCourseDetails(id) {
    try {
        const response = await apiFetch(`/courses/${id}/`);
        const container = document.getElementById('course-details-container');
        
        if (response.ok) {
            const course = await response.json(); 
            const depts = course.allowed_depts && course.allowed_depts.length > 0 
                ? course.allowed_depts.join(', ') 
                : 'Any';
            
            const levels = course.allowed_levels && course.allowed_levels.length > 0 
                ? course.allowed_levels.join(', ') 
                : 'Any';

            let html = `
                <h2>${course.title}</h2>
                <p class="text-muted">Instructor: ${course.instructor}</p>
                <hr>
                <p>${course.description || 'No description available.'}</p>
                
                <h5 class="mt-4">Allowed Departments:</h5>
                <p>${depts}</p>
                
                <h5>Allowed Levels:</h5>
                <p>${levels}</p>
                
                <h5 class="mt-4">Topics:</h5>
                ${course.topics && course.topics.length > 0 ? `
                    <ul>
                        ${course.topics.map(t => `
                            <li>
                                <strong>${t.name}</strong>
                                ${t.resource_link ? `<a href="${t.resource_link}" target="_blank">(Resource Link)</a>` : ''}
                            </li>
                        `).join('')}
                    </ul>
                ` : '<p>No topics available.</p>'}
            `;

            container.innerHTML = html;
        } else {
            container.innerHTML = '<p class="text-danger">Failed to load course details. It may not exist or you lack permission.</p>';
        }
    } catch (e) {
        console.error(e);
        document.getElementById('course-details-container').innerHTML = '<p class="text-danger">Server error.</p>';
    }
}
