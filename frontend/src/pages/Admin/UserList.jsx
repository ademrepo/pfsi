import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';
import { Users, Plus, Download, MoreVertical } from 'lucide-react';
import PageHeader from '../../components/PageHeader';
import TopBar from '../../components/TopBar';
import StatsGrid from '../../components/StatsGrid';

const UserList = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

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

    if (loading) return <div className="page-container">Chargement...</div>;

    const filteredUsers = users.filter(u =>
        u.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        u.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        u.role_display?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const stats = [
        {
            label: 'Total Utilisateurs',
            value: users.length.toLocaleString(),
            icon: Users
        },
        {
            label: 'Actifs',
            value: users.filter(u => u.is_active).length,
            badge: <span className="status-badge status-livre">Actif</span>
        },
        {
            label: 'Inactifs',
            value: users.filter(u => !u.is_active).length
        }
    ];

    return (
        <div className="page-container">
            <PageHeader 
                title="Utilisateurs"
                subtitle="Gestion des comptes utilisateurs et des accès"
            />

            <TopBar
                searchValue={searchTerm}
                onSearchChange={setSearchTerm}
                searchPlaceholder="Rechercher un utilisateur..."
                actions={
                    <>
                        <button className="secondary">
                            <Download size={18} />
                            Exporter
                        </button>
                        <Link to="/admin/users/create" style={{ textDecoration: 'none' }}>
                            <button>
                                <Plus size={18} />
                                Nouvel Utilisateur
                            </button>
                        </Link>
                    </>
                }
            />

            <StatsGrid stats={stats} />

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>USERNAME</th>
                            <th>NOM COMPLET</th>
                            <th>RÔLE</th>
                            <th>STATUT</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredUsers.map(u => (
                            <tr key={u.id}>
                                <td>
                                    <div style={{ fontWeight: '600', color: 'var(--text-main)' }}>
                                        {u.username}
                                    </div>
                                </td>
                                <td>{u.full_name}</td>
                                <td>
                                    <span className="role-badge">
                                        {u.role_display}
                                    </span>
                                </td>
                                <td>
                                    {u.is_active ? (
                                        <span className="status-badge status-livre">Actif</span>
                                    ) : (
                                        <span className="status-badge status-neutral">Inactif</span>
                                    )}
                                </td>
                                <td>
                                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                        <Link
                                            to={`/admin/users/${u.id}/edit`}
                                            style={{
                                                textDecoration: 'none',
                                                color: 'var(--text-secondary)',
                                                fontSize: '0.875rem',
                                                fontWeight: '500'
                                            }}
                                        >
                                            Modifier
                                        </Link>
                                        <button
                                            onClick={() => toggleStatus(u)}
                                            style={{
                                                background: 'transparent',
                                                border: '1px solid var(--border)',
                                                color: u.is_active ? 'var(--status-delayed-text)' : 'var(--status-delivered-text)',
                                                padding: '0.5rem 1rem',
                                                borderRadius: 'var(--radius-sm)',
                                                cursor: 'pointer',
                                                fontSize: '0.875rem',
                                                fontWeight: '500'
                                            }}
                                        >
                                            {u.is_active ? 'Désactiver' : 'Activer'}
                                        </button>
                                        <button className="btn-icon">
                                            <MoreVertical size={18} />
                                        </button>
                                    </div>
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
