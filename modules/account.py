from bson import ObjectId

import config
import html
from modules.db import get_users
from modules.result import Result
from modules import validator, security


def get_user(user):
    result = Result()
    result.update(validator.has(user, 'username', str))

    return get_users().find_one({'username': user['username']})


def register(user):
    result = Result()
    result.update(validator.valid_user(user))
    if result:
        result.update(login(user), invert=True)
        if result:
            get_users().insert_one({'username': user['username'], 'password': user['password']})
        else:
            result.fail({config.username_taken: True})
    return result


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


def replace(user):
    result = Result()
    result.update(validator.has(user, '_id', ObjectId))
    if not result:
        return result

    result.update(validator.valid_user(user, password=True))
    if not result:
        return result

    users = get_users()
    b = users.replace_one({'_id': user['_id']}, user)
    return result.succeed({'modified': b.modified_count})


def delete(user):
    result = Result()
    result.update(validator.has(user, 'username', str))
    if result:
        count = get_users().delete_many({'username': user['username']}).deleted_count
        result.succeed({'deleted': int(count)})
    return result
