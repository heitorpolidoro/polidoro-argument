"""
Decorator to add an function/method as argument in parser
"""

import inspect

from pyargument import ArgumentAction, ArgumentParser


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
        if not hasattr(method, '__name__'):
            raise RuntimeError('The "method" must have the attribute "__name__"!')
        """ Add the method as argument in parser, to be callas as --METHOD_NAME """
        parser = ArgumentParser.get_parser()

        parameters = [p for p in inspect.signature(method).parameters if not p.startswith('_')]
        # nargs = number of arguments in method
        kwargs.update({
            'action': ArgumentAction,
            'method': method,
            'nargs': len(parameters)
        })
        if parameters:
            kwargs['metavar'] = ' '.join(parameters)

        parser._add_argument('--' + method.__name__, **kwargs)

        return method
