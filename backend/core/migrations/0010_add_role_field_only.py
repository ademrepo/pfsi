

from django .db import migrations ,models 
import django .db .models .deletion 


class Migration (migrations .Migration ):

    dependencies =[
    ('core','0009_destination_geo_fields'),
    ]

    operations =[
    migrations .AddField (
    model_name ='utilisateur',
    name ='role',
    field =models .ForeignKey (default =1 ,on_delete =django .db .models .deletion .PROTECT ,to ='core.role',db_column ='role_id'),
    preserve_default =False ,
    ),
    ]
