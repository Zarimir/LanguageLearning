import config
from bson import ObjectId
from modules.db import Database
from modules import validator, security
from modules.validator import crash


def username_not_taken(username):
    validator.valid_username(username)
    if Database().get_users().find_one({'username': username}):
        crash(config.username_taken)


def register(username, password):
    validator.valid_login(username, password)
    username_not_taken(username)
    hashed = security.hashpw(password)
    return Database().get_users().insert_one({'username': username, 'password': hashed})


def login(username, password):
    try:
        validator.valid_login(username, password)
        account = Database().find_one({'username': username})
        validator.valid_account(account)
        return security.checkpw(password, account['password'])
    finally:
        return False


def replace(account):
    _id = validator.has(account, '_id', ObjectId)
    validator.valid_account(account)
    return Database().get_users().replace_by_id(_id, account)


def delete(_id):
    return Database().get_users().delete_by_id(_id)
