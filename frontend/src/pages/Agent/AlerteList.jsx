import React, { useEffect, useState } from 'react';
import api from '../../api';
import { Bell, BellRing, CheckCircle } from 'lucide-react';
import PageHeader from '../../components/PageHeader';
import StatsGrid from '../../components/StatsGrid';

const AlerteList = () => {
    const [alertes, setAlertes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchAlertes();
    }, []);

    const fetchAlertes = async () => {
        try {
            const res = await api.get('/alertes/');
            setAlertes(res.data);
            setLoading(false);
        } catch (e) {
            setError("Erreur lors du chargement des alertes.");
            setLoading(false);
        }
    };

    const markRead = async (id) => {
        try {
            await api.post(`/alertes/${id}/mark_read/`);
            fetchAlertes();
        } catch (e) {
            alert("Impossible de marquer comme lue.");
        }
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    const stats = [
        {
            label: 'Total Alertes',
            value: alertes.length.toLocaleString(),
            icon: Bell
        },
        {
            label: 'Non Lues',
            value: alertes.filter(a => !a.is_read).length,
            badge: <span className="status-badge status-retard">À traiter</span>
        },
        {
            label: 'Lues',
            value: alertes.filter(a => a.is_read).length,
            icon: CheckCircle
        }
    ];

    return (
        <div className="page-container">
            <PageHeader
                title="Alertes"
                subtitle="Notifications système et alertes importantes"
            />

            <StatsGrid stats={stats} />

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th style={{ width: '50px' }}></th>
                            <th>TITRE</th>
                            <th>DESTINATAIRE</th>
                            <th>DATE</th>
                            <th>STATUT</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {alertes.map((a) => (
                            <tr key={a.id}>
                                <td>
                                    {!a.is_read && (
                                        <BellRing size={18} style={{ color: 'var(--primary)' }} />
                                    )}
                                </td>
                                <td>
                                    <div style={{ fontWeight: a.is_read ? '500' : '700', color: 'var(--text-main)' }}>
                                        {a.titre}
                                    </div>
                                </td>
                                <td>{a.destination}</td>
                                <td>
                                    {a.created_at ? new Date(a.created_at).toLocaleDateString('fr-FR', {
                                        day: '2-digit',
                                        month: 'short',
                                        year: 'numeric',
                                        hour: '2-digit',
                                        minute: '2-digit'
                                    }) : '-'}
                                </td>
                                <td>
                                    {a.is_read ? (
                                        <span className="status-badge status-neutral">Lue</span>
                                    ) : (
                                        <span className="status-badge status-actif">Non lue</span>
                                    )}
                                </td>
                                <td>
                                    {!a.is_read && (
                                        <button
                                            onClick={() => markRead(a.id)}
                                            style={{
                                                background: 'transparent',
                                                border: '1px solid var(--border)',
                                                color: 'var(--text-secondary)',
                                                padding: '0.5rem 1rem',
                                                borderRadius: 'var(--radius-sm)',
                                                cursor: 'pointer',
                                                fontSize: '0.875rem',
                                                fontWeight: '500'
                                            }}
                                        >
                                            Marquer comme lue
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                        {alertes.length === 0 && (
                            <tr>
                                <td colSpan="6" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                    Aucune alerte.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AlerteList;
