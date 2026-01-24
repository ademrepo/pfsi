import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';

const TourneeList = () => {
    const [tournees, setTournees] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchTournees();
    }, []);

    const fetchTournees = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await api.get('/tournees/');
            setTournees(response.data);
        } catch (err) {
            console.error(err);
            setError("Erreur lors du chargement des tournées.");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Voulez-vous vraiment supprimer cette tournée ?')) {
            try {
                // Avant de supprimer, on devrait détacher les expéditions côté backend ou ici
                // Pour simplifier on suppose que le backend gère ou on prévient l'utilisateur
                await api.delete(`/tournees/${id}/`);
                fetchTournees();
            } catch (err) {
                alert("Erreur lors de la suppression.");
            }
        }
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    const getStatusClass = (status) => {
        const map = {
            'Préparée': 'status-Validé',
            'En cours': 'status-En.cours',
            'Terminée': 'status-Livré',
            'Annulée': 'status-Inactif'
        };
        return map[status] || '';
    };

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Journal des Tournées</h1>
                <Link to="/tournees/nouveau" className="btn-primary" style={{ padding: '0.5rem 1rem', textDecoration: 'none', borderRadius: '4px' }}>
                    + Nouvelle Tournée
                </Link>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Code</th>
                            <th>Date</th>
                            <th>Chauffeur</th>
                            <th>Véhicule</th>
                            <th>Colis</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tournees.map(t => (
                            <tr key={t.id}>
                                <td style={{ fontWeight: '600' }}>{t.code_tournee}</td>
                                <td>{new Date(t.date_tournee).toLocaleDateString()}</td>
                                <td>{t.chauffeur_details ? `${t.chauffeur_details.nom} ${t.chauffeur_details.prenom}` : 'N/A'}</td>
                                <td>{t.vehicule_details?.immatriculation}</td>
                                <td style={{ textAlign: 'center' }}>
                                    <span className="role-badge" style={{ background: '#f1f5f9', color: '#475569', minWidth: '40px' }}>
                                        {t.expeditions_count}
                                    </span>
                                </td>
                                <td>
                                    <span className={`status-badge ${getStatusClass(t.statut)}`}>
                                        {t.statut}
                                    </span>
                                </td>
                                <td className="actions">
                                    <Link
                                        to={`/tournees/${t.id}/edit`}
                                        className="btn-primary"
                                        style={{
                                            textDecoration: 'none',
                                            padding: '0.4rem 0.8rem',
                                            background: '#e2e8f0',
                                            color: '#1e293b'
                                        }}
                                    >
                                        Modifier
                                    </Link>
                                    <button
                                        className="btn-primary"
                                        onClick={() => handleDelete(t.id)}
                                        style={{ padding: '0.4rem 0.8rem', background: '#fee2e2', color: '#b91c1c' }}
                                    >
                                        Supprimer
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {tournees.length === 0 && (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', padding: '2rem' }}>Aucune tournée trouvée.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TourneeList;
