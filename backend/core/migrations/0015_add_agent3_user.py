from django .db import migrations 

def add_agent3 (apps ,schema_editor ):
    Utilisateur =apps .get_model ('core','Utilisateur')
    Role =apps .get_model ('core','Role')



    try :
        agent_role =Role .objects .get (code ='AGENT')
    except Role .DoesNotExist :

        agent_role ,_ =Role .objects .get_or_create (
        id =2 ,
        defaults ={'code':'AGENT','libelle':'Agent de transport'}
        )
        if agent_role .code !='AGENT':


            agent_role =Role .objects .filter (code ='AGENT').first ()
            if not agent_role :
                 agent_role =Role .objects .create (code ='AGENT',libelle ='Agent de transport')

    Utilisateur .objects .get_or_create (
    username ='agent3',
    defaults ={
    'email':'ademglps@gmail.com',
    'password':'password123',
    'nom':'Adem',
    'prenom':'Hadjammar',
    'telephone':'0777345478',
    'role':agent_role ,
    'is_active':True 
    }
    )

def remove_agent3 (apps ,schema_editor ):
    Utilisateur =apps .get_model ('core','Utilisateur')
    Utilisateur .objects .filter (username ='agent3').delete ()

class Migration (migrations .Migration ):

    dependencies =[
    ('core','0014_chauffeur_vehicule'),
    ]

    operations =[
    migrations .RunPython (add_agent3 ,remove_agent3 ),
    ]
