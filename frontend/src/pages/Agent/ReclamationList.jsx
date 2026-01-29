import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api';
import { FileText, Plus, Download, Trash2 } from 'lucide-react';
import PageHeader from '../../components/PageHeader';
import TopBar from '../../components/TopBar';
import StatsGrid from '../../components/StatsGrid';

const STATUT_LABELS = {
    EN_COURS: 'En cours',
    RESOLUE: 'Résolue',
    ANNULEE: 'Annulée',
};

const ReclamationList = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

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

    const handleDelete = async (id) => {
        if (!window.confirm('Voulez-vous vraiment supprimer cette réclamation ?')) return;
        try {
            await api.delete(`/reclamations/${id}/`);
            fetchItems();
        } catch (err) {
            const errorMsg = err.response?.data?.detail || "Impossible de supprimer cette réclamation.";
            alert(errorMsg);
        }
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    const filteredItems = items.filter(r =>
        r.objet?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.client_details?.nom?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const stats = [
        {
            label: 'Total Réclamations',
            value: items.length.toLocaleString(),
            icon: FileText
        },
        {
            label: 'En Cours',
            value: items.filter(r => r.statut === 'EN_COURS').length,
            badge: <span className="status-badge status-en-cours">En cours</span>
        },
        {
            label: 'Résolues',
            value: items.filter(r => r.statut === 'RESOLUE').length,
            badge: <span className="status-badge status-livre">Résolue</span>
        },
        {
            label: 'Annulées',
            value: items.filter(r => r.statut === 'ANNULEE').length
        }
    ];

    const getStatusClass = (status) => {
        const map = {
            'EN_COURS': 'status-en-cours',
            'RESOLUE': 'status-livre',
            'ANNULEE': 'status-neutral'
        };
        return map[status] || 'status-neutral';
    };

    return (
        <div className="page-container">
            <PageHeader 
                title="Réclamations"
                subtitle="Gestion des réclamations clients"
            />

            <TopBar
                searchValue={searchTerm}
                onSearchChange={setSearchTerm}
                searchPlaceholder="Rechercher une réclamation..."
                actions={
                    <>
                        <button className="secondary">
                            <Download size={18} />
                            Exporter
                        </button>
                        <Link to="/reclamations/nouveau" style={{ textDecoration: 'none' }}>
                            <button>
                                <Plus size={18} />
                                Nouvelle réclamation
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
                            <th>#</th>
                            <th>DATE</th>
                            <th>CLIENT</th>
                            <th>OBJET</th>
                            <th>LIENS</th>
                            <th>STATUT</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredItems.map((r) => (
                            <tr key={r.id}>
                                <td>
                                    <div style={{ fontWeight: '600', color: 'var(--text-main)' }}>
                                        #{r.id}
                                    </div>
                                </td>
                                <td>
                                    {r.date_reclamation ? new Date(r.date_reclamation).toLocaleDateString('fr-FR', { 
                                        day: '2-digit', 
                                        month: 'short', 
                                        year: 'numeric' 
                                    }) : '-'}
                                </td>
                                <td>
                                    <div style={{ fontWeight: '500' }}>
                                        {r.client_details ? `${r.client_details.nom} ${r.client_details.prenom || ''}`.trim() : '-'}
                                    </div>
                                </td>
                                <td>
                                    <div style={{ maxWidth: '320px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                        {r.objet || '-'}
                                    </div>
                                </td>
                                <td>
                                    <div className="table-secondary-text">
                                        {(r.expedition_codes?.length ? `Colis: ${r.expedition_codes.join(', ')}` : '')}
                                        {(r.facture ? (r.expedition_codes?.length ? ' | ' : '') + `Facture #${r.facture}` : '')}
                                        {(r.type_service ? ` | Service #${r.type_service}` : '')}
                                        {(!r.expedition_codes?.length && !r.facture && !r.type_service) ? '-' : ''}
                                    </div>
                                </td>
                                <td>
                                    <span className={`status-badge ${getStatusClass(r.statut)}`}>
                                        {STATUT_LABELS[r.statut] || r.statut || '-'}
                                    </span>
                                </td>
                                <td>
                                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                        <Link
                                            to={`/reclamations/${r.id}/edit`}
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
                                            onClick={() => handleDelete(r.id)}
                                            style={{ color: '#b91c1c' }}
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {filteredItems.length === 0 && (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
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
