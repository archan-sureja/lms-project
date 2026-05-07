document.addEventListener('DOMContentLoaded', () => {
    if (!isLoggedIn() || getUserRole() !== 'LEARNER') {
        window.location.href = 'index.html';
        return;
    }

    loadTags();
    loadAvailableCourses();
    loadEnrolledCourses();
    loadAssignments();

    document.getElementById('submission-form').addEventListener('submit', handleSubmission);
});

async function loadTags() {
    try {
        const response = await apiFetch('/tags/');
        if (response.ok) {
            const tags = await response.json();
            const tagSelect = document.getElementById('course-tag-filter');
            if (tagSelect) {
                tags.forEach(tag => {
                    const option = document.createElement('option');
                    option.value = tag.id;
                    option.textContent = tag.name;
                    tagSelect.appendChild(option);
                });
            }
        }
    } catch (e) {
        console.error('Error loading tags:', e);
    }
}

async function loadAvailableCourses() {
    try {
        const searchInput = document.getElementById('course-search-input');
        const tagFilter = document.getElementById('course-tag-filter');
        let url = '/courses/';
        const params = new URLSearchParams();
        
        if (searchInput && searchInput.value.trim() !== '') {
            params.append('search', searchInput.value.trim());
        }
        if (tagFilter && tagFilter.value) {
            params.append('tags', tagFilter.value);
        }
        
        if (params.toString()) {
            url += '?' + params.toString();
        }

        const response = await apiFetch(url);
        const courses = await response.json();
        const container = document.getElementById('available-courses-list');
        container.innerHTML = '';
        
        if (courses.length === 0) {
            container.innerHTML = '<p class="text-muted">No courses available.</p>';
            return;
        }

        courses.forEach(course => {
            container.innerHTML += `
                <div class="col-md-4 mb-3">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">${course.title}</h5>
                            <p class="card-text">${course.description || 'No description'}</p>
                            <small class="text-muted d-block mb-2">Tags: ${course.tags && course.tags.length > 0 ? course.tags.join(', ') : 'None'}</small>
                            <a href="course_detail.html?id=${course.id}" class="btn btn-sm btn-outline-primary">View Details</a>
                            <button class="btn btn-sm btn-success float-end" onclick="enrollCourse(${course.id})">Enroll</button>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

async function loadEnrolledCourses() {
    try {
        const response = await apiFetch('/courses/enrolled/');
        const courses = await response.json();
        const container = document.getElementById('enrolled-courses-list');
        container.innerHTML = '';
        
        if (courses.length === 0) {
            container.innerHTML = '<p class="text-muted">You are not enrolled in any courses.</p>';
            return;
        }

        courses.forEach(course => {
            container.innerHTML += `
                <div class="col-md-4 mb-3">
                    <div class="card h-100 border-success">
                        <div class="card-body">
                            <h5 class="card-title">${course.title}</h5>
                            <p class="card-text">${course.description || 'No description'}</p>
                            <a href="course_detail.html?id=${course.id}" class="btn btn-sm btn-primary">Go to Course</a>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

async function enrollCourse(courseId) {
    try {
        const response = await apiFetch('/enrollments/', {
            method: 'POST',
            body: { course: courseId }
        });
        if (response.ok) {
            alert('Successfully enrolled!');
            loadAvailableCourses();
            loadEnrolledCourses();
        } else {
            const err = await response.json();
            alert('Error enrolling: ' + JSON.stringify(err));
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadAssignments() {
    try {
        const response = await apiFetch('/assignments/');
        const assignments = await response.json();
        const container = document.getElementById('assignments-list');
        container.innerHTML = '';
        
        if (assignments.length === 0) {
            container.innerHTML = '<p class="text-muted">No assignments due.</p>';
            return;
        }
        const subResp = await apiFetch('/submissions/');
        const mySubmissions = await subResp.json();
        const submittedAssignIds = mySubmissions.map(s => s.assignment);

        const gradeResp = await apiFetch('/grades/');
        const myGrades = await gradeResp.json();
        
        assignments.forEach(assign => {
            const hasSubmitted = submittedAssignIds.includes(assign.id);
            const submission = mySubmissions.find(s => s.assignment === assign.id);
            let gradeInfo = '';

            if (submission) {
                const grade = myGrades.find(g => g.submission === submission.id);
                if (grade) {
                    gradeInfo = `<span class="badge bg-success">Graded: ${grade.grade} - ${grade.review_text}</span>`;
                } else {
                    gradeInfo = `<span class="badge bg-warning text-dark">Submitted, Pending Grade</span>`;
                }
            } else {
                gradeInfo = `<span class="badge bg-danger">Not Submitted</span>`;
            }

            container.innerHTML += `
                <div class="card mb-3">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <h5 class="card-title mb-0">${assign.title} (Course ID: ${assign.course})</h5>
                            ${gradeInfo}
                        </div>
                        <p class="card-text mt-2">${assign.description || ''}</p>
                        <p class="text-muted small">Deadline: ${new Date(assign.deadline).toLocaleString()}</p>
                        ${!hasSubmitted ? `<button class="btn btn-sm btn-primary" onclick="openSubmitModal(${assign.id})">Submit Assignment</button>` : ''}
                    </div>
                </div>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

function openSubmitModal(assignmentId) {
    document.getElementById('modal-assignment-id').value = assignmentId;
    document.getElementById('submission-form').reset();
    const modal = new bootstrap.Modal(document.getElementById('submissionModal'));
    modal.show();
}

async function handleSubmission(e) {
    e.preventDefault();
    const assignmentId = document.getElementById('modal-assignment-id').value;
    const feedback = document.getElementById('modal-feedback').value;
    const fileInput = document.getElementById('modal-file');
    
    if (fileInput.files.length === 0) return;

    const formData = new FormData();
    formData.append('assignment', assignmentId);
    formData.append('feedback', feedback);
    formData.append('file', fileInput.files[0]);

    try {
        const response = await apiFetch('/submissions/', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            alert('Assignment submitted!');
            const modalEl = document.getElementById('submissionModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
            loadAssignments();
        } else {
            const err = await response.json();
            alert('Error: ' + JSON.stringify(err));
        }
    } catch (e) {
        console.error(e);
        alert('Server error.');
    }
}
