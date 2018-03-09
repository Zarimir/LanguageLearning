from pymongo import response

import config
from flask import Flask, render_template, request, session, abort, redirect, url_for, jsonify
from flask.ext.session import Session
from flask_pymongo import PyMongo
from modules.db import Database
from flask_restful import Resource, Api
from modules.processor import process_request
import os
import constants

app = Flask(__name__)
app.config['MONGO_DBNAME'] = config.database
app.config['MONGO_URI'] = 'mongodb://localhost:27017/%s' % config.database
app.config['SECRET_KEY'] = 'test'
app.secret_key = os.urandom(24)
Session(app)
api = Api(app)
mongo = PyMongo(app, config_prefix='MONGO')


class Collection(Resource):
    def get(self, _id=None):
        return process_request(request, _id)

    def post(self, _id=None):
        return process_request(request, _id)

    def put(self, _id=None):
        return process_request(request, _id)

    def delete(self, _id=None):
        return process_request(request, _id)


addresses = [config.rest.root]
for name in Database().collection_names():
    address = config.rest.root + name
    addresses.append(address)
    addresses.append(address + '/<string:_id>')

api.add_resource(Collection, *addresses)


@app.before_request
def before_request():
    constants.setg()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/word/<_id>', methods=['GET', 'POST'])
def word(_id):
    element = Database().get_words().execute("get", "one", {"_id": _id})
    element['z'] = ["awoidjawoi", "OAWIdjoawid"]
    print(element)

    return render_template('word.html', element=element)


@app.route('/languagez', methods=['GET', 'POST'])
def languagez():
    return render_template('languages.html')


@app.route('/dictionary', methods=['GET', 'POST'])
@app.route('/dictionary/<language>', methods=['GET', 'POST'])
def dictionary(language=None):
    language_id = None
    if language:
        language = Database().find_language(language)
        if language:
            language_id = language["_id"]
    return render_template('dictionary.html', language_id=language_id)


@app.route('/courses/', methods=['GET', 'POST'])
def courses():
    params = {param: request.args.get(param) for param in request.args}
    print(params)
    return render_template("courses.html")


@app.route('/practice/', methods=['GET'])
def practice():
    print("HEllo")


@app.route('/admin/languages', methods=['GET', 'POST'])
def admin_languages():
    return render_template('admin/languages.html')


@app.route('/admin/dictionary', methods=['GET', 'POST'])
@app.route('/admin/dictionary/<language>', methods=['GET', 'POST'])
def admin_dictionary(language):
    language_id = None
    if language:
        language = Database().find_language(language)
        if language:
            language_id = language["_id"]
    return render_template('admin/dictionary.html', language_id=language_id)


if __name__ == '__main__':
    app.run()
