from datetime import datetime, timedelta
import os
from Prediccion.conexion import Conexion
from Prediccion.ObtenerDatos import ObtenerDatos
from Prediccion.EntrenamientoDatos import EntrenamiendoDatos
from Prediccion.PrediccionDatos import Prediccion
from Prediccion.GenerarGrafico import GenerarGrafico
from flask import Flask, render_template, request, redirect, url_for
from flask import redirect
from flask import Flask
from flask_login import LoginManager
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required

app = Flask(__name__)


# Configuración de la base de datos
db = Conexion.conectar_bd('localhost', 'root', '', 'restaurante')
ObtenerD = ObtenerDatos(db)
EntrenarD = EntrenamiendoDatos()
PrediccionD = Prediccion()
GenerarG = GenerarGrafico()

app.config['SECRET_KEY'] = os.urandom(24)

# Inicializar Flask-Login
login_manager = LoginManager(app)

# Definir una clase de Usuario para interactuar con Flask-Login
class Usuario(UserMixin):
    def __init__(self, username):
        self.id = username

# Función para cargar un usuario en la sesión
@login_manager.user_loader
def load_user(username):
    return Usuario(username)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    password = request.form['password']
    
    # Consultar la base de datos para verificar las credenciales
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND clave = %s", (usuario, password))
    usuario_encontrado = cursor.fetchone()
    cursor.close()

    if usuario_encontrado:
        # Autenticación exitosa, cargar usuario en sesión
        usuario = Usuario(usuario)
        login_user(usuario)
        return redirect(url_for('dashboard'))
    else:
        # Autenticación fallida, mostrar alerta y redirigir a la página de inicio de sesión
        return render_template('login.html', error='Credenciales incorrectas. Por favor, inténtalo de nuevo.')

@app.route('/dashboard')
@login_required
def dashboard():
    # Obtener nombre de archivos de las predicciones
    nombre_archivo = request.args.get('nombre_archivo')
    nombre_archivo_1 = request.args.get('nombre_archivo_1')
    nombre_archivo_2 = request.args.get('nombre_archivo_2')

    return render_template('plantilla.html',nombre_archivo=nombre_archivo, nombre_archivo_1=nombre_archivo_1, nombre_archivo_2=nombre_archivo_2)

@app.route('/logout')
@login_required
def logout():
    # Cierra la sesión del usuario
    logout_user()

    # Redirige al usuario a la página de inicio de sesión
    return redirect(url_for('index'))

''''''''''''''''''''''''''''''''''''
'''''''Registrarse'''''''
''''''''''''''''''''''''''''''''''''

@app.route('/registrarse')
def registrarse(): # Llamada a la función ver_registros sin argumentos
    return render_template('registrarse.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    usuario = request.form['usuario']
    password = request.form['password']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    rol = request.form['rol']

    # Insertar los datos en la base de datos (debes implementar esta lógica)
    cursor = db.cursor()
    cursor.execute("INSERT INTO usuarios (usuario, clave, nombre, apellido, rol) VALUES (%s, %s, %s, %s, %s)",
                   (usuario, password, nombre, apellido, rol))
    db.commit()
    cursor.close()

    # Después del registro, redirige a donde desees (por ejemplo, la página de inicio de sesión)
    return redirect(url_for('index'))


''''''''''''''''''''''''''''''''''''
'''''''Prediccion de Demanda'''''''
''''''''''''''''''''''''''''''''''''

@app.route('/form-detalles', methods=['POST'])
def obtener_detalles():
    Tinicio = request.form['Tinicio']
    Tfin = request.form['Tfin']
    Pinicio = request.form['Pinicio']
    Pfin = request.form['periodo']
    return redirect(url_for('generar_prediccion', Tinicio=Tinicio, Tfin=Tfin, Pinicio=Pinicio, Pfin=Pfin))





@app.route('/generar_prediccion')
def generar_prediccion():
    # Obtener fechas de la URL
    Tinicio = request.args.get('Tinicio')
    Tfin = request.args.get('Tfin')
    fecha_inicio_prediccion = request.args.get('Pinicio')
    fecha_fin_prediccion = int(request.args.get('Pfin'))
    
    # Convertir fecha_inicio_prediccion a datetime.date
    fecha_inicio_prediccion = datetime.strptime(fecha_inicio_prediccion, "%Y-%m-%d").date()
    # Calcular la diferencia en días
    dias_a_predecir = fecha_fin_prediccion
    
    # Obtener datos de entrenamiento
    fechas_entrenamiento, ventas_entrenamiento = ObtenerD.obtener_datos_entrenamiento(Tinicio, Tfin)
    
    # Entrenar modelo
    modelo, poly = EntrenarD.entrenar_modelo(fechas_entrenamiento, ventas_entrenamiento)
    
    # Definir nombre_archivo fuera del bloque if-else
    nombre_archivo = None
    nombre_archivo_1 = None
    nombre_archivo_2 = None

    # Predecir ventas
    if dias_a_predecir == 14:
        # Generar gráfico para los primeros 7 días
        fechas_prediccion_1, ventas_prediccion_1 = PrediccionD.predecir_ventas(modelo, poly, fecha_inicio_prediccion, 7)
        nombre_archivo_1 = GenerarG.generar_grafico(fechas_prediccion_1, ventas_prediccion_1)

        # Generar gráfico para los siguientes 7 días
        fechas_prediccion_2, ventas_prediccion_2 = PrediccionD.predecir_ventas(modelo, poly, fecha_inicio_prediccion + timedelta(days=7), 7)
        nombre_archivo_2 = GenerarG.generar_grafico(fechas_prediccion_2, ventas_prediccion_2)
    else:
        fechas_prediccion, ventas_prediccion = PrediccionD.predecir_ventas(modelo, poly, fecha_inicio_prediccion, dias_a_predecir)
        nombre_archivo = GenerarG.generar_grafico(fechas_prediccion, ventas_prediccion)
        

    return redirect(url_for('dashboard', nombre_archivo=nombre_archivo, nombre_archivo_1=nombre_archivo_1, nombre_archivo_2=nombre_archivo_2))




''''''''''''''''''''''''''''''''''''
'''''Segmentacion de Clientes'''''
''''''''''''''''''''''''''''''''''''
@app.route('/ver_productos')
def ver_datos_productos():
    datosP = ObtenerD.mostrar_datos_productos()  # Llamada a la función ver_registros sin argumentos
    return render_template('ver_productos.html', datosP=datosP)

if __name__ == '__main__':
    app.run(debug=True)
#linea115
@app.route('/ver_registro')
def ver_registro():
    registros = ObtenerD.ver_registros()  # Llamada a la función ver_registros sin argumentos
    return render_template('ver_registro.html', registros=registros)


@app.route('/datos_entrenamiento')
def ver_datos_entrenamiento():
    datosE = ObtenerD.mostrar_datos_entrenamiento()  # Llamada a la función ver_registros sin argumentos
    return render_template('datos_entrenamiento.html', datosE=datosE)