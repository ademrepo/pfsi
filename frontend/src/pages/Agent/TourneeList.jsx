import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';
import { Truck, Plus, Download, MapPin, Trash2 } from 'lucide-react';
import PageHeader from '../../components/PageHeader';
import TopBar from '../../components/TopBar';
import StatsGrid from '../../components/StatsGrid';

const TourneeList = () => {
    const [tournees, setTournees] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

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
            'Préparée': 'status-valide',
            'En cours': 'status-en-cours',
            'Terminée': 'status-livre',
            'Annulée': 'status-retard'
        };
        return map[status] || 'status-neutral';
    };

    const filteredTournees = tournees.filter(t =>
        t.code_tournee.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.chauffeur_details?.nom?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.vehicule_details?.immatriculation?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const stats = [
        {
            label: 'Total Tournées',
            value: tournees.length.toLocaleString(),
            icon: Truck
        },
        {
            label: 'En Cours',
            value: tournees.filter(t => t.statut === 'En cours').length,
            badge: <span className="status-badge status-en-cours">En cours</span>
        },
        {
            label: 'Terminées',
            value: tournees.filter(t => t.statut === 'Terminée').length,
            badge: <span className="status-badge status-livre">Terminée</span>
        },
        {
            label: 'Préparées',
            value: tournees.filter(t => t.statut === 'Préparée').length
        }
    ];

    return (
        <div className="page-container">
            <PageHeader 
                title="Journal des Tournées"
                subtitle="Planifiez et suivez vos tournées de livraison"
            />

            <TopBar
                searchValue={searchTerm}
                onSearchChange={setSearchTerm}
                searchPlaceholder="Rechercher une tournée, chauffeur..."
                actions={
                    <>
                        <button className="secondary">
                            <Download size={18} />
                            Exporter
                        </button>
                        <Link to="/tournees/nouveau" style={{ textDecoration: 'none' }}>
                            <button>
                                <Plus size={18} />
                                Nouvelle Tournée
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
                            <th>CODE</th>
                            <th>DATE</th>
                            <th>CHAUFFEUR</th>
                            <th>VÉHICULE</th>
                            <th>COLIS</th>
                            <th>STATUT</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredTournees.map(t => (
                            <tr key={t.id}>
                                <td>
                                    <div style={{ fontWeight: '600', color: 'var(--text-main)' }}>
                                        {t.code_tournee}
                                    </div>
                                </td>
                                <td>{new Date(t.date_tournee).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })}</td>
                                <td>
                                    <div style={{ fontWeight: '500' }}>
                                        {t.chauffeur_details ? `${t.chauffeur_details.nom} ${t.chauffeur_details.prenom}` : 'N/A'}
                                    </div>
                                </td>
                                <td>
                                    <div style={{ fontWeight: '500' }}>
                                        {t.vehicule_details?.immatriculation || 'N/A'}
                                    </div>
                                    <div className="table-secondary-text">
                                        {t.vehicule_details?.marque} {t.vehicule_details?.modele}
                                    </div>
                                </td>
                                <td>
                                    <span style={{ 
                                        background: 'var(--bg-page)',
                                        padding: '0.35rem 0.75rem',
                                        borderRadius: '6px',
                                        fontWeight: '600',
                                        fontSize: '0.875rem'
                                    }}>
                                        {t.expeditions_count}
                                    </span>
                                </td>
                                <td>
                                    <span className={`status-badge ${getStatusClass(t.statut)}`}>
                                        {t.statut}
                                    </span>
                                </td>
                                <td>
                                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                        <Link
                                            to={`/tournees/${t.id}/edit`}
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
                                            className="btn-icon"
                                            type="button"
                                            title="Supprimer"
                                            onClick={() => handleDelete(t.id)}
                                            style={{ color: '#b91c1c' }}
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {filteredTournees.length === 0 && (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                    Aucune tournée trouvée.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TourneeList;
