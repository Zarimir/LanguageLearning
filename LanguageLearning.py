from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'study'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/study'

mongo = PyMongo(app, config_prefix='MONGO')

@app.route('/')
@app.route('/<user>')
def index(user=None):
    return render_template("index.html", user=user)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return 'About Section, method = %s' % request.method


@app.route('/login')
def login():

    #print(output)
    # language.insert({'language':'dutch'})
    return 'Login Section'


@app.route('/languages/')
def languages():
    objs = []
    for obj in mongo.db.language.find():
        objs.append(obj)
    print(objs)
    return render_template("languages.html", languages=objs)


if __name__ == '__main__':
    app.run()
