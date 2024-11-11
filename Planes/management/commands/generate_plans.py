from django.core.management.base import BaseCommand
from Planes.models import PlanInmuebles, PlanPrestamos, PlanServicios


class Command(BaseCommand):
    help = "Genera los tipos basicos de planes"

    def handle(self, *args, **options):

        PlanInmuebles.objects.get_or_create(
            nombre="Plan Cliente",
            defaults={
                "descripcion": "Plan basico para clientes",
                "precio": 0,
                "max_inmuebles": 0,
                "max_empleados": 0,
                "max_alertas": 3,
                "compartir_comision": False,
            },
        )
        self.stdout.write(
            self.style.SUCCESS("Plan Basico de clientes para inmuebles creado")
        )
        PlanInmuebles.objects.get_or_create(
            nombre="Plan Particular",
            defaults={
                "descripcion": "Plan basico para particulares",
                "precio": 0,
                "max_inmuebles": 5,
                "max_empleados": 0,
                "max_alertas": 3,
                "compartir_comision": False,
            },
        )
        self.stdout.write(self.style.SUCCESS("Plan Basico de particulares creado"))
        PlanInmuebles.objects.get_or_create(
            nombre="Plan Inmobiliaria",
            defaults={
                "descripcion": "Plan basico para inmobiliarias",
                "precio": 0,
                "max_inmuebles": 100,
                "max_empleados": 5,
                "max_alertas": 10,
                "compartir_comision": True,
            },
        )
        self.stdout.write(self.style.SUCCESS("Plan Basico de inmobiliarias creado"))
        PlanInmuebles.objects.get_or_create(
            nombre="Plan Agente",
            defaults={
                "descripcion": "Plan basico para agentes inmobiliarios",
                "precio": 0,
                "max_inmuebles": 10,
                "max_empleados": 0,
                "max_alertas": 5,
                "compartir_comision": True,
            },
        )
        self.stdout.write(
            self.style.SUCCESS("Plan Basico de agentes inmobiliarios creado")
        )
        PlanPrestamos.objects.get_or_create(
            nombre="Plan Cliente",
            defaults={
                "descripcion": "Plan basico para clientes",
                "precio": 0,
                "max_clientes": 0,
                "max_alertas": 3,
            },
        )
        self.stdout.write(
            self.style.SUCCESS("Plan Basico de clientes para prestamos creado")
        )
        PlanPrestamos.objects.get_or_create(
            nombre="Plan Agente",
            defaults={
                "descripcion": "Plan basico para agentes de prestamos",
                "precio": 0,
                "max_clientes": 100,
                "max_alertas": 5,
            },
        )
        self.stdout.write(
            self.style.SUCCESS("Plan Basico de agentes de prestamos creado")
        )
        PlanServicios.objects.get_or_create(
            nombre="Plan Cliente",
            defaults={
                "descripcion": "Plan basico para clientes",
                "precio": 0,
                "max_ocupaciones": 0,
                "max_habilidades": 0,
                "max_avisos": 0,
                "max_alertas": 3,
            },
        )
        self.stdout.write(
            self.style.SUCCESS("Plan Basico de clientes para servicios creado")
        )
        PlanServicios.objects.get_or_create(
            nombre="Plan Profesional",
            defaults={
                "descripcion": "Plan basico para profesionales",
                "precio": 0,
                "max_ocupaciones": 5,
                "max_habilidades": 5,
                "max_avisos": 5,
                "max_alertas": 5,
            },
        )
        self.stdout.write(
            self.style.SUCCESS("Plan Basico de profesionales de servicios creado")
        )
