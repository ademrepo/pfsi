import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard = ({ user }) => {
    return (
        <div className="page-container">
            <div className="dashboard-header" style={{ marginBottom: '2.5rem' }}>
                <h1 style={{ margin: 0 }}>Bonjour, {user?.full_name || user?.username} 👋</h1>
                <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                    Voici l'état actuel de votre plateforme de gestion de transport.
                </p>
            </div>

            <div className="stats-grid">
                <div className="stat-card">
                    <span style={{ fontSize: '2rem', marginBottom: '1rem', display: 'block' }}>📦</span>
                    <h3 style={{ marginBottom: '0.5rem' }}>Expéditions</h3>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
                        Gérez les envois, le tracking et la facturation.
                    </p>
                    <div style={{ display: 'flex', gap: '0.75rem' }}>
                        <Link to="/expeditions/nouveau" className="btn-primary" style={{ textDecoration: 'none', padding: '0.5rem 1rem' }}>+ Nouveau</Link>
                        <Link to="/expeditions" className="btn-primary" style={{ textDecoration: 'none', background: 'var(--bg-main)', color: 'var(--text-main)', padding: '0.5rem 1rem', border: '1px solid var(--border)' }}>Consulter</Link>
                    </div>
                </div>

                <div className="stat-card">
                    <span style={{ fontSize: '2rem', marginBottom: '1rem', display: 'block' }}>🚚</span>
                    <h3 style={{ marginBottom: '0.5rem' }}>Tournées</h3>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
                        Organisez et affectez vos livraisons aux chauffeurs.
                    </p>
                    <div style={{ display: 'flex', gap: '0.75rem' }}>
                        <Link to="/tournees/nouveau" className="btn-primary" style={{ textDecoration: 'none', padding: '0.5rem 1rem' }}>+ Planifier</Link>
                        <Link to="/tournees" className="btn-primary" style={{ textDecoration: 'none', background: 'var(--bg-main)', color: 'var(--text-main)', padding: '0.5rem 1rem', border: '1px solid var(--border)' }}>Journal</Link>
                    </div>
                </div>

                <div className="stat-card">
                    <span style={{ fontSize: '2rem', marginBottom: '1rem', display: 'block' }}>📈</span>
                    <h3 style={{ marginBottom: '0.5rem' }}>Statistiques</h3>
                    <div style={{ marginTop: '1rem' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Missions en cours</span>
                            <span className="status-badge status-Validé">En attente</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Taux de livraison</span>
                            <span style={{ fontWeight: '600' }}>94%</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="section-header" style={{ marginTop: '3rem', marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: '700' }}>Référentiels Métier</h2>
            </div>

            <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
                <Link to="/chauffeurs" style={{ textDecoration: 'none' }}>
                    <div className="stat-card" style={{ textAlign: 'center', transition: 'transform 0.2s' }}>
                        <span style={{ fontSize: '1.5rem' }}>👨‍✈️</span>
                        <h4 style={{ color: 'var(--text-main)', marginTop: '0.5rem' }}>Chauffeurs</h4>
                    </div>
                </Link>
                <Link to="/vehicules" style={{ textDecoration: 'none' }}>
                    <div className="stat-card" style={{ textAlign: 'center', transition: 'transform 0.2s' }}>
                        <span style={{ fontSize: '1.5rem' }}>🚛</span>
                        <h4 style={{ color: 'var(--text-main)', marginTop: '0.5rem' }}>Véhicules</h4>
                    </div>
                </Link>
                <Link to="/destinations" style={{ textDecoration: 'none' }}>
                    <div className="stat-card" style={{ textAlign: 'center', transition: 'transform 0.2s' }}>
                        <span style={{ fontSize: '1.5rem' }}>📍</span>
                        <h4 style={{ color: 'var(--text-main)', marginTop: '0.5rem' }}>Destinations</h4>
                    </div>
                </Link>
            </div>
        </div>
    );
};

export default Dashboard;
