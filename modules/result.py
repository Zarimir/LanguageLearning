import config


class Result:
    """A wrapper for function output,
    the value represents whether the function executed as expected,
    the obj represents messages produced by the function during execution"""

    def __init__(self, value=True, obj=None):
        if obj is None:
            obj = {}
        self.value = value
        self.obj = obj

    def __str__(self):
        return "result=" + str(self.value) + ", obj=" + str(self.obj)

    def __iter__(self):
        for key in self.obj:
            yield key

    def __bool__(self):
        return self.value

    def __dict__(self):
        return self.obj.copy()

    def __getitem__(self, item):
        return self.obj[item]

    def __setitem__(self, key, value):
        self.obj[key] = value

    def items(self):
        return self.obj.items()

    def crashed(self):
        return config.internal_error in self.obj

    def consume(self, obj, value=None):
        if value is not None and type(value) is bool:
            self.value = value
        if obj is None:
            obj = {}
        for key, value in obj.items():
            self.obj[key] = value
        return self

    def fail(self, obj=None):
        return self.consume(obj, value=False)

    def crash(self):
        return self.fail({config.internal_error: True})

    def succeed(self, obj=None):
        return self.consume(obj, value=True)

    def update(self, result, invert=False):
        # if the argument's value would cause an error, consume its messages
        if not result and not invert or result and invert:
            self.value = False
            if not invert:
                self.fail(result)
        else:
            if not invert:
                self.consume(result)
        return self
