# Generated by Django 5.1.4 on 2024-12-11 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prestamos', '0013_perfilprestatarioprefab_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreguntaPerfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaPerfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Prestamos.preguntaperfil')),
            ],
        ),
        migrations.AddField(
            model_name='perfilprestatario',
            name='respuestas',
            field=models.ManyToManyField(to='Prestamos.respuestaperfil'),
        ),
        migrations.AddField(
            model_name='perfilprestatarioprefab',
            name='respuestas',
            field=models.ManyToManyField(to='Prestamos.respuestaperfil'),
        ),
    ]
