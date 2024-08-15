import datetime
import hashlib
import os
import MySQLdb
from flask import Flask, flash, render_template, request, redirect, session, url_for, abort, send_file
from flask_mysqldb import MySQL
from config import Config
import io
import math
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'tu_clave_secreta_aqui'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = None
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Redirige al usuario a la URL con los parámetros de búsqueda en la query string
        query_params = {
            'mp': request.form.get('mp'),
            'p': request.form.get('p'),
            'tipo_norma': request.form.get('tipo_norma'),
            'numero': request.form.get('numero'),
            'anio': request.form.get('anio'),
            'descripcion': request.form.get('descripcion'),
            'per_page': request.form.get('per_page', 100)  # Obtener el valor de per_page del formulario
        }
        return redirect(url_for('index', **query_params))

    # Si es un GET request, obtenemos los parámetros de búsqueda de la URL
    mp = request.args.get('mp', 'all')
    p = request.args.get('p', 'all')
    tipo_norma = request.args.get('tipo_norma', 'all')
    numero = request.args.get('numero', '')
    anio = request.args.get('anio', '')
    descripcion = request.args.get('descripcion', '')
    per_page = request.args.get('per_page', 100, type=int)  # Obtener el número de resultados por página (por defecto 100)
    page = request.args.get('page', 1, type=int)  # Obtener el número de página actual

    # Construir la consulta con filtros
    query = """
        SELECT
            t.descripcion AS documento,
            m.descripcion AS macroproceso,
            p.descripcion AS proceso,
            a.numero,
            a.anio,
            a.descripcion AS descargas,
            a.peso,
            a.nombre
        FROM archivos a
        LEFT JOIN listado_documentos ld ON a.nombre = ld.nombre
        LEFT JOIN macroprocesos m ON ld.id_mp = m.id_mp
        LEFT JOIN procesos p ON ld.id_p = p.id_p
        LEFT JOIN tipo_documento t ON a.id_tipo_documento = t.id
        WHERE (m.id_mp = %s OR %s = 'all')
        AND (p.id_p = %s OR %s = 'all')
        AND (a.id_tipo_documento = %s OR %s = 'all')
        AND (a.numero = %s OR %s = '')
        AND (a.anio = %s OR %s = '')
        AND (a.descripcion LIKE %s OR %s = '')
        ORDER BY a.anio DESC
        LIMIT %s OFFSET %s;
    """
               
    params = [
        mp, mp,
        p, p,
        tipo_norma, tipo_norma,
        numero, numero,
        anio, anio,
        f"%{descripcion}%", descripcion,
        per_page,
        (page - 1) * per_page
    ]

    cursor = mysql.connection.cursor()
    cursor.execute(query, tuple(params))
    resultados = cursor.fetchall()

    # Obtener el conteo total de resultados
    query_count = """
        SELECT COUNT(*) AS total
        FROM archivos a
        LEFT JOIN listado_documentos ld ON a.nombre = ld.nombre
        LEFT JOIN macroprocesos m ON ld.id_mp = m.id_mp
        LEFT JOIN procesos p ON ld.id_p = p.id_p
        LEFT JOIN tipo_documento t ON a.id_tipo_documento = t.id
        WHERE (m.id_mp = %s OR %s = 'all')
        AND (p.id_p = %s OR %s = 'all')
        AND (a.id_tipo_documento = %s OR %s = 'all')
        AND (a.numero = %s OR %s = '')
        AND (a.anio = %s OR %s = '')
        AND (a.descripcion LIKE %s OR %s = '');
    """
    cursor.execute(query_count, tuple(params[:-2]))  # Usar los mismos parámetros, excepto LIMIT y OFFSET
    total_results = cursor.fetchone()[0]
    cursor.close()
   
    total_pages = (total_results + per_page - 1) // per_page

    # Datos para los selectores
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_mp, descripcion FROM macroprocesos")
    macroprocesos = cursor.fetchall()
   
    cursor.execute("SELECT id_p, descripcion FROM procesos")
    procesos = cursor.fetchall()
   
    cursor.execute("SELECT id, descripcion FROM tipo_documento")
    documento = cursor.fetchall()
   
    cursor.execute("SELECT DISTINCT anio FROM archivos ORDER BY anio DESC")
    anio = cursor.fetchall()
   
    cursor.close()

    # Convertir resultados en una lista de diccionarios con 'id' y 'nombre'
    resultados = [{'nombre': row[7], 'documento': row[0], 'macroproceso': row[1], 'proceso': row[2], 'numero': row[3], 'anio': row[4], 'descripcion': row[5], 'peso': round(row[6] / 1024, 2)} for row in resultados]

    start_page = max(1, page - 4)
    end_page = min(total_pages, page + 4)

    return render_template('index.html', page=page, total_pages=total_pages, per_page=per_page, macroprocesos=macroprocesos, procesos=procesos, documento=documento, resultados=resultados, anio=anio, start_page=start_page, end_page=end_page)

@app.route('/download/<filename>')
def download_file(filename):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT nombre FROM archivos WHERE nombre = %s', (filename,))
    result = cursor.fetchone()
   
    if result:
        filename = result[0]
        # Aquí deberías implementar la lógica para recuperar el contenido del archivo
        # Ejemplo: cursor.execute('SELECT contenido FROM archivos WHERE nombre = %s', (filename,))
        # El contenido debe estar en una variable llamada file_content
        file_content = b'Contenido del archivo'  # Cambia esto por la lógica real
       
        return send_file(
            io.BytesIO(file_content),
            download_name=filename,
            as_attachment=True
        )
    else:
        abort(404, description="Archivo no encontrado")

@app.route('/footer')
def footer():
    return render_template('footer.html')

@app.route('/header')
def header():
    return render_template('header.html')

# Para el inicio de sesión

# Función para encriptar la contraseña usando SHA-1
def hash_password_sha1(password):
    return hashlib.sha1(password.encode()).hexdigest()

# Asegúrate de que el directorio uploads exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (username,))
        user = cursor.fetchone()

        if user and hash_password_sha1(password) == user['pass']:
            session['loggedin'] = True
            session['id'] = user['nuip']
            session['username'] = user['usuario']
            session['nombres'] = user['nombres']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('nombres', None)
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login'))

@app.route('/cargar_documento', methods=['POST'])
def cargar_documento():
    if 'file' not in request.files:
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Obtener el peso del archivo
        peso = os.path.getsize(file_path)

        # Recoger los otros campos del formulario
        id_mp = request.form.get('id_mp')
        id_p = request.form.get('id_p')
        id_tipo_documento = request.form['id_tipo_documento']
        anio = request.form['anio']
        numero = request.form['numero']
        descripcion = request.form['descripcion']

        # Obtener el usuario que subió el archivo y la fecha de subida
        subido_por = session['username']
        fecha_subida = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor = mysql.connection.cursor()

        # Insertar datos en la tabla archivos
        cursor.execute("""
            INSERT INTO archivos (nombre, id_tipo_documento, anio, numero, peso, descripcion, subido_por, fecha_subida)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (filename, id_tipo_documento, anio, numero, peso, descripcion, subido_por, fecha_subida))

        # Si se han proporcionado id_mp y id_p, verificar existencia y luego insertar en listado_documentos
        if id_mp and id_p:
            # Verificar existencia en la tabla macroprocesos
            cursor.execute("SELECT COUNT(*) FROM macroprocesos WHERE id_mp = %s", [id_mp])
            if cursor.fetchone()[0] == 0:
                flash("El id_mp proporcionado no existe.")
                mysql.connection.rollback()
                return redirect(request.url)

            # Verificar existencia en la tabla procesos
            cursor.execute("SELECT COUNT(*) FROM procesos WHERE id_p = %s AND id_mp = %s", [id_p, id_mp])
            if cursor.fetchone()[0] == 0:
                flash("El id_p proporcionado no existe o no está relacionado con el id_mp dado.")
                mysql.connection.rollback()
                return redirect(request.url)

            # Si ambos existen, insertar en listado_documentos
            cursor.execute("""
                INSERT INTO listado_documentos (nombre, id_mp, id_p)
                VALUES (%s, %s, %s)
            """, (filename, id_mp, id_p))

        mysql.connection.commit()
        cursor.close()

        flash('Documento subido y guardado exitosamente')
        return redirect(url_for('upload'))
    else:
        flash('Tipo de archivo no permitido')
        return redirect(request.url)

    
@app.route('/upload', methods=['GET'])
def upload():
    if 'loggedin' not in session:
        flash('Debe iniciar sesión para acceder a esta página')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    # Datos para los selectores
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_mp, descripcion FROM macroprocesos")
    macroprocesos = cursor.fetchall()
   
    cursor.execute("SELECT id_p, descripcion FROM procesos")
    procesos = cursor.fetchall()
   
    cursor.execute("SELECT id, descripcion FROM tipo_documento")
    documento = cursor.fetchall()
   
    cursor.execute("SELECT DISTINCT anio FROM archivos ORDER BY anio DESC")
    anio = cursor.fetchall()
   
    cursor.close()

    return render_template('upload.html', macroprocesos=macroprocesos, procesos=procesos, documento=documento, anio=anio)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
