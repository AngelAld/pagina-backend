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
    {
        "nombre": "En solicitud",
        "is_system_managed": True,
    },
    {
        "nombre": "En evaluación",
        "is_system_managed": True,
    },
    {
        "nombre": "Observado",
        "is_system_managed": False,
    },
    {
        "nombre": "Aprobado",
        "is_system_managed": False,
    },
    {
        "nombre": "Rechazado",
        "is_system_managed": False,
    },
    {
        "nombre": "Cancelado",
        "is_system_managed": True,
    },
]

etapas = [
    "Solicitud",
    "Evaluación",
    "Resolución",
    "Finalizado",
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
            estadoObj, _ = EstadoEvaluacion.objects.get_or_create(
                nombre=estado["nombre"],
            )
            estadoObj.is_system_managed = estado["is_system_managed"]
            estadoObj.save()

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
