







from django .db import migrations ,models 
import django .db .models .deletion 
import core .models 


def _ensure_sqlite_schema (apps ,schema_editor ):
    if schema_editor .connection .vendor !='sqlite':
        return 

    def cols (table_name :str )->set [str ]:
        with schema_editor .connection .cursor ()as cursor :
            cursor .execute (f"PRAGMA table_info({table_name });")
            return {row [1 ]for row in cursor .fetchall ()}



    alter_add_columns ={
    'incident':[
    ("code_incident","varchar(50) NULL"),
    ("type_incident","varchar(30) NOT NULL DEFAULT 'AUTRE'"),
    ("commentaire","text NULL"),
    ("action_appliquee","varchar(30) NOT NULL DEFAULT 'NONE'"),
    ("notify_direction","bool NOT NULL DEFAULT 1"),
    ("notify_client","bool NOT NULL DEFAULT 0"),
    ("created_at","datetime NOT NULL DEFAULT CURRENT_TIMESTAMP"),
    ("updated_at","datetime NULL"),
    ("created_by","bigint NULL"),
    ("expedition_id","bigint NULL"),
    ("tournee_id","bigint NULL"),
    ],
    'incident_attachment':[
    ("file","varchar(100) NULL"),
    ("original_name","varchar(255) NULL"),
    ("uploaded_at","datetime NOT NULL DEFAULT CURRENT_TIMESTAMP"),
    ("incident_id","bigint NULL"),
    ("uploaded_by","bigint NULL"),
    ],
    'alerte':[
    ("type_alerte","varchar(20) NOT NULL DEFAULT 'INCIDENT'"),
    ("destination","varchar(20) NULL"),
    ("titre","varchar(200) NULL"),
    ("message","text NULL"),
    ("incident_id","bigint NULL"),
    ("expedition_id","bigint NULL"),
    ("tournee_id","bigint NULL"),
    ("is_read","bool NOT NULL DEFAULT 0"),
    ("created_at","datetime NOT NULL DEFAULT CURRENT_TIMESTAMP"),
    ],
    }

    with schema_editor .connection .cursor ()as cursor :
        for table_name ,cols_to_add in alter_add_columns .items ():
            present =cols (table_name )
            for col_name ,col_def in cols_to_add :
                if col_name in present :
                    continue 
                cursor .execute (f"ALTER TABLE {table_name } ADD COLUMN {col_name } {col_def };")


        cursor .execute ("CREATE INDEX IF NOT EXISTS incident_created__3e51bc_idx ON incident (created_at DESC);")
        cursor .execute ("CREATE INDEX IF NOT EXISTS incident_type_in_9ad5f3_idx ON incident (type_incident, created_at DESC);")
        cursor .execute ("CREATE INDEX IF NOT EXISTS incident_expediti_dbb83c_idx ON incident (expedition_id, created_at DESC);")
        cursor .execute ("CREATE INDEX IF NOT EXISTS incident_tournee_7b848d_idx ON incident (tournee_id, created_at DESC);")
        cursor .execute ("CREATE INDEX IF NOT EXISTS alerte_destina_9b3007_idx ON alerte (destination, is_read, created_at DESC);")


class Migration (migrations .Migration ):

    dependencies =[
    ('core','0005_auto_20260124_1653'),
    ]

    operations =[
    migrations .SeparateDatabaseAndState (
    database_operations =[
    migrations .RunSQL (
    sql =[
    """
                        CREATE TABLE IF NOT EXISTS incident (
                            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                            code_incident varchar(50) NULL UNIQUE,
                            type_incident varchar(30) NOT NULL,
                            commentaire text NULL,
                            action_appliquee varchar(30) NOT NULL DEFAULT 'NONE',
                            notify_direction bool NOT NULL DEFAULT 1,
                            notify_client bool NOT NULL DEFAULT 0,
                            created_at datetime NOT NULL,
                            updated_at datetime NULL,
                            created_by bigint NULL REFERENCES utilisateur(id) DEFERRABLE INITIALLY DEFERRED,
                            expedition_id bigint NULL REFERENCES expedition(id) DEFERRABLE INITIALLY DEFERRED,
                            tournee_id bigint NULL REFERENCES tournee(id) DEFERRABLE INITIALLY DEFERRED
                        );
                        """,
    """
                        CREATE TABLE IF NOT EXISTS incident_attachment (
                            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                            file varchar(100) NOT NULL,
                            original_name varchar(255) NULL,
                            uploaded_at datetime NOT NULL,
                            incident_id bigint NOT NULL REFERENCES incident(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
                            uploaded_by bigint NULL REFERENCES utilisateur(id) DEFERRABLE INITIALLY DEFERRED
                        );
                        """,
    """
                        CREATE TABLE IF NOT EXISTS alerte (
                            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                            type_alerte varchar(20) NOT NULL DEFAULT 'INCIDENT',
                            destination varchar(20) NOT NULL,
                            titre varchar(200) NOT NULL,
                            message text NULL,
                            incident_id bigint NULL REFERENCES incident(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
                            expedition_id bigint NULL REFERENCES expedition(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED,
                            tournee_id bigint NULL REFERENCES tournee(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED,
                            is_read bool NOT NULL DEFAULT 0,
                            created_at datetime NOT NULL
                        );
                        """,
    ],
    reverse_sql =[
    "DROP TABLE IF EXISTS alerte;",
    "DROP TABLE IF EXISTS incident_attachment;",
    "DROP TABLE IF EXISTS incident;",
    ],
    ),
    migrations .RunPython (_ensure_sqlite_schema ,reverse_code =migrations .RunPython .noop ),
    ],
    state_operations =[
    migrations .CreateModel (
    name ='Incident',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('code_incident',models .CharField (blank =True ,max_length =50 ,null =True ,unique =True )),
    ('type_incident',models .CharField (choices =[('RETARD','Retard'),('PERTE','Perte'),('ENDOMMAGEMENT','Endommagement'),('PROBLEME_TECHNIQUE','Problème technique'),('AUTRE','Autre')],max_length =30 )),
    ('commentaire',models .TextField (blank =True ,null =True )),
    ('action_appliquee',models .CharField (choices =[('SET_ECHEC_LIVRAISON','Mettre expédition en échec de livraison'),('SET_ANNULEE','Mettre tournée en annulée'),('NONE','Aucun changement de statut')],default ='NONE',max_length =30 )),
    ('notify_direction',models .BooleanField (default =True )),
    ('notify_client',models .BooleanField (default =False )),
    ('created_at',models .DateTimeField (auto_now_add =True )),
    ('updated_at',models .DateTimeField (auto_now =True ,null =True )),
    ('created_by',models .ForeignKey (blank =True ,db_column ='created_by',null =True ,on_delete =django .db .models .deletion .SET_NULL ,to ='core.utilisateur')),
    ('expedition',models .ForeignKey (blank =True ,db_column ='expedition_id',null =True ,on_delete =django .db .models .deletion .CASCADE ,related_name ='incidents',to ='core.expedition')),
    ('tournee',models .ForeignKey (blank =True ,db_column ='tournee_id',null =True ,on_delete =django .db .models .deletion .CASCADE ,related_name ='incidents',to ='core.tournee')),
    ],
    options ={
    'db_table':'incident',
    'managed':True ,
    'ordering':['-created_at'],
    },
    ),
    migrations .CreateModel (
    name ='IncidentAttachment',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('file',models .FileField (upload_to =core .models .incident_attachment_upload_to )),
    ('original_name',models .CharField (blank =True ,max_length =255 ,null =True )),
    ('uploaded_at',models .DateTimeField (auto_now_add =True )),
    ('incident',models .ForeignKey (db_column ='incident_id',on_delete =django .db .models .deletion .CASCADE ,related_name ='attachments',to ='core.incident')),
    ('uploaded_by',models .ForeignKey (blank =True ,db_column ='uploaded_by',null =True ,on_delete =django .db .models .deletion .SET_NULL ,to ='core.utilisateur')),
    ],
    options ={
    'db_table':'incident_attachment',
    'managed':True ,
    'ordering':['-uploaded_at'],
    },
    ),
    migrations .CreateModel (
    name ='Alerte',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('type_alerte',models .CharField (choices =[('INCIDENT','Incident')],default ='INCIDENT',max_length =20 )),
    ('destination',models .CharField (choices =[('DIRECTION','Direction'),('CLIENT','Client')],max_length =20 )),
    ('titre',models .CharField (max_length =200 )),
    ('message',models .TextField (blank =True ,null =True )),
    ('is_read',models .BooleanField (default =False )),
    ('created_at',models .DateTimeField (auto_now_add =True )),
    ('expedition',models .ForeignKey (blank =True ,db_column ='expedition_id',null =True ,on_delete =django .db .models .deletion .SET_NULL ,related_name ='alertes',to ='core.expedition')),
    ('incident',models .ForeignKey (blank =True ,db_column ='incident_id',null =True ,on_delete =django .db .models .deletion .CASCADE ,related_name ='alertes',to ='core.incident')),
    ('tournee',models .ForeignKey (blank =True ,db_column ='tournee_id',null =True ,on_delete =django .db .models .deletion .SET_NULL ,related_name ='alertes',to ='core.tournee')),
    ],
    options ={
    'db_table':'alerte',
    'managed':True ,
    'ordering':['-created_at'],
    },
    ),
    migrations .AddIndex (
    model_name ='incident',
    index =models .Index (fields =['-created_at'],name ='incident_created__3e51bc_idx'),
    ),
    migrations .AddIndex (
    model_name ='incident',
    index =models .Index (fields =['type_incident','-created_at'],name ='incident_type_in_9ad5f3_idx'),
    ),
    migrations .AddIndex (
    model_name ='incident',
    index =models .Index (fields =['expedition','-created_at'],name ='incident_expediti_dbb83c_idx'),
    ),
    migrations .AddIndex (
    model_name ='incident',
    index =models .Index (fields =['tournee','-created_at'],name ='incident_tournee_7b848d_idx'),
    ),
    migrations .AddIndex (
    model_name ='alerte',
    index =models .Index (fields =['destination','is_read','-created_at'],name ='alerte_destina_9b3007_idx'),
    ),
    ],
    ),
    ]
