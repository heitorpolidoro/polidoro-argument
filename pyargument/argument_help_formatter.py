import argparse

from pyargument import ArgumentAction


class ArgumentHelpFormatter(argparse.HelpFormatter):
    def _format_args(self, action, default_metavar):
        if isinstance(action, ArgumentAction) and action.nargs == '*':
            return ' '.join(
                action.required_parameters + ['[%s]' % opt_param for opt_param in action.optional_parameters])
        return super(ArgumentHelpFormatter, self)._format_args(action, default_metavar)
