import React, { useEffect, useState } from 'react';
import api from '../../api';

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

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Alertes</h1>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Destinataire</th>
                            <th>Titre</th>
                            <th>Date</th>
                            <th>Lu</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {alertes.map((a) => (
                            <tr key={a.id}>
                                <td>{a.destination}</td>
                                <td style={{ fontWeight: a.is_read ? '400' : '700' }}>{a.titre}</td>
                                <td>{a.created_at ? new Date(a.created_at).toLocaleString() : '-'}</td>
                                <td>{a.is_read ? 'Oui' : 'Non'}</td>
                                <td className="actions">
                                    {!a.is_read && (
                                        <button
                                            className="btn-primary"
                                            onClick={() => markRead(a.id)}
                                            style={{ padding: '0.4rem 0.8rem', background: '#e2e8f0', color: '#1e293b' }}
                                        >
                                            Marquer lue
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                        {alertes.length === 0 && (
                            <tr>
                                <td colSpan="5" style={{ textAlign: 'center', padding: '2rem' }}>
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

