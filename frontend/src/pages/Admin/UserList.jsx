import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';

const UserList = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const response = await api.get('/utilisateurs/');
            setUsers(response.data);
            setLoading(false);
        } catch (err) {
            console.error(err);
            setLoading(false);
        }
    };

    const toggleStatus = async (user) => {
        const actionText = user.is_active ? 'désactiver' : 'activer';
        if (!window.confirm(`Voulez-vous vraiment ${actionText} cet utilisateur ?`)) return;

        try {
            const action = user.is_active ? 'deactivate' : 'activate';
            await api.post(`/utilisateurs/${user.id}/${action}/`);
            fetchUsers();
        } catch (err) {
            alert("Erreur lors du changement de statut");
        }
    };

    if (loading) return <div>Chargement...</div>;

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Utilisateurs</h1>
                <Link to="/admin/users/create" className="btn-primary" style={{ textDecoration: 'none' }}>
                    + Nouvel Utilisateur
                </Link>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>Nom Complet</th>
                            <th>Rôle</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(u => (
                            <tr key={u.id}>
                                <td style={{ fontWeight: '600' }}>{u.username}</td>
                                <td>{u.full_name}</td>
                                <td><span className="role-badge">{u.role_display}</span></td>
                                <td>
                                    <span className={`status-badge ${u.is_active ? 'status-Actif' : 'status-Inactif'}`}>
                                        {u.is_active ? 'Actif' : 'Inactif'}
                                    </span>
                                </td>
                                <td className="actions">
                                    <Link to={`/admin/users/${u.id}/edit`} className="btn-primary" style={{ textDecoration: 'none', padding: '0.4rem 0.8rem', background: '#e2e8f0', color: '#1e293b' }}>Modifier</Link>
                                    <button
                                        className="btn-primary"
                                        onClick={() => toggleStatus(u)}
                                        style={{ padding: '0.4rem 0.8rem', background: u.is_active ? '#fee2e2' : '#dcfce7', color: u.is_active ? '#b91c1c' : '#166534' }}
                                    >
                                        {u.is_active ? 'Désactiver' : 'Activer'}
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default UserList;
