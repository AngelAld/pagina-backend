from django.core.management.base import BaseCommand
from Prestamos.models import (
    EntidadBancaria,
    EstadoEvaluacion,
    EtapaEvaluacion,
    PreguntaPerfil,
    RespuestaPerfil,
)

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

preguntas = ["pregunta1", "pregunta2", "pregunta3"]

respuestas = ["respuesta1", "respuesta2", "respuesta3"]


class Command(BaseCommand):
    help = "Genera data basica para el modulo de creditos hipotecarios"

    def handle(self, *args, **options):
        self.stdout.write(
            "Generando data basica para el modulo de creditos hipotecarios"
        )

        self.stdout.write("Creando entidades bancarias")

        for entidad in entidades:
            EntidadBancaria.objects.get_or_create(nombre=entidad)

        self.stdout.write("Creando estados de evaluación")

        for estado in estados:
            EstadoEvaluacion.objects.get_or_create(nombre=estado)

        self.stdout.write("Creando etapas de evaluación")

        for etapa in etapas:
            EtapaEvaluacion.objects.get_or_create(nombre=etapa)

        for pregunta in preguntas:
            self.stdout.write(f"Creando {pregunta}")
            pregunta_obj, _ = PreguntaPerfil.objects.get_or_create(nombre=pregunta)

            for respuesta in respuestas:
                texto = f"{pregunta} - {respuesta}"
                RespuestaPerfil.objects.get_or_create(
                    pregunta=pregunta_obj, nombre=texto
                )
