import argparse
import sys


class ArgumentHelpFormatter(argparse.HelpFormatter):
    def _format_args(self, action, default_metavar):
        if action.nargs == '*':
            return 'batata'
        return super(ArgumentHelpFormatter, self)._format_args(action, default_metavar)


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
            for name, value in vars(namespace).items():
                if callable(value):

                    resp = value(*getattr(namespace, name + '_args', []), **getattr(namespace, name + '_kwargs', {}))
                    if resp is not None:
                        print(resp)
                    sys.exit(0)
