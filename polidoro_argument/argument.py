"""
Decorator to add an function/method as argument in parser
"""
from polidoro_argument.argument_action import ArgumentAction
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
        parser = ArgumentParser.get_parser()

        nargs_max, nargs_min, optional_params, required_params = ArgumentParser.get_params_info(method)
        if nargs_min == nargs_max:
            nargs = nargs_min
        else:
            nargs = '*'
        kwargs.update({
            'action': ArgumentAction,
            'method': method,
            'nargs_min': nargs_min,
            'nargs_max': nargs_max,
            'nargs': nargs,
            'metavar': tuple(required_params),
            'required_params': required_params,
            'optional_params': optional_params,
        })

        parser.add_argument('--' + method.__name__, **kwargs)

        return method
