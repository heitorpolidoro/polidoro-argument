import argparse
import inspect
import sys

from polidoro_argument.argument_help_formatter import ArgumentHelpFormatter


class ArgumentParser(argparse.ArgumentParser):
    _parser = None

    def __new__(cls, *args, **kwargs):
        # Only create new if the class parsers does not exists
        if ArgumentParser._parser is None:
            return object.__new__(cls)
        return ArgumentParser._parser

    def __init__(self, *args, **kwargs):
        # Only initialize the parser if the class parsers does not exists
        if ArgumentParser._parser is None:
            super(ArgumentParser, self).__init__(*args, formatter_class=ArgumentHelpFormatter, **kwargs)

    @staticmethod
    def get_parser():
        if ArgumentParser._parser is None:
            ArgumentParser._parser = ArgumentParser()

        return ArgumentParser._parser

    def parse_args(self, args=None, namespace=None):
        # If there is no argument, print usage
        if args is None and not sys.argv[1:]:
            self.print_usage()
            self.exit()
        else:
            namespace = argparse.Namespace()
            setattr(namespace, 'methods_to_run', {})
            namespace = super(ArgumentParser, self).parse_args(args, namespace)
            if namespace.methods_to_run.values():
                for argument_method in sorted(namespace.methods_to_run.values(), key=lambda arg_method: arg_method.order):
                    resp = argument_method()
                    if resp is not None:
                        print(resp)
                sys.exit(0)

            return namespace

    @staticmethod
    def get_params_info(method):
        parameters = {name: info for name, info in inspect.signature(method).parameters.items()
                      if not name.startswith('_')}
        required_params = []
        optional_params = []
        for name, info in parameters.items():
            # noinspection PyUnresolvedReferences,PyProtectedMember
            if info.default == inspect._empty:
                required_params.append(name)
            else:
                optional_params.append(name)
        # nargs = number of arguments in method
        nargs_min = len(required_params)
        nargs_max = len(required_params + optional_params)
        return nargs_max, nargs_min, optional_params, required_params

