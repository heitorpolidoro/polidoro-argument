"""
Test file
"""

import pytest

from polidoro_argument import Argument, ArgumentParser

ArgumentParser._parser = None


@Argument
def simple():
    return 'simple called'


@Argument
def simple2():
    return 'simple2 called'


parser = ArgumentParser()


def test_usage(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert '[--simple]' in out_err.out


def test_help(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--help'])
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert '--simple\n' in out_err.out


def test_call(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--simple'])
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert 'simple called\n' == out_err.out


def test_call_order(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--simple', '--simple2'])
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert 'simple called\nsimple2 called\n' == out_err.out


def test_call_order(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--simple2', '--simple'])
    assert exit_info.value.code == 0

    out_err = capsys.readouterr()
    assert 'simple2 called\nsimple called\n' == out_err.out
