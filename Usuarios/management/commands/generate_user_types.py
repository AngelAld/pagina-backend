from django.core.management.base import BaseCommand, CommandError
from Usuarios.models import TipoUsuario


class Command(BaseCommand):
    help = "Genera los tipos basicos de usuarios"

    def handle(self, *args, **options):
        tipos = [
            "Cliente",
            "Particular Inmuebles",
            "Inmobiliaria",
            "Empleado Inmobiliaria",
            "Agente Prestamos",
            "Profesional Servicios",
        ]
        for tipo in tipos:
            TipoUsuario.objects.get_or_create(nombre=tipo)
            self.stdout.write(self.style.SUCCESS(f"Tipo de usuario {tipo} creado"))
