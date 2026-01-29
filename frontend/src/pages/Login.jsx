import React, { useState } from 'react';
import api from '../api';
import { Link, useNavigate } from 'react-router-dom';
import { Truck, CircleHelp } from 'lucide-react';

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await api.post('/auth/login/', {
                username,
                password
            });
            onLogin(response.data.user);
            navigate('/');
        } catch (err) {
            console.error('Login error:', err);
            setError(
                err.response?.data?.non_field_errors?.[0] ||
                'Échec de la connexion. Vérifiez vos identifiants.'
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-logo">
                    <div className="login-logo-icon">
                        <Truck size={24} strokeWidth={2.5} />
                    </div>
                    <span className="login-logo-text">Logistique Pro</span>
                </div>

                <h1 className="login-title">Connexion</h1>
                <p className="login-subtitle">
                    Accédez à votre portail administrateur pour gérer<br />
                    vos opérations logistiques.
                </p>

                {error && (
                    <div style={{ 
                        background: 'var(--status-delayed-bg)', 
                        color: 'var(--status-delayed-text)',
                        padding: '0.75rem 1rem',
                        borderRadius: 'var(--radius-sm)',
                        marginBottom: '1.5rem',
                        fontSize: '0.875rem',
                        fontWeight: '500'
                    }}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleLogin} className="login-form">
                    <div className="form-group">
                        <label htmlFor="username">Email</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="exemple@logistique.pro"
                            required
                            disabled={loading}
                        />
                    </div>

                    <div className="form-group">
                        <div className="form-group-row">
                            <label htmlFor="password">Mot de passe</label>
                            <Link to="/forgot-password" className="form-link">
                                Mot de passe oublié ?
                            </Link>
                        </div>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••••••"
                            required
                            disabled={loading}
                        />
                    </div>

                    <button type="submit" disabled={loading} style={{ width: '100%', marginTop: '0.5rem' }}>
                        {loading ? 'Connexion en cours...' : 'Se connecter'}
                    </button>
                </form>

                <div className="login-help">
                    <a href="#" className="login-help-link">
                        <CircleHelp size={18} />
                        Besoin d'aide ?
                    </a>
                </div>

                <div style={{ marginTop: '1.5rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    <p style={{ marginBottom: '0.5rem' }}>Comptes de test (password123):</p>
                    <p style={{ fontWeight: '500', color: 'var(--text-secondary)' }}>
                        admin, agent1, comptable1, logistique1
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;
