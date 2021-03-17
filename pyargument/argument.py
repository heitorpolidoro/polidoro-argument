from pyargument.argument_parser import ArgumentParser


class Argument(object):
    def __new__(cls, method=None, **kwargs):
        if callable(method):
            return Argument.add_argument(method, **kwargs)
        else:
            def wrapper(_method):
                return Argument.add_argument(_method, **kwargs)
            return wrapper

    @staticmethod
    def add_argument(method=None, **kwargs):
        ArgumentParser.add_argument(method, **kwargs)
        return method
