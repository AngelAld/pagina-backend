# Generated by Django 5.1.2 on 2024-11-19 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0013_perfilagenteprestamos_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilparticularinmuebles',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/particulares'),
        ),
    ]