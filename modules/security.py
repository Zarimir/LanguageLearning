import codecs
import bcrypt


def encode(arg):
    """
    Encodes input into bytes.
    :param arg: string or bytes
    :return: byte encoded if input is string; input otherwise
    """
    if type(arg) is str:
        return codecs.encode(arg, 'utf-8')
    return arg


def decode(arg):
    """
    Decodes string from bytes.
    :param arg: string or bytes
    :return: decoded bytes if input is bytes; original output otherwise
    """
    if type(arg) is bytes:
        return codecs.decode(arg, 'utf-8')
    return arg


def hashpw(plaintext):
    """
    Input/Output are strings
    :param plaintext: to be hashed
    :return: hash string
    """
    if len(plaintext) > 72:
        # 72 is the hashing limit
        raise ValueError('Could not hash')
    return decode(bcrypt.hashpw(encode(plaintext), bcrypt.gensalt()))


def checkpw(plaintext, hashed):
    """
    Input/Output are strings.
    :param plaintext: string
    :param hashed: string
    :return: True if equal; False otherwise
    """
    return bcrypt.checkpw(encode(plaintext), encode(hashed))
