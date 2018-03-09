import re

from bson import ObjectId

import config


def crash(message=None):
    if message:
        raise ValueError(message)
    raise ValueError(config.internal_error)


def has(obj, field, field_type=None):
    """Checks if obj dict has a field of a given field_type (if specified).
    Outputs internal error messages if the check fails"""

    if type(obj) is not dict and type(obj) is not list:
        crash()
    if field not in obj:
        crash()
    if field_type and type(obj[field]) is not field_type:
        crash()
    return obj[field]


def valid_username(username):
    """Checks if a given username follows the given specifications, only
    higher/lower case letters, digits, periods, underscores and dashes are allowed.
    The minimum length is specified in the config file"""

    pattern = r'^[\w\.-]{' + str(config.username_length) + ',}'
    if type(username) is not str:
        crash()
    match = re.search(pattern, username)
    if not match or match.span()[1] != len(username):
        crash(config.invalid_username)


def valid_password(password):
    """Checks if the password is valid, a string of minimum length specified
    in the config file"""

    if not (type(password) is str and len(password) > config.password_length):
        crash(config.invalid_password)


def valid_login(username, password):
    """
    Checks if both username and password are valid
    :param username:
    :param password:
    :return:
    """

    valid_username(username)
    valid_password(password)


def valid_account(account):
    has(account, 'username', str)
    has(account, 'password', str)
    valid_username(account['username'])


def check_id(_id):
    if type(_id) is dict:
        check_id()
    elif not (type(_id) is str or type(_id) is ObjectId):
        crash()


def check_dict(obj):
    if type(obj) is not dict:
        crash()
