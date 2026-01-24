import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ user, onLogout }) => {
    if (!user) return null;

    const isAdmin = user.role_code === 'ADMIN';

    return (
        <div className="sidebar">
            <div className="user-info">
                <h3>{user.full_name || user.username}</h3>
                <span className="role-badge">{user.role_display}</span>
            </div>

            <nav>
                <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}>
                    🏠 Tableau de bord
                </NavLink>

                <div className="menu-section">OPÉRATIONS</div>
                <NavLink to="/expeditions">📦 Expéditions</NavLink>
                <NavLink to="/tournees">🚚 Tournées</NavLink>
                <NavLink to="/incidents">⚠️ Incidents</NavLink>
                <NavLink to="/alertes">🔔 Alertes</NavLink>
                <NavLink to="/reclamations">📝 Réclamations</NavLink>
                <NavLink to="/clients">👥 Clients</NavLink>

                <div className="menu-section">FACTURATION</div>
                <NavLink to="/factures">📄 Factures</NavLink>
                <NavLink to="/paiements">💰 Paiements</NavLink>

                <div className="menu-section">RÉFÉRENTIELS</div>
                <NavLink to="/chauffeurs">👨‍✈️ Chauffeurs</NavLink>
                <NavLink to="/vehicules">🚛 Véhicules</NavLink>
                <NavLink to="/destinations">📍 Destinations</NavLink>

                {isAdmin && (
                    <>
                        <div className="menu-section">ADMINISTRATION</div>
                        <NavLink to="/admin/users">⚙️ Utilisateurs</NavLink>
                        <NavLink to="/admin/audit">📜 Journal d'Audit</NavLink>
                    </>
                )}

                <div style={{ marginTop: 'auto', paddingTop: '2rem' }}>
                    <button onClick={onLogout} className="logout-btn">
                        🚪 Déconnexion
                    </button>
                </div>
            </nav>
        </div>
    );
};

export default Sidebar;
