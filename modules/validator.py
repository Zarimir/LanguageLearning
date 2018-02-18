def has(obj, field, message=None):
    if type(obj) is not dict and type(obj) is not list:
        raise ValueError("Obj is of type '%s'" % type(obj))
    elif field not in obj:
        if message:
            raise ValueError(message)
        else:
            raise ValueError("'%s' does not belong to obj ''" % field, obj)
    return True