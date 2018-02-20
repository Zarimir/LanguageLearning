import re
import config
from modules.result import Result


def has(obj, field, field_type=None):
    """Checks if obj dict has a field of a given field_type (if specified).
    Outputs internal error messages if the check fails"""

    result = Result()
    if type(obj) is not dict and type(obj) is not list:
        return result.crash()
    if field not in obj:
        return result.crash()
    if field_type and type(obj[field]) is not field_type:
        return result.crash()
    return result.succeed()


def valid_username(username):
    """Checks if a given username follows the given specifications, only
    higher/lower case letters, digits, periods, underscores and dashes are allowed.
    The minimum length is specified in the config file"""

    result = Result()
    pattern = r'^[\w\.-]{' + str(config.username_length) + ',}'
    if type(username) is not str:
        return result.crash()
    match = re.search(pattern, username)
    if not match or match.span()[1] != len(username):
        return result.fail({config.invalid_username: True})
    return result.succeed()


def valid_password(password):
    """Checks if the password is valid, a string of minimum length specified
    in the config file"""

    result = Result()
    if type(password) is str and len(password) > config.password_length:
        return result.succeed()
    return result.fail({config.invalid_password: True})


def valid_user(user, password=None):
    """Checks if a user dict has a valid username and if
    requested, a valid password"""

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
