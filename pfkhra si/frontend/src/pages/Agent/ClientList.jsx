import React, { useState, useEffect } from 'react';
import api from '../../api';

const ClientList = () => {
    const [clients, setClients] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchClients();
    }, []);

    const fetchClients = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await api.get('/clients/');
            setClients(response.data);
        } catch (err) {
            console.error(err);
            setError("Erreur lors du chargement des clients.");
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Chargement...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>Clients</h1>
                <button className="btn-primary">+ Nouveau Client</button>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Nom</th>
                        <th>Prénom</th>
                        <th>Email</th>
                        <th>Téléphone</th>
                        <th>Adresse</th>
                    </tr>
                </thead>
                <tbody>
                    {clients.map(client => (
                        <tr key={client.id}>
                            <td>{client.code_client}</td>
                            <td>{client.nom}</td>
                            <td>{client.prenom}</td>
                            <td>{client.email}</td>
                            <td>{client.telephone}</td>
                            <td>{client.adresse}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ClientList;
