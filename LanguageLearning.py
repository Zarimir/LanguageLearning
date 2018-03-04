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
from modules.util import normalize
from modules import collections
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
            temp = normalize(obj)
            objs.append(temp)
        return objs
    else:
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


class Collection(Resource):
    def get(self, _id=None):
        collection = collections.get_collection(request)
        if collection == config.collections:
            return {'collections': Database().collection_names()}
        return {collection: db_get(Database().get(collection), _id)}

    def post(self, _id=None):
        collection = collections.get_collection(request)

    def delete(self, _id=None):
        collection = collections.get_collection(request)
        return {"haha": "aaa"}


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


@app.route('/admin/languages', methods=['GET', 'POST'])
def admin():
    return render_template('admin/languages.html')


if __name__ == '__main__':
    app.run()