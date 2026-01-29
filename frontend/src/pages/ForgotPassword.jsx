import React, { useState } from 'react';
import api from '../api';
import { Link } from 'react-router-dom';
import { Truck, ArrowLeft, Mail } from 'lucide-react';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setMessage('');

        try {
            const res = await api.post('/auth/password-reset/request/', { email });
            setMessage(res.data?.message || "Si le compte existe, un email a été envoyé.");
        } catch (err) {
            setError(err.response?.data?.detail || "Impossible d'envoyer la demande.");
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

                <h1 className="login-title">Mot de passe oublié</h1>
                <p className="login-subtitle">
                    Entrez votre email. Si un compte existe, vous recevrez un lien sécurisé pour réinitialiser votre mot de passe.
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

                {message && (
                    <div style={{ 
                        background: 'var(--status-delivered-bg)', 
                        color: 'var(--status-delivered-text)',
                        padding: '0.75rem 1rem',
                        borderRadius: 'var(--radius-sm)',
                        marginBottom: '1.5rem',
                        fontSize: '0.875rem',
                        fontWeight: '500',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem'
                    }}>
                        <Mail size={16} />
                        {message}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="exemple@logistique.pro"
                            required
                            disabled={loading}
                        />
                    </div>

                    <button type="submit" disabled={loading} style={{ width: '100%', marginTop: '0.5rem' }}>
                        {loading ? 'Envoi en cours...' : 'Envoyer le lien'}
                    </button>
                </form>

                <div style={{ marginTop: '2rem', textAlign: 'center' }}>
                    <Link to="/login" style={{ 
                        color: 'var(--text-muted)',
                        textDecoration: 'none',
                        fontSize: '0.875rem',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        transition: 'color 0.2s'
                    }}>
                        <ArrowLeft size={16} />
                        Retour à la connexion
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
