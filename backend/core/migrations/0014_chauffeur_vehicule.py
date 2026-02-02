

from django .db import migrations ,models 
import django .db .models .deletion 


class Migration (migrations .Migration ):

    dependencies =[
    ('core','0013_rename_alerte_destina_9b3007_idx_alerte_destina_2e1ecc_idx_and_more'),
    ]

    operations =[
    migrations .AddField (
    model_name ='chauffeur',
    name ='vehicule',
    field =models .ForeignKey (blank =True ,db_column ='vehicule_id',null =True ,on_delete =django .db .models .deletion .SET_NULL ,related_name ='chauffeurs',to ='core.vehicule'),
    ),
    ]
