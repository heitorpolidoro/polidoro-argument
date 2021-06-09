import re
from argparse import SUPPRESS

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
    @Command(help='inner help')
    def inner_command():
        print('command!')

    @staticmethod
    @Argument
    def argument():
        print('argument!')

    @staticmethod
    @Command(help=SUPPRESS)
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
