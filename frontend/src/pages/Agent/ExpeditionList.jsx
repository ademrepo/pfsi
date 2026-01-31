import React, { useState, useEffect } from 'react';
import api from '../../api';
import { useNavigate, Link } from 'react-router-dom';
import { Search, Printer, Plus, Calendar, TrendingUp, Lock, Trash2, MoreVertical } from 'lucide-react';

const ExpeditionList = () => {
    const [expeditions, setExpeditions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');
    const [dateFilter, setDateFilter] = useState({ year: new Date().getFullYear(), month: new Date().getMonth() + 1 });
    const [showDatePicker, setShowDatePicker] = useState(false);
    const navigate = useNavigate();

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

    const getStatusInfo = (status) => {
        const norm = (status || '').toString().toLowerCase().trim();
        switch (norm) {
            case 'en_livraison':
            case 'en cours de livraison':
                return { label: 'En cours de livraison', className: 'status-en_livraison' };
            case 'centre_tri':
            case 'en centre de tri':
                return { label: 'En centre de tri', className: 'status-centre_tri' };
            case 'en_transit':
            case 'en transit':
                return { label: 'En transit', className: 'status-en_transit' };
            case 'livre':
            case 'livné':
            case 'livré':
                return { label: 'Livré', className: 'status-livre' };
            case 'enregistre':
            case 'enregistré':
                return { label: 'Enregistré', className: 'status-enregistre' };
            case 'echec_livraison':
            case 'échec de livraison':
                return { label: 'Échec de livraison', className: 'status-retard' };
            default:
                return { label: status || '—', className: 'status-neutral' };
        }
    };

    // Calculate stats
    const stats = {
        total: expeditions.length,
        enCours: expeditions.filter(e => ['en_livraison', 'en cours de livraison'].includes((e.statut || '').toLowerCase())).length,
        enTransit: expeditions.filter(e => ['en_transit', 'en transit'].includes((e.statut || '').toLowerCase())).length,
        retards: expeditions.filter(e => ['echec_livraison', 'échec de livraison'].includes((e.statut || '').toLowerCase())).length,
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

        const norm = (s) => (s || '').toLowerCase();
        const s = norm(exp.statut);

        if (activeTab === 'all') return true;
        if (activeTab === 'transit') return ['en_transit', 'en transit'].includes(s);
        if (activeTab === 'sorting') return ['centre_tri', 'en centre de tri'].includes(s);
        if (activeTab === 'delivered') return ['livre', 'livré', 'livné'].includes(s);
        if (activeTab === 'delayed') return ['echec_livraison', 'échec de livraison'].includes(s);
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
                    <button className="secondary" onClick={() => window.print()}>
                        <Printer size={18} />
                        Imprimer
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

            <div className="dashboard-table-card">
                <div className="dashboard-table-toolbar">
                    <div className="dashboard-table-tabs">
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
                            En centre de tri ({expeditions.filter(e => ['centre_tri', 'en centre de tri'].includes((e.statut || '').toLowerCase())).length})
                        </button>
                        <button
                            className={`tab ${activeTab === 'delivered' ? 'active' : ''}`}
                            onClick={() => handleTabChange('delivered')}
                        >
                            Livrés ({expeditions.filter(e => ['livre', 'livré', 'livné'].includes((e.statut || '').toLowerCase())).length})
                        </button>
                        <button
                            className={`tab ${activeTab === 'delayed' ? 'active' : ''}`}
                            onClick={() => handleTabChange('delayed')}
                        >
                            Retards ({stats.retards})
                        </button>
                    </div>

                    <div className="dashboard-table-toolbar-right">
                        <div
                            className="dashboard-date-pill"
                            onClick={() => setShowDatePicker(!showDatePicker)}
                            role="button"
                            tabIndex={0}
                        >
                            <Calendar size={18} style={{ color: 'var(--text-muted)' }} />
                            <span>
                                {new Date(dateFilter.year, dateFilter.month - 1).toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' })}
                            </span>
                            <span style={{ opacity: 0.6 }}>▾</span>
                        </div>
                        {showDatePicker && (
                            <div className="dashboard-date-dropdown">
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
                                        >
                                            {d.toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' })}
                                        </button>
                                    );
                                })}
                            </div>
                        )}
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
                            {currentRows.map((exp) => {
                                const { label: statusLabel, className: statusClass } = getStatusInfo(exp.statut);
                                return (
                                    <tr
                                        key={exp.id}
                                        onClick={() => navigate(`/expeditions/${exp.id}`)}
                                        style={{ cursor: 'pointer' }}
                                    >
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
                                            <span className={`status-badge ${statusClass}`}>
                                                {statusLabel}
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
                                                                className="btn-icon"
                                                                title="Modifier"
                                                                onClick={(e) => e.stopPropagation()}
                                                            >
                                                                <MoreVertical size={18} />
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
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        handleDelete(exp.id);
                                                    }}
                                                    style={{ color: '#b91c1c' }}
                                                >
                                                    <Trash2 size={18} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                )
                            })}
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

        </div>
    );
};

export default ExpeditionList;
