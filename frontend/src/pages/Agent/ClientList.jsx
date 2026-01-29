import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';
import { Users, Plus, Download, Trash2 } from 'lucide-react';
import PageHeader from '../../components/PageHeader';
import TopBar from '../../components/TopBar';
import StatsGrid from '../../components/StatsGrid';

const ClientList = () => {
    const [clients, setClients] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchClients();
    }, []);

    const fetchClients = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await api.get('/clients/');
            setClients(response.data);
        } catch (err) {
            console.error(err);
            setError("Erreur lors du chargement des clients.");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Voulez-vous vraiment supprimer ce client ?')) return;
        try {
            await api.delete(`/clients/${id}/`);
            fetchClients();
        } catch (err) {
            const errorMsg = err.response?.data?.detail || "Impossible de supprimer ce client.";
            alert(errorMsg);
        }
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    const filteredClients = clients.filter((client) => {
        const query = (searchTerm || '').trim().toLowerCase();
        if (!query) return true;

        const nom = (client.nom || '').toLowerCase();
        const prenom = (client.prenom || '').toLowerCase();
        const email = (client.email || '').toLowerCase();
        const code = (client.code_client || '').toLowerCase();

        return nom.includes(query) || prenom.includes(query) || email.includes(query) || code.includes(query);
    });

    const totalBalance = clients.reduce((sum, c) => sum + (Number(c.solde) || 0), 0);
    const activeClients = clients.filter(c => c.solde < 0).length;

    const stats = [
        {
            label: 'Total Clients',
            value: clients.length.toLocaleString(),
            icon: Users
        },
        {
            label: 'Clients Actifs',
            value: activeClients,
            badge: <span className="status-badge status-actif">Actif</span>
        },
        {
            label: 'Solde Total',
            value: `${totalBalance.toFixed(2)} €`,
            badge: totalBalance < 0 ? 
                <span className="status-badge status-livre">Crédit</span> :
                <span className="status-badge status-retard">Débit</span>
        }
    ];

    return (
        <div className="page-container">
            <PageHeader 
                title="Clients"
                subtitle="Gérez votre base de données clients"
            />

            <TopBar
                searchValue={searchTerm}
                onSearchChange={setSearchTerm}
                searchPlaceholder="Rechercher un client..."
                actions={
                    <>
                        <button className="secondary">
                            <Download size={18} />
                            Exporter
                        </button>
                        <Link to="/clients/nouveau" style={{ textDecoration: 'none' }}>
                            <button>
                                <Plus size={18} />
                                Nouveau Client
                            </button>
                        </Link>
                    </>
                }
            />

            <StatsGrid stats={stats} />

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>CODE</th>
                            <th>NOM COMPLET</th>
                            <th>EMAIL</th>
                            <th>TÉLÉPHONE</th>
                            <th>ADRESSE</th>
                            <th>SOLDE</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredClients.map(client => (
                            <tr key={client.id}>
                                <td>
                                    <div style={{ fontWeight: '600', color: 'var(--text-main)' }}>
                                        {client.code_client}
                                    </div>
                                </td>
                                <td>
                                    <div style={{ fontWeight: '500', color: 'var(--text-main)' }}>
                                        {client.nom} {client.prenom}
                                    </div>
                                    <div className="table-secondary-text">
                                        {client.ville || 'N/A'}
                                    </div>
                                </td>
                                <td>{client.email || '-'}</td>
                                <td>{client.telephone || '-'}</td>
                                <td>
                                    <div style={{ maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                        {client.adresse || '-'}
                                    </div>
                                </td>
                                <td>
                                    <div style={{ 
                                        fontWeight: '600',
                                        color: Number(client.solde) < 0 ? 'var(--status-delivered-text)' : 'var(--status-delayed-text)'
                                    }}>
                                        {Number(client.solde ?? 0).toFixed(2)} €
                                    </div>
                                </td>
                                <td>
                                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                        <Link
                                            to={`/clients/${client.id}/edit`}
                                            style={{
                                                textDecoration: 'none',
                                                color: 'var(--text-secondary)',
                                                fontSize: '0.875rem',
                                                fontWeight: '500'
                                            }}
                                        >
                                            Modifier
                                        </Link>
                                        <button
                                            className="btn-icon"
                                            type="button"
                                            title="Supprimer"
                                            onClick={() => handleDelete(client.id)}
                                            style={{ color: '#b91c1c' }}
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {filteredClients.length === 0 && (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                    Aucun client trouvé.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ClientList;
