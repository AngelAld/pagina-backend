# Generated by Django 5.1.4 on 2024-12-10 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Prestamos', '0008_alter_documento_evaluacion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perfilprestatarioprefab',
            old_name='usuario',
            new_name='dueño',
        ),
    ]
