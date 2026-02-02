import React, { useState, useEffect, useMemo, useRef } from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, Printer, Plus, Calendar, MoreVertical, Trash2 } from 'lucide-react';
import api from '../api';

const PAGE_SIZE = 10;
const JOURS = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];

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

const Dashboard = ({ user }) => {
  const [tableTab, setTableTab] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [dateFilter, setDateFilter] = useState(() => {
    const d = new Date();
    return { year: d.getFullYear(), month: d.getMonth() + 1 };
  });
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [expeditions, setExpeditions] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const datePickerRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (datePickerRef.current && !datePickerRef.current.contains(e.target)) {
        setShowDatePicker(false);
      }
    };
    if (showDatePicker) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [showDatePicker]);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const [expRes, anaRes] = await Promise.all([
          api.get('/expeditions/'),
          api.get('/analytics/summary/').catch(() => ({ data: null })),
        ]);
        if (cancelled) return;
        setExpeditions(Array.isArray(expRes.data) ? expRes.data : []);
        setAnalytics(anaRes.data);
      } catch (e) {
        if (!cancelled) setError(e.message || 'Erreur chargement');
        if (!cancelled) setExpeditions([]);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => { cancelled = true; };
  }, []);

  const stats = useMemo(() => {
    const list = expeditions;
     
     
    const count = (matches) => list.filter(e => matches.includes((e.statut || '').toLowerCase())).length;

    return {
      total: list.length,
      enCours: count(['en_livraison', 'en cours de livraison']),
      enTransit: count(['en_transit', 'en transit']),
      centreTri: count(['centre_tri', 'en centre de tri']),
      livres: count(['livre', 'livré']),
      retards: count(['echec_livraison', 'échec de livraison']),
    };
  }, [expeditions]);

  const growthPercent = analytics?.shipments?.growth_rate_percent ?? 12;

  const tabs = useMemo(
    () => [
      { id: 'all', label: `Tous (${stats.total})` },
      { id: 'transit', label: `En transit (${stats.enTransit})` },
      { id: 'sorting', label: `En centre de tri (${stats.centreTri})` },
      { id: 'delivered', label: `Livrés (${stats.livres})` },
      { id: 'delayed', label: `Retards (${stats.retards})` },
    ],
    [stats]
  );

  const filteredByTab = useMemo(() => {
    const norm = (s) => (s || '').toLowerCase();
    if (tableTab === 'all') return expeditions;
    if (tableTab === 'transit') return expeditions.filter((e) => ['en_transit', 'en transit'].includes(norm(e.statut)));
    if (tableTab === 'sorting') return expeditions.filter((e) => ['centre_tri', 'en centre de tri'].includes(norm(e.statut)));
    if (tableTab === 'delivered') return expeditions.filter((e) => ['livre', 'livré', 'livrÃ©'].includes(norm(e.statut)));  
    if (tableTab === 'delayed') return expeditions.filter((e) => ['echec_livraison', 'échec de livraison'].includes(norm(e.statut)));
    return expeditions;
  }, [expeditions, tableTab]);

  const filteredByDate = useMemo(() => {
    const { year, month } = dateFilter;
    return filteredByTab.filter((e) => {
      if (!e.date_creation) return true;
      const d = new Date(e.date_creation);
      return d.getFullYear() === year && d.getMonth() + 1 === month;
    });
  }, [filteredByTab, dateFilter]);

  const totalFiltered = filteredByDate.length;
  const totalPages = Math.max(1, Math.ceil(totalFiltered / PAGE_SIZE));
  const page = Math.min(currentPage, totalPages);
  const start = (page - 1) * PAGE_SIZE;
  const pageRows = filteredByDate.slice(start, start + PAGE_SIZE);

  const handleExport = () => {
    window.print();
  };

  const handleDateChange = (year, month) => {
    setDateFilter({ year, month });
    setShowDatePicker(false);
    setCurrentPage(1);
  };

  const volumeByDay = useMemo(() => {
    const { year, month } = dateFilter;
    const inMonth = expeditions.filter((e) => {
      if (!e.date_creation) return false;
      const d = new Date(e.date_creation);
      return d.getFullYear() === year && d.getMonth() + 1 === month;
    });
    const counts = [0, 0, 0, 0, 0, 0, 0];
    const today = new Date();
    let todayWeekday = today.getDay();
    if (todayWeekday === 0) todayWeekday = 7;
    todayWeekday -= 1;

    inMonth.forEach((e) => {
      const d = new Date(e.date_creation);
      let w = d.getDay();
      if (w === 0) w = 7;
      w -= 1;
      counts[w] += 1;
    });

    const max = Math.max(1, ...counts);
    return JOURS.map((label, i) => ({
      label,
      height: Math.round((counts[i] / max) * 100),
      active: i === todayWeekday && dateFilter.month === today.getMonth() + 1 && dateFilter.year === today.getFullYear(),
    }));
  }, [expeditions, dateFilter]);

  const regionData = useMemo(() => {
    const dests = analytics?.rankings?.top_destinations ?? [];
    const byZone = {};
    dests.forEach((d) => {
      const z = d.zone || 'N/A';
      byZone[z] = (byZone[z] || 0) + (d.shipments || 0);
    });
    const arr = Object.entries(byZone)
      .map(([name, shipments]) => ({ name, shipments }))
      .sort((a, b) => b.shipments - a.shipments)
      .slice(0, 10);
    const total = arr.reduce((s, r) => s + r.shipments, 0) || 1;
    return arr.map((r) => ({ ...r, pct: Math.round((r.shipments / total) * 100) }));
  }, [analytics]);

  const months = [];
  for (let y = new Date().getFullYear(); y >= new Date().getFullYear() - 2; y--) {
    for (let m = 12; m >= 1; m--) {
      months.push({ year: y, month: m, label: new Date(y, m - 1, 1).toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' }) });
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Voulez-vous vraiment supprimer cette expédition ?')) {
      try {
        await api.delete(`/expeditions/${id}/`);
         
        setExpeditions(current => current.filter(e => e.id !== id));
      } catch (err) {
        const errorMsg = err.response?.data?.[0] || "Impossible de supprimer cette expédition (déjà liée à une tournée).";
        alert(errorMsg);
      }
    }
  };

  if (loading && expeditions.length === 0) {
    return (
      <div className="page-container">
        <p style={{ color: 'var(--text-muted)' }}>Chargement du tableau de bord…</p>
      </div>
    );
  }

  return (
    <div className="page-container dashboard-print-area">
      <header className="dashboard-header">
        <div>
          <h1>Tableau de Bord</h1>
          <p className="page-subtitle">Aperçu global de votre activité logistique</p>
        </div>
        <div className="dashboard-header-actions">
          <button type="button" className="dashboard-btn-export" onClick={handleExport}>
            <Printer size={18} />
            Imprimer
          </button>
          <Link to="/expeditions/nouveau" className="dashboard-btn-create">
            <Plus size={18} />
            Créer une expédition
          </Link>
        </div>
      </header>

      {error && (
        <p style={{ color: 'var(--status-delayed-text)', marginBottom: '1rem' }}>{error}</p>
      )}

      <div className="dashboard-kpi-grid">
        <div className="dashboard-card">
          <p className="dashboard-kpi-label" style={{ color: 'var(--text-main)' }}>Total Expéditions</p>
          <div className="dashboard-kpi-row">
            <span className="dashboard-kpi-value dashboard-kpi-value--gold">{stats.total.toLocaleString('fr-FR')}</span>
            <span className="dashboard-badge-green">
              <TrendingUp size={12} />
              {typeof growthPercent === 'number' ? `${growthPercent}%` : '12%'}
            </span>
          </div>
        </div>
        <div className="dashboard-card">
          <p className="dashboard-kpi-label">En cours de livraison</p>
          <div className="dashboard-kpi-row">
            <span className="dashboard-kpi-value">{stats.enCours}</span>
            <span className="dashboard-badge-primary">Actif</span>
          </div>
        </div>
        <div className="dashboard-card">
          <p className="dashboard-kpi-label">En transit</p>
          <div className="dashboard-kpi-row">
            <span className="dashboard-kpi-value">{stats.enTransit}</span>
          </div>
        </div>
        <div className="dashboard-card">
          <p className="dashboard-kpi-label">Retards</p>
          <div className="dashboard-kpi-row">
            <span className="dashboard-kpi-value">{stats.retards}</span>
            <span className="dashboard-badge-accent">Action requise</span>
          </div>
        </div>
      </div>

      <div className="dashboard-table-card">
        <div className="dashboard-table-toolbar">
          <div className="dashboard-table-tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                type="button"
                className={`tab ${tableTab === tab.id ? 'active' : ''}`}
                onClick={() => {
                  setTableTab(tab.id);
                  setCurrentPage(1);
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>
          <div className="dashboard-table-toolbar-right" ref={datePickerRef}>
            <div
              className="dashboard-date-pill"
              onClick={() => setShowDatePicker((v) => !v)}
              onKeyDown={(e) => e.key === 'Enter' && setShowDatePicker((v) => !v)}
              role="button"
              tabIndex={0}
              aria-expanded={showDatePicker}
              aria-haspopup="listbox"
            >
              <Calendar size={18} style={{ color: 'var(--text-muted)' }} />
              <span>
                {new Date(dateFilter.year, dateFilter.month - 1, 1).toLocaleDateString('fr-FR', {
                  month: 'short',
                  year: 'numeric',
                })}
              </span>
              <span style={{ opacity: 0.6 }}>▾</span>
            </div>
            {showDatePicker && (
              <div className="dashboard-date-dropdown" role="listbox">
                {months.slice(0, 24).map(({ year, month, label }) => (
                  <button
                    key={`${year}-${month}`}
                    type="button"
                    className="dashboard-date-option"
                    onClick={() => handleDateChange(year, month)}
                    role="option"
                  >
                    {label}
                  </button>
                ))}
              </div>
            )}

          </div>
        </div>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>N° de suivi</th>
                <th>Expéditeur</th>
                <th>Destinataire</th>
                <th style={{ color: 'var(--text-main)' }}>Date de l’expédition</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {pageRows.map((exp) => {
                const clientLabel = exp.client_details
                  ? [exp.client_details.nom, exp.client_details.prenom].filter(Boolean).join(' ')
                  : 'Inconnu';
                const destVille = exp.destination_details?.ville ?? '—';
                const destPays = exp.destination_details?.pays ?? '';
                const dateStr = exp.date_creation
                  ? new Date(exp.date_creation).toLocaleDateString('fr-FR', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric',
                  })
                  : '—';
                const timeStr = exp.date_creation
                  ? new Date(exp.date_creation).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
                  : '';
                const service = exp.type_service_details?.libelle || '—';

                const { label: statusLabel, className: statusClass } = getStatusInfo(exp.statut);

                return (
                  <tr key={exp.id}>
                    <td>
                      <Link
                        to={`/expeditions/${exp.id}/edit`}
                        style={{
                          fontWeight: 700,
                          color: 'var(--text-main)',
                          textDecoration: 'none',
                          fontSize: '0.875rem',
                        }}
                      >
                        {exp.code_expedition}
                      </Link>
                      <p className="table-secondary-text" style={{ margin: 0 }}>{service}</p>
                    </td>
                    <td>
                      <Link
                        to={`/expeditions/${exp.id}/edit`}
                        style={{
                          fontWeight: 600,
                          color: 'var(--text-main)',
                          textDecoration: 'none',
                          fontSize: '0.875rem',
                        }}
                      >
                        {clientLabel}
                      </Link>
                      <p className="table-secondary-text" style={{ margin: 0 }}>
                        {exp.client_details?.ville ?? exp.destination_details?.ville ?? 'N/A'}
                      </p>
                    </td>
                    <td>
                      <p style={{ fontWeight: 600, color: 'var(--text-main)', margin: 0, fontSize: '0.875rem' }}>
                        {destVille}
                      </p>
                      <p className="table-secondary-text" style={{ margin: 0 }}>{destPays}</p>
                    </td>
                    <td>
                      <p style={{ fontWeight: 600, color: 'var(--text-main)', margin: 0, fontSize: '0.875rem' }}>
                        {dateStr}
                      </p>
                      <p className="table-secondary-text" style={{ margin: 0 }}>{timeStr}</p>
                    </td>
                    <td>
                      <span className={`status-badge ${statusClass}`}>{statusLabel}</span>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <Link
                          to={`/expeditions/${exp.id}/edit`}
                          className="btn-icon"
                          title="Voir / modifier"
                          style={{ display: 'inline-flex' }}
                        >
                          <MoreVertical size={20} />
                        </Link>
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
                );
              })}
              {pageRows.length === 0 && (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                    Aucune expédition pour cette sélection.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="dashboard-table-footer">
          <p>
            Affichage de <strong style={{ color: 'var(--text-main)' }}>{totalFiltered === 0 ? 0 : start + 1}</strong>{' '}
            à <strong style={{ color: 'var(--text-main)' }}>{Math.min(start + PAGE_SIZE, totalFiltered)}</strong> sur{' '}
            <strong style={{ color: 'var(--text-main)' }}>{totalFiltered.toLocaleString('fr-FR')}</strong> résultats
          </p>
          <div className="pagination-btns">
            <button
              disabled={page <= 1}
              onClick={(e) => {
                e.preventDefault();
                setCurrentPage(p => Math.max(1, p - 1));
              }}
            >
              Précédent
            </button>
            <button
              disabled={page >= totalPages}
              onClick={(e) => {
                e.preventDefault();
                setCurrentPage(p => Math.min(totalPages, p + 1));
              }}
            >
              Suivant
            </button>
          </div>
        </div>
      </div>

      <div className="dashboard-charts-grid">
        <div className="dashboard-chart-card">
          <h3 className="dashboard-chart-title">Volume des Expéditions</h3>
          <div className="dashboard-volume-bars">
            {Array.isArray(volumeByDay) && volumeByDay.length > 0 && volumeByDay.map((d) => (
              <div
                key={d.label}
                className={`dashboard-volume-bar ${d.active ? 'dashboard-volume-bar--active' : ''}`}
                style={{ height: `${Math.max(8, d.height)}%` }}
                title={d.active ? `${d.label} (Aujourd'hui)` : d.label}
              />
            ))}
          </div>
          <div className="dashboard-volume-labels">
            {Array.isArray(volumeByDay) && volumeByDay.map((d) => (
              <span key={d.label} style={d.active ? { color: 'var(--primary)' } : {}}>
                {d.label}
              </span>
            ))}
          </div>
        </div>

        <div className="dashboard-chart-card">
          <h3 className="dashboard-chart-title">Répartition par région</h3>
          <div className="dashboard-region-list">
            {!Array.isArray(regionData) || regionData.length === 0 ? (
              <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                Aucune donnée pour la période.
              </p>
            ) : (
              regionData.map((r, idx) => {
                const maxPct = Math.max(...regionData.map((x) => x.pct), 1);
                const isFirst = r.pct === maxPct;
                const isLast = idx === regionData.length - 1 && regionData.length > 1;
                let fillClass = 'dashboard-region-bar-fill';
                if (isFirst) fillClass += ' dashboard-region-bar-fill--gold';
                else if (isLast && regionData.length >= 3) fillClass += ' dashboard-region-bar-fill--neutral';
                else fillClass += ' dashboard-region-bar-fill--accent';
                return (
                  <div key={r.name} className="dashboard-region-item">
                    <div className="dashboard-region-item-head">
                      <span>{r.name}</span>
                      <span style={{ color: 'var(--text-main)' }}>{r.pct}%</span>
                    </div>
                    <div className="dashboard-region-bar">
                      <div className={fillClass} style={{ width: `${r.pct}%` }} />
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
