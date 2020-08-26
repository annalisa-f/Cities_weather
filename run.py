from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
RECIPEDB = 'recipes.db'

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

    name = 'name'
    ingredients = []
    quantity = []
    method = []

    for input in request.form:
        if input == 'name':
            name = request.form[input]
        elif 'quantity' in input:
            quantity.append(request.form[input])
        elif 'ingredient' in input:
            ingredients.append(request.form[input])
        elif 'method' in input:
            method.append(request.form[input])

    print(name, quantity, ingredients, method)
    ingreds = dict(zip(ingredients, quantity))

    db = sqlite3.connect(RECIPEDB)

    cur= db.execute(
        'INSERT INTO recipes(name, ingredients, method) VALUES(?, ?, ?)',
        (name, str(ingreds), str(method))
    )

    db.commit()
    db.close()


    return render_template('confirm.html', name=name, ingredients=ingreds, quantity=quantity, method=method)

@app.route('/view')
def view():

    db = sqlite3.connect(RECIPEDB)

    id = []
    name = []
    ingredients = {}
    method = []

    cur= db.execute(
        'SELECT id, name, ingredients, method FROM recipes'
    )

    db.close()

    return render_template('view.html', id=id)
