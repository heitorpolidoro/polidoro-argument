import inspect
from argparse import SUPPRESS

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

    @staticmethod
    def get_final_parser(parser, method):
        full_name = method.__qualname__.replace('setup.<locals>.', '')
        for name in [n.lower() for n in reversed(full_name.split('.')[:-1])]:
            subparsers = _Params.get_subparsers(parser)
            sub_parser = subparsers.choices.get(name, None)
            if sub_parser is None:
                clazz = _Params.get_class_that_defined_object(method)
                clazz_attrs = {k: v for k, v in clazz.__dict__.items() if not k.startswith('__') and not isinstance(v, staticmethod)}
                sub_parser = subparsers.add_parser(
                    name,
                    prog='%s %s' % (parser.prog, name),
                    **clazz_attrs
                )
            parser = sub_parser

        return parser

    @staticmethod
    def get_subparsers(parser):
        if parser.subparsers:
            return parser.subparsers
        return parser.add_subparsers()

    @staticmethod
    def get_class_that_defined_object(obj):
        """
        :param obj: The object to get the classe
        :return: the class that define the object
        """

        if inspect.ismethod(obj):
            for cls in inspect.getmro(obj.__self__.__class__):
                if cls.__dict__.get(obj.__name__) is obj:
                    return cls
            obj = obj.__func__  # fallback to __qualname__ parsing
        if inspect.isfunction(obj):
            cls = getattr(inspect.getmodule(obj),
                          obj.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
            if isinstance(cls, type):
                return cls
        return getattr(obj, '__objclass__', None)



class _ArgumentParams(_Params):
    def add_argument(self, parser: PolidoroArgumentParser):
        parser = self.get_final_parser(parser, self.method)
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
        parser = self.get_final_parser(parser, self.method)
        subparsers = self.get_subparsers(parser)
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