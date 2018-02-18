import config
import html
from modules.db import get_users
from modules.result import Result


def valid_user(user, password=False):
    result = Result()
    if type(user) is not dict:
        return result.fail({config.internal_error: True})
    if 'username' not in user or not user['username'] or type(user['username']) is not str:
        result.fail({config.invalid_username: True})
    if password and ('password' not in user or not user['password'] or type(user['password']) is not str):
        result.fail({config.invalid_password: True})
    return result


def get_user(user):
    return get_users().find_one({'username': user['username']})


def login(user, password=False):
    valid = valid_user(user, password=password)
    if not valid:
        return valid
    pattern = {'username': user['username']}
    if password:
        pattern['password'] = user['password']
    return Result(get_users().find_one(pattern))


def register(user):
    result = valid_user(user)
    if result:
        users = get_users()
        if not users.find_one({'username': user['username']}):
            users.insert_one({'username': user['username'], 'password': user['password']})
            return result
        result.fail({config.username_taken: True})
    return result


def delete(user):
    return get_users().delete_one({'username': user['username']}).deleted_count


def update(user):
    users = get_users()
    users.update_one({"username": user["username"]}, {"$set": user})


def replace(user):
    users = get_users()
    users.replace_one({"username": user["username"]}, user)