import config
from pymongo import MongoClient

def get_users():
    return MongoClient()[config.database][config.users]