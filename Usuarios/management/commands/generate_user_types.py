from django.core.management.base import BaseCommand
from Usuarios.models import TipoUsuario, AuthProvider


class Command(BaseCommand):
    help = "Genera los tipos basicos de usuarios"

    def handle(self, *args, **options):
        tipos = [
            "Cliente",
            "Particular Inmuebles",
            "Agente Inmobiliario",
            "Inmobiliaria",
            "Empleado Inmobiliaria",
            "Agente Hipotecario",
            "Profesional Servicios",
        ]
        for tipo in tipos:
            TipoUsuario.objects.get_or_create(nombre=tipo)
            self.stdout.write(self.style.SUCCESS(f"Tipo de usuario {tipo} creado"))
        AuthProvider.objects.get_or_create(nombre="google")
        self.stdout.write(self.style.SUCCESS("AuthProvider google creado"))
        AuthProvider.objects.get_or_create(nombre="email")
        self.stdout.write(self.style.SUCCESS("AuthProvider email creado"))
