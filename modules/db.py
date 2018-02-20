import bcrypt

import config
from pymongo import MongoClient


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
    users = get_users().find({'username': {'$regex': '^[A-Za-z0-9_\.-]{' + str(config.username_length) + ',}$'}})
    valid = []
    loop = []
    for user in users:
        username = user['username']
        if username in valid and username not in [dictionary['username'] for dictionary in loop]:
            loop.append({'username': username})
        else:
            valid.append(username)
    print(loop)
    for invalid_user in get_users().find({'username': {'$nin': valid}}):
        loop.append({'username': invalid_user['username']})
    print(loop)
    if loop:
        get_users().delete_many({'$or': [expression for expression in loop]})
"""
secret = b'123qwe'
salt = bcrypt.gensalt()
hash = bcrypt.hashpw(secret, salt)
print(secret)
print(hash)
print(bcrypt.checkpw(secret, hash))
"""