# Generated by Django 5.1.4 on 2024-12-10 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prestamos', '0011_perfilprestatarioprefab_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentoevaluacionprefab',
            name='perfil_prefab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='Prestamos.perfilprestatarioprefab'),
        ),
    ]