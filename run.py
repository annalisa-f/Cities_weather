from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

app.jinja_env.filters['zip'] = zip

RECIPEDB = 'recipes.db'

def fetchrecipes(db):

    name = []
    ingredients = []
    method = []
    cur = db.execute('SELECT name FROM Recipes')
    for row in cur:
        print(row)
        nrow = row[0]
        name.append(nrow)

    for n in name:

        oneingred = []
        onemethod = []

        cur = db.execute('SELECT ingredients FROM ' + n)
        for row in cur:
            if row[0] is not None:
                oneingred.append(row[0])
        ingredients.append(oneingred)

        cur = db.execute('SELECT steps FROM ' + n)
        for row in cur:
            if row[0] is not None:
                onemethod.append(row[0])
        method.append(onemethod)


    return [name, ingredients, method]

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
    ingreds = []

    for input in request.form:
        if input == 'name':
            name = request.form[input]
        elif 'quantity' in input:
            quantity.append(request.form[input])
        elif 'ingredient' in input:
            ingredients.append(request.form[input])
        elif 'method' in input:
            method.append(request.form[input])

    for q, i in zip(quantity, ingredients):
        qi = q, i
        qistr = " ".join(qi)
        ingreds.append(qistr)


    namedb = name.replace(" ", "_")
    namedb = str(namedb)
    print(name)
    db = sqlite3.connect(RECIPEDB)

    cur= db.execute(
        'CREATE TABLE IF NOT EXISTS ' + namedb + '( id INTEGER PRIMARY KEY, ingredients TEXT, steps TEXT)'
        )

    cur= db.execute(
        'INSERT INTO Recipes(name) VALUES (?)', (namedb,)
        )

    for i in ingreds:
        db.execute(
        'INSERT INTO ' + namedb +'(ingredients) VALUES (?)', (i,)
        )
        db.commit()

    for m in method:
        db.execute(
        'INSERT INTO ' + namedb +'(steps) VALUES (?)', (m,)
        )
        db.commit()

    db.close()


    return render_template('confirm.html', name=name, ingredients=ingreds, quantity=quantity, method=method)

@app.route('/view')
def view():

    db = sqlite3.connect(RECIPEDB)

    recipes = fetchrecipes(db)

    db.close()

    names = {}
    ingredients = recipes[1]
    method = recipes[2]
    number = 0


    for n in recipes[0]:
        nicen = n.replace("_", " ")
        names[number] = nicen
        number += 1


    return render_template('view.html', names=names, ingredients=ingredients, method=method)
