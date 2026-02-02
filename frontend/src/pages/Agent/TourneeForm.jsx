import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../api';

const TourneeForm = () => {
    const { id } = useParams();
    const isEdit = Boolean(id);
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        chauffeur: '',
        vehicule: '',
        date_tournee: new Date().toISOString().split('T')[0],
        points_passage: '',
        statut: 'Préparée',
        kilometrage_depart: '',
        kilometrage_retour: '',
        duree_minutes: '',
        consommation_litres: ''
    });

    const [selectedExpeditions, setSelectedExpeditions] = useState([]);
    const [availableExpeditions, setAvailableExpeditions] = useState([]);
    const [data, setData] = useState({ chauffeurs: [], vehicules: [] });
    const [loading, setLoading] = useState(false);
    const [fetching, setFetching] = useState(isEdit);

    const isTerminee = formData.statut === 'Terminée';
    const kmDepartFilled = formData.kilometrage_depart !== '' && formData.kilometrage_depart !== null;
    const kmRetourFilled = formData.kilometrage_retour !== '' && formData.kilometrage_retour !== null;
    const computedDistance =
        kmDepartFilled && kmRetourFilled
            ? Math.max(0, Number(formData.kilometrage_retour) - Number(formData.kilometrage_depart))
            : '';

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [chauRes, vehRes, expRes] = await Promise.all([
                    api.get('/chauffeurs/'),
                    api.get('/vehicules/'),
                    api.get('/expeditions/?status=Enregistré')
                ]);

                setData({ chauffeurs: chauRes.data, vehicules: vehRes.data });
                setAvailableExpeditions((expRes.data || []).filter(e => !e.est_facturee));

                if (isEdit) {
                    const tourneeRes = await api.get(`/tournees/${id}/`);
                    const t = tourneeRes.data;

                    setFormData({
                        chauffeur: t.chauffeur || '',
                        vehicule: t.vehicule || '',
                        date_tournee: t.date_tournee || '',
                        points_passage: t.points_passage || '',
                        statut: t.statut || 'Préparée',
                        kilometrage_depart: t.kilometrage_depart || '',
                        kilometrage_retour: t.kilometrage_retour || '',
                        duree_minutes: t.duree_minutes || '',
                        consommation_litres: t.consommation_litres || ''
                    });

                    const linked = Array.isArray(t.expeditions) ? t.expeditions : [];
                    setSelectedExpeditions(linked.map(e => e.id));

                     
                    setAvailableExpeditions(prev => {
                        const existingIds = new Set(prev.map(e => e.id));
                        const missing = linked.filter(e => !existingIds.has(e.id));
                        return [...prev, ...missing];
                    });
                }
            } catch (err) {
                console.error(err);
            } finally {
                setFetching(false);
            }
        };

        fetchData();
    }, [id, isEdit]);

    const handleExpeditionToggle = (expId) => {
        setSelectedExpeditions(prev =>
            prev.includes(expId) ? prev.filter(x => x !== expId) : [...prev, expId]
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            if (isTerminee) {
                 
                const kd = kmDepartFilled ? Number(formData.kilometrage_depart) : null;
                const kr = kmRetourFilled ? Number(formData.kilometrage_retour) : null;

                if ((kd === null) !== (kr === null)) {
                    alert("Renseigne le kilométrage de départ ET de retour.");
                    return;
                }
                if (kd !== null && kr !== null && kr < kd) {
                    alert("Le kilométrage de retour doit être supérieur ou égal au kilométrage de départ.");
                    return;
                }
            }

            const payload = { ...formData, expedition_ids: selectedExpeditions };
             
            delete payload.distance_km;
            if (payload.duree_minutes === '') delete payload.duree_minutes;

             
            if (!isTerminee) {
                delete payload.kilometrage_depart;
                delete payload.kilometrage_retour;
                delete payload.duree_minutes;
                delete payload.consommation_litres;
            }

            if (isEdit) {
                await api.put(`/tournees/${id}/`, payload);
            } else {
                await api.post('/tournees/', payload);
            }

            navigate('/tournees');
        } catch (err) {
            console.error(err);
            const data = err.response?.data;
            let msg = "Erreur lors de l'enregistrement de la tournée";
            if (typeof data === 'string' && data.trim()) {
                msg = data;
            } else if (data?.detail) {
                msg = data.detail;
            } else if (data && typeof data === 'object') {
                 
                const parts = [];
                for (const [k, v] of Object.entries(data)) {
                    if (Array.isArray(v)) {
                        parts.push(`${k}: ${v.join(' ')}`);
                    } else if (typeof v === 'string') {
                        parts.push(`${k}: ${v}`);
                    } else if (v && typeof v === 'object') {
                        parts.push(`${k}: ${JSON.stringify(v)}`);
                    }
                }
                if (parts.length) msg = parts.join('\\n');
            }
            alert(msg);
        } finally {
            setLoading(false);
        }
    };

    if (fetching) return <div className="page-container">Chargement...</div>;

    return (
        <div className="page-container">
            <h1>{isEdit ? 'Modifier la Tournée' : 'Nouvelle Tournée'}</h1>
            <div className="form-card" style={{ maxWidth: '900px' }}>
                <form onSubmit={handleSubmit}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>Date de la tournée</label>
                            <input
                                type="date"
                                value={formData.date_tournee}
                                onChange={e => setFormData({ ...formData, date_tournee: e.target.value })}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>STATUT</label>
                            <select
                                value={formData.statut}
                                onChange={e => setFormData({ ...formData, statut: e.target.value })}
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
                                <option value="Préparée">Préparée</option>
                                <option value="En cours">En cours</option>
                                <option value="Terminée">Terminée</option>
                                <option value="Annulée">Annulée</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>CHAUFFEUR</label>
                            <select
                                value={formData.chauffeur}
                                onChange={e => setFormData({ ...formData, chauffeur: e.target.value })}
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
                                <option value="">Choisir un chauffeur</option>
                                {data.chauffeurs.map(c => (
                                    <option key={c.id} value={c.id}>{c.nom} {c.prenom}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>VÉHICULE</label>
                            <select
                                value={formData.vehicule}
                                onChange={e => setFormData({ ...formData, vehicule: e.target.value })}
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
                                <option value="">Choisir un véhicule</option>
                                {data.vehicules.map(v => (
                                    <option key={v.id} value={v.id}>{v.immatriculation} - {v.marque} {v.modele}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <div className="form-group" style={{ marginTop: '1rem' }}>
                        <label>Points de passage (itinéraires, étapes...)</label>
                        <textarea
                            value={formData.points_passage}
                            onChange={e => setFormData({ ...formData, points_passage: e.target.value })}
                            rows="3"
                            placeholder="Entrez les lieux de passage séparés par des virgules ou des retours à la ligne..."
                        />
                    </div>

                    {isTerminee ? (
                        <div className="form-card" style={{ marginTop: '1.5rem', padding: '1rem', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '8px' }}>
                            <h3 style={{ marginBottom: '1rem' }}>Données du trajet</h3>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: '1rem' }}>
                                <div className="form-group">
                                    <label>Kilométrage début</label>
                                    <input
                                        type="number"
                                        value={formData.kilometrage_depart}
                                        onChange={e => setFormData({ ...formData, kilometrage_depart: e.target.value })}
                                        min="0"
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Kilométrage fin</label>
                                    <input
                                        type="number"
                                        value={formData.kilometrage_retour}
                                        onChange={e => setFormData({ ...formData, kilometrage_retour: e.target.value })}
                                        min="0"
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Distance calculée (km)</label>
                                    <input type="text" value={computedDistance !== '' ? computedDistance : ''} readOnly />
                                </div>
                                <div className="form-group">
                                    <label>Durée (minutes)</label>
                                    <input
                                        type="number"
                                        value={formData.duree_minutes}
                                        onChange={e => setFormData({ ...formData, duree_minutes: e.target.value })}
                                        min="0"
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Consommation (litres) *</label>
                                    <input
                                        type="number"
                                        step="0.1"
                                        value={formData.consommation_litres}
                                        onChange={e => setFormData({ ...formData, consommation_litres: e.target.value })}
                                        min="0"
                                        required
                                    />
                                </div>
                            </div>
                            <p style={{ fontSize: '0.85rem', color: '#475569', marginTop: '0.5rem' }}>
                                Lorsque tu enregistres une tournée en "Terminée", les expéditions liées seront automatiquement marquées "Livré".
                            </p>
                        </div>
                    ) : (
                        <div style={{ marginTop: '1.5rem', padding: '1rem', background: '#fffbeb', border: '1px solid #fef3c7', borderRadius: '8px', color: '#92400e' }}>
                            Les données du trajet (km/durée/consommation) ne peuvent être saisies qu'une fois la tournée passée à <strong>Terminée</strong>.
                        </div>
                    )}

                    <h3 style={{ margin: '2rem 0 1rem 0' }}>Expéditions à charger</h3>
                    <div className="table-container" style={{ maxHeight: '300px', overflowY: 'auto' }}>
                        <table>
                            <thead>
                                <tr>
                                    <th style={{ width: '40px' }}>Select</th>
                                    <th>Code</th>
                                    <th>Client</th>
                                    <th>Destination</th>
                                    <th>Poids</th>
                                </tr>
                            </thead>
                            <tbody>
                                {availableExpeditions.map(exp => (
                                    <tr key={exp.id}>
                                        <td>
                                            <input
                                                type="checkbox"
                                                checked={selectedExpeditions.includes(exp.id)}
                                                onChange={() => handleExpeditionToggle(exp.id)}
                                            />
                                        </td>
                                        <td>{exp.code_expedition}</td>
                                        <td>{exp.client_details?.nom}</td>
                                        <td>{exp.destination_details?.ville}</td>
                                        <td>{exp.poids_kg} kg</td>
                                    </tr>
                                ))}
                                {availableExpeditions.length === 0 && (
                                    <tr>
                                        <td colSpan="5" style={{ textAlign: 'center', padding: '1rem' }}>
                                            Aucune expédition en attente ("Enregistré").
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
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
                            {loading ? 'Enregistrement...' : isEdit ? 'Enregistrer les modifications' : 'Créer la tournée'}
                        </button>
                        {isEdit && (
                            <button
                                type="button"
                                className="secondary"
                                onClick={() => navigate(`/incidents/nouveau?tournee_id=${id}`)}
                                style={{ borderRadius: '25px', padding: '0.75rem 1.5rem', cursor: 'pointer' }}
                            >
                                Signaler un incident
                            </button>
                        )}
                        <button
                            type="button"
                            className="secondary"
                            onClick={() => navigate('/tournees')}
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

export default TourneeForm;
