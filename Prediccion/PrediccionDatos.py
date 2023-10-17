import numpy as np


class Prediccion:

    ''''''''''''''''''''''''''''''''''''
    '''''''Prediccion de Demanda'''''''
    ''''''''''''''''''''''''''''''''''''
    @staticmethod
    def predecir_ventas(modelo, poly):
        ultima_fecha = np.datetime64('2023-10-01')
        fechas_prediccion = [ultima_fecha + np.timedelta64(i, 'D') for i in range(1, 8)]
        fechas_prediccion = np.array(fechas_prediccion).reshape(-1, 1)
        fechas_poly_prediccion = poly.transform(fechas_prediccion)
        ventas_prediccion = modelo.predict(fechas_poly_prediccion)
        return fechas_prediccion, ventas_prediccion
     
