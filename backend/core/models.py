from django .db import models 
from django .db .models .signals import post_save ,pre_save 
from django .dispatch import receiver 
from django .utils import timezone 


class Role (models .Model ):
    """
    Modèle pour les rôles utilisateurs (table existante dans la BD)
    """
    code =models .CharField (max_length =50 ,unique =True )
    libelle =models .CharField (max_length =200 )

    class Meta :
        db_table ='role'
        managed =True 

    def __str__ (self ):
        return self .libelle 


class Utilisateur (models .Model ):
    """
    Modèle pour les utilisateurs (table existante dans la BD)
    Correspond à la table 'utilisateur' créée dans schema.sql
    """
    username =models .CharField (max_length =150 ,unique =True )
    email =models .CharField (max_length =254 ,unique =True )
    password =models .CharField (max_length =255 )
    nom =models .CharField (max_length =150 )
    prenom =models .CharField (max_length =150 )
    telephone =models .CharField (max_length =20 ,null =True ,blank =True )
    role =models .ForeignKey (Role ,on_delete =models .PROTECT ,db_column ='role_id',default =1 )
    is_active =models .BooleanField (default =True )
    created_at =models .DateTimeField (auto_now_add =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True ,blank =True )

    class Meta :
        db_table ='utilisateur'
        managed =True 

    def __str__ (self ):
        return f"{self .prenom } {self .nom } ({self .username })"

    def get_full_name (self ):
        return f"{self .prenom } {self .nom }"

    def has_role (self ,role_code ):
        """Vérifie si l'utilisateur a un rôle spécifique"""
        return self .role .code ==role_code 

    def can_manage_users (self ):
        """Seul l'admin peut gérer les utilisateurs"""
        return self .role .code =='ADMIN'


class AuditLog (models .Model ):
    """
    Journal d'audit pour la traçabilité
    Nouvelle table à créer
    """
    ACTION_CHOICES =[
    ('LOGIN_SUCCESS','Connexion réussie'),
    ('LOGIN_FAILED','Connexion échouée'),
    ('LOGOUT','Déconnexion'),
    ('USER_CREATED','Utilisateur créé'),
    ('USER_UPDATED','Utilisateur modifié'),
    ('USER_ACTIVATED','Utilisateur activé'),
    ('USER_DEACTIVATED','Utilisateur désactivé'),
    ('PASSWORD_RESET','Mot de passe réinitialisé'),
    ('ACCESS_DENIED','Accès refusé'),
    ]

    user =models .ForeignKey (
    Utilisateur ,
    on_delete =models .SET_NULL ,
    null =True ,
    blank =True ,
    related_name ='audit_logs',
    db_column ='utilisateur_id'
    )
    username =models .CharField (max_length =150 )
    action_type =models .CharField (max_length =50 ,choices =ACTION_CHOICES )
    ip_address =models .GenericIPAddressField (null =True ,blank =True )
    user_agent =models .TextField (null =True ,blank =True )
    details =models .JSONField (null =True ,blank =True )
    timestamp =models .DateTimeField (auto_now_add =True )

    class Meta :
        db_table ='audit_log'
        ordering =['-timestamp']
        indexes =[
        models .Index (fields =['-timestamp']),
        models .Index (fields =['user','-timestamp']),
        models .Index (fields =['action_type','-timestamp']),
        ]

    def __str__ (self ):
        return f"{self .username } - {self .get_action_type_display ()} - {self .timestamp }"


class PasswordResetToken (models .Model ):
    user =models .ForeignKey (Utilisateur ,on_delete =models .CASCADE ,related_name ='password_reset_tokens',db_column ='utilisateur_id')
    token_hash =models .CharField (max_length =64 ,unique =True )
    created_at =models .DateTimeField (auto_now_add =True )
    expires_at =models .DateTimeField ()
    used_at =models .DateTimeField (null =True ,blank =True )

    class Meta :
        db_table ='password_reset_token'
        managed =True 
        indexes =[
        models .Index (fields =['token_hash']),
        models .Index (fields =['expires_at']),
        models .Index (fields =['user','-created_at']),
        ]

    def is_valid (self ):
        if self .used_at is not None :
            return False 
        return timezone .now ()<=self .expires_at 


class Client (models .Model ):
    code_client =models .CharField (max_length =50 ,unique =True ,null =True )
    type_client =models .CharField (max_length =50 ,null =True )
    nom =models .CharField (max_length =200 )
    prenom =models .CharField (max_length =200 ,null =True ,blank =True )
    telephone =models .CharField (max_length =50 ,null =True ,blank =True )
    email =models .CharField (max_length =254 ,null =True ,blank =True )
    adresse =models .TextField (null =True ,blank =True )
    ville =models .CharField (max_length =100 ,null =True ,blank =True )
    pays =models .CharField (max_length =100 ,null =True ,blank =True )
    solde =models .FloatField (default =0 )
    statut =models .CharField (max_length =50 ,default ='actif')
    created_at =models .DateTimeField (auto_now_add =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='client'
        managed =True 

    def __str__ (self ):
        if self .prenom :
            return f"{self .nom } {self .prenom }"
        return self .nom 


class Chauffeur (models .Model ):
    matricule =models .CharField (max_length =50 ,unique =True ,null =True )
    nom =models .CharField (max_length =200 )
    prenom =models .CharField (max_length =200 )
    telephone =models .CharField (max_length =50 ,null =True ,blank =True )
    email =models .CharField (max_length =254 ,null =True ,blank =True )
    adresse =models .TextField (null =True ,blank =True )
    num_permis =models .CharField (max_length =100 ,unique =True )
    categorie_permis =models .CharField (max_length =50 ,null =True ,blank =True )
    date_embauche =models .DateField (null =True ,blank =True )
    disponibilite =models .CharField (max_length =50 ,null =True ,blank =True )
    statut =models .CharField (max_length =50 ,null =True ,blank =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='chauffeur'
        managed =True 

    def __str__ (self ):
        return f"{self .nom } {self .prenom } ({self .matricule })"


class Vehicule (models .Model ):
    immatriculation =models .CharField (max_length =50 ,unique =True )
    type_vehicule =models .CharField (max_length =50 ,null =True )
    marque =models .CharField (max_length =100 ,null =True ,blank =True )
    modele =models .CharField (max_length =100 ,null =True ,blank =True )
    capacite_kg =models .FloatField ()
    capacite_m3 =models .FloatField ()
    consommation_100km =models .FloatField (null =True ,blank =True )
    etat =models .CharField (max_length =50 ,null =True ,blank =True )
    disponibilite =models .CharField (max_length =50 ,null =True ,blank =True )
    date_mise_en_service =models .DateField (null =True ,blank =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='vehicule'
        managed =True 

    def __str__ (self ):
        return f"{self .marque } {self .modele } - {self .immatriculation }"


class Destination (models .Model ):
    pays =models .CharField (max_length =100 ,null =True ,blank =True )
    ville =models .CharField (max_length =100 ,null =True ,blank =True )
    zone_geographique =models .CharField (max_length =100 ,null =True ,blank =True )
    code_zone =models .CharField (max_length =50 ,null =True ,blank =True )
    latitude =models .FloatField (null =True ,blank =True )
    longitude =models .FloatField (null =True ,blank =True )
    tarif_base_defaut =models .FloatField ()
    is_active =models .BooleanField (default =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='destination'
        managed =True 

    def __str__ (self ):
        return f"{self .ville }, {self .pays } ({self .zone_geographique })"


class TypeService (models .Model ):
    code =models .CharField (max_length =50 ,unique =True ,null =True )
    libelle =models .CharField (max_length =200 ,null =True ,blank =True )
    description =models .TextField (null =True ,blank =True )
    delai_estime_jours =models .IntegerField (null =True ,blank =True )
    priorite =models .IntegerField (null =True ,blank =True )
    is_active =models .BooleanField (default =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='type_service'
        managed =True 

    def __str__ (self ):
        return self .libelle 


class Tarification (models .Model ):
    type_service =models .ForeignKey (TypeService ,on_delete =models .PROTECT ,db_column ='type_service_id',null =True )
    destination =models .ForeignKey (Destination ,on_delete =models .PROTECT ,db_column ='destination_id',null =True )
    tarif_base =models .FloatField (default =0 )
    tarif_poids_kg =models .FloatField (null =True ,blank =True )
    tarif_volume_m3 =models .FloatField (null =True ,blank =True )
    date_debut =models .DateField (null =True ,blank =True )
    date_fin =models .DateField (null =True ,blank =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='tarification'
        managed =True 


class Tournee (models .Model ):
    code_tournee =models .CharField (max_length =50 ,unique =True ,null =True )
    date_tournee =models .DateField (null =True ,blank =True )
    date_depart =models .DateTimeField (null =True ,blank =True )
    date_retour =models .DateTimeField (null =True ,blank =True )
    chauffeur =models .ForeignKey (Chauffeur ,on_delete =models .PROTECT ,db_column ='chauffeur_id',null =True )
    vehicule =models .ForeignKey (Vehicule ,on_delete =models .PROTECT ,db_column ='vehicule_id',null =True )
    statut =models .CharField (max_length =50 ,null =True ,blank =True )
    kilometrage_depart =models .FloatField (null =True ,blank =True )
    kilometrage_retour =models .FloatField (null =True ,blank =True )
    distance_km =models .FloatField (null =True ,blank =True )
    duree_minutes =models .IntegerField (null =True ,blank =True )
    consommation_litres =models .FloatField (null =True ,blank =True )
    notes =models .TextField (null =True ,blank =True )
    points_passage =models .TextField (null =True ,blank =True )
    created_by =models .ForeignKey (Utilisateur ,on_delete =models .SET_NULL ,db_column ='created_by',null =True ,blank =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='tournee'
        managed =True 

    def __str__ (self ):
        return self .code_tournee 


class Expedition (models .Model ):
    code_expedition =models .CharField (max_length =50 ,unique =True ,null =True )
    client =models .ForeignKey (Client ,on_delete =models .PROTECT ,db_column ='client_id',null =True )
    type_service =models .ForeignKey (TypeService ,on_delete =models .PROTECT ,db_column ='type_service_id',null =True )
    destination =models .ForeignKey (Destination ,on_delete =models .PROTECT ,db_column ='destination_id',null =True )
    poids_kg =models .FloatField ()
    volume_m3 =models .FloatField ()
    description_colis =models .TextField (null =True ,blank =True )
    adresse_livraison =models .TextField (null =True ,blank =True )
    nom_destinataire =models .CharField (max_length =200 ,null =True ,blank =True )
    telephone_destinataire =models .CharField (max_length =50 ,null =True ,blank =True )
    date_creation =models .DateTimeField (auto_now_add =True )
    statut =models .CharField (max_length =50 ,null =True ,blank =True )
    montant_total =models .FloatField (default =0 )
    est_facturee =models .BooleanField (default =False )
    tournee =models .ForeignKey (Tournee ,on_delete =models .SET_NULL ,db_column ='tournee_id',null =True ,blank =True ,related_name ='expeditions')
    created_by =models .ForeignKey (Utilisateur ,on_delete =models .SET_NULL ,db_column ='created_by',null =True ,blank =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='expedition'
        managed =True 

    def __str__ (self ):
        return self .code_expedition 


class TrackingExpedition (models .Model ):
    expedition =models .ForeignKey (Expedition ,on_delete =models .CASCADE ,db_column ='expedition_id',null =True ,related_name ='tracking_history')
    chauffeur =models .ForeignKey (Chauffeur ,on_delete =models .SET_NULL ,db_column ='chauffeur_id',null =True ,blank =True )
    tournee =models .ForeignKey (Tournee ,on_delete =models .SET_NULL ,db_column ='tournee_id',null =True ,blank =True )
    statut =models .CharField (max_length =50 ,null =True ,blank =True )
    lieu =models .CharField (max_length =200 ,null =True ,blank =True )
    commentaire =models .TextField (null =True ,blank =True )
    date_statut =models .DateTimeField (null =True ,blank =True )

    class Meta :
        db_table ='tracking_expedition'
        managed =True 


class Incident (models .Model ):
    TYPE_CHOICES =[
    ('RETARD','Retard'),
    ('PERTE','Perte'),
    ('ENDOMMAGEMENT','Endommagement'),
    ('PROBLEME_TECHNIQUE','Problème technique'),
    ('AUTRE','Autre'),
    ]


    ACTION_CHOICES =[
    ('SET_ECHEC_LIVRAISON','Mettre expédition en échec de livraison'),
    ('SET_ANNULEE','Mettre tournée en annulée'),
    ('NONE','Aucun changement de statut'),
    ]

    code_incident =models .CharField (max_length =50 ,unique =True ,null =True ,blank =True )
    type_incident =models .CharField (max_length =30 ,choices =TYPE_CHOICES )
    expedition =models .ForeignKey (
    Expedition ,
    on_delete =models .CASCADE ,
    db_column ='expedition_id',
    null =True ,
    blank =True ,
    related_name ='incidents',
    )
    tournee =models .ForeignKey (
    Tournee ,
    on_delete =models .CASCADE ,
    db_column ='tournee_id',
    null =True ,
    blank =True ,
    related_name ='incidents',
    )
    commentaire =models .TextField (null =True ,blank =True )
    action_appliquee =models .CharField (max_length =30 ,choices =ACTION_CHOICES ,default ='NONE')
    notify_direction =models .BooleanField (default =True )
    notify_client =models .BooleanField (default =False )
    created_by =models .ForeignKey (Utilisateur ,on_delete =models .SET_NULL ,db_column ='created_by',null =True ,blank =True )
    created_at =models .DateTimeField (auto_now_add =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='incident'
        managed =True 
        ordering =['-created_at']
        indexes =[
        models .Index (fields =['-created_at']),
        models .Index (fields =['type_incident','-created_at']),
        models .Index (fields =['expedition','-created_at']),
        models .Index (fields =['tournee','-created_at']),
        ]

    def __str__ (self ):
        return self .code_incident or f"Incident #{self .id }"


def incident_attachment_upload_to (instance ,filename :str )->str :
    incident_id =instance .incident_id or 'new'
    return f"incidents/{incident_id }/{filename }"


class IncidentAttachment (models .Model ):
    incident =models .ForeignKey (Incident ,on_delete =models .CASCADE ,related_name ='attachments',db_column ='incident_id')
    file =models .FileField (upload_to =incident_attachment_upload_to )
    original_name =models .CharField (max_length =255 ,null =True ,blank =True )
    uploaded_by =models .ForeignKey (Utilisateur ,on_delete =models .SET_NULL ,db_column ='uploaded_by',null =True ,blank =True )
    uploaded_at =models .DateTimeField (auto_now_add =True )

    class Meta :
        db_table ='incident_attachment'
        managed =True 
        ordering =['-uploaded_at']

    def __str__ (self ):
        return self .original_name or self .file .name or f"Attachment #{self .id }"


class Alerte (models .Model ):
    DEST_CHOICES =[
    ('DIRECTION','Direction'),
    ('CLIENT','Client'),
    ]
    TYPE_CHOICES =[
    ('INCIDENT','Incident'),
    ]

    type_alerte =models .CharField (max_length =20 ,choices =TYPE_CHOICES ,default ='INCIDENT')
    destination =models .CharField (max_length =20 ,choices =DEST_CHOICES )
    titre =models .CharField (max_length =200 )
    message =models .TextField (null =True ,blank =True )
    incident =models .ForeignKey (Incident ,on_delete =models .CASCADE ,null =True ,blank =True ,related_name ='alertes',db_column ='incident_id')
    expedition =models .ForeignKey (Expedition ,on_delete =models .SET_NULL ,null =True ,blank =True ,related_name ='alertes',db_column ='expedition_id')
    tournee =models .ForeignKey (Tournee ,on_delete =models .SET_NULL ,null =True ,blank =True ,related_name ='alertes',db_column ='tournee_id')
    is_read =models .BooleanField (default =False )
    created_at =models .DateTimeField (auto_now_add =True )

    class Meta :
        db_table ='alerte'
        managed =True 
        ordering =['-created_at']
        indexes =[
        models .Index (fields =['destination','is_read','-created_at']),
        ]

    def __str__ (self ):
        return f"{self .get_destination_display ()} - {self .titre }"


class Reclamation (models .Model ):
    STATUT_CHOICES =[
    ('EN_COURS','En cours'),
    ('RESOLUE','Résolue'),
    ('ANNULEE','Annulée'),
    ]

    client =models .ForeignKey (Client ,on_delete =models .PROTECT ,db_column ='client_id',null =True )
    objet =models .TextField (null =True ,blank =True )
    description =models .TextField (null =True ,blank =True )
    date_reclamation =models .DateField (null =True ,blank =True )
    statut =models .CharField (max_length =20 ,choices =STATUT_CHOICES ,default ='EN_COURS',null =True ,blank =True )


    expedition =models .ForeignKey (
    Expedition ,
    on_delete =models .SET_NULL ,
    db_column ='expedition_id',
    null =True ,
    blank =True ,
    related_name ='reclamations_principales',
    )
    expeditions =models .ManyToManyField (
    Expedition ,
    through ='ReclamationExpedition',
    related_name ='reclamations',
    blank =True ,
    )

    facture =models .ForeignKey ('Facture',on_delete =models .SET_NULL ,db_column ='facture_id',null =True ,blank =True )
    type_service =models .ForeignKey ('TypeService',on_delete =models .SET_NULL ,db_column ='type_service_id',null =True ,blank =True )

    traite_par =models .ForeignKey (Utilisateur ,on_delete =models .SET_NULL ,db_column ='traite_par',null =True ,blank =True ,related_name ='reclamations_traitees')
    date_resolution =models .DateField (null =True ,blank =True )

    class Meta :
        db_table ='reclamation'
        managed =True 
        ordering =['-date_reclamation','-id']
        indexes =[
        models .Index (fields =['client','-date_reclamation']),
        models .Index (fields =['statut','-date_reclamation']),
        ]

    def __str__ (self ):
        return f"Réclamation #{self .id }"


class ReclamationExpedition (models .Model ):
    reclamation =models .ForeignKey (Reclamation ,on_delete =models .CASCADE ,db_column ='reclamation_id')
    expedition =models .ForeignKey (Expedition ,on_delete =models .CASCADE ,db_column ='expedition_id')

    class Meta :
        db_table ='reclamation_expedition'
        managed =True 
        unique_together =(('reclamation','expedition'),)


class Facture (models .Model ):
    numero_facture =models .CharField (max_length =50 ,unique =True ,null =True )
    client =models .ForeignKey (Client ,on_delete =models .PROTECT ,db_column ='client_id',null =True )
    date_facture =models .DateField (null =True ,blank =True )
    total_ht =models .FloatField (null =True ,blank =True )
    montant_tva =models .FloatField (null =True ,blank =True )
    total_ttc =models .FloatField (null =True ,blank =True )
    statut =models .CharField (max_length =50 ,null =True ,blank =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='facture'
        managed =True 

    def __str__ (self ):
        return self .numero_facture or f"Facture #{self .id }"


class FactureExpedition (models .Model ):
    facture =models .ForeignKey ('Facture',on_delete =models .CASCADE ,db_column ='facture_id',null =True )
    expedition =models .ForeignKey (Expedition ,on_delete =models .CASCADE ,db_column ='expedition_id',null =True )

    class Meta :
        db_table ='facture_expedition'
        managed =True 
        unique_together =(('facture','expedition'),)


class Paiement (models .Model ):
    facture =models .ForeignKey ('Facture',on_delete =models .CASCADE ,db_column ='facture_id',null =True ,blank =True )
    client =models .ForeignKey (Client ,on_delete =models .CASCADE ,db_column ='client_id',null =True )
    date_paiement =models .DateField (null =True ,blank =True )
    mode_paiement =models .CharField (max_length =100 ,null =True ,blank =True )
    montant =models .FloatField (null =True ,blank =True )
    statut =models .CharField (max_length =50 ,null =True ,blank =True )
    updated_at =models .DateTimeField (auto_now =True ,null =True )

    class Meta :
        db_table ='paiement'
        managed =True 

    def __str__ (self ):
        return f"Paiement {self .id } - {self .montant }€"




@receiver (pre_save ,sender =Client )
def generate_client_code (sender ,instance ,**kwargs ):
    """Generate client code if not provided"""
    if not instance .code_client or instance .code_client =='':

        last_client =Client .objects .order_by ('-id').first ()
        next_id =(last_client .id +1 )if last_client else 1 
        instance .code_client =f'CLI-{str (next_id ).zfill (5 )}'

@receiver (pre_save ,sender =Chauffeur )
def generate_chauffeur_matricule (sender ,instance ,**kwargs ):
    """Generate chauffeur matricule if not provided"""
    if not instance .matricule or instance .matricule =='':
        last_chauffeur =Chauffeur .objects .order_by ('-id').first ()
        next_id =(last_chauffeur .id +1 )if last_chauffeur else 1 
        instance .matricule =f'CHF-{str (next_id ).zfill (5 )}'

@receiver (pre_save ,sender =Expedition )
def generate_expedition_code (sender ,instance ,**kwargs ):
    """Generate expedition code if not provided"""
    if not instance .code_expedition or instance .code_expedition =='':
        last_expedition =Expedition .objects .order_by ('-id').first ()
        next_id =(last_expedition .id +1 )if last_expedition else 1 
        date_str =timezone .now ().strftime ('%Y%m%d')
        instance .code_expedition =f'EXP-{date_str }-{str (next_id ).zfill (5 )}'

@receiver (pre_save ,sender =Tournee )
def generate_tournee_code (sender ,instance ,**kwargs ):
    """Generate tournee code if not provided"""
    if not instance .code_tournee or instance .code_tournee =='':
        last_tournee =Tournee .objects .order_by ('-id').first ()
        next_id =(last_tournee .id +1 )if last_tournee else 1 
        date_str =timezone .now ().strftime ('%Y%m%d')
        instance .code_tournee =f'TRN-{date_str }-{str (next_id ).zfill (2 )}'

@receiver (pre_save ,sender =Incident )
def generate_incident_code (sender ,instance ,**kwargs ):
    """Generate incident code if not provided"""
    if not instance .code_incident or instance .code_incident =='':
        last_item =Incident .objects .order_by ('-id').first ()
        next_id =(last_item .id +1 )if last_item else 1 
        date_str =timezone .now ().strftime ('%Y%m%d')
        instance .code_incident =f'INC-{date_str }-{str (next_id ).zfill (5 )}'

@receiver (pre_save ,sender =Facture )
def generate_facture_numero (sender ,instance ,**kwargs ):
    """Generate invoice number if not provided"""
    if not instance .numero_facture or instance .numero_facture =='':
        last_facture =Facture .objects .order_by ('-id').first ()
        next_id =(last_facture .id +1 )if last_facture else 1 
        date_str =timezone .now ().strftime ('%Y%m')
        instance .numero_facture =f'FACT-{date_str }-{str (next_id ).zfill (5 )}'

@receiver (post_save ,sender =Expedition )
def expedition_post_save (sender ,instance ,created ,**kwargs ):
    """Handle expedition creation and updates"""
    if created :

        TrackingExpedition .objects .create (
        expedition =instance ,
        statut ='Enregistré',
        lieu ='Création expédition',
        date_statut =timezone .now ()
        )

@receiver (post_save ,sender =TrackingExpedition )
def tracking_post_save (sender ,instance ,created ,**kwargs ):
    """Update expedition statut when new tracking is created"""
    if created and instance .expedition :
        instance .expedition .statut =instance .statut 
        instance .expedition .save (update_fields =['statut'])

@receiver (post_save ,sender =FactureExpedition )
def facture_expedition_post_save (sender ,instance ,created ,**kwargs ):
    """Mark expedition as invoiced when linked to invoice"""
    if created :
        instance .expedition .est_facturee =True 
        instance .expedition .save (update_fields =['est_facturee'])

