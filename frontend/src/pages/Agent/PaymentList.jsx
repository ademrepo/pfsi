import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';

const PaymentList = () => {
    const [payments, setPayments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [clients, setClients] = useState([]);
    const [filters, setFilters] = useState({ client_id: '' });

    useEffect(() => {
        fetchClients();
        fetchPayments();
    }, []);

    const fetchClients = async () => {
        try {
            const res = await api.get('/clients/');
            setClients(res.data);
        } catch (err) { console.error(err); }
    };

    const fetchPayments = async (currentFilters = filters) => {
        setLoading(true);
        try {
            const params = new URLSearchParams();
            if (currentFilters.client_id) params.append('client_id', currentFilters.client_id);
            const res = await api.get(`/paiements/?${params.toString()}`);
            setPayments(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        const newFilters = { ...filters, [name]: value };
        setFilters(newFilters);
        fetchPayments(newFilters);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Supprimer ce paiement ? Cela augmentera à nouveau le solde débiteur du client.')) {
            try {
                await api.delete(`/paiements/${id}/`);
                fetchPayments();
            } catch (err) {
                alert("Erreur lors de la suppression");
            }
        }
    };

    const handlePrintReceipt = (payment) => {
        // Logic for printing a simple receipt could go here or in a separate detail view
        // For now, let's just alert or open print
        window.print();
    };

    if (loading && payments.length === 0) return <div className="page-container">Chargement...</div>;

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Journal des Paiements</h1>
                <Link to="/paiements/nouveau" className="btn-primary" style={{ textDecoration: 'none' }}>
                    + Enregistrer un Paiement
                </Link>
            </div>

            <div className="form-card" style={{ marginBottom: '2rem', display: 'flex', gap: '1rem', alignItems: 'flex-end', padding: '1.5rem' }}>
                <div className="form-group" style={{ marginBottom: 0, flex: 1 }}>
                    <label>Filtrer par Client</label>
                    <select name="client_id" value={filters.client_id} onChange={handleFilterChange}>
                        <option value="">Tous les clients</option>
                        {clients.map(c => <option key={c.id} value={c.id}>{c.nom} {c.prenom}</option>)}
                    </select>
                </div>
                <button className="secondary" onClick={() => { setFilters({ client_id: '' }); fetchPayments({ client_id: '' }); }}>Réinitialiser</button>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Client</th>
                            <th>Facture Liée</th>
                            <th>Mode</th>
                            <th>Montant</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {payments.map(p => (
                            <tr key={p.id}>
                                <td>{new Date(p.date_paiement).toLocaleDateString()}</td>
                                <td style={{ fontWeight: '600' }}>{p.client_details?.nom} {p.client_details?.prenom}</td>
                                <td>{p.facture_numero || 'Paiement Libre'}</td>
                                <td>{p.mode_paiement}</td>
                                <td style={{ fontWeight: '700', color: '#059669' }}>{p.montant} €</td>
                                <td className="actions">
                                    <button
                                        className="btn-primary"
                                        onClick={() => handleDelete(p.id)}
                                        style={{ padding: '0.4rem 0.8rem', background: '#fee2e2', color: '#b91c1c' }}
                                    >
                                        Supprimer
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {payments.length === 0 && !loading && (
                            <tr><td colSpan="6" style={{ textAlign: 'center', padding: '2rem' }}>Aucun paiement trouvé.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PaymentList;
