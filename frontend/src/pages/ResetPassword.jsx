import React, { useMemo, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import api from '../api';
import { Truck, ArrowLeft, CheckCircle } from 'lucide-react';

function useQuery() {
    const { search } = useLocation();
    return useMemo(() => new URLSearchParams(search), [search]);
}

const ResetPassword = () => {
    const query = useQuery();
    const navigate = useNavigate();

    const token = query.get('token') || '';

    const [newPassword, setNewPassword] = useState('');
    const [confirm, setConfirm] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setMessage('');

        try {
            const res = await api.post('/auth/password-reset/confirm/', {
                token,
                new_password: newPassword,
                new_password_confirm: confirm,
            });
            setMessage(res.data?.message || 'Mot de passe mis à jour avec succès.');
            setTimeout(() => navigate('/login'), 1200);
        } catch (err) {
            setError(err.response?.data?.detail || err.response?.data?.new_password?.[0] || 'Impossible de réinitialiser le mot de passe.');
        } finally {
            setLoading(false);
        }
    };

    const missingToken = !token;

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-logo">
                    <div className="login-logo-icon">
                        <Truck size={24} strokeWidth={2.5} />
                    </div>
                    <span className="login-logo-text">Logistique Pro</span>
                </div>

                <h1 className="login-title">Nouveau mot de passe</h1>
                <p className="login-subtitle">
                    Choisissez un nouveau mot de passe sécurisé pour votre compte.
                </p>

                {missingToken && (
                    <div style={{ 
                        background: 'var(--status-delayed-bg)', 
                        color: 'var(--status-delayed-text)',
                        padding: '0.75rem 1rem',
                        borderRadius: 'var(--radius-sm)',
                        marginBottom: '1.5rem',
                        fontSize: '0.875rem',
                        fontWeight: '500'
                    }}>
                        Token manquant. Veuillez utiliser le lien reçu par email.
                    </div>
                )}

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
                        <CheckCircle size={16} />
                        {message}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label htmlFor="new_password">Nouveau mot de passe</label>
                        <input
                            type="password"
                            id="new_password"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            placeholder="Minimum 8 caractères"
                            required
                            disabled={loading || missingToken}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="confirm">Confirmer le mot de passe</label>
                        <input
                            type="password"
                            id="confirm"
                            value={confirm}
                            onChange={(e) => setConfirm(e.target.value)}
                            placeholder="Retapez votre mot de passe"
                            required
                            disabled={loading || missingToken}
                        />
                    </div>

                    <button type="submit" disabled={loading || missingToken} style={{ width: '100%', marginTop: '0.5rem' }}>
                        {loading ? 'Validation...' : 'Réinitialiser le mot de passe'}
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

export default ResetPassword;
