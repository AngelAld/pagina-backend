# Generated by Django 5.1.2 on 2024-11-04 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlanInmuebles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_propiedades', models.PositiveIntegerField()),
                ('max_empleados', models.PositiveIntegerField()),
                ('max_alertas', models.PositiveIntegerField()),
                ('compartir_comision', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PlanPrestamos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_clientes', models.PositiveIntegerField()),
                ('max_empleados', models.PositiveIntegerField()),
                ('max_alertas', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PlanServicios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_ocupaciones', models.PositiveIntegerField()),
                ('max_habilidades', models.PositiveIntegerField()),
                ('max_avisos', models.PositiveIntegerField()),
                ('max_alertas', models.PositiveIntegerField()),
            ],
        ),
    ]
