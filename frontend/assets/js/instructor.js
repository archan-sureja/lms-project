document.addEventListener('DOMContentLoaded', () => {
    if (!isLoggedIn() || getUserRole() !== 'INSTRUCTOR') {
        window.location.href = 'index.html';
        return;
    }

    
    const courseForm = document.getElementById('course-form');
    if (courseForm) {
        loadInstructorCourses();
        courseForm.addEventListener('submit', handleCourseSubmit);
    }

    const assignmentForm = document.getElementById('assignment-form');
    if (assignmentForm) {
        loadInstructorAssignments();
        loadSubmissions();
        assignmentForm.addEventListener('submit', handleAssignmentSubmit);
    }

    const gradeForm = document.getElementById('grade-form');
    if (gradeForm) {
        gradeForm.addEventListener('submit', handleGradeSubmit);
    }


    const enrollmentsTable = document.getElementById('enrollments-table-body');
    if (enrollmentsTable) {
        loadEnrollments();
    }
});


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
   const allowed_depts = Array.from(document.getElementById('course-depts').selectedOptions)
    .map(opt =>parseInt(opt.value));

    const allowed_levels = Array.from(document.getElementById('course-levels').selectedOptions)
    .map(opt => parseInt(opt.value));

    const tags = Array.from(document.getElementById('course-tags').selectedOptions)
    .map(opt => parseInt(opt.value)); 
    console.log(tags,allowed_depts,allowed_levels)
    const topicElements = document.querySelectorAll('.topic-input-group');
    const topics = Array.from(topicElements).map(el => ({
        name: el.querySelector('.topic-name').value,
        resource_link: el.querySelector('.topic-link').value || null
    })).filter(t => t.name);

    const method = id ? 'PUT' : 'POST';
    const endpoint = id ? `/courses/${id}/` : '/courses/';

    try {
        const response = await apiFetch(endpoint, {
            method: method,
            body: { title, description, tags, allowed_depts, allowed_levels, topics }
        });

        if (response.ok) {
            alert(id ? 'Course updated!' : 'Course created!');
            const modal = bootstrap.Modal.getInstance(document.getElementById('courseModal'));
            modal.hide();
            loadInstructorCourses();
            resetCourseForm();
        } else {
            const err = await response.json();
            alert('Error: ' + JSON.stringify(err));
        }
    } catch (e) {
        console.error(e);
    }
}

function addTopicField() {
    const container = document.getElementById('topics-container');
    const topicIndex = container.children.length;
    const html = `
        <div class="topic-input-group card p-2 mb-2">
            <div class="row">
                <div class="col-md-6 mb-2">
                    <input type="text" class="form-control topic-name form-control-sm" placeholder="Topic name" required>
                </div>
                <div class="col-md-6 mb-2">
                    <input type="url" class="form-control topic-link form-control-sm" placeholder="Resource link (optional)">
                </div>
                <div class="col-md-12">
                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="this.parentElement.parentElement.parentElement.remove()">Remove</button>
                </div>
            </div>
        </div>
    `;
    container.innerHTML += html;
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
                    <td>${en.department || 'N/A'}</td>
                    <td>${en.course}</td>
                    <td>${new Date(en.enrolled_at).toLocaleString()}</td>
                </tr>
            `;
        });
    } catch (e) {
        console.error(e);
    }
}

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
    const course = parseInt(document.getElementById('assign-course-id').value);
    const title = document.getElementById('assign-title').value;
    const description = document.getElementById('assign-desc').value;
    const deadlineLocal = document.getElementById('assign-deadline').value;
    const deadline = new Date(deadlineLocal).toISOString();
    const now = new Date();
    const tenMinutesFromNow = new Date(now.getTime() + 10 * 60000);
    
    if (new Date(deadline) <= tenMinutesFromNow) {
        document.getElementById('deadline-error').classList.remove('d-none');
        return;
    }
    document.getElementById('deadline-error').classList.add('d-none');

    const method = id ? 'PUT' : 'POST';
    const endpoint = id ? `/assignments/${id}/` : '/assignments/';

    try {
        const response = await apiFetch(endpoint, {
            method: method,
            body: { course, title, description, deadline }
        });

        if (response.ok) {
            alert('Assignment saved!');
            const modal = bootstrap.Modal.getInstance(document.getElementById('assignmentModal'));
            modal.hide();
            loadInstructorAssignments();
            resetAssignmentForm();
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
            const fileLink = sub.file_url ? `<a href="#" onclick="handleFileDownload('${sub.file_url}')">View File</a>` : 'No file';
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
async function handleFileDownload(filePath) {
    filePath = filePath.replace("http://localhost:8000", "");   
    console.log(filePath)
    const res = await apiFetch(filePath);
    if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');      
        a.href = url;
        a.download = filePath.split('/').pop(); 
        document.body.appendChild(a);
        a.click();
        a.remove();
    } else {
        alert('Failed to download file.');
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
