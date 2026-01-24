import React, { useState, useEffect } from 'react';
import api from '../../api';

const ReadOnlyTable = ({ title, endpoint, columns }) => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [search, setSearch] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);
            try {
                const res = await api.get(endpoint);
                setData(res.data);
            } catch (err) {
                console.error(err);
                setError(err.response?.data?.detail || "Erreur lors de la récupération des données.");
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [endpoint]);

    const filteredData = data.filter(item => {
        if (!search) return true;
        // Search in all columns
        return columns.some(col => {
            const val = item[col.key];
            if (val == null) return false;
            return String(val).toLowerCase().includes(search.toLowerCase());
        });
    });

    const handlePrint = () => {
        window.print();
    };

    if (loading) return <div>Chargement...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="page-container">
            <div className="header-actions">
                <h1>{title}</h1>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <input
                        type="text"
                        placeholder="Rechercher..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                    />
                    <button className="secondary" onClick={handlePrint}>Imprimer</button>
                </div>
            </div>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            {columns.map((col, idx) => (
                                <th key={idx}>{col.header}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {filteredData.map((item, idx) => (
                            <tr key={item.id || idx}>
                                {columns.map((col, cIdx) => (
                                    <td key={cIdx}>
                                        {col.render ? col.render(item) : item[col.key]}
                                    </td>
                                ))}
                            </tr>
                        ))}
                        {filteredData.length === 0 && (
                            <tr>
                                <td colSpan={columns.length} style={{ textAlign: 'center' }}>Aucun résultat.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ReadOnlyTable;
