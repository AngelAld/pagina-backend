# Generated by Django 5.1.4 on 2024-12-09 20:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Planes', '0003_rename_max_propiedades_planinmuebles_max_inmuebles'),
        ('Prestamos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilAgentePrestamos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar/agentes')),
                ('telefono', models.CharField(max_length=9)),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Prestamos.entidadbancaria')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Planes.planprestamos')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_agente', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]