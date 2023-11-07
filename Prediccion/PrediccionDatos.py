import numpy as np


class Prediccion:

    ''''''''''''''''''''''''''''''''''''
    '''''''Prediccion de Demanda'''''''
    ''''''''''''''''''''''''''''''''''''
    @staticmethod
    def predecir_ventas(modelo, poly, fecha_inicio, dias_a_predecir):
        fecha_inicio = np.datetime64(fecha_inicio)
        fechas_prediccion = [fecha_inicio + np.timedelta64(i, 'D') for i in range(1, dias_a_predecir+1)]
        fechas_prediccion = np.array(fechas_prediccion).reshape(-1, 1)
        fechas_poly_prediccion = poly.transform(fechas_prediccion)
        ventas_prediccion = modelo.predict(fechas_poly_prediccion)
        return fechas_prediccion, ventas_prediccion

