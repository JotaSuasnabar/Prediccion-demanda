import numpy as np
from Prediccion.conexion import Conexion

class ObtenerDatos:
        
    def __init__(self, conexion):
        self.cursor = conexion.cursor()

    def ver_registros(self):
        query= "SELECT id, comida, id_orden, cantidad, p_unitario, p_total, extras, fecha FROM o_pedidos;"
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        return resultados
    
    
    ''''''''''''''''''''''''''''''''''''
    '''''''Prediccion de Demanda'''''''
    ''''''''''''''''''''''''''''''''''''
    
    def mostrar_datos_entrenamiento(self):
        query= "SELECT fecha, SUM(p_total) FROM o_pedidos WHERE fecha BETWEEN '2023-05-01' AND '2023-10-01' GROUP BY fecha;"
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        return resultados

    @staticmethod
    def obtener_datos_entrenamiento():
        conexion = Conexion.conectar_bd('localhost', 'root', '', 'restaurante')
        cursor = conexion.cursor()
        cursor.execute("SELECT fecha, SUM(p_total) FROM o_pedidos WHERE fecha BETWEEN '2023-05-01' AND '2023-10-01' GROUP BY fecha")
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        fechas, ventas = zip(*resultados)
        fechas = np.array([np.datetime64(fecha) for fecha in fechas]).reshape(-1, 1)
        ventas = np.array(ventas)
        return fechas, ventas
    
    ''''''''''''''''''''''''''''''''''''
    '''''''Segmentacion de Clientes'''''''
    ''''''''''''''''''''''''''''''''''''
    def mostrar_datos_productos(self):
        query= """SELECT fecha, comida, SUM(cantidad) as Cantidad_total, DAYOFWEEK(fecha) as Dia_semana FROM o_pedidos WHERE fecha BETWEEN '2023-05-01' AND '2023-10-01' GROUP BY comida, fecha"""
        #query = "SELECT comida, fecha, SUM(cantidad) as total_cantidad FROM o_pedidos GROUP BY comida, fecha;"
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        return resultados
    
    @staticmethod
    def Obtener_datos_por_dia_semana():
        conexion = Conexion.conectar_bd('localhost', 'root', '', 'restaurante')
        cursor = conexion.cursor()
        cursor.execute("""SELECT fecha, comida, SUM(cantidad) as Cantidad_total, DAYOFWEEK(fecha) as Dia_semana FROM  o_pedidos  WHERE fecha BETWEEN '2023-05-01' AND '2023-10-01' GROUP BY comida, fecha""")
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        # Separamos los resultados entre días de semana y fines de semana
        dias_semana = [(fecha, comida, cantidad) for fecha, comida, cantidad, dia in resultados if dia >= 2 and dia <= 6]
        fines_semana = [(fecha, comida, cantidad) for fecha, comida, cantidad, dia in resultados if dia == 1 or dia == 7]

        # Procesamos los datos para retornarlos
        fechas_dias_semana, productos_dias_semana, ventas_dias_semana = zip(*dias_semana)
        fechas_fines_semana, productos_fines_semana, ventas_fines_semana = zip(*fines_semana)

        fechas_dias_semana = [str(fecha) for fecha in fechas_dias_semana]
        fechas_fines_semana = [str(fecha) for fecha in fechas_fines_semana]

        productos_dias_semana = np.array(productos_dias_semana)
        productos_fines_semana = np.array(productos_fines_semana)

        ventas_dias_semana = np.array(ventas_dias_semana)
        ventas_fines_semana = np.array(ventas_fines_semana)

        return fechas_dias_semana, ventas_dias_semana, productos_dias_semana, fechas_fines_semana, ventas_fines_semana, productos_fines_semana
