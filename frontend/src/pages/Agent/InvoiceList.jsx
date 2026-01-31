import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';
import { FileSpreadsheet, Plus, Download, Eye, Trash2 } from 'lucide-react';
import PageHeader from '../../components/PageHeader';
import TopBar from '../../components/TopBar';
import StatsGrid from '../../components/StatsGrid';

const InvoiceList = () => {
    const [invoices, setInvoices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filters, setFilters] = useState({ client_id: '', statut: '' });
    const [clients, setClients] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

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
            'Brouillon': 'status-neutral',
            'Émise': 'status-valide',
            'Partiellement Payée': 'status-en-cours',
            'Payée': 'status-livre',
            'Annulée': 'status-retard'
        };
        return map[status] || '';
    };

    const filteredInvoices = invoices.filter(f =>
        f.numero_facture?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        f.client_details?.nom?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const totalRevenue = invoices.reduce((sum, f) => sum + (Number(f.total_ttc) || 0), 0);
    const totalUnpaid = invoices.reduce((sum, f) => sum + (Number(f.reste_a_payer) || 0), 0);

    const stats = [
        {
            label: 'Total Factures',
            value: invoices.length.toLocaleString(),
            icon: FileSpreadsheet
        },
        {
            label: 'Chiffre d\'Affaires',
            value: `${totalRevenue.toFixed(2)} €`,
            badge: <span className="status-badge status-livre">TTC</span>
        },
        {
            label: 'À Encaisser',
            value: `${totalUnpaid.toFixed(2)} €`,
            badge: totalUnpaid > 0 ? <span className="status-badge status-retard">En attente</span> : null
        },
        {
            label: 'Payées',
            value: invoices.filter(f => f.statut === 'Payée').length
        }
    ];

    return (
        <div className="page-container">
            <PageHeader
                title="Journal des Factures"
                subtitle="Gérez vos factures et suivez les paiements"
            />

            <TopBar
                searchValue={searchTerm}
                onSearchChange={setSearchTerm}
                searchPlaceholder="Rechercher une facture, client..."
                actions={
                    <>
                        <button className="secondary">
                            <Download size={18} />
                            Exporter
                        </button>
                        <Link to="/factures/nouveau" style={{ textDecoration: 'none' }}>
                            <button>
                                <Plus size={18} />
                                Nouvelle Facture
                            </button>
                        </Link>
                    </>
                }
            />

            <StatsGrid stats={stats} />

            <div style={{
                background: 'var(--surface)',
                padding: '1.5rem',
                borderRadius: 'var(--radius)',
                border: '1px solid var(--border-light)',
                marginBottom: '1.5rem',
                display: 'flex',
                gap: '1rem',
                alignItems: 'center'
            }}>
                <div className="form-group" style={{ marginBottom: 0, flex: 1 }}>
                    <label>Filtrer par Client</label>
                    <select
                        name="client_id"
                        value={filters.client_id}
                        onChange={handleFilterChange}
                        style={{
                            appearance: 'none',
                            backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E")`,
                            backgroundRepeat: 'no-repeat',
                            backgroundPosition: 'calc(100% - 12px) center',
                            paddingRight: '2.5rem'
                        }}
                    >
                        <option value="">Tous les clients</option>
                        {clients.map(c => <option key={c.id} value={c.id}>{c.nom} {c.prenom}</option>)}
                    </select>
                </div>
                <div className="form-group" style={{ marginBottom: 0, flex: 1 }}>
                    <label>Statut</label>
                    <select
                        name="statut"
                        value={filters.statut}
                        onChange={handleFilterChange}
                        style={{
                            appearance: 'none',
                            backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E")`,
                            backgroundRepeat: 'no-repeat',
                            backgroundPosition: 'calc(100% - 12px) center',
                            paddingRight: '2.5rem'
                        }}
                    >
                        <option value="">Tous les statuts</option>
                        <option value="Brouillon">Brouillon</option>
                        <option value="Émise">Émise</option>
                        <option value="Partiellement Payée">Partiellement Payée</option>
                        <option value="Payée">Payée</option>
                    </select>
                </div>
                <div style={{ paddingTop: '1.375rem' }}> {/* Adjusted +2px to be lower */}
                    <button
                        className="secondary"
                        onClick={() => { setFilters({ client_id: '', statut: '' }); fetchInvoices({ client_id: '', statut: '' }); }}
                        style={{
                            background: '#C68E17',
                            color: 'white',
                            borderRadius: '12px',
                            padding: '0.5rem 1.5rem',
                            border: 'none',
                            fontWeight: '600',
                            cursor: 'pointer'
                        }}
                    >
                        Réinitialiser
                    </button>
                </div>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>N° FACTURE</th>
                            <th>DATE</th>
                            <th>CLIENT</th>
                            <th>TOTAL TTC</th>
                            <th>RESTE À PAYER</th>
                            <th>STATUT</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredInvoices.map(f => (
                            <tr key={f.id}>
                                <td>
                                    <div style={{ fontWeight: '600', color: 'var(--text-main)' }}>
                                        {f.numero_facture}
                                    </div>
                                </td>
                                <td>{new Date(f.date_facture).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })}</td>
                                <td>
                                    <div style={{ fontWeight: '500' }}>
                                        {f.client_details?.nom} {f.client_details?.prenom}
                                    </div>
                                </td>
                                <td>
                                    <div style={{ fontWeight: '600' }}>{f.total_ttc} €</div>
                                </td>
                                <td>
                                    <div style={{
                                        color: Number(f.reste_a_payer) > 0 ? 'var(--status-delayed-text)' : 'var(--status-delivered-text)',
                                        fontWeight: '600'
                                    }}>
                                        {f.reste_a_payer} €
                                    </div>
                                </td>
                                <td>
                                    <span className={`status-badge ${getStatusClass(f.statut)}`}>
                                        {f.statut}
                                    </span>
                                </td>
                                <td>
                                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                        <Link to={`/factures/${f.id}`} style={{ textDecoration: 'none' }}>
                                            <button className="btn-icon" title="Voir les détails">
                                                <Eye size={18} />
                                            </button>
                                        </Link>
                                        <button
                                            className="btn-icon"
                                            type="button"
                                            title="Supprimer"
                                            onClick={() => handleDelete(f.id)}
                                            style={{ color: '#b91c1c' }}
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {filteredInvoices.length === 0 && !loading && (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                    Aucune facture trouvée.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default InvoiceList;
