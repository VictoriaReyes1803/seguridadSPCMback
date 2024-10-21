import csv
from django.core.management.base import BaseCommand
from spcmapp.models import Producto_maquina , Producto, Maquina

class Command(BaseCommand):
    help = 'Importa datos desde un archivo CSV a la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='La ruta del archivo CSV a importar')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        try:
            print("Importando datos desde el archivo CSV: ", csv_file_path)
            
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    
                    cleaned_row = {key.lstrip('\ufeff'): value for key, value in row.items()}
                    
                    Maquina.objects.create(
                        maquina=cleaned_row['maquina'],
                        estado= True,    
                        )
                
                # reader = csv.DictReader(file)
                # for row in reader:
                #     # print(row)
                #     cleaned_row = {key.lstrip('\ufeff'): value for key, value in row.items()}
                #     # print(cleaned_row)
                #     Producto.objects.create(
                #         producto=cleaned_row['producto'],
                #         descripcion=cleaned_row['descripcion'],
                #         codigo_cliente=cleaned_row['codigo_cliente'],
                #         resina_1=cleaned_row['resina_1'],
                #         categoria=cleaned_row['categoria'],
                #         estado=cleaned_row['estado'].lower() == 'activo',  # Convierte a booleano
                #         resina_2=None,  
                #         Maquina=None,  
                            
                #         )
                # csv_reader = csv.reader(file)
                # next(csv_reader)  

                # for row in csv_reader:
                #     Producto_maquina.objects.create(
                #     Ruta=row[0],
                #     Descripcion_1=row[1],
                #     Categoria=row[2],
                #     Operación=row[3],
                #     Subcontratacion=row[4],
                #     Centro_trabajo_ppal=row[5],
                #     Destino_ope=row[6],
                #     Cod_maquina=row[7],
                #     Tipo_tpo_operacional=row[8],
                #     Tiempo_ajuste=row[9],
                #     Tpo_operacional=row[10],
                #     Cadencia=row[11],
                #     Cadence_theo=row[12],
                #     Utillaje=row[13],
                #     Eficiencia=row[14]
                #         )
                
            self.stdout.write(self.style.SUCCESS('Datos importados exitosamente'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Error al importar datos: %s' % str(e)))
            
            
              
                
               