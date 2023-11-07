from matplotlib import pyplot as plt
import time

class GenerarGrafico:
     
    ''''''''''''''''''''''''''''''''''''
    '''''''Prediccion de Demanda'''''''
    ''''''''''''''''''''''''''''''''''''
    @staticmethod
    def generar_grafico(fechas_prediccion, ventas_prediccion):
        # Crear el gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(fechas_prediccion, ventas_prediccion, marker='o')

        # Configurar etiquetas y título
        plt.xlabel('Fechas')
        plt.ylabel('Venta Estimada')
        plt.title('Ventas Estimadas para los próximos 7 días')

        # Rotar las etiquetas del eje X para mayor legibilidad
        plt.xticks(rotation=45)

        # Generar un nombre de archivo único con un timestamp
        timestamp = int(time.time())
        nombre_archivo = f'static/img/grafico_{timestamp}.png'

        # Guardar el gráfico como una imagen
        plt.tight_layout()
        plt.savefig(nombre_archivo)

        # Cerrar la figura para liberar memoria
        plt.close()

        return nombre_archivo  # Devolver el nombre del archivo generado
