from matplotlib import pyplot as plt

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

        # Mostrar el gráfico
        plt.tight_layout()
        plt.show()