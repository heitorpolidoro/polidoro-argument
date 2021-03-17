import argparse
import inspect

from pyargument.argument_action import ArgumentAction


class ArgumentParser(argparse.ArgumentParser):
    _parser = None

    def __new__(cls, *args, **kwargs):
        if ArgumentParser._parser is None:
            return object.__new__(cls)
        return ArgumentParser._parser
    
    def __init__(self, *args, **kwargs):
        if ArgumentParser._parser is None:
            ArgumentParser._parser = super(ArgumentParser, self).__init__(*args, **kwargs)

    def add_argument(method_or_argparse=None, *args, **kwargs):

        if callable(method_or_argparse):
            method = method_or_argparse
            if ArgumentParser._parser is None:
                ArgumentParser._parser = ArgumentParser()

            parser = ArgumentParser._parser

            parameters = [p for p in inspect.signature(method).parameters if not p.startswith('_')]
            # nargs = number of arguments in method
            kwargs.update({
                'action': ArgumentAction,
                'method': method,
                'nargs': len(parameters)
            })
            if parameters:
                kwargs['metavar'] = ' '.join(parameters)

            parser.add_argument('--' + method.__name__, **kwargs)

        else:
            super(ArgumentParser, method_or_argparse).add_argument(*args, **kwargs)

    def parse_args(self, args=None, namespace=None):
        if args is None:
            self.print_usage()
            self.exit()
        else:
            super(ArgumentParser, self).parse_args(args, namespace)
