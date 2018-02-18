import bcrypt

import config
from flask import Flask, render_template, request, session, abort, redirect, url_for, g
from flask_pymongo import PyMongo

from modules import account

app = Flask(__name__)
app.config['MONGO_DBNAME'] = config.database
app.config['MONGO_URI'] = 'mongodb://localhost:27017/%s' % config.database
app.config['SECRET_KEY'] = 'test'


mongo = PyMongo(app, config_prefix='MONGO')


"""
@app.before_request
def before_request():
    g.user = None
    if 'user' is in session:
        g.user = session['user']

    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)



def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = some_random_string()
        app.jinj
    return session['_csrf_token']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None) ??
        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('protected'))


    return render_template('index.html')


@app.route('/protected')
def protected():
    if g.user:
        return render_template('protected.html')
    return redirect(url_for('index'))



@app.route('/about', methods=['GET', 'POST'])
def about():
    return 'About Section, method = %s' % request.method


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if not user.get_user(request.form['username']):
            hash = bcrypt.gensalt()
            password = bcrypt.hashpw(request.form['password'], hash)


        return 'That user already exists!'

"""


@app.route('/')
def index():
    return "Welcome!"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = {'username': request.form['username'], 'password': request.form['password']}
        account.register(user)





        if not account.get_user(user):
            if account.register(user):
                return redirect(url_for('index'))
            return render_template('register.html', error=True)
        return render_template('register.html', username_exists=True)
    return render_template('register.html')


@app.route('/login')
def login():
    #print(output)
    # language.insert({'language':'dutch'})
    return 'Login Section'


@app.route('/languages/')
def languages():
    objs = []
    for obj in mongo.db.languages.find():
        objs.append(obj)
    print(objs)
    return render_template("languages.html", languages=objs)


if __name__ == '__main__':
    app.run()
