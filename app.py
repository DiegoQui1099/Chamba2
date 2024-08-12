from flask import Flask, render_template, request, redirect, url_for, json
from flask_mysqldb import MySQL
from config import Config
import requests

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    
    if request.method == 'POST':
        # Obtener parámetros del formulario
        mp = request.form.get('mp')
        p = request.form.get('p')
        tipo_norma = request.form.get('tipo_norma')
        numero = request.form.get('numero')
        anio = request.form.get('anio')
        descripcion = request.form.get('descripcion')

        query = """
        SELECT 
            t.descripcion AS documento,
            m.descripcion AS macroproceso,
            p.descripcion AS proceso,
            a.numero,
            a.anio,
            a.descripcion AS descargas,
            a.peso
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
        ORDER BY a.anio DESC;
        """
                
        params = [
            mp, mp,
            p, p,
            tipo_norma, tipo_norma,
            numero, numero,
            anio, anio,
            f"%{descripcion}%", descripcion
        ]

        cursor = mysql.connection.cursor()
        cursor.execute(query, tuple(params))
        resultados = cursor.fetchall()
        cursor.close()

    # Datos para los selectores
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_mp, descripcion FROM macroprocesos")
    macroprocesos = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_p, descripcion FROM procesos")
    procesos = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, descripcion FROM tipo_documento")
    documento = cursor.fetchall()
    cursor.close()

    return render_template('index.html', macroprocesos=macroprocesos, procesos=procesos, documento=documento, resultados=resultados)

@app.route('/footer')
def footer():
    return render_template('footer.html')

@app.route('/header')
def header():
    return render_template('header.html')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
    
    