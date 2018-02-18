import bcrypt

import config
from pymongo import MongoClient


def get_users():
    return MongoClient()[config.database][config.users]



secret = b'123qwe'
salt = bcrypt.gensalt()
hash = bcrypt.hashpw(secret, salt)
print(secret)
print(hash)
print(bcrypt.checkpw(secret, hash))