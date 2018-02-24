import bcrypt
from bson import ObjectId

import config
from pymongo import MongoClient

from modules import validator


class Database:
    def __init__(self):
        self.db = get_db()
        self.current = None

    def get_users(self):
        self.current = get_db(config.users)
        return self

    def get_languages(self):
        self.current = get_db(config.languages)
        return self

    def get_words(self):
        self.current = get_db(config.words)
        return self

    def insert_one(self, obj):
        validator.check_dict(obj)
        return self.current.insert_one(obj.copy()).inserted_id

    def find_one(self, pattern):
        validator.check_dict(pattern)
        return self.current.find_one(pattern)

    def find(self, pattern=None):
        if pattern is None:
            pattern = {}
        validator.check_dict(pattern)
        return self.current.find(pattern)

    def find_by_id(self, _id):
        validator.check_id(_id)
        return self.current.find_one({'_id': ObjectId(_id)})

    def replace_by_id(self, _id, new):
        validator.check_id(_id)
        validator.check_dict(new)
        return self.current.replace_one({'_id': ObjectId(_id)}, new).modified_count

    def delete_by_id(self, _id):
        validator.check_id(_id)
        return self.current.delete_one({'_id': ObjectId(_id)}).deleted_count


def get_db(collection=None):
    db = MongoClient()[config.database]
    if collection:
        return db[collection]
    return db


def get_users():
    return get_db(config.users)


def get_languages():
    return get_db(config.languages)


def get_words():
    return get_db(config.words)


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


"""
cleanup()

db = Database().get_users()
pattern = {'username': 'awoidawd', 'password': 'aowifhOAWIFhafwwaf'}
db.insert_one(pattern)
print(pattern)
ids = []
for obj in db.find(pattern):
    ids.append(obj['_id'])

for arg in ids:
    print(arg)
    print(type(arg))
    db.delete_by_id(arg)

for a in db.find():
    print(a)

"""