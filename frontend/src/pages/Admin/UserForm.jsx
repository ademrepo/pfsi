import React, { useState, useEffect } from 'react';
import api from '../../api';
import { useNavigate, useParams } from 'react-router-dom';

const UserForm = () => {
    const { id } = useParams();
    const isEdit = !!id;
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        username: '',
        email: '',
        nom: '',
        prenom: '',
        telephone: '',
        role_id: '',
        password: '',
        password_confirm: '',
        is_active: true
    });

    const [roles, setRoles] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchRoles();
        if (isEdit) {
            fetchUser();
        }
    }, [id]);

    const fetchRoles = async () => {
        try {
            const res = await api.get('/roles/');
            setRoles(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const fetchUser = async () => {
        try {
            const res = await api.get(`/utilisateurs/${id}/`);
             
            const user = res.data;
            setFormData({
                ...user,
                role_id: user.role,  
                 
                 
                 
                 
                 
                 
                 
                 
            });

             
            if (typeof user.role === 'object') {
                setFormData(prev => ({ ...prev, role_id: user.role.id }));
            } else {
                setFormData(prev => ({ ...prev, role_id: user.role }));
            }

        } catch (err) {
            console.error("User fetch error", err);
        }
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            if (isEdit) {
                await api.put(`/utilisateurs/${id}/`, formData);
            } else {
                await api.post('/utilisateurs/', formData);
            }
            navigate('/admin/users');
        } catch (err) {
            alert(err.response?.data?.detail || "Erreur lors de l'enregistrement");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleResetPassword = async () => {
        const newPass = prompt("Nouveau mot de passe :");
        if (!newPass) return;

        try {
            await api.post(`/utilisateurs/${id}/reset_password/`, {
                new_password: newPass,
                new_password_confirm: newPass
            });
            alert("Mot de passe mis à jour !");
        } catch (err) {
            alert("Erreur reset password");
        }
    };

    return (
        <div className="page-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <h1 style={{ width: '100%', maxWidth: '600px', textAlign: 'left', marginBottom: '1.5rem' }}>
                {isEdit ? 'Modifier Utilisateur' : 'Nouvel Utilisateur'}
            </h1>

            <form onSubmit={handleSubmit} style={{ background: 'white', padding: '2.5rem', maxWidth: '600px', width: '100%', borderRadius: '12px', boxShadow: 'var(--shadow-md)' }}>

                <div className="form-group">
                    <label>Nom d'utilisateur</label>
                    <input name="username" value={formData.username} onChange={handleChange} required disabled={isEdit} />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                    <div className="form-group">
                        <label>Nom</label>
                        <input name="nom" value={formData.nom} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label>Prénom</label>
                        <input name="prenom" value={formData.prenom} onChange={handleChange} required />
                    </div>
                </div>

                <div className="form-group">
                    <label>Email</label>
                    <input type="email" name="email" value={formData.email} onChange={handleChange} required />
                </div>

                <div className="form-group">
                    <label>Téléphone</label>
                    <input name="telephone" value={formData.telephone || ''} onChange={handleChange} />
                </div>

                <div className="form-group">
                    <label>RÔLE</label>
                    <select
                        name="role_id"
                        value={formData.role_id}
                        onChange={handleChange}
                        required
                        style={{
                            borderRadius: '12px',
                            appearance: 'none',
                            backgroundImage: `url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%23CBD5E0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>')`,
                            backgroundRepeat: 'no-repeat',
                            backgroundPosition: 'right 12px center',
                            paddingRight: '35px',
                            cursor: 'pointer'
                        }}
                    >
                        <option value="">Sélectionner un rôle...</option>
                        {roles.map(r => (
                            <option key={r.id} value={r.id}>{r.libelle}</option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', cursor: 'pointer', fontWeight: '500' }}>
                        <input
                            type="checkbox"
                            name="is_active"
                            checked={formData.is_active}
                            onChange={handleChange}
                            style={{ width: '18px', height: '18px', cursor: 'pointer' }}
                        />
                        COMPTE ACTIF
                    </label>
                </div>

                {!isEdit && (
                    <>
                        <hr style={{ margin: '1.5rem 0', border: '0', borderTop: '1px solid var(--border)' }} />
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div className="form-group">
                                <label>MOT DE PASSE</label>
                                <input type="password" name="password" value={formData.password} onChange={handleChange} required={!isEdit} style={{ borderRadius: '12px' }} />
                            </div>
                            <div className="form-group">
                                <label>CONFIRMER MOT DE PASSE</label>
                                <input type="password" name="password_confirm" value={formData.password_confirm} onChange={handleChange} required={!isEdit} style={{ borderRadius: '12px' }} />
                            </div>
                        </div>
                    </>
                )}

                <div style={{ marginTop: '2.5rem', display: 'flex', gap: '1.25rem' }}>
                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            borderRadius: '25px',
                            padding: '0.75rem 2rem',
                            fontSize: '1rem',
                            fontWeight: '600',
                            transition: 'all 0.2s',
                            background: '#0d9488',
                            color: 'white',
                            border: 'none',
                            cursor: 'pointer'
                        }}
                    >
                        {loading ? 'Enregistrement...' : 'Enregistrer les modifications'}
                    </button>

                    {isEdit && (
                        <button
                            type="button"
                            className="secondary"
                            onClick={handleResetPassword}
                            style={{
                                background: '#C68E17',
                                color: 'white',
                                borderRadius: '25px',
                                padding: '0.75rem 1.5rem',
                                border: 'none',
                                fontWeight: '600',
                                opacity: 1,
                                cursor: 'pointer'
                            }}
                        >
                            Réinitialiser MDP
                        </button>
                    )}

                    <button
                        type="button"
                        className="secondary"
                        onClick={() => navigate('/admin/users')}
                        style={{ borderRadius: '25px', padding: '0.75rem 1.5rem', cursor: 'pointer' }}
                    >
                        Annuler
                    </button>
                </div>
            </form>
        </div>
    );
};

export default UserForm;
