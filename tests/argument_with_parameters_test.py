"""
Test file
"""
import re

import pytest

from polidoro_argument import Argument, ArgumentParser

ArgumentParser._parser = None


@Argument
def simple_with_one_arg(arg1):
    print('simple_with_one_arg called, arg: %s' % arg1)


@Argument
def simple_with_args(arg1, arg2, optional1=None, optional2=None):
    print(
        'simple_with_args called, args: %s, %s' % (arg1, arg2) +
        (', %s' % optional1 if optional1 else '') +
        (', %s' % optional2 if optional2 else ''))


parser = ArgumentParser()


def test_usage(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert '[--simple_with_one_arg arg1]' in out_err.out
    assert re.match(r'.*\[--simple_with_args.*arg1.*arg2.*\[optional1].*\[optional2]]\n',
                    out_err.out,
                    re.DOTALL)


def test_help(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--help'])
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert '--simple_with_one_arg arg1\n' in out_err.out
    assert '--simple_with_args arg1 arg2 [optional1] [optional2]\n' in out_err.out


def test_call_without_passing_arg(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--simple_with_one_arg'])
    assert exit_info.value.code == 2

    out_err = capsys.readouterr()
    assert 'error: argument --simple_with_one_arg: expected 1 argument' in out_err.err


def test_call_without_passing_all_args(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args('--simple_with_args TEST_ARG1'.split())
    assert exit_info.value.code == 2

    out_err = capsys.readouterr()
    assert 'error: argument --simple_with_args: expected 2-4 arguments' in out_err.err


def test_call_passing_all_args(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args('--simple_with_one_arg TEST_ARG1'.split())
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert 'simple_with_one_arg called, arg: TEST_ARG1\n' == out_err.out


def test_call_without_passing_optional_args(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args('--simple_with_args TEST_ARG1 TEST_ARG2'.split())
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert 'simple_with_args called, args: TEST_ARG1, TEST_ARG2\n' == out_err.out


def test_call_passing_optional_args(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args('--simple_with_args TEST_ARG1 TEST_ARG2 TEST_OPT'.split())
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert 'simple_with_args called, args: TEST_ARG1, TEST_ARG2, TEST_OPT\n' == out_err.out
