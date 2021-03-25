import os
import re
from string import Template

from tests.helper import generate_tests

template = """
import re
import pytest
from polidoro_argument.argument_parser import ArgumentParser
${import_str}

parser = ArgumentParser(prog='test')

@pytest.fixture(autouse=True)
def clear_parser():
    parser = ArgumentParser()
    parser.set_defaults(methods_to_run={})

${method}

def test_usage(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    output = re.sub(r'\\n *', ' ', out_err.out)
    assert '${usage}' in output, "in:\\n%s\\nshould have %s" % (output, '${usage}')


def test_help(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--help'])
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    output = out_err.out
    assert re.search(r'${help}', output, flags=re.DOTALL), "in:\\n%s\\nshould have %s" % (output, '${help}\\n')
    
    
def test_successful_call(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(${method_call}.split())
    assert exit_info.value.code == 0
    
    out_err = capsys.readouterr()
    output = out_err.out
    assert_str = "${method_name} called with these arguments: " + str(${args_call})
    assert assert_str in output
"""
decorator = 'Argument'
for test_case in generate_tests(decorator):
    import_str = 'from polidoro_argument.%s import %s' % (decorator.lower(), decorator)
    file_name = test_case.method_name.replace('method_with_', '') + '_test.py'
    if not os.getcwd().endswith('/tests'):
        file_name = '/tests/' + file_name

    with open(file_name, 'w') as arq:
        arq.write(Template(template).substitute(
            method=test_case.method,
            method_call=test_case.method_call,
            method_name=test_case.method_name,
            args_call=[re.sub(r'.*=', '', a) for a in test_case.args_call],
            usage=test_case.usage,
            help=test_case.help,
            arguments=test_case.arguments_to_print,
            import_str=import_str
        ))
