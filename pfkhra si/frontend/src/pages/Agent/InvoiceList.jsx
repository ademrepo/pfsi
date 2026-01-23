import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';

const InvoiceList = () => {
    const [invoices, setInvoices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filters, setFilters] = useState({ client_id: '', statut: '' });
    const [clients, setClients] = useState([]);

    useEffect(() => {
        fetchClients();
        fetchInvoices();
    }, []);

    const fetchClients = async () => {
        try {
            const res = await api.get('/clients/');
            setClients(res.data);
        } catch (err) { console.error(err); }
    };

    const fetchInvoices = async (currentFilters = filters) => {
        setLoading(true);
        try {
            const params = new URLSearchParams();
            if (currentFilters.client_id) params.append('client_id', currentFilters.client_id);
            if (currentFilters.statut) params.append('statut', currentFilters.statut);

            const response = await api.get(`/factures/?${params.toString()}`);
            const data = Array.isArray(response.data)
                ? response.data
                : Array.isArray(response.data.results)
                    ? response.data.results
                    : [];
            setInvoices(data);
        } catch (err) {
            setError('Erreur lors du chargement des factures');
        } finally {
            setLoading(false);
        }
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        const newFilters = { ...filters, [name]: value };
        setFilters(newFilters);
        fetchInvoices(newFilters);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Attention: La suppression d\'une facture annulera ses paiements et mettra à jour le solde client. Continuer ?')) {
            try {
                await api.delete(`/factures/${id}/`);
                fetchInvoices();
            } catch (err) {
                alert("Erreur lors de la suppression");
            }
        }
    };

    if (loading && invoices.length === 0) return <div className="page-container">Chargement...</div>;

    const getStatusClass = (status) => {
        const map = {
            'Brouillon': 'status-Inactif',
            'Émise': 'status-Validé',
            'Partiellement Payée': 'status-En.cours',
            'Payée': 'status-Livré',
            'Annulée': 'status-Inactif'
        };
        return map[status] || '';
    };

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Journal des Factures</h1>
                <Link to="/factures/nouveau" className="btn-primary" style={{ textDecoration: 'none' }}>
                    + Nouvelle Facture
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
                <div className="form-group" style={{ marginBottom: 0, flex: 1 }}>
                    <label>Statut</label>
                    <select name="statut" value={filters.statut} onChange={handleFilterChange}>
                        <option value="">Tous les statuts</option>
                        <option value="Brouillon">Brouillon</option>
                        <option value="Émise">Émise</option>
                        <option value="Partiellement Payée">Partiellement Payée</option>
                        <option value="Payée">Payée</option>
                    </select>
                </div>
                <button className="secondary" onClick={() => { setFilters({ client_id: '', statut: '' }); fetchInvoices({ client_id: '', statut: '' }); }}>Réinitialiser</button>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>N° Facture</th>
                            <th>Date</th>
                            <th>Client</th>
                            <th>Total TTC</th>
                            <th>Reste à Payer</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {invoices.map(f => (
                            <tr key={f.id}>
                                <td style={{ fontWeight: '600' }}>{f.numero_facture}</td>
                                <td>{new Date(f.date_facture).toLocaleDateString()}</td>
                                <td>{f.client_details?.nom} {f.client_details?.prenom}</td>
                                <td style={{ fontWeight: '600' }}>{f.total_ttc} €</td>
                                <td style={{ color: f.reste_a_payer > 0 ? '#b91c1c' : '#059669', fontWeight: '600' }}>
                                    {f.reste_a_payer} €
                                </td>
                                <td>
                                    <span className={`status-badge ${getStatusClass(f.statut)}`}>
                                        {f.statut}
                                    </span>
                                </td>
                                <td className="actions">
                                    <Link to={`/factures/${f.id}`} className="btn-primary" style={{ textDecoration: 'none', padding: '0.4rem 0.8rem', background: '#e2e8f0', color: '#1e293b' }}>
                                        Détails
                                    </Link>
                                    <button
                                        className="btn-primary"
                                        onClick={() => handleDelete(f.id)}
                                        style={{ padding: '0.4rem 0.8rem', background: '#fee2e2', color: '#b91c1c' }}
                                    >
                                        Supprimer
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {invoices.length === 0 && !loading && (
                            <tr><td colSpan="7" style={{ textAlign: 'center', padding: '2rem' }}>Aucune facture trouvée.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default InvoiceList;
