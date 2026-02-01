from django.db import migrations

def add_agent3(apps, schema_editor):
    Utilisateur = apps.get_model('core', 'Utilisateur')
    Role = apps.get_model('core', 'Role')
    
    # Try to find the AGENT role, assuming it exists from initial data
    # data.sql defines 'AGENT' with id=2
    try:
        agent_role = Role.objects.get(code='AGENT')
    except Role.DoesNotExist:
        # If specific role doesn't exist, try to get by ID 2 as per data.sql
        agent_role, _ = Role.objects.get_or_create(
            id=2, 
            defaults={'code': 'AGENT', 'libelle': 'Agent de transport'}
        )
        if agent_role.code != 'AGENT':
            # If ID 2 exists but isn't AGENT, we have a problem, but let's just use it or find AGENT
            # Ideally we want the AGENT role.
            agent_role = Role.objects.filter(code='AGENT').first()
            if not agent_role:
                 agent_role = Role.objects.create(code='AGENT', libelle='Agent de transport')

    Utilisateur.objects.get_or_create(
        username='agent3',
        defaults={
            'email': 'ademglps@gmail.com',
            'password': 'password123',
            'nom': 'Adem',
            'prenom': 'Hadjammar',
            'telephone': '0777345478',
            'role': agent_role,
            'is_active': True
        }
    )

def remove_agent3(apps, schema_editor):
    Utilisateur = apps.get_model('core', 'Utilisateur')
    Utilisateur.objects.filter(username='agent3').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_chauffeur_vehicule'),
    ]

    operations = [
        migrations.RunPython(add_agent3, remove_agent3),
    ]
