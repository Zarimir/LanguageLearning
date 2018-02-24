from bson import ObjectId


def jsonify(obj):
    if type(obj) is ObjectId:
        return str(obj)
    elif type(obj) is dict or type(obj) is list:
        for key in obj:
            obj[key] = jsonify(obj[key])
    return obj