"""
Decorator to add an function/method as command in parser
"""

from polidoro_argument import ArgumentParser, HIDE_HELP
from polidoro_argument.argument_method import ArgumentMethod


class Command(object):
    def __new__(cls, method=None, **kwargs):
        if callable(method):
            # When the decorator has no commands
            # noinspection PyTypeChecker
            return Command._add_command(method, **kwargs)
        else:
            # When the decorator has commands
            def wrapper(_method):
                return Command._add_command(_method, **kwargs)

            return wrapper

    @staticmethod
    def _add_command(method, **kwargs):
        """ Add the method as command in parser, to be callas as --METHOD_NAME """
        method_name = getattr(method, '__name__', None)
        if method_name is None:
            raise RuntimeError('The "method" must have the attribute "__name__"!')
        parser = ArgumentParser()

        argument_action_kwargs = ArgumentParser.generate_argument_action_kwargs(method)
        kwargs.setdefault('help', '')

        subparsers = parser.add_subparsers(help=HIDE_HELP, title="Commands", metavar='command')
        parser = subparsers.add_parser(
            method_name,
            prog='%s %s' % (parser.prog, method_name),
            parser_id=method_name,
            **kwargs
        )
        parser.set_defaults(methods_to_run={method_name: ArgumentMethod(method)})

        # generic args e kwargs

        generic_args_param = argument_action_kwargs['generic_args_param']
        if generic_args_param:
            parser.add_argument('arguments', nargs='*')
        else:
            required_params = argument_action_kwargs['required_params']
            if required_params:
                parser.add_argument('arguments', nargs=len(required_params))

        for optional_param in argument_action_kwargs['optional_params']:
            parser.add_argument('--' + optional_param)

        generic_kwargs_param = argument_action_kwargs['generic_kwargs_param']
        if generic_kwargs_param:
            parser.set_defaults(generic_kwargs_param=generic_kwargs_param)
        # kwargs.update({
        #     'action': CommandAction,
        #     'method': method,
        #     'nargs_min': nargs_min,
        #     'nargs_max': nargs_max,
        #     'nargs': nargs,
        #     'metavar': tuple(required_params),
        #     'required_params': required_params,
        #     'optional_params': optional_params,
        # })
        #
        # parser.add_command('--' + method.__name__, **kwargs)


        return method
