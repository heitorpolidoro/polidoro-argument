import os
import shutil
from string import Template

from helper import generate_tests

if not os.getcwd().endswith('/tests'):
    os.chdir('tests')

if os.path.exists('test_files'):
    shutil.rmtree('test_files')
os.mkdir('test_files')
os.chdir('test_files')

TESTS = 1  # tests per decorator

base_template = """
import re
import pytest
from polidoro_argument.argument_parser import ArgumentParser
${import_}


@pytest.fixture(autouse=True)
def clear_parser():
    ArgumentParser._parsers = {} 


${test_help}

${test_successful_call}
"""


def generate_test_files():
    count = 0
    for var_keyword in [False, True]:
        for n_keyword in range(3):
            for var_positional in [False, True]:
                for n_positional in range(3):
                    for decorator in ['Argument', 'Command']:
                        method_name = generate_method_name(
                            decorator,
                            n_positional,
                            var_positional,
                            n_keyword,
                            var_keyword
                        )
                        import_ = 'from polidoro_argument.%s import %s' % (decorator.lower(), decorator)

                        with open(method_name, 'w') as arq:
                            template = Template(base_template).safe_substitute(
                                import_=import_,
                                test_help=test_help_template(decorator),
                                test_successful_call=test_help_template(decorator),
                            )

                            template = Template(template).safe_substitute(
                                method=method_template()
                            )

                            template = Template(template).substitute(
                                decorator=decorator,
                                method_name=decorator.lower(),
                                help='This is the help',
                                arguments_signature=generate_arguments_signature(
                                    n_positional,
                                    var_positional,
                                    n_keyword,
                                    var_keyword
                                ),
                                arguments_call='arguments_call',
                            )
                            print(template)

                    count += 1
                    if TESTS == count:
                        return


def generate_method_name(decorator, qtde_args, n_args, qtde_kwargs, n_kwargs):
    def _args(str, qtde, n, ):
        _name = []
        if qtde > 0:
            _name.append('%d_%s' % (qtde, str))
            if qtde > 1:
                _name[-1] += 's'

        if n:
            _name.append('var_%s' % str)
        return _name

    args_name = _args('positional', qtde_args, n_args)
    args_name.extend(_args('keyword', qtde_kwargs, n_kwargs))

    if not args_name:
        args_name = ['no_arguments']
    elif len(args_name) > 1:
        args_name.insert(-1, 'and')

    return '_'.join([
                        decorator.title(),
                        'with'
                    ] + args_name)


def test_help_template(decorator):
    test_help = """
def test_${decorator}_help(capsys):
    parser = ArgumentParser(prog='test${decorator}')
${method}
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args('${decorator} ${arguments_call}'.split())
    assert exit_info.value.code == 0

    output = capsys.readouterr().out
    assert 'usage: ${decorator} [-h]' == output.split('\\n')[0]    
"""
    return test_help


def method_template():
    return """
    @${decorator}(help='${help}')
    def ${method_name}(${arguments_signature}):
        print('${method_name} called')
        return ${arguments_signature}
    """


def generate_arguments_signature(n_positional, var_positional, n_keyword, var_keyword):
    signature = []

    for positional in range(1, n_positional + 1):
        signature.append('positional_%d' % positional)

    if var_positional:
        signature.append('*var_positional')

    for keyword in range(1, n_keyword + 1):
        signature.append('keyword_%d=None' % keyword)

    if var_keyword:
        signature.append('**var_keyword')

    return ', '.join(signature)


generate_test_files()

#
#
#
#
# test_usage = """
# def test_usage(capsys):
#     parser = ArgumentParser(prog='test${decorator}')
# ${method}
#     with pytest.raises(SystemExit) as exit_info:
#         parser.parse_args([])
#     assert exit_info.value.code == 0
#
#     out_err = capsys.readouterr()
#     output = re.sub(r'\\n *', ' ', out_err.out)
#     assert '${usage}' in output, "in:\\n%s\\nshould have %s" % (output, '${usage}')
# """
#
# test_successful_call = """
# def test_successful_call(capsys):
#     parser = ArgumentParser(prog='test${decorator}')
# ${method}
#     with pytest.raises(SystemExit) as exit_info:
#         parser.parse_args(${method_call}.split())
#     assert exit_info.value.code == 0
#
#     out_err = capsys.readouterr()
#     output = out_err.out
#     assert_str = "${decorator_name} ${method_name} called with these arguments: ${args_call}"
#     assert assert_str in output
# """
#
#
# def generate_argument_test_files(**kwargs):
#     test_help = """
# def test_help(capsys):
#     parser = ArgumentParser(prog='test${decorator}')
# ${method}
#     with pytest.raises(SystemExit) as exit_info:
#         parser.parse_args(['--help'])
#     assert exit_info.value.code == 0
#
#     out_err = capsys.readouterr()
#     output = out_err.out
#     assert re.search(r'${help_regex}', output, flags=re.DOTALL), "in:\\n%s\\nshould have %s" % (output, '${help}\\n')
# """
#     generate_test_files('Argument', test_usage, test_help, test_successful_call, **kwargs)
#
#
# def generate_command_test_files(**kwargs):
#     test_help = """
# def test_help(capsys):
#     parser = ArgumentParser(prog='test${decorator}')
# ${method}
#     with pytest.raises(SystemExit) as exit_info:
#         parser.parse_args(['--help'])
#     assert exit_info.value.code == 0
#
#     out_err = capsys.readouterr()
#     output = out_err.out
#     assert re.search(r'${help_regex}', output, flags=re.DOTALL), "in:\\n%s\\nshould have %s" % (output, '${help}\\n')
#
#     with pytest.raises(SystemExit) as exit_info:
#         parser.parse_args('${method_name} --help'.split())
#     assert exit_info.value.code == 0
#
#     out_err = capsys.readouterr()
#     output = out_err.out
#     assert re.search(r'${help_regex}', output, flags=re.DOTALL), "in:\\n%s\\nshould have %s" % (output, '${help}\\n')
# """
#     generate_test_files('Command', test_usage, test_help, test_successful_call, **kwargs)
#
#
# def generate_test_files(decorator, test_usage, test_help, test_successful_call, tests=0):
#     for test_case in generate_tests(decorator):
#         import_str = 'from polidoro_argument.%s import %s' % (decorator.lower(), decorator)
#         file_name = '_'.join([decorator.lower(), test_case.method_name, 'test.py'])
#         with open('test_files/' + file_name, 'w') as arq:
#             test_case_dict = {k: v for k, v in test_case.__dict__.items()}
#             template = Template(base_template).substitute(
#                 test_usage=test_usage,
#                 test_help=test_help,
#                 test_successful_call=test_successful_call,
#                 import_str=import_str,
#                 **test_case_dict
#             )
#             arq.write(Template(template).substitute(
#                 decorator=decorator,
#                 decorator_name=decorator,
#                 **test_case_dict
#             ))
#
#         tests -= 1
#         if tests == 0:
#             return
#
# # tests = 1
# # generate_argument_test_files(tests=tests)
# # generate_command_test_files(tests=tests)
