from django.core.management.base import BaseCommand
from Prestamos.models import EntidadBancaria, EstadoEvaluacion, EtapaEvaluacion

entidades = ["BCP"]

estados = [
    "En solicitud",
    "En evaluación",
    "Observado",
    "Aprobado",
    "Rechazado",
]

etapas = [
    "Solicitud",
    "Evaluación",
    "Resolución",
]


class Command(BaseCommand):
    help = "Genera data basica para el modulo de creditos hipotecarios"

    def handle(self, *args, **options):
        self.stdout.write(
            "Generando data basica para el modulo de creditos hipotecarios"
        )

        self.stdout.write("Creando entidades bancarias")

        for entidad in entidades:
            EntidadBancaria.objects.create(nombre=entidad)

        self.stdout.write("Creando estados de evaluación")

        for estado in estados:
            EstadoEvaluacion.objects.create(nombre=estado)

        self.stdout.write("Creando etapas de evaluación")

        for etapa in etapas:
            EtapaEvaluacion.objects.create(nombre=etapa)
