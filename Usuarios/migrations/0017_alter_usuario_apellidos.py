# Generated by Django 5.1.4 on 2024-12-10 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0016_remove_perfilempleadoinmobiliaria_banner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='apellidos',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]