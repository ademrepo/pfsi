import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../api';

const ClientForm = () => {
    const { id } = useParams();
    const isEdit = Boolean(id);
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        type_client: 'particulier',
        nom: '',
        prenom: '',
        telephone: '',
        email: '',
        adresse: '',
        ville: '',
        pays: ''
    });

    const [loading, setLoading] = useState(false);
    const [fetching, setFetching] = useState(isEdit);

    useEffect(() => {
        const fetchClient = async () => {
            if (!isEdit) return;
            try {
                const res = await api.get(`/clients/${id}/`);
                const c = res.data;
                setFormData({
                    type_client: c.type_client || 'particulier',
                    nom: c.nom || '',
                    prenom: c.prenom || '',
                    telephone: c.telephone || '',
                    email: c.email || '',
                    adresse: c.adresse || '',
                    ville: c.ville || '',
                    pays: c.pays || ''
                });
            } catch (err) {
                console.error(err);
                alert("Impossible de charger le client");
            } finally {
                setFetching(false);
            }
        };
        fetchClient();
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
                await api.put(`/clients/${id}/`, formData);
            } else {
                await api.post('/clients/', formData);
            }
            navigate('/clients');
        } catch (err) {
            console.error(err);
            const msg = err.response?.data?.detail || "Erreur lors de l'enregistrement du client";
            alert(msg);
        } finally {
            setLoading(false);
        }
    };

    if (fetching) return <div className="page-container">Chargement...</div>;

    return (
        <div className="page-container">
            <h1>{isEdit ? 'Modifier le client' : 'Nouveau client'}</h1>
            <div className="form-card" style={{ maxWidth: '900px' }}>
                <form onSubmit={handleSubmit}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>Type</label>
                            <select name="type_client" value={formData.type_client} onChange={handleChange} required>
                                <option value="particulier">Particulier</option>
                                <option value="entreprise">Entreprise</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Nom</label>
                            <input name="nom" value={formData.nom} onChange={handleChange} required />
                        </div>

                        <div className="form-group">
                            <label>Prénom</label>
                            <input name="prenom" value={formData.prenom} onChange={handleChange} />
                        </div>

                        <div className="form-group">
                            <label>Téléphone</label>
                            <input name="telephone" value={formData.telephone} onChange={handleChange} />
                        </div>

                        <div className="form-group">
                            <label>Email</label>
                            <input type="email" name="email" value={formData.email} onChange={handleChange} />
                        </div>

                        <div className="form-group">
                            <label>Pays</label>
                            <input name="pays" value={formData.pays} onChange={handleChange} />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Adresse</label>
                        <textarea name="adresse" value={formData.adresse} onChange={handleChange} rows="2" />
                    </div>

                    <div className="form-group">
                        <label>Ville</label>
                        <input name="ville" value={formData.ville} onChange={handleChange} />
                    </div>

                    <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
                        <button type="submit" disabled={loading}>
                            {loading ? 'Enregistrement...' : isEdit ? 'Mettre à jour' : 'Créer le client'}
                        </button>
                        <button type="button" className="secondary" onClick={() => navigate('/clients')}>
                            Annuler
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ClientForm;

