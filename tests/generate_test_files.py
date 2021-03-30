import os
from string import Template

from helper import generate_tests


base_template = """
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
${test_usage}

def test_help(capsys):
${test_help}

def test_successful_call(capsys):
${test_successful_call}
"""


def generate_argument_test_files():
    test_usage = """
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    output = re.sub(r'\\n *', ' ', out_err.out)
    assert '${usage}' in output, "in:\\n%s\\nshould have %s" % (output, '${usage}')
    """

    test_help = """
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--help'])
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    output = out_err.out
    assert re.search(r'${help_regex}', output, flags=re.DOTALL), "in:\\n%s\\nshould have %s" % (output, '${help}\\n')
    """
    
    test_successful_call = """
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(${method_call}.split())
    assert exit_info.value.code == 0
    
    out_err = capsys.readouterr()
    output = out_err.out
    assert_str = "${method_name} called with these arguments: " + str(${args_call})
    assert assert_str in output
    """
    generate_test_files('Argument', test_usage, test_help, test_successful_call)


def generate_test_files(decorator, test_usage, test_help, test_successful_call):
    for test_case in generate_tests(decorator):
        import_str = 'from polidoro_argument.%s import %s' % (decorator.lower(), decorator)
        file_name = '_'.join([decorator.lower(), test_case.method_name, 'test.py'])
        if not os.getcwd().endswith('/tests'):
            file_name = 'tests/' + file_name

        with open(file_name, 'w') as arq:
            test_case_dict = {k: v for k, v in test_case.__dict__.items()}
            template = Template(base_template).substitute(
                test_usage=test_usage,
                test_help=test_help,
                test_successful_call=test_successful_call,
                import_str=import_str,
                **test_case_dict
            )
            arq.write(Template(template).substitute(
                **test_case_dict
            ))


generate_argument_test_files()
