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
            // Adjust data to match form expectations
            const user = res.data;
            setFormData({
                ...user,
                role_id: user.role, // role is object or id? in serializer output it is object usually but we need ID for update
                // Wait, UserSerializer has "role" field which is PK? No, usually nested or PK.
                // Let's check UserSerializer. It has 'role' field.
                // Actually UserSerializer: role = ForeignKey. Default serialization is PK unless depth set.
                // But core/serializers.py line 67: role = models.ForeignKey. 
                // BUT UserSerializer (Read) has: role_display, role_code. And 'role' field.
                // If it is ModelSerializer default, it returns ID.
                // Let's assume ID. If fail, I debug.
                // Also "role" in formData should be ID.
            });

            // Fix role_id if 'role' is object
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
        <div className="page-container">
            <h1>{isEdit ? 'Modifier Utilisateur' : 'Nouvel Utilisateur'}</h1>

            <form onSubmit={handleSubmit} style={{ background: 'white', padding: '2rem', maxWidth: '600px', borderRadius: '8px' }}>

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
                    <label>Rôle</label>
                    <select name="role_id" value={formData.role_id} onChange={handleChange} required>
                        <option value="">Sélectionner...</option>
                        {roles.map(r => (
                            <option key={r.id} value={r.id}>{r.libelle}</option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <input type="checkbox" name="is_active" checked={formData.is_active} onChange={handleChange} />
                        Compte Actif
                    </label>
                </div>

                {!isEdit && (
                    <>
                        <hr />
                        <div className="form-group">
                            <label>Mot de passe</label>
                            <input type="password" name="password" value={formData.password} onChange={handleChange} required={!isEdit} />
                        </div>
                        <div className="form-group">
                            <label>Confirmer Mot de passe</label>
                            <input type="password" name="password_confirm" value={formData.password_confirm} onChange={handleChange} required={!isEdit} />
                        </div>
                    </>
                )}

                <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
                    <button type="submit" disabled={loading}>{loading ? 'Enregistrement...' : 'Enregistrer'}</button>

                    {isEdit && (
                        <button type="button" className="secondary" onClick={handleResetPassword} style={{ background: '#ecc94b', opacity: 1 }}>
                            Réinitialiser MDP
                        </button>
                    )}

                    <button type="button" className="secondary" onClick={() => navigate('/admin/users')}>Annuler</button>
                </div>
            </form>
        </div>
    );
};

export default UserForm;
