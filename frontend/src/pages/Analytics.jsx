import React, { useEffect, useMemo, useState } from 'react';
import api from '../api';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    BarChart,
    Bar,
    Legend,
} from 'recharts';

const formatPct = (v) => (v === null || v === undefined ? '-' : `${v}%`);

const Analytics = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const [start, setStart] = useState('');
    const [end, setEnd] = useState('');

    const fetchData = async () => {
        setLoading(true);
        setError('');
        try {
            const params = {};
            if (start) params.start = start;
            if (end) params.end = end;
            const res = await api.get('/analytics/advanced/', { params });
            setData(res.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Impossible de charger les analytics.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const series = useMemo(() => {
        if (!data) return [];
        const shipments = (data.shipments?.series || []).map((x) => ({ month: x.month.slice(0, 7), shipments: x.count }));
        const revenue = (data.revenue?.series || []).map((x) => ({ month: x.month.slice(0, 7), revenue: x.total }));
        const fuel = (data.fuel?.series || []).map((x) => ({ month: x.month.slice(0, 7), fuel: x.total }));
        const incidents = (data.incidents?.series || []).map((x) => ({ month: x.month.slice(0, 7), incidents: x.count }));

        const byMonth = new Map();
        shipments.forEach((s) => byMonth.set(s.month, { month: s.month, shipments: s.shipments }));
        revenue.forEach((r) => {
            const cur = byMonth.get(r.month) || { month: r.month };
            cur.revenue = r.revenue;
            byMonth.set(r.month, cur);
        });
        fuel.forEach((f) => {
            const cur = byMonth.get(f.month) || { month: f.month };
            cur.fuel = f.fuel;
            byMonth.set(f.month, cur);
        });
        incidents.forEach((i) => {
            const cur = byMonth.get(i.month) || { month: i.month };
            cur.incidents = i.incidents;
            byMonth.set(i.month, cur);
        });
        return Array.from(byMonth.values()).sort((a, b) => a.month.localeCompare(b.month));
    }, [data]);

    const mapModel = useMemo(() => {
        const pts = data?.map?.destination_points || [];
        if (!pts.length) return { points: [], center: [0, 0] };

        let latSum = 0;
        let lngSum = 0;
        let n = 0;
        pts.forEach((p) => {
            if (typeof p.latitude === 'number' && typeof p.longitude === 'number') {
                latSum += p.latitude;
                lngSum += p.longitude;
                n += 1;
            }
        });

        if (!n) return { points: [], center: [0, 0] };
        return { points: pts, center: [latSum / n, lngSum / n] };
    }, [data]);

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container"><div className="error">{error}</div></div>;
    if (!data) return null;

    const kpi = [
        { label: 'Expéditions', value: data.shipments?.total ?? 0, sub: `Croissance: ${formatPct(data.shipments?.growth_rate_percent)}` },
        { label: 'CA (TTC)', value: `${(data.revenue?.total_ttc ?? 0).toFixed(2)} €`, sub: `Croissance: ${formatPct(data.revenue?.growth_rate_percent)}` },
        { label: 'Tournées terminées', value: data.routes?.completed ?? 0, sub: `Croissance: ${formatPct(data.routes?.growth_rate_percent)}` },
        {
            label: 'Livraison',
            value: data.shipments?.success_rate_percent === null ? '-' : `${data.shipments?.success_rate_percent}%`,
            sub: `Livrées: ${data.shipments?.delivered ?? 0} | Échec: ${data.shipments?.failed ?? 0} | Retards: ${data.shipments?.delayed ?? 0}`,
        },
        {
            label: 'Retards',
            value: data.shipments?.delayed_rate_percent === null ? '-' : `${data.shipments?.delayed_rate_percent}%`,
            sub: `Taux échec: ${formatPct(data.shipments?.failed_rate_percent)}`,
        },
        {
            label: 'Carburant',
            value: data.fuel?.fuel_per_100km === null ? '-' : `${data.fuel?.fuel_per_100km} L/100km`,
            sub: `Total: ${(data.fuel?.total_liters ?? 0).toFixed(2)} L`,
        },
        {
            label: 'Coût moyen / tournée',
            value: data.operations?.avg_cost_per_route_estimated === null ? '-' : `${data.operations?.avg_cost_per_route_estimated} €`,
            sub: `Colis / tournée: ${data.operations?.avg_shipments_per_route ?? '-'}`,
        },
        {
            label: 'Marge (estim.)',
            value: data.profitability?.margin_percent === null ? '-' : `${data.profitability?.margin_percent}%`,
            sub: `Profit: ${(data.profitability?.profit_estimated ?? 0).toFixed(2)} €`,
        },
    ];

    return (
        <div className="page-container">
            <div className="header-actions">
                <div>
                    <h1 style={{ marginBottom: '0.5rem' }}>Analytics</h1>
                    <div style={{ color: 'var(--text-muted)' }}>
                        Période: {data.period?.start} → {data.period?.end}
                    </div>
                </div>

                <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'end', flexWrap: 'wrap' }}>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Début</label>
                        <input type="date" value={start} onChange={(e) => setStart(e.target.value)} />
                    </div>
                    <div>
                        <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Fin</label>
                        <input type="date" value={end} onChange={(e) => setEnd(e.target.value)} />
                    </div>
                    <button onClick={fetchData} style={{ height: '42px' }}>Appliquer</button>
                </div>
            </div>

            <div className="stats-grid" style={{ marginBottom: '2rem' }}>
                {kpi.map((x) => (
                    <div key={x.label} className="stat-card">
                        <h3 style={{ marginBottom: '0.5rem' }}>{x.label}</h3>
                        <div style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: '0.25rem' }}>{x.value}</div>
                        <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{x.sub}</div>
                    </div>
                ))}
            </div>

            <div className="stats-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                <div className="stat-card">
                    <h3 style={{ marginBottom: '1rem' }}>Expéditions (mensuel)</h3>
                    <div style={{ width: '100%', height: 280 }}>
                        <ResponsiveContainer>
                            <LineChart data={series} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="month" />
                                <YAxis />
                                <Tooltip />
                                <Line type="monotone" dataKey="shipments" stroke="#4f46e5" strokeWidth={2} dot={false} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="stat-card">
                    <h3 style={{ marginBottom: '1rem' }}>Chiffre d'affaires (mensuel)</h3>
                    <div style={{ width: '100%', height: 280 }}>
                        <ResponsiveContainer>
                            <BarChart data={series} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="month" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="revenue" fill="#10b981" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            <div className="stats-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
                <div className="stat-card">
                    <h3 style={{ marginBottom: '1rem' }}>Carburant (mensuel)</h3>
                    <div style={{ width: '100%', height: 280 }}>
                        <ResponsiveContainer>
                            <LineChart data={series} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="month" />
                                <YAxis />
                                <Tooltip />
                                <Line type="monotone" dataKey="fuel" stroke="#f59e0b" strokeWidth={2} dot={false} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="stat-card">
                    <h3 style={{ marginBottom: '1rem' }}>Incidents (mensuel)</h3>
                    <div style={{ width: '100%', height: 280 }}>
                        <ResponsiveContainer>
                            <LineChart data={series} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="month" />
                                <YAxis />
                                <Tooltip />
                                <Line type="monotone" dataKey="incidents" stroke="#ef4444" strokeWidth={2} dot={false} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            <div className="stats-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Top clients (volume)</th>
                                <th>Expéditions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(data.rankings?.top_customers_by_volume || []).map((r) => (
                                <tr key={r.client_id}>
                                    <td>{r.client_name}</td>
                                    <td>{r.shipments}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Top destinations</th>
                                <th>Expéditions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(data.rankings?.top_destinations || []).map((r) => (
                                <tr key={r.destination_id}>
                                    <td>{r.label}{r.zone ? ` (${r.zone})` : ''}</td>
                                    <td>{r.shipments}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="stats-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Top clients (CA)</th>
                                <th>CA</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(data.rankings?.top_customers_by_revenue || []).map((r) => (
                                <tr key={r.client_id}>
                                    <td>{r.client_name}</td>
                                    <td>{r.revenue.toFixed(2)} €</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Top chauffeurs</th>
                                <th>Tournées</th>
                                <th>Incidents</th>
                                <th>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(data.rankings?.top_drivers || []).map((r) => (
                                <tr key={r.chauffeur_id}>
                                    <td>{r.name}</td>
                                    <td>{r.tournees_completed}</td>
                                    <td>{r.incidents}</td>
                                    <td>{r.score}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="stats-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Zones (activité)</th>
                                <th>Expéditions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(data.zones?.top_by_shipments || []).map((r) => (
                                <tr key={r.zone}>
                                    <td>{r.zone}</td>
                                    <td>{r.shipments}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Zones (incidents)</th>
                                <th>Incidents</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(data.zones?.top_by_incidents || []).map((r) => (
                                <tr key={r.zone}>
                                    <td>{r.zone}</td>
                                    <td>{r.incidents}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="stats-grid" style={{ gridTemplateColumns: '1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Prévision staffing (3 mois)</th>
                                <th>Colis (prévu)</th>
                                <th>Véhicules</th>
                                <th>Chauffeurs</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(data.staffing?.forecast_next_3_months || []).map((r) => (
                                <tr key={r.month}>
                                    <td>{r.month.slice(0, 7)}</td>
                                    <td>{r.forecast_shipments}</td>
                                    <td>{r.required_vehicles ?? '-'}</td>
                                    <td>{r.required_drivers ?? '-'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="stats-grid" style={{ gridTemplateColumns: '1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Profitabilité par service (estim.)</th>
                                <th>Colis</th>
                                <th>CA estimé</th>
                                <th>Coût estimé</th>
                                <th>Profit estimé</th>
                                <th>Marge</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(data.profitability?.by_service_type || []).map((r) => (
                                <tr key={r.type_service_id || r.type_service}>
                                    <td>{r.type_service}</td>
                                    <td>{r.shipments}</td>
                                    <td>{(r.revenue_estimated ?? 0).toFixed(2)} €</td>
                                    <td>{(r.cost_estimated ?? 0).toFixed(2)} €</td>
                                    <td>{(r.profit_estimated ?? 0).toFixed(2)} €</td>
                                    <td>{r.margin_percent === null || r.margin_percent === undefined ? '-' : `${r.margin_percent}%`}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="stats-grid" style={{ gridTemplateColumns: '1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
                <div className="stat-card">
                    <h3 style={{ marginBottom: '1rem' }}>Carte (destinations)</h3>
                    {mapModel.points.length ? (
                        <div style={{ width: '100%', height: 420, borderRadius: 12, overflow: 'hidden' }}>
                            <MapContainer center={mapModel.center} zoom={5} style={{ height: '100%', width: '100%' }}>
                                <TileLayer
                                    attribution='&copy; OpenStreetMap contributors'
                                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                />
                                {mapModel.points.map((p) => (
                                    <CircleMarker
                                        key={p.destination_id}
                                        center={[p.latitude, p.longitude]}
                                        radius={6}
                                        pathOptions={{ color: '#4f46e5' }}
                                    >
                                        <Popup>
                                            <div style={{ fontWeight: 700, marginBottom: 6 }}>{p.label}</div>
                                            <div>Zone: {p.zone || 'N/A'}</div>
                                            <div>Expéditions: {p.shipments}</div>
                                            <div>Incidents: {p.incidents}</div>
                                        </Popup>
                                    </CircleMarker>
                                ))}
                            </MapContainer>
                        </div>
                    ) : (
                        <div style={{ color: 'var(--text-muted)' }}>
                            Aucune destination géolocalisée (latitude/longitude manquants).
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Analytics;
