import random
import re
from string import Template

TEMPLATE = """
@$decorator
def ${method_name}(${signature}):
    args_to_print = []
    for arg_to_print in ${arguments}:
        if isinstance(arg_to_print, tuple):
            args_to_print += arg_to_print
        elif isinstance(arg_to_print, dict):
            args_to_print += arg_to_print.values()
        else:
            args_to_print.append(arg_to_print)
    ${print_or_return}("${method_name} called with these arguments: " + str(args_to_print))
    """


class TestCase(object):
    def __init__(self, method_name, decorator, args):
        self.has_help = random.choice([True, False])
        self.method_name = method_name
        help_info = ('Help for %s' % method_name) if self.has_help else ''
        self.arguments_to_print = '[' + re.sub(r'[\'*=None]', '', ', '.join(args)) + ']'

        self.args = []
        self.kwargs = {}
        args_help = []
        self.args_call = []
        for arg in args:
            if arg.startswith('**'):
                self.kwargs['kwargs1'] = 'KWARGS1'
                self.kwargs['kwargs2'] = 'KWARGS2'
                self.args_call.append('kwargs1=TEST_KWARGS1')
                self.args_call.append('kwargs2=TEST_KWARGS2')
            elif arg.startswith('*'):
                args_help.append('[args ...]')
                self.args += ['ARGS1', 'ARGS2']
                self.args_call.append('TEST_ARGS1')
                self.args_call.append('TEST_ARGS2')
            elif arg.startswith('kw'):
                kwarg = arg.replace('=None', '')
                self.kwargs[kwarg] = kwarg.upper()
                args_help.append('[%s=value]' % kwarg)
                self.args_call.append('%s=%s' % (kwarg, kwarg.upper()))
            else:
                args_help.append(arg)
                self.args_call.append(arg.upper())
                self.args.append(arg.upper())

        self.method = Template(TEMPLATE).substitute(
            decorator=decorator + '(help="%s")' % help_info,
            method_name=method_name,
            signature=', '.join(args),
            arguments=self.arguments_to_print,
            print_or_return=random.choice(['print', 'return']))

        if decorator == 'Argument':
            self.usage = '[--%s%s]' % (method_name, ' ' + ' '.join(args_help) if args_help else '')
            self.help = ('--%s%s.*%s' % (method_name, ' ' + ' '.join(args_help) if args_help else '', help_info)).replace('[', '\[')
            self.method_call = '"--%s%s"' % (method_name, ' ' + ' '.join(self.args_call) if self.args_call else '')

    def __call__(self):
        exec(self.method)


def generate_tests(decorator):
    def generate_method_name(_qtde_args, _n_args, _qtde_kwargs, _n_kwargs):
        _args = generate_partial_method_name('arg', _qtde_args, _n_args)
        kwargs = generate_partial_method_name('kwarg', _qtde_kwargs, _n_kwargs)
        _method_name = 'method_with_'
        if _args and kwargs:
            return _method_name + _args + '_and_' + kwargs
        if _args or kwargs:
            return _method_name + _args + kwargs
        return _method_name + 'no_args'

    # noinspection PyPep8Naming
    def generate_partial_method_name(var, qtde, N):
        name = ''
        if qtde > 0:
            name = str(qtde)
        if N:
            if name:
                name += '_plus_'
            name += 'N'
        if name:
            name += '_' + var
        return name

    tests_cases = []
    for n_kwargs in [False, True]:
        for qtde_kwargs in range(3):
            for n_args in [False, True]:
                for qtde_args in range(3):
                    method_name = generate_method_name(qtde_args, n_args, qtde_kwargs, n_kwargs)
                    args = ['arg%d' % (qtde + 1) for qtde in range(qtde_args)]
                    if n_args:
                        args.append('*args')

                    args += ['kwarg%d=None' % (qtde + 1) for qtde in range(qtde_kwargs)]
                    if n_kwargs:
                        args.append('**kwargs')

                    tests_cases.append(TestCase(method_name, decorator, args))

    return tests_cases
