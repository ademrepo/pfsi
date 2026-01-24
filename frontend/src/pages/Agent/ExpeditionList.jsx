import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';

const ExpeditionList = () => {
    const [expeditions, setExpeditions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchExpeditions();
    }, []);

    const fetchExpeditions = async () => {
        try {
            const response = await api.get('/expeditions/');
            setExpeditions(response.data);
            setLoading(false);
        } catch (err) {
            setError('Erreur lors du chargement des expéditions');
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Voulez-vous vraiment supprimer cette expédition ?')) {
            try {
                await api.delete(`/expeditions/${id}/`);
                fetchExpeditions();
            } catch (err) {
                const errorMsg = err.response?.data?.[0] || "Impossible de supprimer cette expédition (déjà liée à une tournée).";
                alert(errorMsg);
            }
        }
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    const getStatusClass = (status) => {
        const map = {
            'Enregistré': 'status-Validé',
            'Validé': 'status-Validé',
            'En transit': 'status-En.cours',
            'En centre de tri': 'status-En.cours',
            'En cours de livraison': 'status-En.cours',
            'Livré': 'status-Livré',
            'Échec de livraison': 'status-Inactif'
        };
        return map[status] || '';
    };

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Expéditions</h1>
                <Link to="/expeditions/nouveau" className="btn-primary" style={{ textDecoration: 'none' }}>
                    + Nouvelle Expédition
                </Link>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Code</th>
                            <th>Date</th>
                            <th>Client</th>
                            <th>Destination</th>
                            <th>Service</th>
                            <th>Détails</th>
                            <th>Montant</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {expeditions.map((exp) => (
                            <tr key={exp.id}>
                                <td style={{ fontWeight: '600' }}>{exp.code_expedition}</td>
                                <td>{new Date(exp.date_creation).toLocaleDateString()}</td>
                                <td>{exp.client_details ? `${exp.client_details.nom} ${exp.client_details.prenom || ''}` : 'Inconnu'}</td>
                                <td>{exp.destination_details?.ville}</td>
                                <td>{exp.type_service_details?.libelle}</td>
                                <td style={{ fontSize: '0.85rem' }}>{exp.poids_kg}kg / {exp.volume_m3}m³</td>
                                <td style={{ fontWeight: '600' }}>{exp.montant_total} €</td>
                                <td>
                                    <span className={`status-badge ${getStatusClass(exp.statut)}`}>
                                        {exp.statut}
                                    </span>
                                </td>
                                <td className="actions">
                                    <Link
                                        to={`/expeditions/${exp.id}/edit`}
                                        className="btn-primary"
                                        style={{
                                            textDecoration: 'none',
                                            padding: '0.4rem 0.8rem',
                                            background: '#e2e8f0',
                                            color: '#1e293b',
                                            display: exp.tournee ? 'none' : 'inline-block'
                                        }}
                                    >
                                        Modifier
                                    </Link>
                                    <button
                                        className="btn-primary"
                                        onClick={() => handleDelete(exp.id)}
                                        style={{
                                            padding: '0.4rem 0.8rem',
                                            background: '#fee2e2',
                                            color: '#b91c1c',
                                            display: exp.tournee ? 'none' : 'inline-block'
                                        }}
                                    >
                                        Supprimer
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {expeditions.length === 0 && (
                            <tr>
                                <td colSpan="9" style={{ textAlign: 'center', padding: '2rem' }}>Aucune expédition trouvée.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ExpeditionList;
