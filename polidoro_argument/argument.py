"""
Decorator to add an function/method as argument in parser
"""
from polidoro_argument.argument_parser import ArgumentParser


class Argument(object):
    def __new__(cls, method=None, **kwargs):
        if callable(method):
            # When the decorator has no arguments
            # noinspection PyTypeChecker
            return Argument._add_argument(method, **kwargs)
        else:
            # When the decorator has arguments
            def wrapper(_method):
                return Argument._add_argument(_method, **kwargs)

            return wrapper

    @staticmethod
    def _add_argument(method, **kwargs):
        """ Add the method as argument in parser, to be callas as --METHOD_NAME """
        if not hasattr(method, '__name__'):
            raise RuntimeError('The "method" must have the attribute "__name__"!')
        parser = ArgumentParser()

        kwargs.update(ArgumentParser.generate_argument_action_kwargs(method))
        parser.add_argument('--' + method.__name__, **kwargs)

        return method
