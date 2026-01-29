import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';
import { CreditCard, Plus, Download, Trash2 } from 'lucide-react';
import PageHeader from '../../components/PageHeader';
import TopBar from '../../components/TopBar';
import StatsGrid from '../../components/StatsGrid';

const PaymentList = () => {
    const [payments, setPayments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [clients, setClients] = useState([]);
    const [filters, setFilters] = useState({ client_id: '' });
    const [searchTerm, setSearchTerm] = useState('');

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

    if (loading && payments.length === 0) return <div className="page-container">Chargement...</div>;

    const filteredPayments = payments.filter(p =>
        p.client_details?.nom?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.facture_numero?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const totalAmount = payments.reduce((sum, p) => sum + (Number(p.montant) || 0), 0);

    const stats = [
        {
            label: 'Total Paiements',
            value: payments.length.toLocaleString(),
            icon: CreditCard
        },
        {
            label: 'Montant Total',
            value: `${totalAmount.toFixed(2)} €`,
            badge: <span className="status-badge status-livre">Encaissé</span>
        },
        {
            label: 'Espèces',
            value: payments.filter(p => p.mode_paiement === 'Espèces').length
        },
        {
            label: 'Carte/Virement',
            value: payments.filter(p => ['Carte', 'Virement'].includes(p.mode_paiement)).length
        }
    ];

    return (
        <div className="page-container">
            <PageHeader 
                title="Journal des Paiements"
                subtitle="Suivi des paiements reçus"
            />

            <TopBar
                searchValue={searchTerm}
                onSearchChange={setSearchTerm}
                searchPlaceholder="Rechercher un paiement, client..."
                actions={
                    <>
                        <button className="secondary">
                            <Download size={18} />
                            Exporter
                        </button>
                        <Link to="/paiements/nouveau" style={{ textDecoration: 'none' }}>
                            <button>
                                <Plus size={18} />
                                Enregistrer un Paiement
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
                alignItems: 'flex-end'
            }}>
                <div className="form-group" style={{ marginBottom: 0, flex: 1 }}>
                    <label>Filtrer par Client</label>
                    <select name="client_id" value={filters.client_id} onChange={handleFilterChange}>
                        <option value="">Tous les clients</option>
                        {clients.map(c => <option key={c.id} value={c.id}>{c.nom} {c.prenom}</option>)}
                    </select>
                </div>
                <button className="secondary" onClick={() => { setFilters({ client_id: '' }); fetchPayments({ client_id: '' }); }}>
                    Réinitialiser
                </button>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>DATE</th>
                            <th>CLIENT</th>
                            <th>FACTURE LIÉE</th>
                            <th>MODE</th>
                            <th>MONTANT</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredPayments.map(p => (
                            <tr key={p.id}>
                                <td>
                                    {new Date(p.date_paiement).toLocaleDateString('fr-FR', { 
                                        day: '2-digit', 
                                        month: 'short', 
                                        year: 'numeric' 
                                    })}
                                </td>
                                <td>
                                    <div style={{ fontWeight: '600' }}>
                                        {p.client_details?.nom} {p.client_details?.prenom}
                                    </div>
                                </td>
                                <td>
                                    <div style={{ fontWeight: '500' }}>
                                        {p.facture_numero || 'Paiement Libre'}
                                    </div>
                                </td>
                                <td>
                                    <span className="status-badge status-neutral">
                                        {p.mode_paiement}
                                    </span>
                                </td>
                                <td>
                                    <div style={{ fontWeight: '700', color: 'var(--status-delivered-text)' }}>
                                        {p.montant} €
                                    </div>
                                </td>
                                <td>
                                    <button
                                        className="btn-icon"
                                        type="button"
                                        title="Supprimer"
                                        onClick={() => handleDelete(p.id)}
                                        style={{ color: '#b91c1c' }}
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {filteredPayments.length === 0 && !loading && (
                            <tr>
                                <td colSpan="6" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                    Aucun paiement trouvé.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PaymentList;
