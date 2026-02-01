import React, { useState, useEffect } from 'react';
import api from '../../api';
import { useNavigate, useLocation } from 'react-router-dom';

const PaymentForm = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const initialInvoiceId = queryParams.get('facture_id');

    const [clients, setClients] = useState([]);
    const [invoices, setInvoices] = useState([]);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        client: '',
        facture: initialInvoiceId || '',
        montant: '',
        date_paiement: new Date().toISOString().split('T')[0],
        mode_paiement: 'Espèces',
        statut: 'Validé'
    });

    useEffect(() => {
        fetchClients();
    }, []);

    useEffect(() => {
        if (formData.client) {
            fetchInvoices(formData.client);
        } else {
            setInvoices([]);
        }
    }, [formData.client]);

    const fetchClients = async () => {
        try {
            const res = await api.get('/clients/');
            setClients(res.data);
            if (initialInvoiceId) {
                const facRes = await api.get(`/factures/${initialInvoiceId}/`);
                setFormData(prev => ({
                    ...prev,
                    client: facRes.data.client,
                    facture: facRes.data.id,
                    montant: facRes.data.reste_a_payer
                }));
            }
        } catch (err) {
            console.error(err);
        }
    };

    const fetchInvoices = async (clientId) => {
        try {
            const res = await api.get(`/factures/?client_id=${clientId}`);
            const data = Array.isArray(res.data) ? res.data : res.data.results || [];
            setInvoices(data.filter(f => f.statut !== 'Payée' && f.statut !== 'Annulée'));
        } catch (err) {
            console.error(err);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));

        if (name === 'facture' && value) {
            const selectedFac = invoices.find(f => f.id === parseInt(value, 10));
            if (selectedFac) {
                setFormData(prev => ({
                    ...prev,
                    montant: selectedFac.reste_a_payer,
                    client: selectedFac.client
                }));
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!formData.facture) {
            alert('Vous devez sélectionner une facture à régler.');
            return;
        }

        setLoading(true);
        try {
            const payload = {
                facture: formData.facture,
                date_paiement: formData.date_paiement,
                mode_paiement: formData.mode_paiement,
                montant: formData.montant,
                statut: formData.statut
            };
            await api.post('/paiements/', payload);
            navigate('/paiements');
        } catch (err) {
            console.error(err);
            alert("Erreur lors de l'enregistrement du paiement");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container">
            <h1>Enregistrer un Paiement</h1>
            <div className="form-card" style={{ maxWidth: '600px' }}>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>CLIENT</label>
                        <select
                            name="client"
                            value={formData.client}
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
                            <option value="">-- Choisir un client --</option>
                            {clients.map(c => <option key={c.id} value={c.id}>{c.nom} {c.prenom}</option>)}
                        </select>
                    </div>

                    <div className="form-group">
                        <label>FACTURE À RÉGLER</label>
                        <select
                            name="facture"
                            value={formData.facture}
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
                            <option value="">Paiement Libre (Acompte / Solde)</option>
                            {invoices.map(f => (
                                <option key={f.id} value={f.id}>
                                    {f.numero_facture} - Reste à payer: {f.reste_a_payer} €
                                </option>
                            ))}
                        </select>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label>Date du paiement</label>
                            <input type="date" name="date_paiement" value={formData.date_paiement} onChange={handleChange} required />
                        </div>
                        <div className="form-group">
                            <label>Montant (€)</label>
                            <input type="number" step="0.01" name="montant" value={formData.montant} onChange={handleChange} required />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Mode de Paiement</label>
                        <select name="mode_paiement" value={formData.mode_paiement} onChange={handleChange} required>
                            <option value="Espèces">Espèces</option>
                            <option value="Chèque">Chèque</option>
                            <option value="Virement">Virement</option>
                            <option value="Carte Bancaire">Carte Bancaire</option>
                        </select>
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
                            {loading ? 'Enregistrement...' : 'Enregistrer les modifications'}
                        </button>
                        <button
                            type="button"
                            className="secondary"
                            onClick={() => navigate('/paiements')}
                            style={{ borderRadius: '25px', padding: '0.75rem 1.5rem', cursor: 'pointer' }}
                        >
                            Annuler
                        </button>
                    </div>
                </form>
            </div>

            <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#fffbeb', border: '1px solid #fef3c7', borderRadius: '8px', color: '#92400e' }}>
                <strong>Note :</strong> L'enregistrement de ce paiement diminuera automatiquement le solde débiteur du client.
            </div>
        </div>
    );
};

export default PaymentForm;
