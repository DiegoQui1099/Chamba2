from flask import Flask, render_template, request, redirect, url_for, session, flash
import os



app = Flask(__name__)
app.secret_key = 'jeje'

@app.route('/')
def index():
    return render_template('index.html')



# -- conexion unicamente local -- #
if __name__ == '__main__':
    app.run(debug=True, port=4000)