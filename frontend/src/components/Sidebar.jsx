import React from 'react';
import { NavLink } from 'react-router-dom';
import { Truck, LayoutDashboard, TrendingUp, Package, MapPin, AlertCircle, Bell, FileText, Users, FileSpreadsheet, CreditCard, User as UserIcon, Wrench, ScrollText, Settings } from 'lucide-react';

const Sidebar = ({ user, onLogout }) => {
    if (!user) return null;

    const ROLE_LABELS = {
        ADMIN: 'Administrateur',
        AGENT: 'Agent',
        LOGISTIQUE: 'Logistique',
        COMPTABLE: 'Comptable',
        DIRECTION: 'Direction',
        CHAUFFEUR: 'Chauffeur',
    };

    const roleCode = user.role_code;
    const isAdmin = roleCode === 'ADMIN';
    const roleLabel = ROLE_LABELS[roleCode] || user.role_display || roleCode || 'Utilisateur';
    const portalLabel = `Portail ${roleLabel}`;

    return (
        <div className="sidebar">
            <div className="sidebar-logo">
                <div className="sidebar-logo-icon">
                    <Truck size={20} strokeWidth={2.5} />
                </div>
                <div className="sidebar-logo-text">
                    <h2>Logistique Pro</h2>
                    <p>{portalLabel}</p>
                </div>
            </div>

            <div className="user-info">
                <h3>{user.full_name || user.username}</h3>
                <span className="role-badge">{roleLabel}</span>
            </div>

            <nav>
                <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}>
                    <LayoutDashboard size={18} />
                    Tableau de bord
                </NavLink>

                <NavLink to="/analytics">
                    <TrendingUp size={18} />
                    Rapports
                </NavLink>

                <div className="menu-section">OPÉRATIONS</div>
                <NavLink to="/expeditions">
                    <Package size={18} />
                    Expéditions
                </NavLink>
                <NavLink to="/clients">
                    <Users size={18} />
                    Clients
                </NavLink>
                <NavLink to="/tournees">
                    <MapPin size={18} />
                    Tournées
                </NavLink>
                <NavLink to="/incidents">
                    <AlertCircle size={18} />
                    Incidents
                </NavLink>
                <NavLink to="/alertes">
                    <Bell size={18} />
                    Alertes
                </NavLink>
                <NavLink to="/reclamations">
                    <FileText size={18} />
                    Réclamations
                </NavLink>

                <div className="menu-section">FACTURATION</div>
                <NavLink to="/factures">
                    <FileSpreadsheet size={18} />
                    Factures
                </NavLink>
                <NavLink to="/paiements">
                    <CreditCard size={18} />
                    Paiements
                </NavLink>

                <div className="menu-section">RÉFÉRENTIELS</div>
                <NavLink to="/chauffeurs">
                    <UserIcon size={18} />
                    Chauffeurs
                </NavLink>
                <NavLink to="/vehicules">
                    <Truck size={18} />
                    Véhicules
                </NavLink>
                <NavLink to="/destinations">
                    <MapPin size={18} />
                    Destinations
                </NavLink>

                {isAdmin && (
                    <>
                        <div className="menu-section">ADMINISTRATION</div>
                        <NavLink to="/admin/users">
                            <Settings size={18} />
                            Utilisateurs
                        </NavLink>
                        <NavLink to="/admin/audit">
                            <ScrollText size={18} />
                            Journal d'Audit
                        </NavLink>
                    </>
                )}
            </nav>

            <NavLink to="/settings">
                <Settings size={18} />
                Paramètres
            </NavLink>

            <button onClick={onLogout} className="logout-btn">
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <Users size={18} style={{ transform: 'rotate(180deg)' }} /> {/* Using Users as placeholder for LogOut if not available, checking imports.. LogOut not imported, using existing User or just text */}
                    Déconnexion
                </div>
            </button>
        </div>
    );
};

export default Sidebar;
