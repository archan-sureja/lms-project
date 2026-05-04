document.addEventListener('DOMContentLoaded', () => {
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
        return;
    }

    loadUserProfile();
    setupDashboardLink();
    setupEventListeners();
});

async function loadUserProfile() {
    try {
        const response = await apiFetch('/profile/');
        
        if (response.ok) {
            const profile = await response.json();
            displayProfile(profile);
        } else {
            showError('Failed to load profile. Please try again.');
        }
    } catch (e) {
        console.error('Error loading profile:', e);
        showError('Server error. Please try again later.');
    }
}

function displayProfile(profile) {
    document.getElementById('loadingSpinner').style.display = 'none';
    document.getElementById('profileContent').style.display = 'block';
    document.getElementById('firstName').textContent = profile.first_name || '-';
    document.getElementById('lastName').textContent = profile.last_name || '-';
    document.getElementById('email').textContent = profile.email || '-';
    document.getElementById('username').textContent = profile.username || '-';
    const roleText = profile.role === 'INSTRUCTOR' ? 'Instructor' : 'Learner';
    const badgeClass = profile.role === 'INSTRUCTOR' ? 'bg-warning' : 'bg-info';
    document.getElementById('roleBadge').textContent = roleText;
    document.getElementById('roleBadge').className = `badge badge-role ${badgeClass}`;
    
    document.getElementById('department').textContent = profile.department || '-';
    document.getElementById('level').textContent = profile.level || '-';
    const fullName = `${profile.first_name} ${profile.last_name}`.trim();
    document.getElementById('profileName').textContent = fullName || profile.username;
    document.getElementById('profileUsername').textContent = `@${profile.username}`;
}

function setupEventListeners() {
    document.getElementById('changePasswordBtn').addEventListener('click', (e) => {
        e.preventDefault();
        const modal = new bootstrap.Modal(document.getElementById('changePasswordModal'));
        modal.show();
    });
    
    document.getElementById('backBtn').addEventListener('click', (e) => {
        e.preventDefault();
        window.history.back();
    });
    document.getElementById('changePasswordForm').addEventListener('submit', handleChangePassword);
}

function setupDashboardLink() {
    const role = getUserRole();
    const dashboardLink = document.getElementById('dashboardLink');
    
    if (role === 'INSTRUCTOR') {
        dashboardLink.href = 'instructor_dashboard.html';
    } else if (role === 'LEARNER') {
        dashboardLink.href = 'learner_dashboard.html';
    }
}

async function handleChangePassword(e) {
    e.preventDefault();
    
    const oldPassword = document.getElementById('oldPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const errorDiv = document.getElementById('passwordError');

    if (newPassword !== confirmPassword) {
        errorDiv.textContent = 'New passwords do not match.';
        errorDiv.classList.remove('d-none');
        return;
    }
    
    if (newPassword.length < 6) {
        errorDiv.textContent = 'New password must be at least 6 characters.';
        errorDiv.classList.remove('d-none');
        return;
    }
    
    try {
        const response = await apiFetch('/change-password/', {
            method: 'PUT',
            body: {
                old_password: oldPassword,
                new_password: newPassword
            }
        });
        
        if (response.ok) {
            errorDiv.classList.add('d-none');
            alert('Password changed successfully!');
            document.getElementById('changePasswordForm').reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
            modal.hide();
            logout()
        } else {
            const err = await response.json();
            errorDiv.textContent = Object.values(err).join(' ');
            errorDiv.classList.remove('d-none');
        }
    } catch (e) {
        console.error('Error changing password:', e);
        errorDiv.textContent = 'Server error. Please try again later.';
        errorDiv.classList.remove('d-none');
    }
}

function showError(message) {
    document.getElementById('loadingSpinner').style.display = 'none';
    document.getElementById('errorMessage').classList.add('error-message');
    document.getElementById('errorText').textContent = message;
}
