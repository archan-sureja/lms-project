document.addEventListener('DOMContentLoaded', () => {
    if (!isLoggedIn() || getUserRole() !== 'INSTRUCTOR') {
        window.location.href = 'index.html';
        return;
    }

    // Identify which page we are on and attach event listeners
    const courseForm = document.getElementById('course-form');
    if (courseForm) {
        loadInstructorCourses();
        courseForm.addEventListener('submit', handleCourseSubmit);
    }

    const assignmentForm = document.getElementById('assignment-form');
    if (assignmentForm) {
        assignmentForm.addEventListener('submit', handleAssignmentSubmit);
    }

    const gradeForm = document.getElementById('grade-form');
    if (gradeForm) {
        gradeForm.addEventListener('submit', handleGradeSubmit);
    }
});

// --- COURSES ---
async function loadInstructorCourses() {
    try {
        const response = await apiFetch('/courses/');
        const courses = await response.json();
        const container = document.getElementById('instructor-courses-list');
        container.innerHTML = '';
        
        if (courses.length === 0) {
            container.innerHTML = '<p class="text-muted">You have not created any courses.</p>';
            return;
        }

        courses.forEach(course => {
            container.innerHTML += `
                <div class="col-md-4 mb-3">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">${course.title} (ID: ${course.id})</h5>
                            <p class="card-text">${course.description || 'No description'}</p>
                            <button class="btn btn-sm btn-danger float-end ms-2" onclick="deleteCourse(${course.id})">Delete</button>
                            <a href="course_detail.html?id=${course.id}" class="btn btn-sm btn-info float-end ms-2">Details</a>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

function resetCourseForm() {
    document.getElementById('course-id').value = '';
    document.getElementById('course-form').reset();
}

async function handleCourseSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('course-id').value;
    const title = document.getElementById('course-title').value;
    const description = document.getElementById('course-description').value;

    const method = id ? 'PUT' : 'POST';
    const endpoint = id ? `/courses/${id}/` : '/courses/';

    try {
        const response = await apiFetch(endpoint, {
            method: method,
            body: { title, description }
        });

        if (response.ok) {
            alert(id ? 'Course updated!' : 'Course created!');
            const modal = bootstrap.Modal.getInstance(document.getElementById('courseModal'));
            modal.hide();
            loadInstructorCourses();
        } else {
            const err = await response.json();
            alert('Error: ' + JSON.stringify(err));
        }
    } catch (e) {
        console.error(e);
    }
}

async function deleteCourse(id) {
    if (!confirm('Are you sure you want to delete this course?')) return;
    try {
        const response = await apiFetch(`/courses/${id}/`, { method: 'DELETE' });
        if (response.ok || response.status === 204) {
            alert('Course deleted.');
            loadInstructorCourses();
        }
    } catch (e) {
        console.error(e);
    }
}

// --- ENROLLMENTS ---
async function loadEnrollments() {
    try {
        const response = await apiFetch('/enrollments/');
        const enrollments = await response.json();
        const tbody = document.getElementById('enrollments-table-body');
        tbody.innerHTML = '';

        if (enrollments.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No enrollments found.</td></tr>';
            return;
        }

        enrollments.forEach(en => {
            tbody.innerHTML += `
                <tr>
                    <td>${en.id}</td>
                    <td>${en.user}</td>
                    <td>${en.user_email || 'N/A'}</td>
                    <td>${en.course}</td>
                    <td>${new Date(en.enrolled_at).toLocaleString()}</td>
                </tr>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

// --- ASSIGNMENTS ---
function resetAssignmentForm() {
    document.getElementById('assign-id').value = '';
    document.getElementById('assignment-form').reset();
}

async function loadInstructorAssignments() {
    try {
        const response = await apiFetch('/assignments/');
        const assignments = await response.json();
        const container = document.getElementById('assignments-list');
        container.innerHTML = '';
        
        if (assignments.length === 0) {
            container.innerHTML = '<p class="text-muted">No assignments created.</p>';
            return;
        }

        assignments.forEach(assign => {
            container.innerHTML += `
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${assign.title} (Course: ${assign.course})</h5>
                            <p class="card-text">${assign.description || ''}</p>
                            <p class="small text-muted">Deadline: ${new Date(assign.deadline).toLocaleString()}</p>
                            <p class="small fw-bold">Max Score: ${assign.total_score}</p>
                            <button class="btn btn-sm btn-danger float-end" onclick="deleteAssignment(${assign.id})">Delete</button>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

async function handleAssignmentSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('assign-id').value;
    const course = document.getElementById('assign-course-id').value;
    const title = document.getElementById('assign-title').value;
    const description = document.getElementById('assign-desc').value;
    const deadline = document.getElementById('assign-deadline').value;
    const total_score = document.getElementById('assign-score').value;

    const method = id ? 'PUT' : 'POST';
    const endpoint = id ? `/assignments/${id}/` : '/assignments/';

    try {
        const response = await apiFetch(endpoint, {
            method: method,
            body: { course, title, description, deadline, total_score }
        });

        if (response.ok) {
            alert('Assignment saved!');
            const modal = bootstrap.Modal.getInstance(document.getElementById('assignmentModal'));
            modal.hide();
            loadInstructorAssignments();
        } else {
            const err = await response.json();
            alert('Error: ' + JSON.stringify(err));
        }
    } catch (e) {
        console.error(e);
    }
}

async function deleteAssignment(id) {
    if (!confirm('Are you sure you want to delete this assignment?')) return;
    try {
        const response = await apiFetch(`/assignments/${id}/`, { method: 'DELETE' });
        if (response.ok || response.status === 204) {
            alert('Assignment deleted.');
            loadInstructorAssignments();
        }
    } catch (e) {
        console.error(e);
    }
}

// --- SUBMISSIONS & GRADING ---
async function loadSubmissions() {
    try {
        const response = await apiFetch('/submissions/');
        const submissions = await response.json();
        const tbody = document.getElementById('submissions-table-body');
        tbody.innerHTML = '';

        if (submissions.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No submissions found.</td></tr>';
            return;
        }

        submissions.forEach(sub => {
            const fileLink = sub.file ? `<a href="${API_BASE_URL}${sub.file}" target="_blank">View File</a>` : 'No file';
            tbody.innerHTML += `
                <tr>
                    <td>${sub.id}</td>
                    <td>${sub.assignment}</td>
                    <td>${sub.submitted_by}</td>
                    <td>${fileLink}</td>
                    <td>
                        <button class="btn btn-sm btn-success" onclick="openGradeModal(${sub.id})">Grade</button>
                    </td>
                </tr>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

function openGradeModal(submissionId) {
    document.getElementById('grade-sub-id').value = submissionId;
    document.getElementById('grade-form').reset();
    const modal = new bootstrap.Modal(document.getElementById('gradeModal'));
    modal.show();
}

async function handleGradeSubmit(e) {
    e.preventDefault();
    const submissionId = document.getElementById('grade-sub-id').value;
    const score = document.getElementById('grade-score').value;
    const feedback = document.getElementById('grade-feedback').value;

    try {
        const response = await apiFetch(`/submissions/${submissionId}/grade/`, {
            method: 'POST',
            body: { score, feedback }
        });

        if (response.ok) {
            alert('Graded successfully!');
            const modal = bootstrap.Modal.getInstance(document.getElementById('gradeModal'));
            modal.hide();
        } else {
            const err = await response.json();
            alert('Error: ' + JSON.stringify(err));
        }
    } catch (e) {
        console.error(e);
    }
}
