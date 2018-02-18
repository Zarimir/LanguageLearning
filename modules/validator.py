import re

import config
from modules.result import Result


def has(obj, field, field_type=None):
    result = Result()
    if type(obj) is not dict and type(obj) is not list:
        return result.crash()
    if field not in obj:
        return result.crash()
    if field_type and type(obj[field]) is not field_type:
        return result.crash()
    return result.succeed()


def valid_username(username):
    result = Result()
    pattern = r'[^A-Za-z0-9\._-]'
    if type(username) is str and len(username) > config.username_length and not re.search(pattern, username):
        return result.succeed()
    return result.fail({config.invalid_username: True})


def valid_password(password):
    result = Result()
    if type(password) is str and len(password) > config.password_length:
        return result.succeed()
    return result.fail({config.invalid_password: True})


def valid_user(user, password=None):
    result = Result()
    has_username = has(user, 'username', str)
    result.update(has_username)
    if has_username:
        result.update(valid_username(user['username']))
    if password:
        has_password = has(user, 'password', str)
        result.update(has_password)
        if has_password:
            result.update(valid_password(user['password']))
    return result
