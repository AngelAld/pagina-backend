# Generated by Django 5.1.4 on 2024-12-12 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prestamos', '0018_perfilprestatario_inmueble'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacioncrediticia',
            name='estado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Prestamos.estadoevaluacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evaluacioncrediticia',
            name='etapa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Prestamos.etapaevaluacion'),
            preserve_default=False,
        ),
    ]