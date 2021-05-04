import inspect

from polidoro_argument.action import ArgumentAction, CommandAction
from polidoro_argument.polidoro_argument_parser import PolidoroArgumentParser


class _Params(object):
    def __init__(self, method, **kwargs):
        self.method = method
        self.method_name = method.__name__
        self.kwargs = kwargs
        self.positional = []
        self.var_positional = None
        self.keyword = []
        self.var_keyword = None
        self.nargs = None
        self.added = False

        self.inspect_signature()

    def inspect_signature(self):
        for name, info in inspect.signature(self.method).parameters.items():
            if not name.startswith('_'):
                if info.kind == inspect.Parameter.VAR_POSITIONAL:
                    self.var_positional = name
                elif info.kind == inspect.Parameter.VAR_KEYWORD:
                    self.var_keyword = name
                elif info.default == info.empty:
                    self.positional.append(name)
                else:
                    self.keyword.append(name)

        nargs = len(self.positional)
        if self.var_positional or self.var_keyword:
            nargs = '%d+' % nargs
        elif self.keyword:
            nargs = '%d-%d' % (nargs, len(self.keyword))

        self.nargs = nargs


class _ArgumentParams(_Params):
    def add_argument(self, parser: PolidoroArgumentParser):
        # parser._subparsers._actions[1]._name_parser_map['name']
        parser.add_argument(
            '--' + self.method_name,
            action=ArgumentAction,
            method=self.method,
            nargs=self.nargs,
            positional=self.positional,
            var_positional=self.var_positional,
            keyword=self.keyword,
            var_keyword=self.var_keyword,
            **self.kwargs
        )


class _CommandParams(_Params):
    def add_command(self, parser: PolidoroArgumentParser):
        def get_subparsers(_parser):
            if parser.subparsers:
                return parser.subparsers
            return parser.add_subparsers()

        subparsers = get_subparsers(parser)
        sub_parser = subparsers.add_parser(
            self.method_name,
            prog='%s %s' % (parser.prog, self.method_name),
            **self.kwargs
        )

        if self.positional:
            self.kwargs.setdefault('metavar', ' '.join(self.positional))

        sub_parser.add_argument(
            'positional',
            action=CommandAction,
            method=self.method,
            nargs=self.nargs,
            positional=self.positional,
            var_positional=self.var_positional,
            keyword=self.keyword,
            var_keyword=self.var_keyword,
            **self.kwargs
        )

        for kw in self.keyword:
            sub_parser.add_argument('--' + kw)