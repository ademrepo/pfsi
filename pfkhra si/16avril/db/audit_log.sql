-- Ajouter la table audit_log pour la traçabilité
-- À exécuter après l'initialisation de la base de données

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER,
    username TEXT NOT NULL,
    action_type TEXT NOT NULL CHECK (action_type IN (
        'LOGIN_SUCCESS', 'LOGIN_FAILED', 'LOGOUT',
        'USER_CREATED', 'USER_UPDATED', 'USER_ACTIVATED',
        'USER_DEACTIVATED', 'PASSWORD_RESET', 'ACCESS_DENIED'
    )),
    ip_address TEXT,
    user_agent TEXT,
    details TEXT,  -- JSON format
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
);

-- Index pour améliorer les performances des requêtes
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_user_timestamp ON audit_log(utilisateur_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_action_timestamp ON audit_log(action_type, timestamp DESC);
