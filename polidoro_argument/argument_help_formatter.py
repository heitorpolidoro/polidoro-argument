import argparse

from polidoro_argument.argument_action import ArgumentAction


class ArgumentHelpFormatter(argparse.HelpFormatter):
    def _format_args(self, action, default_metavar):
        if isinstance(action, ArgumentAction) and action.nargs == '*':
            help_str = list(action.required_params)
            if action.generic_args_param:
                help_str.append('[%s ...]' % action.generic_args_param)
            for opt_param in action.optional_params:
                help_str.append('[%s=value]' % opt_param)
            return ' '.join(help_str)

        # noinspection PyProtectedMember
        return super(ArgumentHelpFormatter, self)._format_args(action, default_metavar)
