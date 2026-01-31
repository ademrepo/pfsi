import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import api from '../../api';
import { AlertTriangle, Plus, Printer, Trash2 } from 'lucide-react';
import PageHeader from '../../components/PageHeader';
import TopBar from '../../components/TopBar';
import StatsGrid from '../../components/StatsGrid';

const TYPE_LABELS = {
    RETARD: 'Retard',
    PERTE: 'Perte',
    ENDOMMAGEMENT: 'Endommagement',
    PROBLEME_TECHNIQUE: 'Problème technique',
    AUTRE: 'Autre',
};

const ACTION_LABELS = {
    SET_ECHEC_LIVRAISON: 'Échec de livraison',
    SET_ANNULEE: 'Tournée annulée',
    NONE: '-',
};

function useQuery() {
    const { search } = useLocation();
    return React.useMemo(() => new URLSearchParams(search), [search]);
}

const IncidentList = () => {
    const query = useQuery();
    const [incidents, setIncidents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    const expeditionId = query.get('expedition_id');
    const tourneeId = query.get('tournee_id');

    useEffect(() => {
        fetchIncidents();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [expeditionId, tourneeId]);

    const fetchIncidents = async () => {
        try {
            const params = {};
            if (expeditionId) params.expedition_id = expeditionId;
            if (tourneeId) params.tournee_id = tourneeId;
            const res = await api.get('/incidents/', { params });
            setIncidents(res.data);
            setLoading(false);
        } catch (e) {
            setError("Erreur lors du chargement des incidents.");
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Voulez-vous vraiment supprimer cet incident ?')) return;
        try {
            await api.delete(`/incidents/${id}/`);
            fetchIncidents();
        } catch (err) {
            const errorMsg = err.response?.data?.detail || "Impossible de supprimer cet incident.";
            alert(errorMsg);
        }
    };

    const refLabel = (inc) => {
        if (inc.expedition_code) return `Expédition ${inc.expedition_code}`;
        if (inc.tournee_code) return `Tournée ${inc.tournee_code}`;
        return '-';
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    const filteredIncidents = incidents.filter(inc =>
        inc.code_incident?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        inc.expedition_code?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        inc.tournee_code?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const stats = [
        {
            label: 'Total Incidents',
            value: incidents.length.toLocaleString(),
            icon: AlertTriangle
        },
        {
            label: 'Retards',
            value: incidents.filter(i => i.type_incident === 'RETARD').length,
            badge: <span className="status-badge status-retard">Retard</span>
        },
        {
            label: 'Pertes',
            value: incidents.filter(i => i.type_incident === 'PERTE').length
        },
        {
            label: 'Endommagements',
            value: incidents.filter(i => i.type_incident === 'ENDOMMAGEMENT').length
        }
    ];

    return (
        <div className="page-container">
            <PageHeader
                title="Incidents"
                subtitle="Suivez et gérez les incidents signalés"
            />

            <TopBar
                searchValue={searchTerm}
                onSearchChange={setSearchTerm}
                searchPlaceholder="Rechercher un incident..."
                actions={
                    <>
                        <button className="secondary" onClick={() => window.print()}>
                            <Printer size={18} />
                            Imprimer
                        </button>
                        <Link
                            to={`/incidents/nouveau${expeditionId ? `?expedition_id=${expeditionId}` : tourneeId ? `?tournee_id=${tourneeId}` : ''}`}
                            style={{ textDecoration: 'none' }}
                        >
                            <button>
                                <Plus size={18} />
                                Signaler un incident
                            </button>
                        </Link>
                    </>
                }
            />

            <StatsGrid stats={stats} variant="bold" />

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>CODE</th>
                            <th>DATE</th>
                            <th>TYPE</th>
                            <th>RÉFÉRENCE</th>
                            <th>ACTION STATUT</th>
                            <th>PIÈCES JOINTES</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredIncidents.map((inc) => (
                            <tr key={inc.id}>
                                <td>
                                    <div style={{ fontWeight: '600', color: 'var(--text-main)' }}>
                                        {inc.code_incident}
                                    </div>
                                </td>
                                <td>
                                    {inc.created_at ? new Date(inc.created_at).toLocaleDateString('fr-FR', {
                                        day: '2-digit',
                                        month: 'short',
                                        year: 'numeric'
                                    }) : '-'}
                                </td>
                                <td>
                                    <span className={`status-badge ${inc.type_incident === 'RETARD' ? 'status-retard' : 'status-neutral'}`}>
                                        {TYPE_LABELS[inc.type_incident] || inc.type_incident}
                                    </span>
                                </td>
                                <td>
                                    <div style={{ fontWeight: '500' }}>
                                        {refLabel(inc)}
                                    </div>
                                </td>
                                <td>{ACTION_LABELS[inc.action_appliquee] || inc.action_appliquee}</td>
                                <td>
                                    <span style={{
                                        background: 'var(--bg-page)',
                                        padding: '0.35rem 0.75rem',
                                        borderRadius: '6px',
                                        fontWeight: '600',
                                        fontSize: '0.875rem'
                                    }}>
                                        {inc.attachments?.length || 0}
                                    </span>
                                </td>
                                <td>
                                    <button
                                        className="btn-icon"
                                        type="button"
                                        title="Supprimer"
                                        onClick={() => handleDelete(inc.id)}
                                        style={{ color: '#b91c1c' }}
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {filteredIncidents.length === 0 && (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                    Aucun incident trouvé.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default IncidentList;
