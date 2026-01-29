import React, { useEffect, useMemo, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import api from '../../api';

const INCIDENT_TYPES = [
    { value: 'RETARD', label: 'Retard' },
    { value: 'PERTE', label: 'Perte' },
    { value: 'ENDOMMAGEMENT', label: 'Endommagement' },
    { value: 'PROBLEME_TECHNIQUE', label: 'Problème technique' },
    { value: 'AUTRE', label: 'Autre' },
];

const IncidentForm = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const query = useMemo(() => new URLSearchParams(location.search), [location.search]);

    const prefillExpeditionId = query.get('expedition_id') || '';
    const prefillTourneeId = query.get('tournee_id') || '';

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const [expeditions, setExpeditions] = useState([]);
    const [tournees, setTournees] = useState([]);

    const [targetType, setTargetType] = useState(prefillExpeditionId ? 'EXPEDITION' : prefillTourneeId ? 'TOURNEE' : 'EXPEDITION');
    const [expeditionId, setExpeditionId] = useState(prefillExpeditionId);
    const [tourneeId, setTourneeId] = useState(prefillTourneeId);
    const [typeIncident, setTypeIncident] = useState('RETARD');
    const [commentaire, setCommentaire] = useState('');
    const [notifyDirection, setNotifyDirection] = useState(true);
    const [notifyClient, setNotifyClient] = useState(false);
    const [files, setFiles] = useState([]);

    useEffect(() => {
        fetchRefs();
    }, []);

    useEffect(() => {
        if (targetType === 'EXPEDITION') {
            setTourneeId('');
        } else {
            setExpeditionId('');
            setNotifyClient(false);
        }
    }, [targetType]);

    const fetchRefs = async () => {
        try {
            const [expRes, trnRes] = await Promise.all([
                api.get('/expeditions/'),
                api.get('/tournees/'),
            ]);
            setExpeditions(expRes.data);
            setTournees(trnRes.data);
        } catch (e) {
            setError("Impossible de charger les expéditions / tournées.");
        }
    };

    const selectedExpedition = expeditions.find((e) => String(e.id) === String(expeditionId));
    const selectedTournee = tournees.find((t) => String(t.id) === String(tourneeId));

    const submit = async (e) => {
        e.preventDefault();
        setError(null);

        if (targetType === 'EXPEDITION' && !expeditionId) {
            setError("Veuillez sélectionner une expédition.");
            return;
        }
        if (targetType === 'TOURNEE' && !tourneeId) {
            setError("Veuillez sélectionner une tournée.");
            return;
        }

        setLoading(true);
        try {
            const formData = new FormData();
            formData.append('type_incident', typeIncident);
            formData.append('commentaire', commentaire || '');
            formData.append('notify_direction', notifyDirection ? 'true' : 'false');
            formData.append('notify_client', notifyClient ? 'true' : 'false');

            if (targetType === 'EXPEDITION') {
                formData.append('expedition', expeditionId);
            } else {
                formData.append('tournee', tourneeId);
            }

            for (const f of files) {
                formData.append('files', f);
            }

            await api.post('/incidents/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            navigate('/incidents');
        } catch (err) {
            const msg = err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || "Erreur lors de l'enregistrement de l'incident.";
            setError(typeof msg === 'string' ? msg : "Erreur lors de l'enregistrement de l'incident.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Signaler un incident</h1>
                <Link to="/incidents" className="btn-primary" style={{ textDecoration: 'none', background: 'var(--bg-main)', color: 'var(--text-main)', border: '1px solid var(--border)' }}>
                    Historique
                </Link>
            </div>

            {error && <div className="error" style={{ marginBottom: '1rem' }}>{error}</div>}

            <div className="table-container" style={{ padding: '1.5rem' }}>
                <form onSubmit={submit}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>Concerne</label>
                            <select value={targetType} onChange={(e) => setTargetType(e.target.value)}>
                                <option value="EXPEDITION">Expédition</option>
                                <option value="TOURNEE">Tournée</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Type d'incident</label>
                            <select value={typeIncident} onChange={(e) => setTypeIncident(e.target.value)}>
                                {INCIDENT_TYPES.map((t) => (
                                    <option key={t.value} value={t.value}>{t.label}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {targetType === 'EXPEDITION' ? (
                        <div className="form-group">
                            <label>Expédition concernée</label>
                            <select value={expeditionId} onChange={(e) => setExpeditionId(e.target.value)}>
                                <option value="">-- Sélectionner --</option>
                                {expeditions.map((e) => (
                                    <option key={e.id} value={e.id}>
                                        {e.code_expedition} {e.client_details ? `- ${e.client_details.nom} ${e.client_details.prenom || ''}` : ''}
                                    </option>
                                ))}
                            </select>
                        </div>
                    ) : (
                        <div className="form-group">
                            <label>Tournée concernée</label>
                            <select value={tourneeId} onChange={(e) => setTourneeId(e.target.value)}>
                                <option value="">-- Sélectionner --</option>
                                {tournees.map((t) => (
                                    <option key={t.id} value={t.id}>
                                        {t.code_tournee} - {t.date_tournee ? new Date(t.date_tournee).toLocaleDateString() : ''}
                                    </option>
                                ))}
                            </select>
                            {selectedTournee && (
                                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                                    {selectedTournee.expeditions_count != null ? `${selectedTournee.expeditions_count} expéditions` : ''}
                                </div>
                            )}
                        </div>
                    )}

                    <div className="form-group">
                        <label>Commentaires</label>
                        <textarea value={commentaire} onChange={(e) => setCommentaire(e.target.value)} rows="4" placeholder="Décrivez l'incident..." />
                    </div>

                    <div className="form-group">
                        <label>Alertes</label>
                        <div className="option-grid">
                            <div className="option-tile">
                                <input
                                    type="checkbox"
                                    checked={notifyDirection}
                                    onChange={(e) => setNotifyDirection(e.target.checked)}
                                    style={{ marginTop: '0.15rem' }}
                                />
                                <div>
                                    <div style={{ fontWeight: 700 }}>Direction</div>
                                    <div className="meta">Crée une alerte interne pour suivi et escalade.</div>
                                </div>
                            </div>
                            <div className={`option-tile ${targetType !== 'EXPEDITION' ? 'disabled' : ''}`}>
                                <input
                                    type="checkbox"
                                    checked={notifyClient}
                                    disabled={targetType !== 'EXPEDITION'}
                                    onChange={(e) => setNotifyClient(e.target.checked)}
                                    style={{ marginTop: '0.15rem' }}
                                />
                                <div>
                                    <div style={{ fontWeight: 700 }}>Client</div>
                                    <div className="meta">Disponible uniquement si l’incident est lié à une expédition.</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Documents / Photos (optionnel)</label>
                        <input type="file" multiple onChange={(e) => setFiles(Array.from(e.target.files || []))} />
                        {files.length > 0 && (
                            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                                {files.length} fichier(s) sélectionné(s)
                            </div>
                        )}
                    </div>

                    <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
                        <button type="submit" disabled={loading}>
                            {loading ? 'Enregistrement...' : 'Créer l’incident'}
                        </button>
                        <button type="button" className="secondary" onClick={() => navigate(-1)}>
                            Annuler
                        </button>
                    </div>

                    <div style={{ marginTop: '1rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                        La création d’un incident met automatiquement à jour le statut (expédition: échec de livraison / tournée: annulée) et ajoute une trace de suivi.
                    </div>
                </form>
            </div>
        </div>
    );
};

export default IncidentForm;
