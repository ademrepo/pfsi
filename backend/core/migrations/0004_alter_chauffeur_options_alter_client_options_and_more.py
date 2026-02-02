

from django .db import migrations 


class Migration (migrations .Migration ):

    dependencies =[
    ('core','0003_facture_factureexpedition_paiement'),
    ]

    operations =[
    migrations .AlterModelOptions (
    name ='chauffeur',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='client',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='destination',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='expedition',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='facture',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='factureexpedition',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='paiement',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='role',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='tarification',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='tournee',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='trackingexpedition',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='typeservice',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='utilisateur',
    options ={'managed':True },
    ),
    migrations .AlterModelOptions (
    name ='vehicule',
    options ={'managed':True },
    ),
    ]
