import bcrypt
from pymongo import response

import config
from flask import Flask, render_template, request, session, abort, redirect, url_for, g, jsonify
from flask.ext.session import Session
from flask_pymongo import PyMongo
from modules.form import Form
from modules import languages as lang
from modules.course import Course
from modules.db import Database
from flask_restful import Resource, Api
import os
from modules.util import jsonify as normalize

app = Flask(__name__)
app.config['MONGO_DBNAME'] = config.database
app.config['MONGO_URI'] = 'mongodb://localhost:27017/%s' % config.database
app.config['SECRET_KEY'] = 'test'
app.secret_key = os.urandom(24)
Session(app)
api = Api(app)
mongo = PyMongo(app, config_prefix='MONGO')


def db_get(db, _id=None):
    if _id is None:
        objs = []
        for obj in db.find():
            objs.append(normalize(obj))
        return objs
    else:
        obj = db.find_by_id(_id)
        return normalize(obj)


class Languages(Resource):
    def get(self, _id=None):
        print(request.form.get('trol', None, str))
        return {'languages': db_get(Database().get_languages(), _id)}


class Words(Resource):
    def get(self, _id=None):
        print(request.content_type)
        print('get')
        print(request.is_json)
        try:
            print(request)
            print(request.get_json())
        except Exception as msg:
            print("ERROR MODA FUCKA")
            print(msg)
        return {'words': db_get(Database().get_words(), _id)}

    def delete(self, _id=None):
        print("DELETE")
        print(request.get_json())
        print(request.is_json)
        print(request.content_type)
        return None

    def delete(self, _id=None):
        print("DELETE")
        print(request.get_json())
        print(request.is_json)
        print(request.content_type)
        return None
'''    
    def post(self, _id=None):
        print('post')
        print(request)
        print(request.get_json())
        db = Database().get_words()
        _id = request.form.get('_id', None, str)
        language = request.form.get('language', None, str)
        spelling = request.form.get('spelling', None, str)
        meaning = request.form.get('meaning', None, str)
        obj = {
            'language': language,
            'spelling': spelling,
            'meaning': meaning
        }
        if _id is None:
            _id = db.insert_one(obj)
            obj['_id'] = _id
        else:
            db.replace_by_id(_id, obj)
        return normalize(obj)
        #print(request.form['spelling'])

    def delete(self, _id=None):
        print('delete')
        result = False
        if _id is not None:
            db = Database().get_words()
            count = db.delete_by_id(_id)
            result = count > 0
        return {'success': result}
'''

api.add_resource(Languages, '/rest/languages', '/rest/languages/<string:_id>')
api.add_resource(Words, '/rest/words', '/rest/words/<string:_id>')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ajax', methods=['GET', 'POST', 'PUT', 'DELETE'])
def ajax():
    print("mehtod is ")
    print(request.method)
    print(request.get_json())
    print(request.content_type)
    print(request.json)
    print(request.is_json)
    return jsonify({"success": True})


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/languagez', methods=['GET', 'POST'])
def languagez():
    config.setg()
    return render_template('languages.html')


@app.route('/courses/', methods=['GET', 'POST'])
def courses():
    config.setg()
    if request.method == 'POST':
        try:
            course_id = request.form.get(config.course, None, str)
            language_id = request.form.get(config.language, None, str)
            session[config.course] = Course().set(course_id, language_id)
            return redirect(url_for('index'))
        except ValueError:
            return redirect(url_for('courses'))

    objs = [language for language in lang.get_languages()]
    print(objs)
    return render_template("courses.html", languages=objs)


@app.route('/practice/', methods=['GET'])
def practice():
    config.setg()


if __name__ == '__main__':
    app.run(debug=True)




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

"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Form(request)
    if request.method == 'POST':
        try:
            account.register(form['username'], form['password'])
            render_template(url_for('/'))
        except ValueError as error:
            render_
            print(error)



        if not account.get_user(user):
            if account.register(user):
                return redirect(url_for('index'))
            return render_template('register.html', error=True)
        return render_template('register.html', username_exists=True)
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

    #print(output)
    # language.insert({'language':'dutch'})
    return 'Login Section'


"""