import React, { useState, useEffect } from 'react';
import api from '../../api';
import { useNavigate } from 'react-router-dom';

const InvoiceForm = () => {
    const navigate = useNavigate();
    const [clients, setClients] = useState([]);
    const [selectedClient, setSelectedClient] = useState('');
    const [availableExpeditions, setAvailableExpeditions] = useState([]);
    const [selectedExpeditions, setSelectedExpeditions] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchClients = async () => {
            try {
                const res = await api.get('/clients/');
                setClients(res.data);
            } catch (err) { console.error(err); }
        };
        fetchClients();
    }, []);

    useEffect(() => {
        if (selectedClient) {
            fetchExpeditions();
        } else {
            setAvailableExpeditions([]);
            setSelectedExpeditions([]);
        }
    }, [selectedClient]);

    const fetchExpeditions = async () => {
        try {
             
            const res = await api.get(`/expeditions/?client_id=${selectedClient}`);
            setAvailableExpeditions(res.data.filter(e => !e.est_facturee));
        } catch (err) { console.error(err); }
    };

    const handleToggle = (id) => {
        setSelectedExpeditions(prev =>
            prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (selectedExpeditions.length === 0) {
            alert("Veuillez sélectionner au moins une expédition");
            return;
        }
        setLoading(true);
        try {
            await api.post('/factures/', {
                client: selectedClient,
                expeditions: selectedExpeditions
            });
            navigate('/factures');
        } catch (err) {
            console.error(err);
            alert("Erreur lors de la création de la facture");
        } finally {
            setLoading(false);
        }
    };

    const totalHT = availableExpeditions
        .filter(e => selectedExpeditions.includes(e.id))
        .reduce((sum, e) => sum + e.montant_total, 0);
    const totalTTC = totalHT * 1.20;  

    return (
        <div className="page-container">
            <h1>Nouvelle Facture</h1>
            <div className="form-card" style={{ maxWidth: '900px' }}>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>SÉLECTIONNER UN CLIENT</label>
                        <select
                            value={selectedClient}
                            onChange={e => setSelectedClient(e.target.value)}
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

                    {selectedClient && (
                        <>
                            <h3 style={{ margin: '1.5rem 0 1rem 0' }}>Expéditions Non Facturées</h3>
                            <div className="table-container" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                                <table>
                                    <thead>
                                        <tr>
                                            <th style={{ width: '40px' }}>Select</th>
                                            <th>Code</th>
                                            <th>Date</th>
                                            <th>Destination</th>
                                            <th>Montant HT</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {availableExpeditions.map(exp => (
                                            <tr key={exp.id}>
                                                <td>
                                                    <input
                                                        type="checkbox"
                                                        checked={selectedExpeditions.includes(exp.id)}
                                                        onChange={() => handleToggle(exp.id)}
                                                    />
                                                </td>
                                                <td>{exp.code_expedition}</td>
                                                <td>{new Date(exp.date_creation).toLocaleDateString()}</td>
                                                <td>{exp.destination_details?.ville}</td>
                                                <td>{exp.montant_total} €</td>
                                            </tr>
                                        ))}
                                        {availableExpeditions.length === 0 && (
                                            <tr><td colSpan="5" style={{ textAlign: 'center', padding: '2rem' }}>Aucune expédition en attente pour ce client.</td></tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>

                            <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span>Sous-total HT :</span>
                                    <span style={{ fontWeight: '600' }}>{totalHT.toFixed(2)} €</span>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span>TVA (20%) :</span>
                                    <span style={{ fontWeight: '600' }}>{(totalHT * 0.20).toFixed(2)} €</span>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.2rem', marginTop: '1rem', borderTop: '2px solid #e2e8f0', paddingTop: '1rem' }}>
                                    <span style={{ fontWeight: '700' }}>Total TTC :</span>
                                    <span style={{ fontWeight: '800', color: 'var(--primary)' }}>{totalTTC.toFixed(2)} €</span>
                                </div>
                            </div>
                        </>
                    )}

                    <div style={{ marginTop: '2.5rem', display: 'flex', gap: '1.25rem' }}>
                        <button
                            type="submit"
                            disabled={loading || selectedExpeditions.length === 0}
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
                            {loading ? 'Création...' : 'Enregistrer les modifications'}
                        </button>
                        <button
                            type="button"
                            className="secondary"
                            onClick={() => navigate('/factures')}
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

export default InvoiceForm;
