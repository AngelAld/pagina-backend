# Generated by Django 5.1.2 on 2024-11-09 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0012_alter_usuario_provider_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilagenteprestamos',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/agentes'),
        ),
    ]
