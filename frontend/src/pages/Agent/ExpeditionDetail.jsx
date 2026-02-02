import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
    Package,
    Search,
    Bell,
    Printer,
    ChevronRight,
    Home,
    Truck,
    Check,
    MapPin,
    Clock,
    Edit,
    ShieldCheck,
    Download,
    ArrowLeft
} from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

 
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34]
});
L.Marker.prototype.options.icon = DefaultIcon;

import api from '../../api';

const ExpeditionDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [expedition, setExpedition] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchId, setSearchId] = useState('');

    useEffect(() => {
        fetchExpedition();
    }, [id]);

    const fetchExpedition = async () => {
        try {
            const response = await api.get(`/expeditions/${id}/`);
            setExpedition(response.data);
            setLoading(false);
        } catch (err) {
            setError('Erreur lors du chargement des détails de l\'expédition.');
            setLoading(false);
        }
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container error">{error}</div>;
    if (!expedition) return <div className="page-container">Expédition non trouvée.</div>;

    const getStatusStyle = (status) => {
        const norm = (status || '').toString().toLowerCase().trim();
         
        if (norm.includes('échec') || norm.includes('echec') || norm.includes('retard')) return { bg: '#FEF2F2', text: '#DC2626' };
        if (norm.includes('livraison') || norm.includes('cours')) return { bg: '#E0F2F1', text: '#00695C' };
        if (norm.includes('livr')) return { bg: '#E8F5E9', text: '#2E7D32' };
        if (norm.includes('centre')) return { bg: '#EFEBE9', text: '#5D4037' };
        if (norm.includes('transit')) return { bg: '#E0F7FA', text: '#00838F' };
        if (norm.includes('enregistre') || norm.includes('neutre')) return { bg: '#F5F5F5', text: '#757575' };
        return { bg: '#F5F5F5', text: '#757575' };
    };

    const statusStyle = getStatusStyle(expedition.statut);

     
    const creationDate = new Date(expedition.date_creation);
    const estimatedDate = new Date(creationDate);
    estimatedDate.setDate(creationDate.getDate() + 2);
    const estimatedDateStr = estimatedDate.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });

    return (
        <div style={{ background: '#f8f9fa', minHeight: '100vh' }}>
            { }
            <section style={{ background: 'white', padding: '3rem 2rem', borderBottom: '1px solid #e5e7eb' }}>
                <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
                    <button
                        onClick={() => navigate('/expeditions')}
                        style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b', fontSize: '0.875rem', marginBottom: '1.5rem', border: 'none', background: 'none', cursor: 'pointer', padding: 0 }}
                    >
                        <ArrowLeft size={16} /> Retour à la liste
                    </button>

                    <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'flex-end', justifyContent: 'space-between', gap: '1.5rem' }}>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                            <span style={{ fontSize: '0.75rem', fontWeight: '600', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.1em', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <Package size={14} /> {expedition.type_service_details?.libelle || 'Colis Standard'}
                            </span>
                            <h1 style={{ fontSize: '2.5rem', fontWeight: '800', color: '#0f172a', letterSpacing: '-0.02em', margin: 0 }}>
                                {expedition.code_expedition}
                            </h1>
                        </div>



                        <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1rem' }}>
                            <button
                                onClick={() => window.print()}
                                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.625rem 1.25rem', fontSize: '0.875rem', fontWeight: '600', border: '1px solid #e2e8f0', borderRadius: '8px', background: 'white', cursor: 'pointer', color: '#0f172a' }}
                            >
                                <Printer size={18} /> Imprimer l'expédition
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Content Area */}
            <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '3rem 2rem' }}>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '2.5rem' }}>

                    {/* Left Column: Timeline and History */}
                    <div style={{ gridColumn: 'span 7' }}>
                        <div style={{ background: 'white', borderRadius: '12px', border: '1px solid #e2e8f0', overflow: 'hidden', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}>
                            <div style={{ padding: '1.5rem', borderBottom: '1px solid #f1f5f9', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h2 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#1e293b', textTransform: 'uppercase', letterSpacing: '0.025em', margin: 0 }}>
                                    Avancement de l'expédition
                                </h2>
                                <span style={{
                                    background: statusStyle.bg,
                                    color: statusStyle.text,
                                    padding: '0.375rem 1rem',
                                    borderRadius: '9999px',
                                    fontSize: '0.625rem',
                                    fontWeight: '800',
                                    textTransform: 'uppercase',
                                    letterSpacing: '0.1em'
                                }}>
                                    {expedition.statut}
                                </span>
                            </div>

                            <div style={{ padding: '2.5rem', position: 'relative' }}>
                                { }
                                <div style={{ position: 'absolute', top: '2.5rem', bottom: '2.5rem', left: 'calc(2.5rem + 15px)', width: '2px', background: '#e2e8f0' }} />

                                <div style={{ display: 'flex', flexDirection: 'column', gap: '3.5rem' }}>

                                    { }
                                    { }

                                    { }
                                    <div style={{ position: 'relative', paddingLeft: '3rem', opacity: expedition.statut === 'Livré' ? 1 : 0.4 }}>
                                        <div style={{ position: 'absolute', left: 0, top: 0, width: '32px', height: '32px', borderRadius: '50%', background: 'white', border: '2px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1, backgroundColor: expedition.statut === 'Livré' ? '#351c15' : 'white' }}>
                                            <Home size={14} color={expedition.statut === 'Livré' ? 'white' : '#94a3b8'} />
                                        </div>
                                        <div>
                                            <h3 style={{ fontSize: '1rem', fontWeight: '600', color: '#0f172a', margin: 0 }}>Livré (Destination finale)</h3>
                                            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0.25rem 0' }}>{expedition.adresse_livraison}</p>
                                        </div>
                                    </div>

                                    { }
                                    <div style={{ position: 'relative', paddingLeft: '3rem' }}>
                                        <div style={{
                                            position: 'absolute',
                                            left: 0,
                                            top: 0,
                                            width: '32px',
                                            height: '32px',
                                            borderRadius: '50%',
                                            background: '#e3b12a',  
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            zIndex: 1,
                                            boxShadow: '0 10px 15px -3px rgb(227 177 42 / 0.3)',
                                            outline: '4px solid rgb(227 177 42 / 0.1)'
                                        }}>
                                            <Truck size={14} color="white" />
                                        </div>
                                        <div>
                                            <h3 style={{ fontSize: '1rem', fontWeight: '700', color: '#e3b12a', margin: 0 }}>{expedition.statut}</h3>
                                            <p style={{ fontSize: '0.875rem', fontWeight: '600', color: '#1e293b', margin: '0.25rem 0' }}>En temps réel</p>
                                            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0.5rem 0', lineHeight: 1.5 }}>
                                                {expedition.description_colis || "L'expédition est en cours de traitement par nos services."}
                                            </p>
                                        </div>
                                    </div>

                                    { }
                                    <div style={{ position: 'relative', paddingLeft: '3rem' }}>
                                        <div style={{ position: 'absolute', left: 0, top: 0, width: '32px', height: '32px', borderRadius: '50%', background: '#f1f5f9', border: '2px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1 }}>
                                            <Check size={14} color="#64748b" />
                                        </div>
                                        <div>
                                            <h3 style={{ fontSize: '1rem', fontWeight: '600', color: '#0f172a', margin: 0 }}>Expédiée</h3>
                                            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0.25rem 0' }}>
                                                {new Date(expedition.date_creation).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })} • {expedition.client_details?.ville || 'Origine'}
                                            </p>
                                        </div>
                                    </div>

                                </div>
                            </div>
                        </div>

                        { }
                        <div style={{ background: 'white', borderRadius: '12px', border: '1px solid #e2e8f0', overflow: 'hidden', marginTop: '2.5rem', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}>
                            <div style={{ padding: '1.5rem', borderBottom: '1px solid #f1f5f9', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h2 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#1e293b', textTransform: 'uppercase', letterSpacing: '0.025em', margin: 0 }}>
                                    Historique complet
                                </h2>
                                <button
                                    onClick={() => window.print()}
                                    style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: '#351c15', fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.1em', cursor: 'pointer', border: 'none', background: 'none' }}
                                >
                                    <Printer size={14} /> Imprimer
                                </button>
                            </div>
                            <div style={{ overflowX: 'auto' }}>
                                <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
                                    <thead>
                                        <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                                            <th style={{ padding: '1rem 2rem', fontSize: '0.625rem', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase' }}>Date / Heure</th>
                                            <th style={{ padding: '1rem 2rem', fontSize: '0.625rem', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase' }}>Lieu</th>
                                            <th style={{ padding: '1rem 2rem', fontSize: '0.625rem', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase' }}>Activité</th>
                                        </tr>
                                    </thead>
                                    <tbody style={{ fontSize: '0.875rem' }}>
                                        { }
                                        {(expedition.tracking_history || []).length > 0 ? (
                                            expedition.tracking_history.map((t, idx) => (
                                                <tr key={idx} style={{ borderBottom: '1px solid #f8fafc' }}>
                                                    <td style={{ padding: '1.25rem 2rem', fontWeight: '600' }}>
                                                        {new Date(t.date_statut || t.created_at).toLocaleString('fr-FR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })}
                                                    </td>
                                                    <td style={{ padding: '1.25rem 2rem', color: '#64748b' }}>{t.lieu || 'Transit'}</td>
                                                    <td style={{ padding: '1.25rem 2rem' }}>
                                                        <span style={{ display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: '#e3b12a', marginRight: '0.5rem' }}></span>
                                                        {t.statut}
                                                    </td>
                                                </tr>
                                            ))
                                        ) : (
                                            <tr style={{ borderBottom: '1px solid #f8fafc' }}>
                                                <td style={{ padding: '1.25rem 2rem', fontWeight: '600' }}>
                                                    {new Date(expedition.date_creation).toLocaleString('fr-FR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })}
                                                </td>
                                                <td style={{ padding: '1.25rem 2rem', color: '#64748b' }}>{expedition.client_details?.ville || '-'}</td>
                                                <td style={{ padding: '1.25rem 2rem' }}>
                                                    <span style={{ display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: '#e3b12a', marginRight: '0.5rem' }}></span>
                                                    Enregistré
                                                </td>
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    { }
                    <div style={{ gridColumn: 'span 5', display: 'flex', flexDirection: 'column', gap: '2rem' }}>

                        <div style={{ background: 'white', borderRadius: '12px', border: '1px solid #e2e8f0', overflow: 'hidden', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}>
                            <div style={{ position: 'relative', height: '128px', background: '#FDF5E6', display: 'flex', alignItems: 'center', padding: '2rem' }}>
                                <div style={{ position: 'absolute', inset: 0, opacity: 0.1, background: 'linear-gradient(45deg, transparent 25%, rgba(0,0,0,0.05) 50%, transparent 75%)', backgroundSize: '100px 100px' }} />
                                <h2 style={{ color: '#351c15', fontSize: '1.25rem', fontWeight: '700', textTransform: 'uppercase', margin: 0, zIndex: 1, transform: 'translateY(-2px)' }}>
                                    Informations de livraison
                                </h2>
                            </div>

                            <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
                                <div>
                                    <span style={{ fontSize: '0.625rem', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.2em' }}>Date Estimée</span>
                                    <h3 style={{ fontSize: '1.875rem', fontWeight: '800', color: '#e3b12a', marginTop: '0.5rem', margin: '0.5rem 0' }}>{estimatedDateStr}</h3>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b', fontSize: '0.875rem' }}>
                                        <Clock size={14} /> Avant 19:00
                                    </div>
                                </div>

                                <div style={{ display: 'flex', gap: '1rem' }}>
                                    <div style={{ marginTop: '0.25rem' }}>
                                        <MapPin color="#e3b12a" />
                                    </div>
                                    <div>
                                        <span style={{ fontSize: '0.625rem', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.2em' }}>Destinataire</span>
                                        <p style={{ fontWeight: '700', color: '#1e293b', fontSize: '1rem', marginTop: '0.25rem', marginBottom: '0.25rem' }}>{expedition.nom_destinataire || expedition.client_details?.nom}</p>
                                        <p style={{ fontSize: '0.875rem', color: '#64748b', lineHeight: 1.5, margin: 0 }}>
                                            {expedition.adresse_livraison}<br />
                                            {expedition.destination_details?.ville}, {expedition.destination_details?.pays}
                                        </p>
                                    </div>
                                </div>

                                <div style={{
                                    height: '220px',
                                    borderRadius: '12px',
                                    background: '#f1f5f9',
                                    border: '1px solid #e2e8f0',
                                    position: 'relative',
                                    overflow: 'hidden'
                                }}>
                                    {expedition.destination_details?.latitude ? (
                                        <MapContainer
                                            center={[expedition.destination_details.latitude, expedition.destination_details.longitude]}
                                            zoom={13}
                                            style={{ height: '100%', width: '100%', zIndex: 0 }}
                                            zoomControl={false}
                                        >
                                            <TileLayer
                                                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                            />
                                            <Marker position={[expedition.destination_details.latitude, expedition.destination_details.longitude]}>
                                                <Popup>
                                                    <b>Destination</b><br />
                                                    {expedition.destination_details.ville}, {expedition.destination_details.pays}
                                                </Popup>
                                            </Marker>
                                        </MapContainer>
                                    ) : (
                                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', gap: '1rem' }}>
                                            <MapPin size={32} color="#94a3b8" />
                                            <div style={{ textAlign: 'center', padding: '0 1rem' }}>
                                                <p style={{ margin: 0, fontSize: '0.875rem', color: '#64748b' }}>Coordonnées non disponibles</p>
                                                <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.75rem', color: '#94a3b8' }}>{expedition.adresse_livraison || expedition.destination_details?.ville}</p>
                                            </div>
                                            <button
                                                onClick={() => window.open(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${expedition.adresse_livraison || ''} ${expedition.destination_details?.ville || ''}`)}`)}
                                                style={{
                                                    background: 'white',
                                                    color: '#351c15',
                                                    border: '1px solid #e2e8f0',
                                                    borderRadius: '8px',
                                                    padding: '0.5rem 1rem',
                                                    fontSize: '0.75rem',
                                                    fontWeight: '700',
                                                    textTransform: 'uppercase',
                                                    cursor: 'pointer',
                                                    boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
                                                }}
                                            >
                                                Ouvrir Google Maps
                                            </button>
                                        </div>
                                    )}
                                </div>

                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                                    <div style={{ marginBottom: '0.5rem' }}>
                                        <span style={{ fontSize: '0.625rem', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase', display: 'block', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>Type d'envoi</span>
                                        <span style={{ fontSize: '0.925rem', fontWeight: '700', color: '#1e293b', letterSpacing: '0.02em' }}>{expedition.type_service_details?.libelle || 'Standard'}</span>
                                    </div>
                                    <div style={{ marginBottom: '0.5rem' }}>
                                        <span style={{ fontSize: '0.625rem', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase', display: 'block', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>Poids</span>
                                        <span style={{ fontSize: '0.925rem', fontWeight: '700', color: '#1e293b', letterSpacing: '0.02em' }}>{expedition.poids_kg} kg</span>
                                    </div>
                                    <div style={{ marginBottom: '0.5rem' }}>
                                        <span style={{ fontSize: '0.625rem', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase', display: 'block', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>Code Client</span>
                                        <span style={{ fontSize: '0.925rem', fontWeight: '700', color: '#1e293b', textTransform: 'uppercase', letterSpacing: '0.02em' }}>{expedition.client_details?.id ? `C-${expedition.client_details.id.toString().padStart(4, '0')}` : '-'}</span>
                                    </div>
                                    <div style={{ marginBottom: '0.5rem' }}>
                                        <span style={{ fontSize: '0.625rem', fontWeight: '700', color: '#94a3b8', textTransform: 'uppercase', display: 'block', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>Volume</span>
                                        <span style={{ fontSize: '0.925rem', fontWeight: '700', color: '#1e293b', letterSpacing: '0.02em' }}>{expedition.volume_m3} m³</span>
                                    </div>
                                </div>

                                <button
                                    onClick={() => navigate(`/expeditions/${expedition.id}/edit`)}
                                    style={{
                                        width: '100%',
                                        padding: '1rem',
                                        borderRadius: '12px',
                                        border: '2px solid #351c15',
                                        color: '#351c15',
                                        background: 'transparent',
                                        fontSize: '0.875rem',
                                        fontWeight: '700',
                                        textTransform: 'uppercase',
                                        letterSpacing: '0.05em',
                                        cursor: 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '0.5rem'
                                    }}
                                >
                                    <Edit size={18} /> Modifier l'expédition
                                </button>
                            </div>
                        </div>

                        <div style={{ background: '#f0f4f8', borderRadius: '12px', padding: '1.5rem', border: '1px solid #e2e8f0', display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                            <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)' }}>
                                <ShieldCheck color="#e3b12a" />
                            </div>
                            <div>
                                <h4 style={{ margin: 0, fontSize: '0.875rem', fontWeight: '700', color: '#1e293b' }}>Protégez vos envois</h4>
                                <p style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.25rem', lineHeight: 1.5 }}>
                                    Ajoutez une assurance ad-valorem pour vos colis de valeur jusqu'à 50 000€.
                                </p>
                                <a href="#" style={{ display: 'inline-block', marginTop: '0.75rem', fontSize: '0.75rem', fontWeight: '700', color: '#351c15', textDecoration: 'none', textTransform: 'uppercase' }}>
                                    En savoir plus →
                                </a>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    );
};

export default ExpeditionDetail;
