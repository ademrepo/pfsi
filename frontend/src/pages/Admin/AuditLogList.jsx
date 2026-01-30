import React, { useState, useEffect } from 'react';
import api from '../../api';

const AuditLogList = () => {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filters, setFilters] = useState({
        user_id: '',
        action_type: ''
    });

    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetchData();
        fetchUsers();
    }, []);

    useEffect(() => {
        fetchData();
    }, [filters]);

    const fetchUsers = async () => {
        try {
            const res = await api.get('/utilisateurs/');
            setUsers(res.data);
        } catch (err) { }
    };

    const fetchData = async () => {
        setLoading(true);
        try {
            const params = {};
            if (filters.user_id) params.user_id = filters.user_id;
            if (filters.action_type) params.action_type = filters.action_type;

            const response = await api.get('/audit-logs/', { params });
            setLogs(response.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const getActionStyle = (type) => {
        switch (type) {
            case 'LOGIN_SUCCESS': return 'status-livre';
            case 'LOGIN_FAILED': return 'status-retard';
            case 'LOGOUT': return 'status-neutral';
            case 'USER_CREATED': return 'status-en_cours';
            case 'USER_UPDATED': return 'status-retard'; // Using beige/orange for update
            default: return 'status-neutral';
        }
    };

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Journal d'Audit</h1>
            </div>

            <div className="form-card" style={{ maxWidth: 'none', padding: '1.5rem', marginBottom: '2rem', display: 'flex', gap: '1.5rem', alignItems: 'flex-end', borderRadius: '15px' }}>
                <div className="form-group" style={{ marginBottom: 0, flex: 1 }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '0.5rem', display: 'block' }}>UTILISATEUR</label>
                    <select
                        value={filters.user_id}
                        onChange={(e) => setFilters({ ...filters, user_id: e.target.value })}
                        style={{
                            borderRadius: '12px',
                            appearance: 'none',
                            backgroundImage: `url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%23CBD5E0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>')`,
                            backgroundRepeat: 'no-repeat',
                            backgroundPosition: 'right 12px center',
                            paddingRight: '35px',
                            height: '45px'
                        }}
                    >
                        <option value="">Tous les utilisateurs</option>
                        {users.map(u => <option key={u.id} value={u.id}>{u.username}</option>)}
                    </select>
                </div>

                <div className="form-group" style={{ marginBottom: 0, flex: 1 }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '0.5rem', display: 'block' }}>TYPE D'ACTION</label>
                    <select
                        value={filters.action_type}
                        onChange={(e) => setFilters({ ...filters, action_type: e.target.value })}
                        style={{
                            borderRadius: '12px',
                            appearance: 'none',
                            backgroundImage: `url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%23CBD5E0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>')`,
                            backgroundRepeat: 'no-repeat',
                            backgroundPosition: 'right 12px center',
                            paddingRight: '35px',
                            height: '45px'
                        }}
                    >
                        <option value="">Toutes les actions</option>
                        <option value="LOGIN_SUCCESS">Connexion réussie</option>
                        <option value="LOGIN_FAILED">Échec connexion</option>
                        <option value="LOGOUT">Déconnexion</option>
                        <option value="USER_CREATED">Utilisateur créé</option>
                        <option value="USER_UPDATED">Utilisateur modifié</option>
                        <option value="USER_DEACTIVATED">Utilisateur désactivé</option>
                        <option value="PASSWORD_RESET">Reset mot de passe</option>
                    </select>
                </div>

                <button
                    onClick={() => setFilters({ user_id: '', action_type: '' })}
                    style={{
                        width: 'auto',
                        borderRadius: '12px',
                        padding: '0 1.5rem',
                        height: '45px',
                        background: '#C68E17',
                        color: 'white',
                        border: 'none',
                        fontWeight: '600',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                    }}
                >
                    Réinitialiser
                </button>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>DATE</th>
                            <th>UTILISATEUR</th>
                            <th>ACTION</th>
                            <th>IP</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logs.map(log => (
                            <tr key={log.id}>
                                <td style={{ fontSize: '0.85rem', whiteSpace: 'nowrap', color: 'var(--text-muted)' }}>
                                    {new Date(log.timestamp).toLocaleString()}
                                </td>
                                <td style={{ fontWeight: '600', color: 'var(--text-main)' }}>{log.user_display || log.username || 'Anonyme'}</td>
                                <td>
                                    <span className={`status-badge ${getActionStyle(log.action_type)}`}>
                                        {log.action_display || log.action_type}
                                    </span>
                                </td>
                                <td style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>{log.ip_address}</td>
                            </tr>
                        ))}
                        {logs.length === 0 && (
                            <tr>
                                <td colSpan="5" style={{ textAlign: 'center', padding: '2rem' }}>Aucun log trouvé.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AuditLogList;
