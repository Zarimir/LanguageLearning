import config
import html
from modules.db import get_users
from modules.result import Result
from modules import validator, security


def get_user(user):
    result = Result()
    result.update(validator.has(user, 'username', str))

    return get_users().find_one({'username': user['username']})


def login(attempt, password=False):
    result = validator.valid_user(attempt, password=password)
    if not result:
        return result
    pattern = {'username': attempt['username']}
    user = get_users().find_one(pattern)
    if not user:
        return result.fail({config.account_found: None})
    result.succeed({config.account_found: user})
    if password:
        if not validator.has(user, 'password', str) or not validator.has(user, 'salt', str):
            return result.crash()
        elif not validator.has(attempt, 'password', str):
            return result.fail({config.invalid_password: True})
        valid_password = security.hashcmp(attempt['password'], user['password'], user['salt'])
        result.consume({config.invalid_password: not valid_password}, value=valid_password)
    return result

print(login({'username': 'Archling', 'password':'123'}, password=True))
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