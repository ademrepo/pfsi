import React, { useState, useEffect } from 'react';
import api from '../../api';
import { useNavigate, useParams } from 'react-router-dom';

const TourneeForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const isEdit = !!id;

    const [formData, setFormData] = useState({
        chauffeur: '',
        vehicule: '',
        date_tournee: new Date().toISOString().split('T')[0],
        points_passage: '',
        statut: 'Préparée'
    });

    const [selectedExpeditions, setSelectedExpeditions] = useState([]);
    const [availableExpeditions, setAvailableExpeditions] = useState([]);
    const [data, setData] = useState({ chauffeurs: [], vehicules: [] });
    const [loading, setLoading] = useState(false);
    const [fetching, setFetching] = useState(isEdit);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [chauRes, vehRes, expRes] = await Promise.all([
                    api.get('/chauffeurs/'),
                    api.get('/vehicules/'),
                    api.get('/expeditions/?status=Enregistré')
                ]);

                setData({ chauffeurs: chauRes.data, vehicules: vehRes.data });
                setAvailableExpeditions(expRes.data);

                if (isEdit) {
                    const tourneeRes = await api.get(`/tournees/${id}/`);
                    const t = tourneeRes.data;
                    setFormData({
                        chauffeur: t.chauffeur || '',
                        vehicule: t.vehicule || '',
                        date_tournee: t.date_tournee || '',
                        points_passage: t.points_passage || '',
                        statut: t.statut || 'Préparée'
                    });
                    // On récupère aussi les expéditions déjà liées à cette tournée
                    const linkedExpRes = await api.get(`/expeditions/?tournee_id=${id}`);
                    setSelectedExpeditions(linkedExpRes.data.map(e => e.id));
                    // Fusionner avec les disponibles pour l'affichage
                    setAvailableExpeditions(prev => {
                        const existingIds = new Set(prev.map(e => e.id));
                        const missing = linkedExpRes.data.filter(e => !existingIds.has(e.id));
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
            prev.includes(expId) ? prev.filter(id => id !== expId) : [...prev, expId]
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            let tourneeId = id;
            if (isEdit) {
                await api.put(`/tournees/${id}/`, formData);
            } else {
                const res = await api.post('/tournees/', formData);
                tourneeId = res.data.id;
            }

            // Mise à jour massive des expéditions
            // Idéalement on ferait un endpoint batch, mais ici on va faire des appels PATCH
            // car le backend n'a pas encore d'action batch_link
            await Promise.all(selectedExpeditions.map(expId =>
                api.patch(`/expeditions/${expId}/`, { tournee: tourneeId, statut: 'Validé' })
            ));

            navigate('/tournees');
        } catch (err) {
            console.error(err);
            alert("Erreur lors de l'enregistrement de la tournée");
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
                            <input type="date" value={formData.date_tournee} onChange={e => setFormData({ ...formData, date_tournee: e.target.value })} required />
                        </div>

                        <div className="form-group">
                            <label>Statut</label>
                            <select value={formData.statut} onChange={e => setFormData({ ...formData, statut: e.target.value })} required>
                                <option value="Préparée">Préparée</option>
                                <option value="En cours">En cours</option>
                                <option value="Terminée">Terminée</option>
                                <option value="Annulée">Annulée</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Chauffeur</label>
                            <select value={formData.chauffeur} onChange={e => setFormData({ ...formData, chauffeur: e.target.value })} required>
                                <option value="">Choisir un chauffeur</option>
                                {data.chauffeurs.map(c => (
                                    <option key={c.id} value={c.id}>{c.nom} {c.prenom}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Véhicule</label>
                            <select value={formData.vehicule} onChange={e => setFormData({ ...formData, vehicule: e.target.value })} required>
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
                                    <tr><td colSpan="5" style={{ textAlign: 'center', padding: '1rem' }}>Aucune expédition en attente ("Enregistré").</td></tr>
                                )}
                            </tbody>
                        </table>
                    </div>

                    <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
                        <button type="submit" disabled={loading}>
                            {loading ? 'Enregistrement...' : isEdit ? 'Mettre à jour' : 'Créer la tournée'}
                        </button>
                        <button type="button" className="secondary" onClick={() => navigate('/tournees')}>
                            Annuler
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default TourneeForm;
