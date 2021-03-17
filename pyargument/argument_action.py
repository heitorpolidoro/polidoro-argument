import argparse
import sys


class ArgumentAction(argparse.Action):
    def __init__(self, *args, method=None, **kwargs):
        self.method = method
        super(ArgumentAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        resp = self.method(*values)
        if resp is not None:
            print(resp)
        sys.exit(0)
