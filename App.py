from flask import Flask, render_template
from Prediccion.conexion import Conexion
from Prediccion.ObtenerDatos import ObtenerDatos
from Prediccion.EntrenamientoDatos import EntrenamiendoDatos
from Prediccion.PrediccionDatos import Prediccion
from Prediccion.GenerarGrafico import GenerarGrafico

app = Flask(__name__)

# Configuración de la base de datos
db = Conexion.conectar_bd('localhost', 'root', '', 'restaurante')
ObtenerD = ObtenerDatos(db)
EntrenarD = EntrenamiendoDatos()
PrediccionD = Prediccion()
GenerarG = GenerarGrafico()

@app.route('/')
def index():
    return render_template('plantilla.html')

''''''''''''''''''''''''''''''''''''
'''''''Prediccion de Demanda'''''''
''''''''''''''''''''''''''''''''''''

@app.route('/ver_registro')
def ver_registro():
    registros = ObtenerD.ver_registros()  # Llamada a la función ver_registros sin argumentos
    return render_template('ver_registro.html', registros=registros)

@app.route('/datos_entrenamiento')
def ver_datos_entrenamiento():
    datosE = ObtenerD.mostrar_datos_entrenamiento()  # Llamada a la función ver_registros sin argumentos
    return render_template('datos_entrenamiento.html', datosE=datosE)

@app.route('/generar_prediccion')
def generar_prediccion():
    # Obtener datos de entrenamiento
    fechas_entrenamiento, ventas_entrenamiento = ObtenerD.obtener_datos_entrenamiento()
    
    # Entrenar modelo
    modelo, poly = EntrenarD.entrenar_modelo(fechas_entrenamiento, ventas_entrenamiento)
    
    # Predecir ventas
    fechas_prediccion, ventas_prediccion = PrediccionD.predecir_ventas(modelo, poly)
    
    # Generar gráfico
    GenerarG.generar_grafico(fechas_prediccion, ventas_prediccion)
    
    return render_template('plantilla.html', fechas_prediccion=fechas_prediccion, ventas_prediccion=ventas_prediccion)

''''''''''''''''''''''''''''''''''''
'''''Segmentacion de Clientes'''''
''''''''''''''''''''''''''''''''''''
@app.route('/ver_productos')
def ver_datos_productos():
    datosP = ObtenerD.mostrar_datos_productos()  # Llamada a la función ver_registros sin argumentos
    return render_template('ver_productos.html', datosP=datosP)

if __name__ == '__main__':
    app.run(debug=True)
