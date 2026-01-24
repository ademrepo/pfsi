import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api';

const STATUT_LABELS = {
    EN_COURS: 'En cours',
    RESOLUE: 'Résolue',
    ANNULEE: 'Annulée',
};

const ReclamationList = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchItems();
    }, []);

    const fetchItems = async () => {
        try {
            const res = await api.get('/reclamations/');
            setItems(res.data);
            setLoading(false);
        } catch (e) {
            setError("Erreur lors du chargement des réclamations.");
            setLoading(false);
        }
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Réclamations</h1>
                <Link to="/reclamations/nouveau" className="btn-primary" style={{ textDecoration: 'none' }}>
                    + Nouvelle réclamation
                </Link>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Date</th>
                            <th>Client</th>
                            <th>Objet</th>
                            <th>Liens</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items.map((r) => (
                            <tr key={r.id}>
                                <td style={{ fontWeight: 600 }}>{r.id}</td>
                                <td>{r.date_reclamation ? new Date(r.date_reclamation).toLocaleDateString() : '-'}</td>
                                <td>{r.client_details ? `${r.client_details.nom} ${r.client_details.prenom || ''}` : '-'}</td>
                                <td style={{ maxWidth: 320, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                    {r.objet || '-'}
                                </td>
                                <td style={{ fontSize: '0.85rem' }}>
                                    {(r.expedition_codes?.length ? `Colis: ${r.expedition_codes.join(', ')}` : '')}
                                    {(r.facture ? (r.expedition_codes?.length ? ' | ' : '') + `Facture #${r.facture}` : '')}
                                    {(r.type_service ? ` | Service #${r.type_service}` : '')}
                                    {(!r.expedition_codes?.length && !r.facture && !r.type_service) ? '-' : ''}
                                </td>
                                <td>{STATUT_LABELS[r.statut] || r.statut || '-'}</td>
                                <td className="actions">
                                    <Link
                                        to={`/reclamations/${r.id}/edit`}
                                        className="btn-primary"
                                        style={{ textDecoration: 'none', padding: '0.4rem 0.8rem', background: '#e2e8f0', color: '#1e293b' }}
                                    >
                                        Modifier
                                    </Link>
                                </td>
                            </tr>
                        ))}
                        {items.length === 0 && (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', padding: '2rem' }}>
                                    Aucune réclamation.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ReclamationList;

