import config
import html
from modules.db import get_users
from modules.result import Result
from modules import validator


def get_user(user):
    result = Result()
    result.update(validator.has(user, 'username', str))

    return get_users().find_one({'username': user['username']})


def login(user, password=False):
    valid = validator.valid_user(user, password=password)
    if not valid:
        return valid
    pattern = {'username': user['username']}
    if password:
        pattern['password'] = user['password']
    return Result(get_users().find_one(pattern))


def register(user):
    result = validator.valid_user(user)
    if result:
        users = get_users()
        if not users.find_one({'username': user['username']}):
            users.insert_one({'username': user['username'], 'password': user['password']})
            return result
        result.fail({config.username_taken: True})
    return result


def delete(user):
    result = Result()
    result.update(validator.has(user, 'username', str))
    if result:
        count = get_users().delete_one({'username': user['username']}).deleted_count
        result.succeed({'deleted': count > 0})
    return result


def update(user):
    users = get_users()
    users.update_one({"username": user["username"]}, {"$set": user})


def replace(user):
    users = get_users()
    users.replace_one({"username": user["username"]}, user)