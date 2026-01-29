# Migration to acknowledge existing fields without changes

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_add_missing_fields'),
    ]

    operations = [
        # This is a no-op migration to acknowledge the current state
        # The fields already exist in the database from the schema.sql
        migrations.RunPython(migrations.RunPython.noop),
    ]