import React, { useState, useEffect } from 'react';
import api from '../../api';
import { useNavigate, useParams } from 'react-router-dom';

const ExpeditionForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const isEdit = !!id;

    const [formData, setFormData] = useState({
        client: '',
        type_service: '',
        destination: '',
        poids_kg: '',
        volume_m3: '',
        description_colis: '',
        adresse_livraison: '',
        nom_destinataire: '',
        telephone_destinataire: '',
        statut: 'Enregistré'
    });

    const [loading, setLoading] = useState(false);
    const [fetching, setFetching] = useState(isEdit);
    const [initialData, setInitialData] = useState({
        clients: [],
        destinations: [],
        services: []
    });

    const expeditionStatuses = [
        'Enregistré', 'Validé', 'En transit', 'En centre de tri',
        'En cours de livraison', 'Livré', 'Échec de livraison'
    ];

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [clientsRes, destRes, servicesRes] = await Promise.all([
                    api.get('/clients/'),
                    api.get('/destinations/'),
                    api.get('/types-service/')
                ]);
                setInitialData({
                    clients: clientsRes.data,
                    destinations: destRes.data,
                    services: servicesRes.data
                });

                if (isEdit) {
                    const expRes = await api.get(`/expeditions/${id}/`);
                    const exp = expRes.data;
                    setFormData({
                        client: exp.client || '',
                        type_service: exp.type_service || '',
                        destination: exp.destination || '',
                        poids_kg: exp.poids_kg || '',
                        volume_m3: exp.volume_m3 || '',
                        description_colis: exp.description_colis || '',
                        adresse_livraison: exp.adresse_livraison || '',
                        nom_destinataire: exp.nom_destinataire || '',
                        telephone_destinataire: exp.telephone_destinataire || '',
                        statut: exp.statut || 'Enregistré'
                    });
                }
            } catch (err) {
                console.error("Erreur chargement données", err);
            } finally {
                setFetching(false);
            }
        };
        fetchData();
    }, [id, isEdit]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            if (isEdit) {
                await api.put(`/expeditions/${id}/`, formData);
            } else {
                await api.post('/expeditions/', formData);
            }
            navigate('/expeditions');
        } catch (err) {
            console.error(err);
            const errorMsg = err.response?.data?.non_field_errors?.[0] || err.response?.data?.[0] || "Erreur lors de l'enregistrement";
            alert(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    if (fetching) return <div className="page-container">Chargement...</div>;

    return (
        <div className="page-container">
            <h1>{isEdit ? 'Modifier l\'expédition' : 'Nouvelle Expédition'}</h1>
            <div className="form-card">
                <form onSubmit={handleSubmit}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>Client</label>
                            <select name="client" value={formData.client} onChange={handleChange} required>
                                <option value="">Sélectionner un client</option>
                                {initialData.clients.map(c => (
                                    <option key={c.id} value={c.id}>{c.nom} {c.prenom}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Type de Service</label>
                            <select name="type_service" value={formData.type_service} onChange={handleChange} required>
                                <option value="">Sélectionner un service</option>
                                {initialData.services.map(s => (
                                    <option key={s.id} value={s.id}>{s.libelle}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Destination</label>
                            <select name="destination" value={formData.destination} onChange={handleChange} required>
                                <option value="">Sélectionner une destination</option>
                                {initialData.destinations.map(d => (
                                    <option key={d.id} value={d.id}>{d.ville}, {d.pays}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Statut</label>
                            <select name="statut" value={formData.statut} onChange={handleChange} required>
                                {expeditionStatuses.map(s => (
                                    <option key={s} value={s}>{s}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Poids (kg)</label>
                            <input type="number" step="0.01" name="poids_kg" value={formData.poids_kg} onChange={handleChange} required />
                        </div>
                        <div className="form-group">
                            <label>Volume (m³)</label>
                            <input type="number" step="0.01" name="volume_m3" value={formData.volume_m3} onChange={handleChange} required />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Description du colis</label>
                        <textarea name="description_colis" value={formData.description_colis} onChange={handleChange} rows="3" />
                    </div>

                    <h3 style={{ margin: '1.5rem 0 1rem 0' }}>Informations Livraison</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>Nom Destinataire</label>
                            <input type="text" name="nom_destinataire" value={formData.nom_destinataire} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label>Téléphone Destinataire</label>
                            <input type="text" name="telephone_destinataire" value={formData.telephone_destinataire} onChange={handleChange} />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Adresse de Livraison</label>
                        <textarea name="adresse_livraison" value={formData.adresse_livraison} onChange={handleChange} rows="2" />
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
                            {loading ? 'Enregistrement...' : isEdit ? 'Enregistrer les modifications' : 'Créer l\'expédition'}
                        </button>
                        {isEdit && (
                            <button
                                type="button"
                                className="secondary"
                                onClick={() => navigate(`/incidents/nouveau?expedition_id=${id}`)}
                                style={{ borderRadius: '25px', padding: '0.75rem 1.5rem', cursor: 'pointer' }}
                            >
                                Signaler un incident
                            </button>
                        )}
                        <button
                            type="button"
                            className="secondary"
                            onClick={() => navigate('/expeditions')}
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

export default ExpeditionForm;
