"""
Test file
"""
import re

import pytest
from polidoro_argument import VERSION

from polidoro_argument.argument import Argument
from polidoro_argument.argument_parser import ArgumentParser
from polidoro_argument.command import Command


# @Argument
# def simple_with_2_args(arg1, arg2):
#     """ Command line argument with two arguments """
#     print('those are your args: %s %s' % (arg1, arg2))
#
#
# class ClassArgument:
#     """ Command line command class """
#
#     @staticmethod
#     @Argument
#     def argument_in_class():
#         """ Class command line argument """
#         print('argument_in_class')


@pytest.fixture(autouse=True)
def clean_scenario():
    Argument.arguments = []


def test_simple(capsys):
    assert VERSION == '3.0.0'
    @Argument
    def simple():
        """ Simple command line argument """
        print('simple')

    parser = ArgumentParser()
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code is None
    out_err = capsys.readouterr()
    assert '--simple' in out_err.out

    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args('--simple')

    print(out_err)
    out_err = capsys.readouterr()
    assert '--simple' in out_err.out


def test_simple_with_arg(capsys):
    @Argument
    def simple_with_arg(arg):
        """ Command line argument with one argument and help """
        print('this is your arg %s' % arg)

    parser = ArgumentParser()
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args()
    assert exit_info.value.code is None
    out_err = capsys.readouterr()
    print(out_err)
    assert '--simple_with_arg' in out_err.out
