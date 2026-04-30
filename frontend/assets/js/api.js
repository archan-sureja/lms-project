const API_BASE_URL = 'http://127.0.0.1:8000'; // Adjust if backend runs on a different port

function getTokens() {
    return {
        access: localStorage.getItem('access_token'),
        refresh: localStorage.getItem('refresh_token')
    };
}

function setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

function decodeJWT(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
}

function getUserRole() {
    const tokens = getTokens();
    if (!tokens.access) return null;
    const payload = decodeJWT(tokens.access);
    return payload ? payload.role : null;
}

function isLoggedIn() {
    return !!getTokens().access;
}

function logout() {
    clearTokens();
    window.location.href = 'login.html';
}

// Custom fetch wrapper to automatically add the Authorization header
async function apiFetch(endpoint, options = {}) {
    const tokens = getTokens();
    
    if (!options.headers) {
        options.headers = {};
    }
    
    if (tokens.access) {
        options.headers['Authorization'] = `Bearer ${tokens.access}`;
    }
    
    if (!(options.body instanceof FormData)) {
        options.headers['Content-Type'] = 'application/json';
        if (options.body && typeof options.body === 'object') {
            options.body = JSON.stringify(options.body);
        }
    } else {
         // let browser set content type for FormData
         delete options.headers['Content-Type'];
    }

    let response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    
    if (response.status === 401 && tokens.refresh) {
        // Token might be expired, try to refresh (not fully implemented to keep it simple, 
        // just redirect to login for now)
        logout();
    }
    
    return response;
}
