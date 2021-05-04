"""
Decorator to add an function/method as argument in parser
"""

from polidoro_argument.params import _CommandParams


class Command(object):
    _commands = []

    def __new__(cls, method=None, **kwargs):
        if callable(method):
            # When the decorator has no arguments
            Command._commands.append(_CommandParams(method, **kwargs))
            return method
        else:
            # When the decorator has arguments
            def wrapper(_method):
                Command._commands.append(_CommandParams(_method, **kwargs))
                return _method

            return wrapper

    @staticmethod
    def get_command(item):
        for c in Command._commands:
            if item in [c.method_name, c.method]:
                return c
