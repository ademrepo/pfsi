import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import api from '../../api';

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

    const refLabel = (inc) => {
        if (inc.expedition_code) return `Expédition ${inc.expedition_code}`;
        if (inc.tournee_code) return `Tournée ${inc.tournee_code}`;
        return '-';
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Incidents</h1>
                <Link
                    to={`/incidents/nouveau${expeditionId ? `?expedition_id=${expeditionId}` : tourneeId ? `?tournee_id=${tourneeId}` : ''}`}
                    className="btn-primary"
                    style={{ textDecoration: 'none' }}
                >
                    + Signaler un incident
                </Link>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Code</th>
                            <th>Date</th>
                            <th>Type</th>
                            <th>Référence</th>
                            <th>Action statut</th>
                            <th>Pièces jointes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {incidents.map((inc) => (
                            <tr key={inc.id}>
                                <td style={{ fontWeight: '600' }}>{inc.code_incident}</td>
                                <td>{inc.created_at ? new Date(inc.created_at).toLocaleString() : '-'}</td>
                                <td>{TYPE_LABELS[inc.type_incident] || inc.type_incident}</td>
                                <td>{refLabel(inc)}</td>
                                <td>{ACTION_LABELS[inc.action_appliquee] || inc.action_appliquee}</td>
                                <td>{inc.attachments?.length || 0}</td>
                            </tr>
                        ))}
                        {incidents.length === 0 && (
                            <tr>
                                <td colSpan="6" style={{ textAlign: 'center', padding: '2rem' }}>
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
