class Form:
    def __init__(self, request):
        self.request = request

    def __getitem__(self, item):
        if item in self.request.form:
            return self.request.form[item]
        return None
