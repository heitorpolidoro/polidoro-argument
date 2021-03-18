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

        parameters = {name: info for name, info in inspect.signature(method).parameters.items() if
                      not name.startswith('_')}
        required_parameters = []
        optional_parameters = []
        for name, info in parameters.items():
            if info.default == inspect._empty:
                required_parameters.append(name)
            else:
                optional_parameters.append(name)
        # nargs = number of arguments in method
        nargs_min = len(required_parameters)
        nargs_max = len(required_parameters + optional_parameters)
        metavar = tuple(parameters)
        if nargs_min == nargs_max:
            nargs = nargs_min
        else:
            nargs = '*'
            # metavar = ' '.join(required_parameters + ['[%s]' % opt_param for opt_param in optional_parameters])
        kwargs.update({
            'action': ArgumentAction,
            'method': method,
            'nargs_min': nargs_min,
            'nargs_max': nargs_max,
            'nargs': nargs,
            'metavar': metavar
        })

        parser.add_argument('--' + method.__name__, **kwargs)

        return method
