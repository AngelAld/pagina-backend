from django.core.management.base import BaseCommand
from Inmuebles.models import (
    Caracteristica,
    TipoAntiguedad,
    TipoInmueble,
    SubTipoInmueble,
    EstadoInmueble,
    TipoOperacion,
    Inmueble,
    ImagenInmueble,
    UbicacionInmueble,
)
from Ubicacion.models import Distrito
from Usuarios.models import Usuario

caracteristicas = [
    "Cerca a parques",
    "Cerca a centro comercial",
    "Cerca a colegio",
    "Acceso para discapacitados",
]

tipo_antiguedades = [
    "Nuevo",
    "Años de antiguedad",
    "En construcción",
]

tipo_inmuebles = [
    "Casa",
    "Departamento",
    "Terreno",
    "Local",
]

subtipos_casa = [
    "Casa de campo",
    "Casa de playa",
    "Casa de ciudad",
]

subtipos_departamento = [
    "Departamento de playa",
    "Departamento de ciudad",
]

subtipos_local = [
    "Local comercial",
    "Local industrial",
]

estados = [
    "Publicado",
    "En borrador",
    "Operación finalizada",
]

tipo_operaciones = [
    "Venta",
    "Alquiler",
    "Temporal",
]

inmuebles = [
    {
        "titulo": "Casa en la playa",
        "descripcion": "Casa de playa en la costa verde",
        "precio": 1000000,
        "tipo_antiguedad": "Nuevo",
        "años": 0,
        "tipo_inmueble": "Casa",
        "subtipo_inmueble": "Casa de playa",
        "caracteristicas": ["Cerca a parques", "Cerca a centro comercial"],
        "estado": "Publicado",
        "tipo_operacion": "Venta",
    },
    {
        "titulo": "Departamento en la ciudad",
        "descripcion": "Departamento en la ciudad",
        "precio": 500000,
        "tipo_antiguedad": "Años de antiguedad",
        "años": 5,
        "tipo_inmueble": "Departamento",
        "subtipo_inmueble": "Departamento de ciudad",
        "caracteristicas": ["Cerca a parques", "Cerca a colegio"],
        "estado": "Publicado",
        "tipo_operacion": "Venta",
    },
    {
        "titulo": "Local comercial",
        "descripcion": "Local comercial",
        "precio": 200000,
        "tipo_antiguedad": "Nuevo",
        "años": 0,
        "tipo_inmueble": "Local",
        "subtipo_inmueble": "Local comercial",
        "caracteristicas": ["Cerca a parques", "Acceso para discapacitados"],
        "estado": "Publicado",
        "tipo_operacion": "Venta",
    },
]


class Command(BaseCommand):
    help = "Genera data basica para el modulo de inmuebles"

    def handle(self, *args, **options):
        self.stdout.write("Generando data basica para el modulo de inmuebles")
        for caracteristica in caracteristicas:
            Caracteristica.objects.get_or_create(nombre=caracteristica)
        for tipo_antiguedad in tipo_antiguedades:
            TipoAntiguedad.objects.get_or_create(nombre=tipo_antiguedad)
        for tipo_inmueble in tipo_inmuebles:
            TipoInmueble.objects.get_or_create(nombre=tipo_inmueble)
        for subtipo_casa in subtipos_casa:
            SubTipoInmueble.objects.get_or_create(
                nombre=subtipo_casa,
                tipo_inmueble=TipoInmueble.objects.get(nombre="Casa"),
            )
        for subtipo_departamento in subtipos_departamento:
            SubTipoInmueble.objects.get_or_create(
                nombre=subtipo_departamento,
                tipo_inmueble=TipoInmueble.objects.get(nombre="Departamento"),
            )
        for subtipo_local in subtipos_local:
            SubTipoInmueble.objects.get_or_create(
                nombre=subtipo_local,
                tipo_inmueble=TipoInmueble.objects.get(nombre="Local"),
            )
        for estado in estados:
            EstadoInmueble.objects.get_or_create(nombre=estado)
        for tipo_operacion in tipo_operaciones:
            TipoOperacion.objects.get_or_create(nombre=tipo_operacion)
        for inmueble in inmuebles:
            inmueble_obj = Inmueble.objects.create(
                dueño=Usuario.objects.first(),
                titulo=inmueble["titulo"],
                descripcion=inmueble["descripcion"],
                tipo_antiguedad=TipoAntiguedad.objects.get(
                    nombre=inmueble["tipo_antiguedad"]
                ),
                años=inmueble["años"],
                tipo_inmueble=TipoInmueble.objects.get(
                    nombre=inmueble["tipo_inmueble"]
                ),
                subtipo_inmueble=SubTipoInmueble.objects.get(
                    nombre=inmueble["subtipo_inmueble"]
                ),
                estado=EstadoInmueble.objects.get(nombre=inmueble["estado"]),
                tipo_operacion=TipoOperacion.objects.get(
                    nombre=inmueble["tipo_operacion"]
                ),
            )
            for caracteristica in inmueble["caracteristicas"]:
                inmueble_obj.caracteristicas.add(
                    Caracteristica.objects.get(nombre=caracteristica)
                )
            ImagenInmueble.objects.create(
                inmueble=inmueble_obj,
                imagen="inmuebles/default.jpg",
                is_portada=True,
            )
            UbicacionInmueble.objects.create(
                inmueble=inmueble_obj,
                calle="Av. Javier Prado",
                numero="123",
                latitud=-12.085,
                longitud=-77.045,
                distrito=Distrito.objects.get(
                    nombre="San Isidro", provincia__nombre="Lima"
                ),
            )
