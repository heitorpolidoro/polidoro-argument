import argparse
import sys

from polidoro_argument.argument_method import ArgumentMethod


class ArgumentAction(argparse.Action):
    def __init__(self,
                 *,
                 method,
                 nargs_min,
                 nargs_max,
                 required_params,
                 optional_params,
                 **kwargs):

        self.method = method
        self.nargs_min = nargs_min
        self.nargs_max = nargs_max
        self.required_params = required_params
        self.optional_params = optional_params
        super(ArgumentAction, self).__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if self.nargs_min is not None and len(values) < self.nargs_min or \
                self.nargs_max is not None and len(values) > self.nargs_max:
            nargs = [str(value) for value in [self.nargs_min, self.nargs_max] if value is not None]
            error_message = 'error: argument --%s: expected %s arguments\n' % (self.method.__name__, '-'.join(nargs))
            sys.stderr.write(error_message)
            sys.exit(2)

        namespace.methods_to_run[self.dest] = ArgumentMethod(self.method, values)
