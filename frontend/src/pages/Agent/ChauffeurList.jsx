import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api';
import { Search, Printer, Plus, TrendingUp, MoreVertical, User } from 'lucide-react';

const ChauffeurList = () => {
    const [chauffeurs, setChauffeurs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [activeTab, setActiveTab] = useState('all');

    useEffect(() => {
        fetchChauffeurs();
    }, []);

    const fetchChauffeurs = async () => {
        try {
            const response = await api.get('/chauffeurs/');
            setChauffeurs(response.data);
            setLoading(false);
        } catch (err) {
            setError('Erreur lors du chargement des chauffeurs');
            setLoading(false);
        }
    };

    const stats = useMemo(() => {
        const norm = (s) => (s || '').toLowerCase();
        return {
            total: chauffeurs.length,
            actifs: chauffeurs.filter(c => !c.statut || ['actif', 'active'].includes(norm(c.statut))).length,
            conge: chauffeurs.filter(c => norm(c.statut) === 'conge' || norm(c.statut) === 'congé').length,
            indisponibles: chauffeurs.filter(c => norm(c.statut) === 'indisponible').length,
        };
    }, [chauffeurs]);

    const getStatusInfo = (statut) => {
        const s = (statut || '').toLowerCase();
        if (s === 'actif' || s === 'active') return { label: 'Actif', class: 'status-en_livraison' };
        if (s === 'conge' || s === 'congé') return { label: 'En congé', class: 'status-conge' };
        if (s === 'indisponible') return { label: 'Indisponible', class: 'status-indisponible' };
        return { label: statut || 'Actif', class: 'status-en_livraison' }; // Fallback
    };

    const filteredChauffeurs = chauffeurs.filter(c => {
        const query = searchTerm.toLowerCase();
        const matchesSearch =
            c.nom.toLowerCase().includes(query) ||
            c.prenom.toLowerCase().includes(query) ||
            (c.telephone && c.telephone.includes(query)) ||
            (c.num_permis && c.num_permis.toLowerCase().includes(query));

        if (!matchesSearch) return false;

        const s = (c.statut || 'actif').toLowerCase();
        if (activeTab === 'actifs' && !['actif', 'active'].includes(s)) return false;
        if (activeTab === 'conge' && s !== 'conge' && s !== 'congé') return false;
        if (activeTab === 'indisponibles' && s !== 'indisponible') return false;

        return true;
    });

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;

    return (
        <div className="page-container">
            <div className="page-header">
                <h1>Gestion des Chauffeurs</h1>
                <p className="page-subtitle">Supervisez et gérez votre flotte de conducteurs en temps réel.</p>
            </div>

            <div className="top-bar">
                <div className="search-bar">
                    <Search size={18} className="search-icon" />
                    <input
                        type="text"
                        placeholder="Rechercher un chauffeur, téléphone, permis..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="top-bar-actions">
                    <button className="secondary" onClick={() => window.print()}>
                        <Printer size={18} />
                        Imprimer
                    </button>
                    <Link to="/chauffeurs/nouveau">
                        <button>
                            <Plus size={18} />
                            Ajouter un Chauffeur
                        </button>
                    </Link>
                </div>
            </div>

            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">Total Chauffeurs</span>
                    </div>
                    <div className="stat-card-value">{stats.total}</div>
                    <div className="stat-card-meta">
                        <span className="badge-increase">
                            <TrendingUp size={12} />
                            +4%
                        </span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">Chauffeurs Actifs</span>
                    </div>
                    <div className="stat-card-value">{stats.actifs}</div>
                    <div className="stat-card-meta">
                        <span className="status-badge status-en_livraison">Actif</span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">En Congé</span>
                    </div>
                    <div className="stat-card-value">{stats.conge}</div>
                    <div className="stat-card-meta">
                        <span className="status-badge status-conge">Congé</span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">Indisponibles</span>
                    </div>
                    <div className="stat-card-value">{stats.indisponibles}</div>
                    <div className="stat-card-meta">
                        <span className="status-badge status-indisponible">Hors ligne</span>
                    </div>
                </div>
            </div>

            <div className="dashboard-table-card">
                <div className="dashboard-table-toolbar">
                    <div className="dashboard-table-tabs">
                        <button
                            className={`tab ${activeTab === 'all' ? 'active' : ''}`}
                            onClick={() => setActiveTab('all')}
                        >
                            Tous ({stats.total})
                        </button>
                        <button
                            className={`tab ${activeTab === 'actifs' ? 'active' : ''}`}
                            onClick={() => setActiveTab('actifs')}
                        >
                            Actifs ({stats.actifs})
                        </button>
                        <button
                            className={`tab ${activeTab === 'conge' ? 'active' : ''}`}
                            onClick={() => setActiveTab('conge')}
                        >
                            En congé ({stats.conge})
                        </button>
                        <button
                            className={`tab ${activeTab === 'indisponibles' ? 'active' : ''}`}
                            onClick={() => setActiveTab('indisponibles')}
                        >
                            Indisponibles ({stats.indisponibles})
                        </button>
                    </div>
                </div>

                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Chauffeur</th>
                                <th>Numéro Permis</th>
                                <th>Téléphone</th>
                                <th>Zone Actuelle</th>
                                <th>Statut</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredChauffeurs.map((c) => {
                                const { label: statusLabel, class: statusClass } = getStatusInfo(c.statut);
                                return (
                                    <tr key={c.id}>
                                        <td>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                                <div style={{
                                                    width: '40px',
                                                    height: '40px',
                                                    borderRadius: '50%',
                                                    background: 'var(--bg-page)',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'center',
                                                    color: 'var(--text-muted)'
                                                }}>
                                                    <User size={20} />
                                                </div>
                                                <div>
                                                    <div style={{ fontWeight: '700', color: 'var(--text-main)' }}>
                                                        {c.nom} {c.prenom}
                                                    </div>
                                                    <div className="table-secondary-text">ID: #CH-{c.id}</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div style={{ fontWeight: '500', color: 'var(--text-main)' }}>{c.num_permis || '—'}</div>
                                        </td>
                                        <td>
                                            <div style={{ fontWeight: '500', color: 'var(--text-main)' }}>{c.telephone || '—'}</div>
                                        </td>
                                        <td>
                                            <div style={{ fontWeight: '500', color: 'var(--text-main)' }}>Région Nord</div>
                                            <div className="table-secondary-text">Secteur Principal</div>
                                        </td>
                                        <td>
                                            <span className={`status-badge ${statusClass}`}>
                                                {statusLabel}
                                            </span>
                                        </td>
                                        <td>
                                            <Link to={`/chauffeurs/${c.id}/edit`} className="btn-icon" title="Modifier">
                                                <MoreVertical size={18} />
                                            </Link>
                                        </td>
                                    </tr>
                                );
                            })}
                            {filteredChauffeurs.length === 0 && (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                        Aucun chauffeur trouvé.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>

                <div className="dashboard-table-footer">
                    <p>
                        Affichage de <strong>1 à {filteredChauffeurs.length}</strong> sur <strong>{chauffeurs.length}</strong> résultats
                    </p>
                    <div className="pagination-btns">
                        <button disabled>Précédent</button>
                        <button disabled>Suivant</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChauffeurList;
