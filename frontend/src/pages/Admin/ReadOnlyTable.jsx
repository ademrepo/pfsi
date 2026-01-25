import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Download, Search as SearchIcon } from 'lucide-react';
import PageHeader from '../../components/PageHeader';

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

    if (loading) return <div className="page-container">Chargement...</div>;
    if (error) return <div className="page-container"><div className="error">{error}</div></div>;

    return (
        <div className="page-container">
            <PageHeader 
                title={title}
                subtitle="Données de référence en lecture seule"
            />

            <div className="top-bar">
                <div className="search-bar">
                    <SearchIcon size={18} className="search-icon" />
                    <input
                        type="text"
                        placeholder="Rechercher..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
                <div className="top-bar-actions">
                    <button className="secondary" onClick={handlePrint}>
                        <Download size={18} />
                        Imprimer
                    </button>
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
                                <td colSpan={columns.length} style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                    Aucun résultat.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            <div style={{ 
                marginTop: '1.5rem',
                fontSize: '0.875rem',
                color: 'var(--text-muted)'
            }}>
                Affichage de {filteredData.length} sur {data.length} résultats
            </div>
        </div>
    );
};

export default ReadOnlyTable;
