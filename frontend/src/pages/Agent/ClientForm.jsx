import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../api';
import PageHeader from '../../components/PageHeader';
import { ArrowLeft } from 'lucide-react';

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
            <button
                onClick={() => navigate('/clients')}
                style={{
                    background: 'transparent',
                    border: 'none',
                    color: 'var(--text-muted)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    marginBottom: '1rem',
                    cursor: 'pointer',
                    fontSize: '0.875rem',
                    padding: '0.5rem 0'
                }}
            >
                <ArrowLeft size={18} />
                Retour aux clients
            </button>

            <PageHeader
                title={isEdit ? 'Modifier le client' : 'Nouveau client'}
                subtitle={isEdit ? 'Modifiez les informations du client' : 'Créez un nouveau client dans la base de données'}
            />

            <div className="form-card" style={{ maxWidth: '900px' }}>
                <form onSubmit={handleSubmit}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>TYPE DE CLIENT</label>
                            <select
                                name="type_client"
                                value={formData.type_client}
                                onChange={handleChange}
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
                                <option value="particulier">Particulier</option>
                                <option value="entreprise">Entreprise</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Nom *</label>
                            <input name="nom" value={formData.nom} onChange={handleChange} placeholder="Nom du client" required />
                        </div>

                        <div className="form-group">
                            <label>Prénom</label>
                            <input name="prenom" value={formData.prenom} onChange={handleChange} placeholder="Prénom du client" />
                        </div>

                        <div className="form-group">
                            <label>Téléphone</label>
                            <input name="telephone" value={formData.telephone} onChange={handleChange} placeholder="+33 6 12 34 56 78" />
                        </div>

                        <div className="form-group">
                            <label>Email</label>
                            <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="client@exemple.fr" />
                        </div>

                        <div className="form-group">
                            <label>Ville</label>
                            <input name="ville" value={formData.ville} onChange={handleChange} placeholder="Paris" />
                        </div>

                        <div className="form-group">
                            <label>Pays</label>
                            <input name="pays" value={formData.pays} onChange={handleChange} placeholder="France" />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Adresse complète</label>
                        <textarea name="adresse" value={formData.adresse} onChange={handleChange} rows="3" placeholder="123 Rue de la République, 75001 Paris" />
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
                            {loading ? 'Enregistrement...' : isEdit ? 'Enregistrer les modifications' : 'Créer le client'}
                        </button>
                        <button
                            type="button"
                            className="secondary"
                            onClick={() => navigate('/clients')}
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

export default ClientForm;
