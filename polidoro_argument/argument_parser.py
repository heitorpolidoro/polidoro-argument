import argparse
import inspect
import sys

from polidoro_argument.argument_action import ArgumentAction
from polidoro_argument.argument_help_formatter import ArgumentHelpFormatter


class ArgumentParser(argparse.ArgumentParser):
    _parsers = {}

    def __new__(cls, *args, parser_id=None, **kwargs):
        # Only create new if the class parsers does not exists
        if parser_id not in ArgumentParser._parsers:
            return object.__new__(cls)

        return ArgumentParser._parsers[parser_id]

    def __init__(self, *args, parser_id=None, **kwargs):
        # Only initialize the parser if the class parsers does not exists
        if parser_id not in ArgumentParser._parsers:
            super(ArgumentParser, self).__init__(*args, formatter_class=ArgumentHelpFormatter, **kwargs)
            ArgumentParser._parsers[parser_id] = self

    def parse_args(self, args=None, namespace=None):
        namespace = super(ArgumentParser, self).parse_args(args=args, namespace=namespace)
        namespace_dict = namespace.__dict__
        methods_to_run = namespace_dict.pop('methods_to_run')
        if methods_to_run:
            call_args = namespace_dict.pop('arguments', [])
            call_kwargs = namespace_dict

            for argument_method in sorted(methods_to_run.values(), key=lambda arg_method: arg_method.order):
                resp = argument_method(*call_args, **call_kwargs)
                if resp is not None:
                    print(resp)
            sys.exit(0)

        self.print_usage()
        self.exit()

    def parse_known_args(self, args=None, namespace=None):
        if self.get_default('methods_to_run') is None:
            self.set_defaults(methods_to_run={})
        namespace, args = super(ArgumentParser, self).parse_known_args(args, namespace)
        generic_kwargs_param = getattr(namespace, 'generic_kwargs_param', None)
        if generic_kwargs_param:
            delattr(namespace, 'generic_kwargs_param')
            for arg in list(args):
                name, _, value = arg.partition('=')
                if value:
                    setattr(namespace, name, value)
                    args.remove(arg)
        return namespace, args

    @staticmethod
    def generate_argument_action_kwargs(method):
        kwargs = {}
        parameters = {name: info for name, info in inspect.signature(method).parameters.items()
                      if not name.startswith('_')}
        required_params = []
        optional_params = []
        nargs_min = 0
        nargs_max = 0
        generic_args_param = None
        generic_kwargs_param = None
        for name, info in parameters.items():
            if info.kind in [
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
                inspect.Parameter.POSITIONAL_ONLY
            ]:
                # noinspection PyProtectedMember,PyUnresolvedReferences
                if info.default == inspect._empty:
                    required_params.append(name)
                    nargs_min += 1
                    if nargs_max < sys.maxsize:
                        nargs_max += 1
                else:
                    optional_params.append(name)
                    if nargs_max < sys.maxsize:
                        nargs_max += 1

            elif info.kind == inspect.Parameter.VAR_POSITIONAL:
                generic_args_param = name
                nargs_max = sys.maxsize

            elif info.kind == inspect.Parameter.VAR_KEYWORD:
                generic_kwargs_param = name
                nargs_max = sys.maxsize

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
            'generic_args_param': generic_args_param,
            'generic_kwargs_param': generic_kwargs_param,
        })
        return kwargs
