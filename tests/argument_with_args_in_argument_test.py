"""
Test file
"""
import re

import pytest

from pyargument import Argument, ArgumentParser

ArgumentParser._parser = None


@Argument(help="simple_with_args_in_argument help")
def simple_with_args_in_argument():
    print('simple_with_args_in_argument called')


parser = ArgumentParser()


def test_usage(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert '[--simple_with_args_in_argument]' in out_err.out


def test_help(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--help'])
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert re.match('.*--simple_with_args_in_argument[ \\n]+simple_with_args_in_argument help', out_err.out,
                    flags=re.DOTALL)


def test_call(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(['--simple_with_args_in_argument'])
    assert exit_info.value.code is 0

    out_err = capsys.readouterr()
    assert 'simple_with_args_in_argument called\n' == out_err.out
