import React from 'react';
import { NavLink } from 'react-router-dom';
import { Truck, LayoutDashboard, TrendingUp, Package, MapPin, AlertCircle, Bell, FileText, Users, FileSpreadsheet, CreditCard, User as UserIcon, ChevronLeft, ChevronRight, ScrollText, Settings } from 'lucide-react';

const Sidebar = ({ user, onLogout, collapsed = false, onToggle }) => {
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
        <div className={`sidebar ${collapsed ? 'sidebar--collapsed' : ''}`}>
            <button
                type="button"
                className="sidebar-toggle"
                onClick={onToggle}
                aria-label={collapsed ? 'Ouvrir le menu' : 'Réduire le menu'}
                title={collapsed ? 'Ouvrir le menu' : 'Réduire le menu'}
            >
                {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
            </button>
            <div className="sidebar-logo">
                <div className="sidebar-logo-icon">
                    <Truck size={20} strokeWidth={2.5} />
                </div>
                <div className="sidebar-logo-text">
                    <h2>DeliveryForSure</h2>
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
                    <span className="menu-text">Tableau de bord</span>
                </NavLink>

                <NavLink to="/analytics">
                    <TrendingUp size={18} />
                    <span className="menu-text">Rapports</span>
                </NavLink>

                <div className="menu-section">OPÉRATIONS</div>
                <NavLink to="/expeditions">
                    <Package size={18} />
                    <span className="menu-text">Expéditions</span>
                </NavLink>
                <NavLink to="/clients">
                    <Users size={18} />
                    <span className="menu-text">Clients</span>
                </NavLink>
                <NavLink to="/tournees">
                    <MapPin size={18} />
                    <span className="menu-text">Tournées</span>
                </NavLink>
                <NavLink to="/incidents">
                    <AlertCircle size={18} />
                    <span className="menu-text">Incidents</span>
                </NavLink>
                <NavLink to="/alertes">
                    <Bell size={18} />
                    <span className="menu-text">Alertes</span>
                </NavLink>
                <NavLink to="/reclamations">
                    <FileText size={18} />
                    <span className="menu-text">Réclamations</span>
                </NavLink>

                <div className="menu-section">FACTURATION</div>
                <NavLink to="/factures">
                    <FileSpreadsheet size={18} />
                    <span className="menu-text">Factures</span>
                </NavLink>
                <NavLink to="/paiements">
                    <CreditCard size={18} />
                    <span className="menu-text">Paiements</span>
                </NavLink>

                <div className="menu-section">RÉFÉRENTIELS</div>
                <NavLink to="/chauffeurs">
                    <UserIcon size={18} />
                    <span className="menu-text">Chauffeurs</span>
                </NavLink>
                <NavLink to="/vehicules">
                    <Truck size={18} />
                    <span className="menu-text">Véhicules</span>
                </NavLink>
                <NavLink to="/destinations">
                    <MapPin size={18} />
                    <span className="menu-text">Destinations</span>
                </NavLink>

                {isAdmin && (
                    <>
                        <div className="menu-section">ADMINISTRATION</div>
                        <NavLink to="/admin/users">
                            <Settings size={18} />
                            <span className="menu-text">Utilisateurs</span>
                        </NavLink>
                        <NavLink to="/admin/audit">
                            <ScrollText size={18} />
                            <span className="menu-text">Journal d'Audit</span>
                        </NavLink>
                    </>
                )}
            </nav>

            <button onClick={onLogout} className="logout-btn">
                Paramètres
            </button>
        </div>
    );
};

export default Sidebar;
