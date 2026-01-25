import React, { useState } from 'react';
import api from '../api';
import { Link } from 'react-router-dom';

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
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#f0f2f5' }}>
            <div className="container" style={{ maxWidth: '420px', width: '100%' }}>
                <h1>Mot de passe oublié</h1>
                <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>
                    Entrez votre email. Si un compte existe, vous recevrez un lien sécurisé pour réinitialiser votre mot de passe.
                </p>

                {error && <div className="error">{error}</div>}
                {message && <div style={{ background: '#ecfdf5', border: '1px solid #10b98133', padding: '0.75rem', borderRadius: '8px', color: '#065f46', marginBottom: '1rem' }}>{message}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="ex: admin@transport.dz"
                            required
                            disabled={loading}
                        />
                    </div>

                    <button type="submit" disabled={loading}>
                        {loading ? 'Envoi...' : 'Envoyer le lien'}
                    </button>
                </form>

                <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                    <Link to="/login" style={{ color: 'var(--primary)' }}>Retour à la connexion</Link>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
