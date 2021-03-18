import argparse
import sys


class ArgumentAction(argparse.Action):
    def __init__(self, *args, method=None, nargs_min=None, nargs_max=None, **kwargs):
        self.method = method
        self.nargs_min = nargs_min
        self.nargs_max = nargs_max
        super(ArgumentAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if self.nargs_min is not None and len(values) < self.nargs_min or \
                self.nargs_max is not None and len(values) > self.nargs_max:
            nargs = [str(value) for value in [self.nargs_min, self.nargs_max] if value is not None]
            error_message = 'error: argument --simple_with_args: expected %s arguments' % ('-'.join(nargs))
            sys.stderr.write(error_message)
            sys.exit(2)
        setattr(namespace, self.dest, self.method)
        setattr(namespace, self.dest + '_args', values)
        # resp = self.method(*values)
        # if resp is not None:
        #     print(resp)
        # sys.exit(0)
