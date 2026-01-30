import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';
import { Search, Download, Plus, Calendar, Filter, TrendingUp, Lock, Trash2 } from 'lucide-react';

const ExpeditionList = () => {
    const [expeditions, setExpeditions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');
    const [dateFilter, setDateFilter] = useState({ year: new Date().getFullYear(), month: new Date().getMonth() + 1 });
    const [showDatePicker, setShowDatePicker] = useState(false);

    // Pagination state
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

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
    const filteredExpeditions = expeditions.filter((exp) => {
        const query = (searchTerm || '').trim().toLowerCase();

        const code = (exp.code_expedition || '').toLowerCase();
        const clientNom = (exp.client_details?.nom || '').toLowerCase();
        const clientPrenom = (exp.client_details?.prenom || '').toLowerCase();
        const destVille = (exp.destination_details?.ville || '').toLowerCase();

        const matchesSearch = !query ||
            code.includes(query) ||
            clientNom.includes(query) ||
            clientPrenom.includes(query) ||
            destVille.includes(query);

        if (!matchesSearch) return false;

        // Date Filtering
        if (exp.date_creation) {
            const d = new Date(exp.date_creation);
            if (d.getFullYear() !== dateFilter.year || d.getMonth() + 1 !== dateFilter.month) {
                return false;
            }
        }

        if (activeTab === 'all') return true;
        if (activeTab === 'transit') return exp.statut === 'En transit';
        if (activeTab === 'sorting') return exp.statut === 'En centre de tri';
        if (activeTab === 'delivered') return exp.statut === 'Livré';
        if (activeTab === 'delayed') return exp.statut === 'Échec de livraison';
        return true;
    });

    // Pagination Logic
    const totalPages = Math.ceil(filteredExpeditions.length / itemsPerPage);
    const currentRows = filteredExpeditions.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    const handleTabChange = (tab) => {
        setActiveTab(tab);
        setCurrentPage(1); // Reset to page 1 on tab change
    };

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
                        onChange={(e) => {
                            setSearchTerm(e.target.value);
                            setCurrentPage(1);
                        }}
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

            <div className="dashboard-table-tabs" style={{ marginBottom: '1.5rem' }}>
                <button
                    className={`tab ${activeTab === 'all' ? 'active' : ''}`}
                    onClick={() => handleTabChange('all')}
                >
                    Tous ({stats.total})
                </button>
                <button
                    className={`tab ${activeTab === 'transit' ? 'active' : ''}`}
                    onClick={() => handleTabChange('transit')}
                >
                    En transit ({stats.enTransit})
                </button>
                <button
                    className={`tab ${activeTab === 'sorting' ? 'active' : ''}`}
                    onClick={() => handleTabChange('sorting')}
                >
                    En centre de tri ({expeditions.filter(e => e.statut === 'En centre de tri').length})
                </button>
                <button
                    className={`tab ${activeTab === 'delivered' ? 'active' : ''}`}
                    onClick={() => handleTabChange('delivered')}
                >
                    Livrés ({expeditions.filter(e => e.statut === 'Livré').length})
                </button>
                <button
                    className={`tab ${activeTab === 'delayed' ? 'active' : ''}`}
                    onClick={() => handleTabChange('delayed')}
                >
                    Retards ({stats.retards})
                </button>
            </div>

            {/* Date Picker & Filter Toolbar */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', position: 'relative', zIndex: 20 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', position: 'relative' }}>

                    {/* Date Selector */}
                    <div
                        className="dashboard-date-pill"
                        onClick={() => setShowDatePicker(!showDatePicker)}
                        style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'var(--surface)', padding: '0.5rem 1rem', borderRadius: '12px', border: '1px solid var(--border)', fontWeight: 500 }}
                    >
                        <Calendar size={18} style={{ color: 'var(--text-muted)' }} />
                        <span>
                            {new Date(dateFilter.year, dateFilter.month - 1).toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })}
                        </span>
                        <span style={{ fontSize: '0.75rem', opacity: 0.5 }}>▼</span>
                    </div>

                    {/* Date Dropdown */}
                    {showDatePicker && (
                        <div className="dashboard-date-dropdown" style={{ position: 'absolute', top: '110%', left: 0, background: 'white', border: '1px solid var(--border)', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)', padding: '0.5rem', zIndex: 50, maxHeight: '300px', overflowY: 'auto' }}>
                            {Array.from({ length: 24 }).map((_, i) => {
                                const d = new Date();
                                d.setMonth(d.getMonth() - i);
                                const y = d.getFullYear();
                                const m = d.getMonth() + 1;
                                return (
                                    <button
                                        key={`${y}-${m}`}
                                        className="dashboard-date-option"
                                        onClick={() => {
                                            setDateFilter({ year: y, month: m });
                                            setShowDatePicker(false);
                                            setCurrentPage(1);
                                        }}
                                        style={{ display: 'block', width: '100%', padding: '0.5rem 1rem', textAlign: 'left', border: 'none', background: 'transparent', cursor: 'pointer', whiteSpace: 'nowrap' }}
                                    >
                                        {d.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })}
                                    </button>
                                );
                            })}
                        </div>
                    )}

                    <button className="btn-icon" title="Plus de filtres">
                        <Filter size={18} />
                    </button>
                </div>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>N° DE SUIVI</th>
                            <th>EXPÉDITEUR</th>
                            <th>DESTINATAIRE</th>
                            <th>DATE</th>
                            <th>STATUT</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {currentRows.map((exp) => (
                            <tr key={exp.id}>
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
                                    <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                                        {(() => {
                                            const isDelivered = exp.statut === 'Livré' || exp.statut === 'LivrÃ©';
                                            const canEdit = !isDelivered && !exp.tournee;
                                            if (canEdit) {
                                                return (
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
                                                );
                                            }

                                            if (isDelivered) {
                                                return <Lock size={18} title="Livrée" style={{ color: 'var(--text-muted)' }} />;
                                            }

                                            return <span style={{ color: 'var(--text-muted)' }}>—</span>;
                                        })()}

                                        <button
                                            className="btn-icon"
                                            type="button"
                                            title="Supprimer"
                                            onClick={() => handleDelete(exp.id)}
                                            style={{ color: '#b91c1c' }}
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {filteredExpeditions.length === 0 && (
                            <tr>
                                <td colSpan="6" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                    Aucune expédition trouvée.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {/* Pagination Controls */}
            <div className="dashboard-table-footer">
                <p>
                    Affichage de <strong style={{ color: 'var(--text-main)' }}>{currentRows.length === 0 ? 0 : (currentPage - 1) * itemsPerPage + 1}</strong> à <strong style={{ color: 'var(--text-main)' }}>{Math.min(currentPage * itemsPerPage, filteredExpeditions.length)}</strong> sur <strong style={{ color: 'var(--text-main)' }}>{filteredExpeditions.length.toLocaleString()}</strong> résultats
                </p>
                <div className="pagination-btns">
                    <button
                        disabled={currentPage <= 1}
                        onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    >
                        Précédent
                    </button>
                    <button
                        disabled={currentPage >= totalPages}
                        onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    >
                        Suivant
                    </button>
                </div>
            </div>

        </div>
    );
};

export default ExpeditionList;
