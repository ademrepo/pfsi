import axios from 'axios';

// Créer une instance axios avec configuration de base
const api = axios.create({
    baseURL: '/api',  // Le proxy Vite redirigera vers http://localhost:8000/api
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Important pour envoyer/recevoir les cookies de session
});

// Intercepteur pour gérer le token CSRF
api.interceptors.request.use(async (config) => {
    // Fonction pour récupérer le cookie CSRF (standard Django)
    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    const csrftoken = getCookie('csrftoken');

    if (csrftoken) {
        config.headers['X-CSRFToken'] = csrftoken;
    }

    return config;
}, (error) => {
    return Promise.reject(error);
});

export default api;
