from datetime import datetime


class ArgumentMethod(object):
    def __init__(self, method, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.order = datetime.utcnow()

    def __call__(self, *args, **kwargs):
        return self.method(*(*self.args, *args), **{**self.kwargs, **kwargs})
