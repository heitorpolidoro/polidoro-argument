import argparse


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
            super(ArgumentParser, self).__init__(*args, **kwargs)

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
            super(ArgumentParser, self).parse_args(args, namespace)
