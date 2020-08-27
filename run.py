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
        'CREATE TABLE ' + namedb + '( id INTEGER PRIMARY KEY, ingredients TEXT, steps TEXT)'
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

    name=recipes[0]
    cleanname = []
    ingredients = []
    methods = []

    for i in recipes[1]:
        i.insert(0, 'Ingredients: ')
        ingredients.append(i)

    for m in recipes[2]:
        m.insert(0, 'Method: ')
        methods.append(m)


    for n in name:
        cleanname.append(n.replace("_", " "))

    ingred_method = []


    for i, m in zip(ingredients, methods):
        im = []
        im.append(i)
        im.append(m)
        ingred_method.append(im)



    allrecipes = dict(zip(cleanname, ingred_method))

    #print(name)
    #print(allrecipes)



    return render_template('view.html', allrecipes=allrecipes)
