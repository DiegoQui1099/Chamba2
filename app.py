from flask import Flask, render_template, request, redirect, url_for, json
from flask_mysqldb import MySQL
from config import Config
import requests

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/footer')
def footer():
    return render_template('footer.html')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])