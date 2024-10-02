import csv
from django.core.management.base import BaseCommand
from spcmapp.models import producto_maquina

class Command(BaseCommand):
    help = 'Importa datos desde un archivo CSV a la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='La ruta del archivo CSV a importar')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        try:
            print("Importando datos desde el archivo CSV: ", csv_file_path)
            
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  

                for row in csv_reader:
                    producto_maquina.objects.create(
                        Ruta=row[0],
                        Descripcion_1=row[1],
                        Categoria=row[2],
                        Operación=row[3],
                        Subcontratacion=row[4],
                        Centro_trabajo_ppal=row[5],
                        Destino_ope=row[6],
                        Cod_maquina=row[7],
                        Tipo_tpo_operacional=row[8],
                        Tiempo_ajuste=row[9],
                        Tpo_operacional=row[10],
                        Cadencia=row[11],
                        Cadence_theo=row[12],
                        Utillaje=row[13],
                        Eficiencia=row[14]
                    )
            
            self.stdout.write(self.style.SUCCESS('Datos importados exitosamente'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Error al importar datos: %s' % str(e)))