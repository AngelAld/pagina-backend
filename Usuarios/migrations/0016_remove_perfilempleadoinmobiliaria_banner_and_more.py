# Generated by Django 5.1.4 on 2024-12-09 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0015_perfilempleadoinmobiliaria_banner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfilempleadoinmobiliaria',
            name='banner',
        ),
        migrations.DeleteModel(
            name='PerfilAgentePrestamos',
        ),
    ]