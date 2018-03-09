import config
from modules.db import Database
from flask import jsonify


def split_on_first_capital(string):
    split = []
    index = 0
    for i in range(len(string)):
        ascii_value = ord(string[i])
        if ord("A") <= ascii_value <= ord("Z"):
            split.append(string[index:i].lower())
            index = i
    split.append(string[index:].lower())
    return split


def process_collection(request):
    collection = request.path[len(config.rest.root):]
    if collection:
        if '/' in collection:
            collection = collection[:collection.index('/')]
        return collection
    return config.collections


def process_request(request, _id):
    info = {}
    info['collection'] = process_collection(request)
    if info['collection'] == config.collections:
        return {config.collections: Database().collection_names()}
    info['method'] = request.method.lower()
    info['json'] = process_json(request)
    info['event'] = info['json'].pop('event', None)
    if info['event']:
        info['quantity'] = split_on_first_capital(info['event'])[2]
    elif _id:
        info['json'] = {'_id': _id}
        info['quantity'] = 'one'
    else:
        info['quantity'] = 'many'
    return execute(info)


def process_json(request):
    if request.method == 'GET':
        json = {param: request.args.get(param) for param in request.args}
    else:
        json = request.get_json()
    return json


def execute(info):
    res = Database(info['collection']).execute(info['method'], info['quantity'], info['json'])
    print(res)
    return jsonify(res)