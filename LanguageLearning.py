from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'study'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/study'

mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/<name>')
def index(name):
    return render_template("index.html", name=name)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return 'About Section, method = %s' % request.method


@app.route('/login')
def login():
    language = mongo.db.language
    output = []
    for obj in language.find():
        output.append(obj['language'])
    print(output)
    # language.insert({'language':'dutch'})
    return 'Login Section'


@app.route('/languages/<int:language>')
def language(language):
    return "The id is %s" % language


if __name__ == '__main__':
    app.run()
