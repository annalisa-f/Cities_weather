from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/numbers')
def numbers():
    return render_template('numbers.html')

@app.route('/add', methods=['POST'])
def add():
    print(request.form)

    ingred = request.form['ingred']
    fieldnames = []

    for i in range(int(ingred)):
        fieldnames.append(i)

    return render_template('add.html', ingred=fieldnames)
