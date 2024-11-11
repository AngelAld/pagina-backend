import time
from django.core.management.base import BaseCommand, CommandError
from ...models import Departamento, Provincia, Distrito
import csv


class Command(BaseCommand):
    help = "Carga todos los datos de los departamentos, provincias y distritos"

    def handle(self, *args, **options):
        start_time = time.time()
        departamentos = 0
        failed_departamentos = 0
        provincias = 0
        failed_provincias = 0
        distritos = 0
        failed_distritos = 0
        # Carga de departamentos
        with open(
            # "Ubicacion\\management\\commands\\Ubicacion.csv", encoding="utf-8"            # Windows
            "Ubicacion/management/commands/Ubicacion.csv",  #                               # Linux
            encoding="utf-8",
        ) as csvfile:
            self.stdout.write(
                self.style.SUCCESS("Cargando departamentos, provincias y distritos...")
            )
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    departamento, created = Departamento.objects.get_or_create(
                        nombre=row["Departamento"]
                    )
                    if created:
                        departamentos += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"Departamento {departamento} creado")
                        )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error creando departamento: {e}")
                    )
                    failed_departamentos += 1

                try:
                    provincia, created = Provincia.objects.get_or_create(
                        nombre=row["Provincia"], departamento=departamento
                    )
                    if created:
                        provincias += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"Provincia {provincia} creada")
                        )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando provincia: {e}"))
                    failed_provincias += 1

                try:
                    distrito, created = Distrito.objects.get_or_create(
                        nombre=row["Distrito"], provincia=provincia
                    )
                    if created:
                        distritos += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"Distrito {distrito} creado")
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error creando distrito: {e} on {row}")
                    )
                    failed_distritos += 1

        elapsed_time = time.time() - start_time
        self.stdout.write(
            self.style.SUCCESS(f"Datos cargados en {elapsed_time:.2f} segundos.")
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Departamentos: {departamentos}, Provincias: {provincias}, Distritos: {distritos}"
            )
        )
        if failed_departamentos:
            self.stdout.write(
                self.style.ERROR(f"Departamentos fallidos: {failed_departamentos}")
            )
        if failed_provincias:
            self.stdout.write(
                self.style.ERROR(f"Provincias fallidas: {failed_provincias}")
            )
        if failed_distritos:
            self.stdout.write(
                self.style.ERROR(f"Distritos fallidos: {failed_distritos}")
            )
