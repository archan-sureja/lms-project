document.addEventListener('DOMContentLoaded', () => {
    if (isLoggedIn()) {
        window.location.href = 'index.html';
        return;
    }

    const loginForm = document.getElementById('login-form');
    const errorMsg = document.getElementById('error-msg');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/token/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                setTokens(data.access, data.refresh);
                window.location.href = 'index.html';
            } else {
                const errData = await response.json();
                errorMsg.textContent = errData.detail || 'Invalid credentials';
                errorMsg.classList.remove('d-none');
            }
        } catch (error) {
            errorMsg.textContent = 'Server error. Please try again.';
            errorMsg.classList.remove('d-none');
        }
    });
});
