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

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Journal d'Audit</h1>
            </div>

            <div className="form-card" style={{ maxWidth: 'none', padding: '1.5rem', marginBottom: '2rem', display: 'flex', gap: '1.5rem', alignItems: 'flex-end' }}>
                <div className="form-group" style={{ marginBottom: 0, flex: 1 }}>
                    <label>Utilisateur</label>
                    <select
                        value={filters.user_id}
                        onChange={(e) => setFilters({ ...filters, user_id: e.target.value })}
                    >
                        <option value="">Tous les utilisateurs</option>
                        {users.map(u => <option key={u.id} value={u.id}>{u.username}</option>)}
                    </select>
                </div>

                <div className="form-group" style={{ marginBottom: 0, flex: 1 }}>
                    <label>Type d'Action</label>
                    <select
                        value={filters.action_type}
                        onChange={(e) => setFilters({ ...filters, action_type: e.target.value })}
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

                <button className="secondary" onClick={() => setFilters({ user_id: '', action_type: '' })} style={{ width: 'auto' }}>
                    Réinitialiser
                </button>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Utilisateur</th>
                            <th>Action</th>
                            <th>IP</th>
                            <th>Détails</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logs.map(log => (
                            <tr key={log.id}>
                                <td style={{ fontSize: '0.85rem', whiteSpace: 'nowrap' }}>
                                    {new Date(log.timestamp).toLocaleString()}
                                </td>
                                <td style={{ fontWeight: '500' }}>{log.user_display || log.username || 'Anonyme'}</td>
                                <td>
                                    <span className="status-badge" style={{ background: '#f1f5f9', color: '#475569' }}>
                                        {log.action_display || log.action_type}
                                    </span>
                                </td>
                                <td style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{log.ip_address}</td>
                                <td style={{ fontSize: '0.8rem', color: '#64748b', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                    {log.details && JSON.stringify(log.details)}
                                </td>
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
