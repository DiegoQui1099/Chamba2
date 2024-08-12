from flask import Flask, render_template, request, redirect, url_for, abort, send_file
from flask_mysqldb import MySQL
from config import Config
import io

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    section = request.args.get('section', 1, type=int)  # Obtener la sección actual
    per_section = 100  # Número de resultados por sección

    resultados = []
    total_results = 0
    total_sections = 0

    if request.method == 'POST':
        # Obtener parámetros del formulario
        mp = request.form.get('mp')
        p = request.form.get('p')
        tipo_norma = request.form.get('tipo_norma')
        numero = request.form.get('numero')
        anio = request.form.get('anio')
        descripcion = request.form.get('descripcion')

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
            per_section,
            (section - 1) * per_section
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
        
        total_sections = (total_results + per_section - 1) // per_section

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

    return render_template('index.html', section=section, total_sections=total_sections, macroprocesos=macroprocesos, procesos=procesos, documento=documento, resultados=resultados, anio=anio)


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

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
