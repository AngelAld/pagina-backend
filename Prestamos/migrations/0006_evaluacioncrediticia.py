# Generated by Django 5.1.4 on 2024-12-09 20:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prestamos', '0005_estadoevaluacion_etapaevaluacion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluacionCrediticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='Prestamos.perfilagentehipotecario')),
                ('prestatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='Prestamos.perfilprestatario')),
            ],
        ),
    ]