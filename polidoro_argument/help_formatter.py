"""
HelpFormatter to adapt to arguments
"""
# noinspection PyUnresolvedReferences,PyProtectedMember
from argparse import HelpFormatter, SUPPRESS, _SubParsersAction

from polidoro_argument.action import _Action


# noinspection PyProtectedMember
class ArgumentHelpFormatter(HelpFormatter):
    def _format_args(self, action, default_metavar):
        if isinstance(action, _Action):
            args = action.positional[:]

            if isinstance(action.nargs, str):
                if action.var_positional:
                    args.append('[%s [%s ...]]' % ((action.var_positional, ) * 2))

                if action.keyword:
                    args.extend('[%s=VALUE]' % p for p in action.keyword)

                if action.var_keyword:
                    args.append('[%s=VALUE [%s=VALUE ...]]' % ((action.var_keyword, ) * 2))

            return ' '.join(args)

        else:
            return super(ArgumentHelpFormatter, self)._format_args(action, default_metavar)

    def _format_action_invocation(self, action):
        # To hide subparsers group help
        if isinstance(action, _SubParsersAction):
            return SUPPRESS
        if action.help == SUPPRESS:
            return SUPPRESS
        return super(ArgumentHelpFormatter, self)._format_action_invocation(action)

    def _join_parts(self, part_strings):
        # To hide subparsers group help
        return ''.join([part
                        for part in part_strings
                        if part and SUPPRESS not in part])

