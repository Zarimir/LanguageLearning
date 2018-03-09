import config
from pymongo import MongoClient
from modules import validator
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
        return self.get(config.users)

    def get_languages(self):
        return self.get(config.languages)

    def get_words(self):
        return self.get(config.words)

    def collection_names(self):
        return self.db.collection_names()

    def execute(self, operation, quantity, args):
        if operation == 'get':
            if quantity == 'one':
                return {'elementify': normalize(self.find_by_id(args))}
            else:
                return {'elements': [normalize(element) for element in self.find(args)]}
        elif operation == 'post':
            if quantity == 'one':
                return {'_id': normalize(self.insert_one(args))}
        elif operation == 'put':
            if quantity == 'one':
                return {'modified': normalize(self.replace_by_id(args))}
        elif operation == 'delete':
            if quantity == 'one':
                return {'deleted': normalize(self.delete_by_id(args))}
        raise ValueError('Not Supported')

    def insert_one(self, obj):
        return self.current.insert_one(obj.copy()).inserted_id

    def find_one(self, pattern):
        return self.current.find_one(pattern)

    def find(self, pattern=None):
        print("Pattern is")
        print(pattern)
        if pattern is None:
            pattern = {}
        return self.current.find(pattern.copy())

    def find_by_id(self, arg):
        if type(arg) == dict:
            return self.find_by_id(arg['_id'])
        elif type(arg) == str:
            return self.current.find_one({'_id': ObjectId(arg)})

    def replace_by_id(self, replacement):
        return self.current.replace_one({'_id': ObjectId(replacement['_id'])}, replacement.copy()).modified_count

    def delete_by_id(self, arg):
        if type(arg) == dict:
            return self.delete_by_id(arg['_id'])
        elif type(arg) == str:
            return self.current.delete_one({'_id': ObjectId(arg)}).deleted_count


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


def cleanup():
    to_delete = []
    valid = []
    used_usernames = []
    db = Database().get_users()
    for account in db.find():
        try:
            validator.valid_account(account)
            if account['username'] in used_usernames:
                used_usernames.pop(used_usernames.index(account['username']))
                to_delete.append(account['_id'])
            else:
                used_usernames.append(account['username'])
                valid.append((account['username'], account['_id']))
        except ValueError:
            to_delete.append(account['_id'])
    for account in valid:
        if account[0] not in used_usernames:
            to_delete.append(account[1])
    for _id in to_delete:
        db.delete_by_id(_id)
