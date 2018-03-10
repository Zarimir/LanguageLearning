import config
from pymongo import MongoClient
from bson import ObjectId


class Database:
    def __init__(self, collection=None):
        self.db = Database.connect(collection)
        self.current = None
        if collection is not config.collections:
            self.current = self.db

    @staticmethod
    def connect(collection=None):
        db = MongoClient()[config.database]
        if collection:
            return db[collection]
        return db

    def get(self, collection):
        self.current = Database.connect(collection)
        return self

    def get_users(self):
        return self.get('users')

    def get_languages(self):
        return self.get('languages')

    def get_words(self):
        return self.get('words')

    def get_languages_classes(self):
        return self.get('languagesclassifications')

    def collection_names(self):
        return self.db.collection_names()

    def execute(self, operation, quantity, args):
        if operation == 'get':
            if quantity == 'one':
                return normalize(self.find_by_id(args))
            else:
                return {'elements': self.find(args)}
        elif operation == 'post':
            if quantity == 'one':
                return {'_id': normalize(self.insert_one(args))}
        elif operation == 'put':
            if quantity == 'one':
                self.replace_by_id(args)
                return
        elif operation == 'delete':
            if quantity == 'one':
                self.delete_by_id(args)
                return
        raise ValueError('Not Supported')

    def insert_one(self, obj):
        return self.current.insert_one(obj.copy()).inserted_id

    def find_one(self, pattern):
        return normalize(self.current.find_one(pattern))

    def find(self, pattern=None):
        if pattern is None:
            pattern = {}
        return [normalize(element) for element in self.current.find(pattern.copy())]

    def find_by_id(self, arg):
        if type(arg) == dict:
            return self.find_by_id(arg['_id'])
        elif type(arg) == str or type(arg) == ObjectId:
            return normalize(self.current.find_one({'_id': ObjectId(arg)}))

    def replace_by_id(self, replacement):
        replacement = replacement.copy()
        replacement["_id"] = ObjectId(replacement["_id"])
        self.current.replace_one({'_id': ObjectId(replacement['_id'])}, replacement)

    def delete_by_id(self, arg):
        if type(arg) == dict:
            self.delete_by_id(arg['_id'])
        elif type(arg) == str or type(arg) == ObjectId:
            self.current.delete_one({'_id': ObjectId(arg)})


def normalize(obj):
    """
    Converts any non-json types in to json-compatible types.
    :param obj:
    :return:
    """
    if type(obj) is ObjectId:
        return str(obj)
    elif type(obj) is list:
        for i in range(len(obj)):
            obj[i] = normalize(obj[i])
    elif type(obj) is dict:
        for key in obj:
            obj[key] = normalize(obj[key])
    return obj
