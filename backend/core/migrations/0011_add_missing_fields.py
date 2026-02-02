

from django .db import migrations ,models 
import django .db .models .deletion 


class Migration (migrations .Migration ):

    dependencies =[
    ('core','0010_add_role_field_only'),
    ]

    operations =[
    migrations .AlterField (
    model_name ='utilisateur',
    name ='role',
    field =models .ForeignKey (db_column ='role_id',default =1 ,on_delete =django .db .models .deletion .PROTECT ,to ='core.role'),
    ),
    ]
