import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../api';

const STATUTS = [
    { value: 'EN_COURS', label: 'En cours' },
    { value: 'RESOLUE', label: 'Résolue' },
    { value: 'ANNULEE', label: 'Annulée' },
];

const ReclamationForm = () => {
    const navigate = useNavigate();
    const { id } = useParams();
    const isEdit = Boolean(id);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const [clients, setClients] = useState([]);
    const [expeditions, setExpeditions] = useState([]);
    const [factures, setFactures] = useState([]);
    const [services, setServices] = useState([]);
    const [expSearch, setExpSearch] = useState('');

    const [formData, setFormData] = useState({
        client: '',
        objet: '',
        description: '',
        date_reclamation: '',
        statut: 'EN_COURS',
        expedition_ids: [],
        facture: '',
        type_service: '',
    });

    useEffect(() => {
        fetchRefs();
    }, []);

    useEffect(() => {
        if (isEdit) fetchItem();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [id]);

    const fetchRefs = async () => {
        try {
            const [cRes, eRes, fRes, sRes] = await Promise.all([
                api.get('/clients/'),
                api.get('/expeditions/'),
                api.get('/factures/'),
                api.get('/types-service/'),
            ]);
            setClients(cRes.data);
            setExpeditions(eRes.data);
            setFactures(fRes.data);
            setServices(sRes.data);
        } catch (e) {
            setError("Impossible de charger les référentiels (clients/expéditions/factures/services).");
        }
    };

    const fetchItem = async () => {
        try {
            const res = await api.get(`/reclamations/${id}/`);
            const r = res.data;
            setFormData({
                client: r.client || '',
                objet: r.objet || '',
                description: r.description || '',
                date_reclamation: r.date_reclamation || '',
                statut: r.statut || 'EN_COURS',
                expedition_ids: [],
                facture: r.facture || '',
                type_service: r.type_service || '',
            });
        } catch (e) {
            setError("Impossible de charger la réclamation.");
        }
    };

    const toggleExpedition = (expId) => {
        setFormData((prev) => {
            const exists = prev.expedition_ids.includes(expId);
            const next = exists ? prev.expedition_ids.filter((x) => x !== expId) : [...prev.expedition_ids, expId];
            return { ...prev, expedition_ids: next };
        });
    };

    const filteredExpeditions = expeditions.filter((e) => {
        const q = expSearch.trim().toLowerCase();
        if (!q) return true;
        const code = (e.code_expedition || '').toLowerCase();
        return code.includes(q);
    });

    const submit = async (e) => {
        e.preventDefault();
        setError(null);

        const hasColis = formData.expedition_ids.length > 0;
        const hasFacture = Boolean(formData.facture);
        const hasService = Boolean(formData.type_service);
        if (!hasColis && !hasFacture && !hasService) {
            setError("Veuillez lier la réclamation à au moins un colis, une facture ou un service.");
            return;
        }
        if (!formData.client) {
            setError("Veuillez sélectionner le client concerné.");
            return;
        }

        setLoading(true);
        try {
            const payload = {
                client: formData.client,
                objet: formData.objet,
                description: formData.description,
                date_reclamation: formData.date_reclamation || null,
                statut: formData.statut,
                expedition_ids: formData.expedition_ids,
                facture: formData.facture || null,
                type_service: formData.type_service || null,
            };

            if (isEdit) {
                await api.put(`/reclamations/${id}/`, payload);
            } else {
                await api.post('/reclamations/', payload);
            }

            navigate('/reclamations');
        } catch (err) {
            const msg = err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || "Erreur lors de l'enregistrement.";
            setError(typeof msg === 'string' ? msg : "Erreur lors de l'enregistrement.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>{isEdit ? 'Modifier la réclamation' : 'Nouvelle réclamation'}</h1>
            </div>

            {error && <div className="error" style={{ marginBottom: '1rem' }}>{error}</div>}

            <div className="table-container" style={{ padding: '1.5rem' }}>
                <form onSubmit={submit}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>CLIENT</label>
                            <select
                                value={formData.client}
                                onChange={(e) => setFormData({ ...formData, client: e.target.value })}
                                required
                                style={{
                                    borderRadius: '12px',
                                    appearance: 'none',
                                    backgroundImage: `url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%23CBD5E0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>')`,
                                    backgroundRepeat: 'no-repeat',
                                    backgroundPosition: 'right 12px center',
                                    paddingRight: '35px',
                                    cursor: 'pointer'
                                }}
                            >
                                <option value="">-- Sélectionner --</option>
                                {clients.map((c) => (
                                    <option key={c.id} value={c.id}>
                                        {c.nom} {c.prenom || ''} {c.code_client ? `(${c.code_client})` : ''}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Date</label>
                            <input
                                type="date"
                                value={formData.date_reclamation}
                                onChange={(e) => setFormData({ ...formData, date_reclamation: e.target.value })}
                            />
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>STATUT</label>
                            <select
                                value={formData.statut}
                                onChange={(e) => setFormData({ ...formData, statut: e.target.value })}
                                style={{
                                    borderRadius: '12px',
                                    appearance: 'none',
                                    backgroundImage: `url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%23CBD5E0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>')`,
                                    backgroundRepeat: 'no-repeat',
                                    backgroundPosition: 'right 12px center',
                                    paddingRight: '35px',
                                    cursor: 'pointer'
                                }}
                            >
                                {STATUTS.map((s) => (
                                    <option key={s.value} value={s.value}>{s.label}</option>
                                ))}
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Service (optionnel)</label>
                            <select value={formData.type_service} onChange={(e) => setFormData({ ...formData, type_service: e.target.value })}>
                                <option value="">-- Aucun --</option>
                                {services.map((s) => (
                                    <option key={s.id} value={s.id}>
                                        {s.libelle || s.code || `Service #${s.id}`}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Objet / Nature</label>
                        <input type="text" value={formData.objet} onChange={(e) => setFormData({ ...formData, objet: e.target.value })} />
                    </div>

                    <div className="form-group">
                        <label>Description</label>
                        <textarea rows="4" value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>Facture (optionnel)</label>
                            <select value={formData.facture} onChange={(e) => setFormData({ ...formData, facture: e.target.value })}>
                                <option value="">-- Aucune --</option>
                                {factures.map((f) => (
                                    <option key={f.id} value={f.id}>
                                        {f.numero_facture || `Facture #${f.id}`}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Colis / Expéditions (0..N)</label>
                            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', marginBottom: '0.75rem' }}>
                                <input
                                    type="text"
                                    placeholder="Rechercher par code (ex: EXP-...)"
                                    value={expSearch}
                                    onChange={(e) => setExpSearch(e.target.value)}
                                />
                                <button
                                    type="button"
                                    className="secondary"
                                    onClick={() => setFormData((p) => ({ ...p, expedition_ids: filteredExpeditions.map((x) => x.id) }))}
                                    style={{ whiteSpace: 'nowrap' }}
                                >
                                    Tout
                                </button>
                                <button
                                    type="button"
                                    className="secondary"
                                    onClick={() => setFormData((p) => ({ ...p, expedition_ids: [] }))}
                                    style={{ whiteSpace: 'nowrap' }}
                                >
                                    Aucun
                                </button>
                            </div>
                            <div className="scroll-box">
                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.35rem 1rem' }}>
                                    {filteredExpeditions.map((e) => (
                                        <label
                                            key={e.id}
                                            style={{
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: '0.5rem',
                                                padding: '0.35rem 0.25rem',
                                                borderRadius: 6,
                                            }}
                                        >
                                            <input
                                                type="checkbox"
                                                checked={formData.expedition_ids.includes(e.id)}
                                                onChange={() => toggleExpedition(e.id)}
                                            />
                                            <span style={{ fontSize: '0.9rem' }}>{e.code_expedition}</span>
                                        </label>
                                    ))}
                                </div>
                                {filteredExpeditions.length === 0 && <div style={{ color: 'var(--text-muted)' }}>Aucun résultat.</div>}
                            </div>
                            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                                {formData.expedition_ids.length} colis sélectionné(s)
                            </div>
                        </div>
                    </div>

                    <div style={{ marginTop: '2.5rem', display: 'flex', gap: '1.25rem' }}>
                        <button
                            type="submit"
                            disabled={loading}
                            style={{
                                borderRadius: '25px',
                                padding: '0.75rem 2rem',
                                fontSize: '1rem',
                                fontWeight: '600',
                                background: '#0d9488',
                                color: 'white',
                                border: 'none',
                                cursor: 'pointer',
                                transition: 'all 0.2s'
                            }}
                        >
                            {loading ? 'Enregistrement...' : isEdit ? 'Enregistrer les modifications' : 'Créer la réclamation'}
                        </button>
                        <button
                            type="button"
                            className="secondary"
                            onClick={() => navigate('/reclamations')}
                            style={{ borderRadius: '25px', padding: '0.75rem 1.5rem', cursor: 'pointer' }}
                        >
                            Annuler
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ReclamationForm;
