import React, { useMemo, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import api from '../api';

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
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#f0f2f5' }}>
            <div className="container" style={{ maxWidth: '420px', width: '100%' }}>
                <h1>Nouveau mot de passe</h1>

                {missingToken && (
                    <div className="error">
                        Token manquant. Ouvre le lien reçu par email.
                    </div>
                )}

                {error && <div className="error">{error}</div>}
                {message && <div style={{ background: '#ecfdf5', border: '1px solid #10b98133', padding: '0.75rem', borderRadius: '8px', color: '#065f46', marginBottom: '1rem' }}>{message}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="new_password">Nouveau mot de passe</label>
                        <input
                            type="password"
                            id="new_password"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
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
                            required
                            disabled={loading || missingToken}
                        />
                    </div>

                    <button type="submit" disabled={loading || missingToken}>
                        {loading ? 'Validation...' : 'Valider'}
                    </button>
                </form>

                <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                    <Link to="/login" style={{ color: 'var(--primary)' }}>Retour à la connexion</Link>
                </div>
            </div>
        </div>
    );
};

export default ResetPassword;
