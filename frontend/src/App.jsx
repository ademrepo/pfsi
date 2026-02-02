import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import api from './api';
import Login from './pages/Login';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Layout from './components/Layout';
import ExpeditionList from './pages/Agent/ExpeditionList';
import ExpeditionDetail from './pages/Agent/ExpeditionDetail';
import ExpeditionForm from './pages/Agent/ExpeditionForm';
import ClientList from './pages/Agent/ClientList';
import ClientForm from './pages/Agent/ClientForm';
import TourneeList from './pages/Agent/TourneeList';
import TourneeForm from './pages/Agent/TourneeForm';
import IncidentList from './pages/Agent/IncidentList';
import IncidentForm from './pages/Agent/IncidentForm';
import AlerteList from './pages/Agent/AlerteList';
import ReclamationList from './pages/Agent/ReclamationList';
import ReclamationForm from './pages/Agent/ReclamationForm';
import InvoiceList from './pages/Agent/InvoiceList';
import InvoiceForm from './pages/Agent/InvoiceForm';
import InvoiceDetail from './pages/Agent/InvoiceDetail';
import PaymentList from './pages/Agent/PaymentList';
import PaymentForm from './pages/Agent/PaymentForm';
import ChauffeurList from './pages/Agent/ChauffeurList';
import ChauffeurForm from './pages/Agent/ChauffeurForm';

import UserList from './pages/Admin/UserList';
import UserForm from './pages/Admin/UserForm';
import AuditLogList from './pages/Admin/AuditLogList';
import ReadOnlyTable from './pages/Admin/ReadOnlyTable';

function App() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        checkUserSession();
    }, []);

    const checkUserSession = async () => {
        try {
            await api.get('/auth/csrf/');  
            const response = await api.get('/auth/me/');
            setUser(response.data);
        } catch (error) {
            console.log("No active session or backend not available:", error.message);
            setUser(null);
             
            document.cookie.split(";").forEach((c) => {
                document.cookie = c
                    .replace(/^ +/, "")
                    .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
            });
        } finally {
            setLoading(false);
        }
    };

    const handleLoginSuccess = (userData) => {
        setUser(userData);
    };

    const handleLogout = async () => {
        try {
            await api.post('/auth/logout/');
            setUser(null);
            navigate('/login');
        } catch (error) {
            console.error("Logout failed", error);
        }
    };

    if (loading) {
        return <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>Chargement...</div>;
    }

    return (
        <div className="App">
            <Routes>
                <Route path="/login" element={
                    !user ? <Login onLogin={handleLoginSuccess} /> : <Navigate to="/" replace />
                } />

                <Route path="/forgot-password" element={
                    !user ? <ForgotPassword /> : <Navigate to="/" replace />
                } />

                <Route path="/reset-password" element={
                    !user ? <ResetPassword /> : <Navigate to="/" replace />
                } />

                <Route element={
                    user ? <Layout user={user} onLogout={handleLogout} /> : <Navigate to="/login" replace state={{ from: location }} />
                }>
                    <Route path="/" element={<Dashboard user={user} />} />
                    <Route path="/analytics" element={<Analytics />} />

                    { }
                    <Route path="/expeditions" element={<ExpeditionList />} />
                    <Route path="/expeditions/:id" element={<ExpeditionDetail />} />
                    <Route path="/expeditions/nouveau" element={<ExpeditionForm />} />
                    <Route path="/expeditions/:id/edit" element={<ExpeditionForm />} />
                    <Route path="/clients" element={<ClientList />} />
                    <Route path="/clients/nouveau" element={<ClientForm />} />
                    <Route path="/clients/:id/edit" element={<ClientForm />} />
                    <Route path="/tournees" element={<TourneeList />} />
                    <Route path="/tournees/nouveau" element={<TourneeForm />} />
                    <Route path="/tournees/:id/edit" element={<TourneeForm />} />
                    <Route path="/incidents" element={<IncidentList />} />
                    <Route path="/incidents/nouveau" element={<IncidentForm />} />
                    <Route path="/alertes" element={<AlerteList />} />
                    <Route path="/reclamations" element={<ReclamationList />} />
                    <Route path="/reclamations/nouveau" element={<ReclamationForm />} />
                    <Route path="/reclamations/:id/edit" element={<ReclamationForm />} />

                    <Route path="/factures" element={<InvoiceList />} />
                    <Route path="/factures/nouveau" element={<InvoiceForm />} />
                    <Route path="/factures/:id" element={<InvoiceDetail />} />

                    <Route path="/paiements" element={<PaymentList />} />
                    <Route path="/paiements/nouveau" element={<PaymentForm />} />

                    <Route path="/chauffeurs" element={<ChauffeurList />} />
                    <Route path="/chauffeurs/nouveau" element={<ChauffeurForm />} />
                    <Route path="/chauffeurs/:id/edit" element={<ChauffeurForm />} />

                    <Route path="/vehicules" element={
                        <ReadOnlyTable
                            title="Référentiel Véhicules"
                            endpoint="/vehicules/"
                            columns={[
                                { header: 'Matricule', key: 'immatriculation' },
                                { header: 'Marque', key: 'marque' },
                                { header: 'Modèle', key: 'modele' }
                            ]}
                        />
                    } />

                    <Route path="/destinations" element={
                        <ReadOnlyTable
                            title="Référentiel Destinations"
                            endpoint="/destinations/"
                            columns={[
                                { header: 'Pays', key: 'pays' },
                                { header: 'Ville', key: 'ville' },
                                { header: 'Code Zone', key: 'code_zone' },
                                { header: 'Tarif par défaut', key: 'tarif_base_defaut', render: (d) => `${d.tarif_base_defaut} €` }
                            ]}
                        />
                    } />

                    { }
                    <Route path="/admin/users" element={<UserList />} />
                    <Route path="/admin/users/create" element={<UserForm />} />
                    <Route path="/admin/users/:id/edit" element={<UserForm />} />
                    <Route path="/admin/audit" element={<AuditLogList />} />
                </Route>

                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </div>
    );
}

export default App;
