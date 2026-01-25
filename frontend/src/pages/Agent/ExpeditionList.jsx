import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';
import { Search, Download, Plus, Calendar, Filter, MoreVertical, TrendingUp } from 'lucide-react';

const ExpeditionList = () => {
    const [expeditions, setExpeditions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchExpeditions();
    }, []);

    const fetchExpeditions = async () => {
        try {
            const response = await api.get('/expeditions/');
            setExpeditions(response.data);
            setLoading(false);
        } catch (err) {
            setError('Erreur lors du chargement des expéditions');
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Voulez-vous vraiment supprimer cette expédition ?')) {
            try {
                await api.delete(`/expeditions/${id}/`);
                fetchExpeditions();
            } catch (err) {
                const errorMsg = err.response?.data?.[0] || "Impossible de supprimer cette expédition (déjà liée à une tournée).";
                alert(errorMsg);
            }
        }
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    const getStatusClass = (status) => {
        const map = {
            'Enregistré': 'status-enregistre',
            'Validé': 'status-valide',
            'En transit': 'status-en-transit',
            'En centre de tri': 'status-centre-tri',
            'En cours de livraison': 'status-en-cours',
            'Livré': 'status-livre',
            'Échec de livraison': 'status-retard'
        };
        return map[status] || 'status-neutral';
    };

    // Calculate stats
    const stats = {
        total: expeditions.length,
        enCours: expeditions.filter(e => e.statut === 'En cours de livraison').length,
        enTransit: expeditions.filter(e => e.statut === 'En transit').length,
        retards: expeditions.filter(e => e.statut === 'Échec de livraison').length,
    };

    // Filter expeditions based on active tab
    const filteredExpeditions = expeditions.filter(exp => {
        const matchesSearch = exp.code_expedition.toLowerCase().includes(searchTerm.toLowerCase()) ||
            exp.client_details?.nom?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            exp.destination_details?.ville?.toLowerCase().includes(searchTerm.toLowerCase());
        
        if (!matchesSearch) return false;

        if (activeTab === 'all') return true;
        if (activeTab === 'transit') return exp.statut === 'En transit';
        if (activeTab === 'sorting') return exp.statut === 'En centre de tri';
        if (activeTab === 'delivered') return exp.statut === 'Livré';
        if (activeTab === 'delayed') return exp.statut === 'Échec de livraison';
        return true;
    });

    return (
        <div className="page-container">
            <div className="page-header">
                <h1>Gestion des Expéditions</h1>
                <p className="page-subtitle">
                    Suivez l'état de vos envois en temps réel.
                </p>
            </div>

            <div className="top-bar">
                <div className="search-bar">
                    <Search size={18} className="search-icon" />
                    <input 
                        type="text" 
                        placeholder="Rechercher un n° de suivi, client, ville..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="top-bar-actions">
                    <button className="secondary">
                        <Download size={18} />
                        Exporter
                    </button>
                    <Link to="/expeditions/nouveau" style={{ textDecoration: 'none' }}>
                        <button>
                            <Plus size={18} />
                            Créer une expédition
                        </button>
                    </Link>
                </div>
            </div>

            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">Total Expéditions</span>
                    </div>
                    <div className="stat-card-value">{stats.total.toLocaleString()}</div>
                    <div className="stat-card-meta">
                        <span className="badge-increase">
                            <TrendingUp size={12} />
                            12%
                        </span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">En cours de livraison</span>
                    </div>
                    <div className="stat-card-value">{stats.enCours}</div>
                    <div className="stat-card-meta">
                        <span className="status-badge status-actif">Actif</span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">En transit</span>
                    </div>
                    <div className="stat-card-value">{stats.enTransit}</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">Retards</span>
                    </div>
                    <div className="stat-card-value">{stats.retards}</div>
                    <div className="stat-card-meta">
                        <span className="status-badge status-action-requise">Action requise</span>
                    </div>
                </div>
            </div>

            <div className="tabs-container">
                <div className="tabs">
                    <button 
                        className={`tab ${activeTab === 'all' ? 'active' : ''}`}
                        onClick={() => setActiveTab('all')}
                    >
                        Tous ({stats.total})
                    </button>
                    <button 
                        className={`tab ${activeTab === 'transit' ? 'active' : ''}`}
                        onClick={() => setActiveTab('transit')}
                    >
                        En transit ({stats.enTransit})
                    </button>
                    <button 
                        className={`tab ${activeTab === 'sorting' ? 'active' : ''}`}
                        onClick={() => setActiveTab('sorting')}
                    >
                        En centre de tri ({expeditions.filter(e => e.statut === 'En centre de tri').length})
                    </button>
                    <button 
                        className={`tab ${activeTab === 'delivered' ? 'active' : ''}`}
                        onClick={() => setActiveTab('delivered')}
                    >
                        Livrés ({expeditions.filter(e => e.statut === 'Livré').length})
                    </button>
                    <button 
                        className={`tab ${activeTab === 'delayed' ? 'active' : ''}`}
                        onClick={() => setActiveTab('delayed')}
                    >
                        Retards ({stats.retards})
                    </button>
                </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <button className="btn-icon">
                        <Calendar size={18} />
                    </button>
                    <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Oct 2023</span>
                    <button className="btn-icon">
                        <Filter size={18} />
                    </button>
                </div>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th style={{ width: '40px' }}>
                                <input type="checkbox" />
                            </th>
                            <th>N° DE SUIVI</th>
                            <th>EXPÉDITEUR</th>
                            <th>DESTINATAIRE</th>
                            <th>DATE</th>
                            <th>STATUT</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredExpeditions.map((exp) => (
                            <tr key={exp.id}>
                                <td>
                                    <input type="checkbox" />
                                </td>
                                <td>
                                    <div style={{ fontWeight: '600', color: 'var(--text-main)' }}>
                                        {exp.code_expedition}
                                    </div>
                                    <div className="table-secondary-text">
                                        {exp.type_service_details?.libelle || 'Standard Ground'}
                                    </div>
                                </td>
                                <td>
                                    <div style={{ fontWeight: '500', color: 'var(--text-main)' }}>
                                        {exp.client_details ? `${exp.client_details.nom} ${exp.client_details.prenom || ''}`.trim() : 'Inconnu'}
                                    </div>
                                    <div className="table-secondary-text">
                                        {exp.client_details?.ville || 'N/A'}
                                    </div>
                                </td>
                                <td>
                                    <div style={{ fontWeight: '500', color: 'var(--text-main)' }}>
                                        {exp.destination_details?.ville || 'Destination'}
                                    </div>
                                    <div className="table-secondary-text">
                                        {exp.destination_details?.pays || 'Pays'}
                                    </div>
                                </td>
                                <td>
                                    <div style={{ fontWeight: '500', color: 'var(--text-main)' }}>
                                        {new Date(exp.date_creation).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })}
                                    </div>
                                    <div className="table-secondary-text">
                                        {new Date(exp.date_creation).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                                    </div>
                                </td>
                                <td>
                                    <span className={`status-badge ${getStatusClass(exp.statut)}`}>
                                        {exp.statut === 'En cours de livraison' ? 'En cours de livraison' : 
                                         exp.statut === 'En centre de tri' ? 'En centre de tri' :
                                         exp.statut === 'En transit' ? 'En transit' :
                                         exp.statut === 'Livré' ? 'Livré' :
                                         exp.statut}
                                    </span>
                                </td>
                                <td>
                                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                        {!exp.tournee && (
                                            <>
                                                <Link
                                                    to={`/expeditions/${exp.id}/edit`}
                                                    style={{
                                                        textDecoration: 'none',
                                                        color: 'var(--text-secondary)',
                                                        fontSize: '0.875rem',
                                                        fontWeight: '500'
                                                    }}
                                                >
                                                    Modifier
                                                </Link>
                                            </>
                                        )}
                                        <button className="btn-icon">
                                            <MoreVertical size={18} />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {filteredExpeditions.length === 0 && (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                    Aucune expédition trouvée.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                marginTop: '1.5rem',
                fontSize: '0.875rem',
                color: 'var(--text-muted)'
            }}>
                <span>Affichage de 1 à {filteredExpeditions.length} sur {stats.total} résultats</span>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button className="secondary" style={{ padding: '0.5rem 1rem' }}>Précédent</button>
                    <button style={{ padding: '0.5rem 1rem' }}>Suivant</button>
                </div>
            </div>
        </div>
    );
};

export default ExpeditionList;
