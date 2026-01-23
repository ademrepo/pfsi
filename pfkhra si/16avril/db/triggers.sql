PRAGMA foreign_keys = ON;

-- ===========================
-- CODES AUTOMATIQUES
-- ===========================
CREATE TRIGGER trg_client_code
AFTER INSERT ON client
WHEN NEW.code_client IS NULL OR NEW.code_client = ''
BEGIN
    UPDATE client
    SET code_client = 'CLI-' || SUBSTR('00000' || NEW.id, -5, 5)
    WHERE id = NEW.id;
END;

CREATE TRIGGER trg_chauffeur_matricule
AFTER INSERT ON chauffeur
WHEN NEW.matricule IS NULL OR NEW.matricule = ''
BEGIN
    UPDATE chauffeur
    SET matricule = 'CHF-' || SUBSTR('00000' || NEW.id, -5, 5)
    WHERE id = NEW.id;
END;

CREATE TRIGGER trg_expedition_code
AFTER INSERT ON expedition
WHEN NEW.code_expedition IS NULL OR NEW.code_expedition = ''
BEGIN
    UPDATE expedition
    SET code_expedition = 'EXP-' || strftime('%Y%m%d','now') || '-' || SUBSTR('00000' || NEW.id, -5, 5)
    WHERE id = NEW.id;
END;

CREATE TRIGGER trg_tournee_code
AFTER INSERT ON tournee
WHEN NEW.code_tournee IS NULL OR NEW.code_tournee = ''
BEGIN
    UPDATE tournee
    SET code_tournee = 'TRN-' || strftime('%Y%m%d','now') || '-' || SUBSTR('00' || NEW.id, -2, 2)
    WHERE id = NEW.id;
END;

CREATE TRIGGER trg_facture_numero
AFTER INSERT ON facture
WHEN NEW.numero_facture IS NULL OR NEW.numero_facture = ''
BEGIN
    UPDATE facture
    SET numero_facture = 'FACT-' || strftime('%Y%m','now') || '-' || SUBSTR('00000' || NEW.id, -5, 5)
    WHERE id = NEW.id;
END;

-- ===========================
-- UPDATED_AT
-- ===========================
CREATE TRIGGER trg_updated_at_utilisateur
AFTER UPDATE ON utilisateur
BEGIN
    UPDATE utilisateur SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER trg_updated_at_expedition
AFTER UPDATE ON expedition
BEGIN
    UPDATE expedition SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER trg_updated_at_tournee
AFTER UPDATE ON tournee
BEGIN
    UPDATE tournee SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- ===========================
-- TRACKING AUTOMATIQUE
-- ===========================
CREATE TRIGGER trg_expedition_tracking_initial
AFTER INSERT ON expedition
BEGIN
    INSERT INTO tracking_expedition (expedition_id, statut, lieu, date_statut)
    VALUES (NEW.id, 'enregistre', 'Création expédition', CURRENT_TIMESTAMP);
END;

CREATE TRIGGER trg_tracking_update_expedition_statut
AFTER INSERT ON tracking_expedition
BEGIN
    UPDATE expedition
    SET statut = NEW.statut
    WHERE id = NEW.expedition_id;
END;

-- ===========================
-- SOLDE CLIENT
-- ===========================
CREATE TRIGGER trg_facture_validee_augmente_solde
AFTER UPDATE OF statut ON facture
WHEN OLD.statut != 'validee' AND NEW.statut = 'validee'
BEGIN
    UPDATE client
    SET solde = solde + NEW.total_ttc
    WHERE id = NEW.client_id;
END;

CREATE TRIGGER trg_paiement_diminue_solde
AFTER INSERT ON paiement
WHEN NEW.statut = 'valide'
BEGIN
    UPDATE client
    SET solde = solde - NEW.montant
    WHERE id = NEW.client_id;
END;

-- ===========================
-- BLOQUAGES METIER
-- ===========================
CREATE TRIGGER trg_expedition_no_update_if_facturee
BEFORE UPDATE ON expedition
WHEN OLD.est_facturee = 1
BEGIN
    SELECT RAISE(ABORT, 'Expédition déjà facturée');
END;

CREATE TRIGGER trg_expedition_no_delete_if_facturee
BEFORE DELETE ON expedition
WHEN OLD.est_facturee = 1
BEGIN
    SELECT RAISE(ABORT, 'Expédition déjà facturée');
END;

CREATE TRIGGER trg_expedition_mark_facturee
AFTER INSERT ON facture_expedition
BEGIN
    UPDATE expedition
    SET est_facturee = 1
    WHERE id = NEW.expedition_id;
END;

-- ===========================
-- CALCUL MONTANT EXPEDITION
-- ===========================
CREATE TRIGGER trg_expedition_calcul_montant
AFTER INSERT ON expedition
WHEN NEW.montant_total = 0
BEGIN
    UPDATE expedition
    SET montant_total = (
        SELECT d.tarif_base_defaut +
               (NEW.poids_kg * t.tarif_poids_kg) +
               (NEW.volume_m3 * t.tarif_volume_m3)
        FROM tarification t
        JOIN destination d ON d.id = t.destination_id
        WHERE t.type_service_id = NEW.type_service_id
          AND t.destination_id = NEW.destination_id
    )
    WHERE id = NEW.id;
END;
