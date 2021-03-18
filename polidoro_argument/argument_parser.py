import argparse
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
        if args is None:
            self.print_usage()
            self.exit()
        else:
            namespace = super(ArgumentParser, self).parse_args(args, namespace)
            arguments = {name: value for name, value in vars(namespace).items() if isinstance(value, tuple)}
            for name, value in sorted(arguments.items(), key=lambda item: item[1]):
                _, method, m_args = value
                resp = method(*m_args)
                if resp is not None:
                    print(resp)
                sys.exit(0)
