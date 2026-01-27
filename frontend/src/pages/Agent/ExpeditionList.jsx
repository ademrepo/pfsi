import React, { useState, useEffect, useRef } from 'react';
import api from '../../api';
import { Link } from 'react-router-dom';
import { Search, Download, Plus, Calendar, Filter, TrendingUp, MoreVertical, Pencil, Trash2 } from 'lucide-react';

const ExpeditionList = () => {
    const [expeditions, setExpeditions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedId, setSelectedId] = useState(null);
    const [openMenuId, setOpenMenuId] = useState(null);
    const menuRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (menuRef.current && !menuRef.current.contains(e.target)) {
                setOpenMenuId(null);
            }
        };
        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, []);

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
        if (!query) return true;

        const code = (exp.code_expedition || '').toLowerCase();
        const clientNom = (exp.client_details?.nom || '').toLowerCase();
        const clientPrenom = (exp.client_details?.prenom || '').toLowerCase();
        const destVille = (exp.destination_details?.ville || '').toLowerCase();

        const matchesSearch =
            code.includes(query) ||
            clientNom.includes(query) ||
            clientPrenom.includes(query) ||
            destVille.includes(query);
        
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
                    <div className="stat-card-value stat-card-value--accent">{stats.enCours}</div>
                    <div className="stat-card-meta">
                        <span className="status-badge status-actif">ACTIF</span>
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
                        <span className="status-badge status-action-requise">ACTION REQUISE</span>
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

            <div className="filters-row">
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-md)' }}>
                    <button type="button" className="btn-icon" title="Période">
                        <Calendar size={18} />
                    </button>
                    <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Oct 2023</span>
                    <button type="button" className="btn-icon" title="Filtres">
                        <Filter size={18} />
                    </button>
                </div>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th aria-label="Sélection" />
                            <th>N° DE SUIVI</th>
                            <th>EXPÉDITEUR</th>
                            <th>DESTINATAIRE</th>
                            <th>DATE</th>
                            <th>STATUT</th>
                            <th>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredExpeditions.map((exp) => {
                            const isDelivered = exp.statut === 'Livré' || exp.statut === 'LivrÃ©';
                            const canEdit = !isDelivered && !exp.tournee;
                            const isMenuOpen = openMenuId === exp.id;
                            return (
                                <tr
                                    key={exp.id}
                                    className={selectedId === exp.id ? 'table-row--selected' : ''}
                                >
                                    <td>
                                        <input
                                            type="radio"
                                            name="exp-selection"
                                            className="table-radio"
                                            checked={selectedId === exp.id}
                                            onChange={() => setSelectedId(exp.id)}
                                            aria-label={`Sélectionner ${exp.code_expedition}`}
                                        />
                                    </td>
                                    <td>
                                        <div className="table-cell-primary">
                                            {exp.code_expedition}
                                        </div>
                                        <div className="table-secondary-text">
                                            {exp.type_service_details?.libelle || 'Standard Ground'}
                                        </div>
                                    </td>
                                    <td>
                                        <div className="table-cell-primary">
                                            {exp.client_details ? `${exp.client_details.nom} ${exp.client_details.prenom || ''}`.trim() : 'Inconnu'}
                                        </div>
                                        <div className="table-secondary-text">
                                            {exp.client_details?.ville || 'N/A'}
                                        </div>
                                    </td>
                                    <td>
                                        <div className="table-cell-primary">
                                            {exp.destination_details?.ville || 'Destination'}
                                        </div>
                                        <div className="table-secondary-text">
                                            {exp.destination_details?.pays || 'Pays'}
                                        </div>
                                    </td>
                                    <td>
                                        <div className="table-cell-primary">
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
                                        <div className="table-actions-wrap" ref={isMenuOpen ? menuRef : null}>
                                            <button
                                                type="button"
                                                className="table-actions-btn"
                                                onClick={(e) => { e.stopPropagation(); setOpenMenuId(isMenuOpen ? null : exp.id); }}
                                                aria-expanded={isMenuOpen}
                                                aria-haspopup="true"
                                                title="Actions"
                                            >
                                                <MoreVertical size={18} />
                                            </button>
                                            {isMenuOpen && (
                                                <div className="table-actions-dropdown">
                                                    {canEdit && (
                                                        <Link
                                                            to={`/expeditions/${exp.id}/edit`}
                                                            onClick={() => setOpenMenuId(null)}
                                                        >
                                                            <Pencil size={16} />
                                                            Modifier
                                                        </Link>
                                                    )}
                                                    <button
                                                        type="button"
                                                        className="table-actions-danger"
                                                        onClick={() => { handleDelete(exp.id); setOpenMenuId(null); }}
                                                    >
                                                        <Trash2 size={16} />
                                                        Supprimer
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                            );
                        })}
                        {filteredExpeditions.length === 0 && (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', padding: 'var(--space-3xl)', color: 'var(--text-muted)' }}>
                                    Aucune expédition trouvée.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            <div className="table-pagination">
                <span>Affichage de 1 à {Math.min(filteredExpeditions.length, 10)} sur {stats.total} résultats</span>
                <div className="table-pagination-actions">
                    <button type="button" className="secondary" disabled>Précédent</button>
                    <button type="button" className="secondary">Suivant</button>
                </div>
            </div>
        </div>
    );
};

export default ExpeditionList;
