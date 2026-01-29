from django.db import migrations, models


def bootstrap_unmanaged_tables_for_tests(apps, schema_editor):
    db_name = str(schema_editor.connection.settings_dict.get('NAME', '')).lower()
    if 'test' not in db_name and 'memory' not in db_name:
        return

    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS role (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(50) UNIQUE,
            libelle VARCHAR(200)
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS utilisateur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(150) UNIQUE,
            email VARCHAR(254) UNIQUE,
            password VARCHAR(255),
            nom VARCHAR(150),
            prenom VARCHAR(150),
            telephone VARCHAR(20),
            role_id INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT,
            updated_at TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS client (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_client VARCHAR(50),
            type_client VARCHAR(50),
            nom VARCHAR(200),
            prenom VARCHAR(200),
            telephone VARCHAR(50),
            email VARCHAR(254),
            adresse TEXT,
            ville VARCHAR(100),
            pays VARCHAR(100),
            solde REAL DEFAULT 0,
            statut VARCHAR(50),
            created_at TEXT,
            updated_at TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS destination (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pays VARCHAR(100),
            ville VARCHAR(100),
            zone_geographique VARCHAR(100),
            code_zone VARCHAR(50),
            tarif_base_defaut REAL NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            updated_at TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS type_service (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(50) UNIQUE,
            libelle VARCHAR(200),
            description TEXT,
            delai_estime_jours INTEGER,
            priorite INTEGER,
            is_active BOOLEAN DEFAULT 1,
            updated_at TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS vehicule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            immatriculation VARCHAR(50) UNIQUE,
            type_vehicule VARCHAR(50),
            marque VARCHAR(100),
            modele VARCHAR(100),
            capacite_kg REAL,
            capacite_m3 REAL,
            consommation_100km REAL,
            etat VARCHAR(50),
            disponibilite VARCHAR(50),
            date_mise_en_service TEXT,
            updated_at TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS chauffeur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricule VARCHAR(50) UNIQUE,
            nom VARCHAR(200) NOT NULL,
            prenom VARCHAR(200) NOT NULL,
            telephone VARCHAR(50),
            email VARCHAR(254),
            adresse TEXT,
            num_permis VARCHAR(100) UNIQUE,
            categorie_permis VARCHAR(50),
            date_embauche TEXT,
            disponibilite VARCHAR(50),
            statut VARCHAR(50),
            updated_at TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS tournee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_tournee VARCHAR(50) UNIQUE,
            date_tournee TEXT,
            date_depart TEXT,
            date_retour TEXT,
            chauffeur_id INTEGER,
            vehicule_id INTEGER,
            statut VARCHAR(50),
            kilometrage_depart REAL,
            kilometrage_retour REAL,
            distance_km REAL,
            duree_minutes INTEGER,
            consommation_litres REAL,
            notes TEXT,
            points_passage TEXT,
            created_by INTEGER,
            updated_at TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS expedition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_expedition VARCHAR(50) UNIQUE,
            client_id INTEGER,
            type_service_id INTEGER,
            destination_id INTEGER,
            poids_kg REAL,
            volume_m3 REAL,
            description_colis TEXT,
            adresse_livraison TEXT,
            nom_destinataire VARCHAR(200),
            telephone_destinataire VARCHAR(50),
            date_creation TEXT,
            statut VARCHAR(50),
            montant_total REAL DEFAULT 0,
            est_facturee BOOLEAN DEFAULT 0,
            tournee_id INTEGER,
            created_by INTEGER,
            updated_at TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS tracking_expedition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expedition_id INTEGER,
            chauffeur_id INTEGER,
            tournee_id INTEGER,
            statut VARCHAR(50),
            lieu VARCHAR(200),
            commentaire TEXT,
            date_statut TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS incident (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_incident VARCHAR(50) UNIQUE,
            type_incident VARCHAR(30) NOT NULL,
            expedition_id INTEGER,
            tournee_id INTEGER,
            commentaire TEXT,
            action_appliquee VARCHAR(30) DEFAULT 'NONE',
            notify_direction BOOLEAN DEFAULT 1,
            notify_client BOOLEAN DEFAULT 0,
            created_by INTEGER,
            created_at TEXT,
            updated_at TEXT
        );
        """
    )
    schema_editor.execute(
        """
        CREATE TABLE IF NOT EXISTS facture (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_facture VARCHAR(50) UNIQUE,
            client_id INTEGER,
            date_facture TEXT,
            total_ht REAL,
            montant_tva REAL,
            total_ttc REAL,
            statut VARCHAR(50),
            updated_at TEXT
        );
        """
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_password_reset_token'),
    ]

    operations = [
        migrations.RunPython(bootstrap_unmanaged_tables_for_tests, migrations.RunPython.noop),
        migrations.AddField(
            model_name='destination',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='destination',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
