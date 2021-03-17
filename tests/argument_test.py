"""
Test file
"""
import re

import pytest

from pyargument import Argument, ArgumentParser


@pytest.fixture(autouse=True)
def clean_scenario():
    ArgumentParser._parser = None


def test_simple_usage(capsys):
    @Argument
    def simple():
        """ Simple command line argument """
        print('simple')

    parser = ArgumentParser()
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert '[--simple]' in out_err.out


def test_simple_call(capsys):
    @Argument
    def simple():
        """ Simple command line argument """
        print('simple called')

    parser = ArgumentParser()
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--simple'])
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert 'simple called' in out_err.out


def test_simple_help(capsys):
    @Argument
    def simple():
        """ Simple command line argument """
        print('simple called')

    parser = ArgumentParser()
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--help'])
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert '--simple\n' in out_err.out


def test_simple_usage_with_args_in_argument_decorator(capsys):
    @Argument(help="simple help")
    def simple():
        """ Simple command line argument """
        print('simple')

    parser = ArgumentParser()
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert '[--simple]' in out_err.out


def test_simple_call_with_args_in_argument_decorator(capsys):
    @Argument(help="simple help")
    def simple():
        """ Simple command line argument """
        print('simple called')

    parser = ArgumentParser()
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--simple'])
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert 'simple called' in out_err.out


def test_simple_help_with_args_in_argument_decorator(capsys):
    @Argument(help="simple help")
    def simple():
        """ Simple command line argument """
        print('simple called')

    parser = ArgumentParser()
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--help'])
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert re.match('.*--simple +simple help', out_err.out, flags=re.DOTALL)
