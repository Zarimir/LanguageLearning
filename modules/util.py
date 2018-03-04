from bson import ObjectId


def normalize(obj):
    """
    Converts any non-json types in to json-compatible types.
    :param obj:
    :return:
    """
    if type(obj) is ObjectId:
        return str(obj)
    elif type(obj) is list:
        for i in range(len(obj)):
            obj[i] = normalize(obj[i])
    elif type(obj) is dict:
        for key in obj:
            obj[key] = normalize(obj[key])
    return obj


def split_on_first_capital(string):
    split = []
    index = 0
    for i in range(len(string)):
        ascii_value = ord(string[i])
        if ord("A") <= ascii_value <= ord("Z"):
            split.append(string[index:i])
            index = i
    split.append(string[index:])
    return split
