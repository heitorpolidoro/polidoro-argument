"""
Test file
"""

import pytest

from polidoro_argument import Argument, ArgumentParser

ArgumentParser._parser = None


@Argument
def simple():
    return 'simple called'


parser = ArgumentParser()


def test_usage(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert '[--simple]' in out_err.out


def test_help(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--help'])
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert '--simple\n' in out_err.out


def test_call(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--simple'])
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert 'simple called\n' == out_err.out
