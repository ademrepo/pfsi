import React from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, Package, Truck, Users, FileText, MapPin } from 'lucide-react';

const Dashboard = ({ user }) => {
    return (
        <div className="page-container">
            <div className="page-header">
                <h1>Tableau de Bord</h1>
                <p className="page-subtitle">
                    Aperçu global de votre activité logistique
                </p>
            </div>

            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">Total Expéditions</span>
                    </div>
                    <div className="stat-card-value">1,248</div>
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
                    <div className="stat-card-value">89</div>
                    <div className="stat-card-meta">
                        <span className="status-badge status-actif">ACTIF</span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">En transit</span>
                    </div>
                    <div className="stat-card-value">342</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <span className="stat-card-label">Retards</span>
                    </div>
                    <div className="stat-card-value">12</div>
                    <div className="stat-card-meta">
                        <span className="status-badge status-action-requise">ACTION REQUISE</span>
                    </div>
                </div>
            </div>

            <div style={{ marginBottom: '2rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '1.5rem' }}>
                    Accès Rapide
                </h2>
                <div className="stats-grid">
                    <Link to="/expeditions" style={{ textDecoration: 'none' }}>
                        <div className="stat-card">
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                                <div style={{ 
                                    width: '48px', 
                                    height: '48px', 
                                    background: 'var(--sidebar-active-bg)', 
                                    borderRadius: '12px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: 'var(--primary)'
                                }}>
                                    <Package size={24} />
                                </div>
                                <div>
                                    <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: '600', color: 'var(--text-main)' }}>
                                        Expéditions
                                    </h3>
                                    <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                        Gérez les envois
                                    </p>
                                </div>
                            </div>
                        </div>
                    </Link>

                    <Link to="/tournees" style={{ textDecoration: 'none' }}>
                        <div className="stat-card">
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                                <div style={{ 
                                    width: '48px', 
                                    height: '48px', 
                                    background: 'var(--status-transit-bg)', 
                                    borderRadius: '12px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: 'var(--status-transit-text)'
                                }}>
                                    <Truck size={24} />
                                </div>
                                <div>
                                    <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: '600', color: 'var(--text-main)' }}>
                                        Tournées
                                    </h3>
                                    <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                        Planifier les livraisons
                                    </p>
                                </div>
                            </div>
                        </div>
                    </Link>

                    <Link to="/clients" style={{ textDecoration: 'none' }}>
                        <div className="stat-card">
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                                <div style={{ 
                                    width: '48px', 
                                    height: '48px', 
                                    background: 'var(--status-delivered-bg)', 
                                    borderRadius: '12px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: 'var(--status-delivered-text)'
                                }}>
                                    <Users size={24} />
                                </div>
                                <div>
                                    <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: '600', color: 'var(--text-main)' }}>
                                        Clients
                                    </h3>
                                    <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                        Base clients
                                    </p>
                                </div>
                            </div>
                        </div>
                    </Link>

                    <Link to="/factures" style={{ textDecoration: 'none' }}>
                        <div className="stat-card">
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                                <div style={{ 
                                    width: '48px', 
                                    height: '48px', 
                                    background: '#DBEAFE', 
                                    borderRadius: '12px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: '#1E40AF'
                                }}>
                                    <FileText size={24} />
                                </div>
                                <div>
                                    <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: '600', color: 'var(--text-main)' }}>
                                        Facturation
                                    </h3>
                                    <p style={{ margin: 0, fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                        Factures et paiements
                                    </p>
                                </div>
                            </div>
                        </div>
                    </Link>
                </div>
            </div>

            <div style={{ marginTop: '3rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '1.5rem' }}>
                    Référentiels Métier
                </h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
                    <Link to="/chauffeurs" style={{ textDecoration: 'none' }}>
                        <div className="stat-card" style={{ textAlign: 'center', padding: '1.5rem' }}>
                            <div style={{ 
                                width: '56px', 
                                height: '56px', 
                                background: 'var(--bg-page)', 
                                borderRadius: '12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'var(--primary)',
                                margin: '0 auto 1rem'
                            }}>
                                <Users size={28} />
                            </div>
                            <h4 style={{ color: 'var(--text-main)', margin: 0, fontWeight: '600' }}>Chauffeurs</h4>
                        </div>
                    </Link>

                    <Link to="/vehicules" style={{ textDecoration: 'none' }}>
                        <div className="stat-card" style={{ textAlign: 'center', padding: '1.5rem' }}>
                            <div style={{ 
                                width: '56px', 
                                height: '56px', 
                                background: 'var(--bg-page)', 
                                borderRadius: '12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'var(--primary)',
                                margin: '0 auto 1rem'
                            }}>
                                <Truck size={28} />
                            </div>
                            <h4 style={{ color: 'var(--text-main)', margin: 0, fontWeight: '600' }}>Véhicules</h4>
                        </div>
                    </Link>

                    <Link to="/destinations" style={{ textDecoration: 'none' }}>
                        <div className="stat-card" style={{ textAlign: 'center', padding: '1.5rem' }}>
                            <div style={{ 
                                width: '56px', 
                                height: '56px', 
                                background: 'var(--bg-page)', 
                                borderRadius: '12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'var(--primary)',
                                margin: '0 auto 1rem'
                            }}>
                                <MapPin size={28} />
                            </div>
                            <h4 style={{ color: 'var(--text-main)', margin: 0, fontWeight: '600' }}>Destinations</h4>
                        </div>
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
