import re

import pytest

from polidoro_argument import Command, Argument, PolidoroArgumentParser

parser = None


@pytest.fixture(scope="module", autouse=True)
def setup():
    global parser
    parser = PolidoroArgumentParser(prog='testManual')


class TestCLI(object):
    help = 'cli help'
    description = 'description'

    @staticmethod
    @Command(
        help='inner help',
        aliases=['ic'],
        arguments_help={'arg1': 'Arg1 help', 'kwarg1': 'Kwarg1 Help'},
        arguments_aliases={'kwarg1': 'kw', 'arg1': ['a', 'r']}
    )
    def inner_command(arg1, arg2, kwarg1=None):
        print('command!')

    @staticmethod
    @Argument
    def argument():
        print('argument!')

    @staticmethod
    @Command
    def default_command(*remainder):
        if remainder:
            print('with remainders:', *remainder)
        else:
            print('without remainders')


def test_description(capsys):
    with pytest.raises(SystemExit) as exit_info:
        # noinspection PyUnresolvedReferences
        parser.parse_args('testcli --help'.split())
    assert exit_info.value.code == 0

    output = capsys.readouterr().out
    assert re.search(r'usage: testManual testcli.*\n\ndescription\n\n', output, flags=re.DOTALL), output


def test_help_command_alias(capsys):
    with pytest.raises(SystemExit) as exit_info:
        # noinspection PyUnresolvedReferences
        parser.parse_args('testcli --help'.split())
    assert exit_info.value.code == 0

    output = capsys.readouterr().out
    assert 'inner_command (ic)' in output


def test_default_command_help(capsys):
    with pytest.raises(SystemExit) as exit_info:
        # noinspection PyUnresolvedReferences
        parser.parse_args('testcli --help'.split())
    assert exit_info.value.code == 0

    output = capsys.readouterr().out
    assert 'default_command' not in output


def test_help_command_help_alias(capsys):
    with pytest.raises(SystemExit) as exit_info:
        # noinspection PyUnresolvedReferences
        parser.parse_args('testcli ic --help'.split())
    assert exit_info.value.code == 0

    output = capsys.readouterr().out
    assert re.search(r'--kwarg1.*--kw', output, flags=re.DOTALL), output


def test_default_command_without_remainders(capsys):
    # noinspection PyUnresolvedReferences
    parser.parse_args(['testcli'])

    output = capsys.readouterr().out
    assert 'without remainders\n' == output


def test_default_command_with_remainders(capsys):
    # noinspection PyUnresolvedReferences
    parser.parse_args('testcli default'.split())

    output = capsys.readouterr().out
    assert 'with remainders: default\n' == output
