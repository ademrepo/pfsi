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
            // Si on vient d'une facture, on essaie de trouver le client lié
            if (initialInvoiceId) {
                const facRes = await api.get(`/factures/${initialInvoiceId}/`);
                setFormData(prev => ({ ...prev, client: facRes.data.client, montant: facRes.data.reste_a_payer }));
            }
        } catch (err) { console.error(err); }
    };

    const fetchInvoices = async (clientId) => {
        try {
            const res = await api.get(`/factures/?client_id=${clientId}&statut=Émise,Partiellement+Payée`);
            // Note: le filtrage multi-statut dépend de l'implémentation backend
            // Pour être sûr on filtre côté client si besoin
            setInvoices(res.data.filter(f => f.statut !== 'Payée' && f.statut !== 'Annulée'));
        } catch (err) { console.error(err); }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));

        // Si on change de facture, on peut pré-remplir le montant avec le reste à payer
        if (name === 'facture' && value) {
            const selectedFac = invoices.find(f => f.id === parseInt(value));
            if (selectedFac) {
                setFormData(prev => ({ ...prev, montant: selectedFac.reste_a_payer }));
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await api.post('/paiements/', formData);
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
                        <label>Client</label>
                        <select name="client" value={formData.client} onChange={handleChange} required>
                            <option value="">-- Choisir un client --</option>
                            {clients.map(c => <option key={c.id} value={c.id}>{c.nom} {c.prenom}</option>)}
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Facture Liée (Optionnel)</label>
                        <select name="facture" value={formData.facture} onChange={handleChange}>
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

                    <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
                        <button type="submit" disabled={loading}>
                            {loading ? 'Enregistrement...' : 'Enregistrer le paiement'}
                        </button>
                        <button type="button" className="secondary" onClick={() => navigate('/paiements')}>
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
