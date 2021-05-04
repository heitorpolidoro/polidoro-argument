import argparse

from polidoro_argument_3_X_old.argument_action import ArgumentAction


# noinspection PyProtectedMember
class ArgumentHelpFormatter(argparse.HelpFormatter):
    def _format_args(self, action, default_metavar):
        if isinstance(action, ArgumentAction) and action.nargs == '*':
            help_str = list(action.required_params)
            if action.generic_args_param:
                help_str.append('[%s ...]' % action.generic_args_param)
            for opt_param in action.optional_params:
                help_str.append('[%s=value]' % opt_param)
            return ' '.join(help_str)

        return super(ArgumentHelpFormatter, self)._format_args(action, default_metavar)

    def _format_action(self, action):
        if action.help == 'HIDE':
            return self._join_parts(self._format_action(subaction)
                                    for subaction in self._iter_indented_subactions(action))
        else:
            return super(ArgumentHelpFormatter, self)._format_action(action)
