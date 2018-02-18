import config


class Result:
    def __init__(self, value=True, obj=None):
        if obj is None:
            obj = {}
        self.value = value
        self.obj = obj

    def __str__(self):
        return "result=" + str(self.value) + ", obj=" + str(self.obj)

    def __bool__(self):
        return self.value

    def __dict__(self):
        return self.obj.copy()

    def fail(self, obj=None):
        if obj is None:
            obj = {}
        elif type(obj) is Result:
            obj = obj.__dict__()
        self.value = False
        for key in obj:
            self.obj[key] = obj[key]
        return self

    def crash(self):
        return self.fail({config.internal_error: True})

    def succeed(self, obj=None):
        if obj is None:
            obj = {}
        elif type(obj) is Result:
            obj = obj.__dict__()
        self.value = True
        for key in obj:
            self.obj[key] = obj[key]
        return self

    def update(self, result, invert=False):
        # if the argument's value would cause an error, consume its messages
        if not result and not invert or result and invert:
            if not invert:
                self.fail(result)
            self.value = False
        return self
