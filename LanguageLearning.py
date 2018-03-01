import bcrypt
from pymongo import response

import config
from flask import Flask, render_template, request, session, abort, redirect, url_for
from flask.ext.session import Session
from flask_pymongo import PyMongo
from modules import languages as lang
from modules.course import Course
from modules.db import Database
from flask_restful import Resource, Api
import os
from modules.util import jsonify as normalize
import constants

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
        print(type(db))
        print(type(_id))
        print(_id)
        obj = db.find_by_id(_id)
        return normalize(obj)


class Languages(Resource):
    def get(self, _id=None):
        return {'languages': db_get(Database().get_languages(), _id)}


class Words(Resource):
    def get(self, _id=None):
        return {'words': db_get(Database().get_languages(), _id)}

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


def get_collection(request):
    path = request.path
    if len(path) > len(config.rest.root):
        collection = path[len(config.rest.root):]
        if '/' in collection:
            collection = collection[:collection.index('/')]
        return collection
    return config.collections


class Collection(Resource):
    def get(self, _id=None):
        collection = get_collection(request)
        print(collection)
        if collection == config.collections:
            return {'collections': Database().collection_names()}
        return {collection: db_get(Database().get(collection), _id)}


addresses = [config.rest.root]
for name in Database().collection_names():
    addr = config.rest.root + name
    addresses.append(addr)
    addresses.append(addr + '/<string:_id>')

api.add_resource(Collection, *addresses)


@app.before_request
def before_request():
    constants.setg()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/languagez', methods=['GET', 'POST'])
def languagez():
    return render_template('languages.html')


@app.route('/courses/', methods=['GET', 'POST'])
def courses():
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
    print("HEllo")


if __name__ == '__main__':
    app.run()