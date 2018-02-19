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




secret = b'123qwe'
salt = bcrypt.gensalt()
hash = bcrypt.hashpw(secret, salt)
print(secret)
print(hash)
print(bcrypt.checkpw(secret, hash))