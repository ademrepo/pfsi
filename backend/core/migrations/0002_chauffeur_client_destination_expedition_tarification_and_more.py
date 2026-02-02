

from django .db import migrations ,models 


class Migration (migrations .Migration ):

    dependencies =[
    ('core','0001_initial'),
    ]

    operations =[
    migrations .CreateModel (
    name ='Chauffeur',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('matricule',models .CharField (max_length =50 ,null =True ,unique =True )),
    ('nom',models .CharField (max_length =200 )),
    ('prenom',models .CharField (max_length =200 )),
    ('telephone',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('email',models .CharField (blank =True ,max_length =254 ,null =True )),
    ('adresse',models .TextField (blank =True ,null =True )),
    ('num_permis',models .CharField (max_length =100 ,unique =True )),
    ('categorie_permis',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('date_embauche',models .DateField (blank =True ,null =True )),
    ('disponibilite',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('statut',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('updated_at',models .DateTimeField (auto_now =True ,null =True )),
    ],
    options ={
    'db_table':'chauffeur',
    'managed':False ,
    },
    ),
    migrations .CreateModel (
    name ='Client',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('code_client',models .CharField (max_length =50 ,null =True ,unique =True )),
    ('type_client',models .CharField (max_length =50 ,null =True )),
    ('nom',models .CharField (max_length =200 )),
    ('prenom',models .CharField (blank =True ,max_length =200 ,null =True )),
    ('telephone',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('email',models .CharField (blank =True ,max_length =254 ,null =True )),
    ('adresse',models .TextField (blank =True ,null =True )),
    ('ville',models .CharField (blank =True ,max_length =100 ,null =True )),
    ('pays',models .CharField (blank =True ,max_length =100 ,null =True )),
    ('solde',models .FloatField (default =0 )),
    ('statut',models .CharField (default ='actif',max_length =50 )),
    ('created_at',models .DateTimeField (auto_now_add =True )),
    ('updated_at',models .DateTimeField (auto_now =True ,null =True )),
    ],
    options ={
    'db_table':'client',
    'managed':False ,
    },
    ),
    migrations .CreateModel (
    name ='Destination',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('pays',models .CharField (blank =True ,max_length =100 ,null =True )),
    ('ville',models .CharField (blank =True ,max_length =100 ,null =True )),
    ('zone_geographique',models .CharField (blank =True ,max_length =100 ,null =True )),
    ('code_zone',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('tarif_base_defaut',models .FloatField ()),
    ('is_active',models .BooleanField (default =True )),
    ('updated_at',models .DateTimeField (auto_now =True ,null =True )),
    ],
    options ={
    'db_table':'destination',
    'managed':False ,
    },
    ),
    migrations .CreateModel (
    name ='Expedition',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('code_expedition',models .CharField (max_length =50 ,null =True ,unique =True )),
    ('poids_kg',models .FloatField ()),
    ('volume_m3',models .FloatField ()),
    ('description_colis',models .TextField (blank =True ,null =True )),
    ('adresse_livraison',models .TextField (blank =True ,null =True )),
    ('nom_destinataire',models .CharField (blank =True ,max_length =200 ,null =True )),
    ('telephone_destinataire',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('date_creation',models .DateTimeField (auto_now_add =True )),
    ('statut',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('montant_total',models .FloatField (default =0 )),
    ('est_facturee',models .BooleanField (default =False )),
    ('updated_at',models .DateTimeField (auto_now =True ,null =True )),
    ],
    options ={
    'db_table':'expedition',
    'managed':False ,
    },
    ),
    migrations .CreateModel (
    name ='Tarification',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('tarif_base',models .FloatField (default =0 )),
    ('tarif_poids_kg',models .FloatField (blank =True ,null =True )),
    ('tarif_volume_m3',models .FloatField (blank =True ,null =True )),
    ('date_debut',models .DateField (blank =True ,null =True )),
    ('date_fin',models .DateField (blank =True ,null =True )),
    ('updated_at',models .DateTimeField (auto_now =True ,null =True )),
    ],
    options ={
    'db_table':'tarification',
    'managed':False ,
    },
    ),
    migrations .CreateModel (
    name ='Tournee',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('code_tournee',models .CharField (max_length =50 ,null =True ,unique =True )),
    ('date_tournee',models .DateField (blank =True ,null =True )),
    ('date_depart',models .DateTimeField (blank =True ,null =True )),
    ('date_retour',models .DateTimeField (blank =True ,null =True )),
    ('statut',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('kilometrage_depart',models .FloatField (blank =True ,null =True )),
    ('kilometrage_retour',models .FloatField (blank =True ,null =True )),
    ('distance_km',models .FloatField (blank =True ,null =True )),
    ('duree_minutes',models .IntegerField (blank =True ,null =True )),
    ('consommation_litres',models .FloatField (blank =True ,null =True )),
    ('notes',models .TextField (blank =True ,null =True )),
    ('updated_at',models .DateTimeField (auto_now =True ,null =True )),
    ],
    options ={
    'db_table':'tournee',
    'managed':False ,
    },
    ),
    migrations .CreateModel (
    name ='TrackingExpedition',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('statut',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('lieu',models .CharField (blank =True ,max_length =200 ,null =True )),
    ('commentaire',models .TextField (blank =True ,null =True )),
    ('date_statut',models .DateTimeField (blank =True ,null =True )),
    ],
    options ={
    'db_table':'tracking_expedition',
    'managed':False ,
    },
    ),
    migrations .CreateModel (
    name ='TypeService',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('code',models .CharField (max_length =50 ,null =True ,unique =True )),
    ('libelle',models .CharField (blank =True ,max_length =200 ,null =True )),
    ('description',models .TextField (blank =True ,null =True )),
    ('delai_estime_jours',models .IntegerField (blank =True ,null =True )),
    ('priorite',models .IntegerField (blank =True ,null =True )),
    ('is_active',models .BooleanField (default =True )),
    ('updated_at',models .DateTimeField (auto_now =True ,null =True )),
    ],
    options ={
    'db_table':'type_service',
    'managed':False ,
    },
    ),
    migrations .CreateModel (
    name ='Vehicule',
    fields =[
    ('id',models .BigAutoField (auto_created =True ,primary_key =True ,serialize =False ,verbose_name ='ID')),
    ('immatriculation',models .CharField (max_length =50 ,unique =True )),
    ('type_vehicule',models .CharField (max_length =50 ,null =True )),
    ('marque',models .CharField (blank =True ,max_length =100 ,null =True )),
    ('modele',models .CharField (blank =True ,max_length =100 ,null =True )),
    ('capacite_kg',models .FloatField ()),
    ('capacite_m3',models .FloatField ()),
    ('consommation_100km',models .FloatField (blank =True ,null =True )),
    ('etat',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('disponibilite',models .CharField (blank =True ,max_length =50 ,null =True )),
    ('date_mise_en_service',models .DateField (blank =True ,null =True )),
    ('updated_at',models .DateTimeField (auto_now =True ,null =True )),
    ],
    options ={
    'db_table':'vehicule',
    'managed':False ,
    },
    ),
    ]
