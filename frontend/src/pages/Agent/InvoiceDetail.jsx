import React, { useState, useEffect } from 'react';
import api from '../../api';
import { useParams, useNavigate } from 'react-router-dom';

const InvoiceDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [invoice, setInvoice] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchInvoice = async () => {
            try {
                const res = await api.get(`/factures/${id}/`);
                setInvoice(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchInvoice();
    }, [id]);

    const handlePrint = () => {
        window.print();
    };

    if (loading) return <div className="page-container">Chargement...</div>;
    if (!invoice) return <div className="page-container">Facture non trouvée.</div>;

    return (
        <div className="page-container">
            <div className="header-actions no-print">
                <h1>Détails Facture {invoice.numero_facture}</h1>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button className="secondary" onClick={() => navigate('/factures')}>Retour</button>
                    <button className="btn-primary" onClick={handlePrint}>🖨️ Imprimer / PDF</button>
                </div>
            </div>

            <div className="invoice-print-container" style={{ background: 'white', padding: '3rem', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)', maxWidth: '1000px', margin: '0 auto' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '3rem', borderBottom: '2px solid #f1f5f9', paddingBottom: '2rem' }}>
                    <div>
                        <h2 style={{ color: 'var(--primary)', marginBottom: '0.5rem' }}>DELIVERYFORSURE</h2>
                        <p>123 Rue de la Logistique</p>
                        <p>75000 PARIS</p>
                        <p>Tel: +33 1 23 45 67 89</p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                        <h1 style={{ fontSize: '2.5rem', margin: 0, color: '#1e293b' }}>FACTURE</h1>
                        <p style={{ fontWeight: '600', fontSize: '1.2rem', marginTop: '0.5rem' }}>{invoice.numero_facture}</p>
                        <p>Date: {new Date(invoice.date_facture).toLocaleDateString()}</p>
                    </div>
                </div>

                <div style={{ display: 'flex', gap: '4rem', marginBottom: '3rem' }}>
                    <div style={{ flex: 1 }}>
                        <h4 style={{ color: '#64748b', textTransform: 'uppercase', fontSize: '0.85rem', marginBottom: '1rem' }}>Facturé à</h4>
                        <p style={{ fontWeight: '700', fontSize: '1.1rem' }}>{invoice.client_details?.nom} {invoice.client_details?.prenom}</p>
                        <p>{invoice.client_details?.adresse}</p>
                        <p>{invoice.client_details?.telephone}</p>
                        <p>{invoice.client_details?.email}</p>
                    </div>
                    <div style={{ flex: 1 }}>
                        <h4 style={{ color: '#64748b', textTransform: 'uppercase', fontSize: '0.85rem', marginBottom: '1rem' }}>Statut de paiement</h4>
                        <div style={{ fontSize: '1.1rem', fontWeight: '600' }}>
                            <span className={`status-badge ${invoice.statut === 'Payée' ? 'status-Livré' : 'status-En.cours'}`}>
                                {invoice.statut}
                            </span>
                        </div>
                        <p style={{ marginTop: '1rem' }}>Reste à payer : <span style={{ fontWeight: '700', color: invoice.reste_a_payer > 0 ? '#b91c1c' : '#059669' }}>{invoice.reste_a_payer} €</span></p>
                    </div>
                </div>

                <div className="table-container" style={{ boxShadow: 'none', border: '1px solid #e2e8f0' }}>
                    <table style={{ background: 'transparent' }}>
                        <thead style={{ background: '#f8fafc' }}>
                            <tr>
                                <th>Code Expédition</th>
                                <th>Date</th>
                                <th>Destination</th>
                                <th>Détails</th>
                                <th style={{ textAlign: 'right' }}>Prix HT</th>
                            </tr>
                        </thead>
                        <tbody>
                            {invoice.expedition_details?.map(exp => (
                                <tr key={exp.id}>
                                    <td style={{ fontWeight: '600' }}>{exp.code_expedition}</td>
                                    <td>{new Date(exp.date_creation).toLocaleDateString()}</td>
                                    <td>{exp.destination_details?.ville}</td>
                                    <td>{exp.poids_kg}kg / {exp.volume_m3}m³</td>
                                    <td style={{ textAlign: 'right', fontWeight: '600' }}>{exp.montant_total} €</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '2rem' }}>
                    <div style={{ width: '300px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
                            <span>Total HT :</span>
                            <span style={{ fontWeight: '600' }}>{invoice.total_ht} €</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
                            <span>TVA (20%) :</span>
                            <span style={{ fontWeight: '600' }}>{invoice.montant_tva} €</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem 0', borderTop: '2px solid #1e293b', marginTop: '0.5rem', fontSize: '1.25rem' }}>
                            <span style={{ fontWeight: '700' }}>TOTAL TTC :</span>
                            <span style={{ fontWeight: '800', color: 'var(--primary)' }}>{invoice.total_ttc} €</span>
                        </div>
                    </div>
                </div>

                {invoice.paiements?.length > 0 && (
                    <div style={{ marginTop: '3rem' }}>
                        <h4 style={{ borderBottom: '1px solid #e2e8f0', paddingBottom: '0.5rem', marginBottom: '1rem' }}>Historique des paiements</h4>
                        <table style={{ fontSize: '0.9rem' }}>
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Mode</th>
                                    <th style={{ textAlign: 'right' }}>Montant</th>
                                </tr>
                            </thead>
                            <tbody>
                                {invoice.paiements.map(p => (
                                    <tr key={p.id}>
                                        <td>{new Date(p.date_paiement).toLocaleDateString()}</td>
                                        <td>{p.mode_paiement}</td>
                                        <td style={{ textAlign: 'right', fontWeight: '600' }}>{p.montant} €</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                <div style={{ marginTop: '4rem', textAlign: 'center', color: '#64748b', fontSize: '0.85rem', borderTop: '1px solid #f1f5f9', paddingTop: '2rem' }}>
                    <p>Merci pour votre confiance. En cas de questions, contactez-nous au 01 23 45 67 89.</p>
                </div>
            </div>

            <style>{`
                @media print {
                    .no-print, .sidebar, .logout-btn { display: none !important; }
                    .page-container { padding: 0 !important; margin: 0 !important; width: 100% !important; background: white !important; }
                    .invoice-print-container { box-shadow: none !important; border: none !important; padding: 0 !important; max-width: 100% !important; }
                    body { background: white !important; }
                }
            `}</style>
        </div>
    );
};

export default InvoiceDetail;
