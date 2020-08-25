from flask import Flask, render_template, request, g

import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/numbers')
def numbers():
    return render_template('numbers.html')

@app.route('/add', methods=['POST'])
def add():

    ingred = request.form['ingred']
    method = request.form['steps']
    fieldnames = []
    methodfields = []

    for i in range(int(ingred)):
        fieldnames.append(i)

    for m in range(int(method)):
        methodfields.append(m)

    return render_template('add.html', ingred=fieldnames, methodnum=methodfields)

@app.route('/confirm', methods=['POST'])
def confirm():
    return render_template('confirm.html')
