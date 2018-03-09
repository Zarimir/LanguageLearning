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


def process_request(request):
    collection = process_collection(request)
    json = process_json(request)
    event = json.pop('event', None)
    if collection == config.collections:
        return {config.collections: Database().collection_names()}
    return execute(event, json)


def process_json(request):
    if request.method == 'GET':
        json = {param: request.args.get(param) for param in request.args}
    else:
        json = request.get_json()
    return json


def execute(event, json):
    args = split_on_first_capital(event)
    collection = args[0]
    method = args[1]
    quantity = args[2]
    res = Database(collection).execute(method, quantity, json)
    print(res)
    return jsonify(res)