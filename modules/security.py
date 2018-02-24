import codecs
import bcrypt


def encode(arg):
    if type(arg) is str:
        return codecs.encode(arg, 'utf-8')
    return arg


def decode(arg):
    if type(arg) is bytes:
        return codecs.decode(arg, 'utf-8')
    return arg


def hashpw(plaintext):
    """
    Assumes that all input is in string form
    :param plaintext: String
    :return: hash; type(hash) is String
    """
    if len(plaintext) > 72:
        # 72 is the hashing limit
        raise ValueError('Could not hash')
    return decode(bcrypt.hashpw(encode(plaintext), bcrypt.gensalt()))


def checkpw(plaintext, hashed):
    """
    Assumes that all input is in string form.
    :param plaintext: String
    :param hashed: String
    :return: True if equal; False otherwise
    """
    return bcrypt.checkpw(encode(plaintext), encode(hashed))
