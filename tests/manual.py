# class TestCLI(object):
# @Command(help='help')
# @Command
# def command():
#     pass
import inspect
from argparse import ArgumentParser

from polidoro_argument.argument import Argument
from polidoro_argument.polidoro_argument_parser import PolidoroArgumentParser


@Argument
def argument():
    return b


for name, info in inspect.signature(argument).parameters.items():
    print(name, info.kind, info.default, info.empty)
# argument(1, 2, b=3)
# @Command
# def test(arg1, arroz=None, **kwargs):
#     print(arg1, arroz, kwargs)


# @Argument
# def args1(arg1, arg2, optional=None):
#     print('simple_with_args called, args: %s, %s' % (arg1, arg2) + (', %s' % optional if optional else ''))
#
#
# @Argument
# def args2(arg1, arg2, optional=None):
#     print('simple_with_args called, args: %s, %s' % (arg1, arg2) + (', %s' % optional if optional else ''))

parser = PolidoroArgumentParser()
# subparsers = parser.add_subparsers()
# p1 = subparsers.add_parser('1')
# p2 = subparsers.add_parser('2')
parser.parse_args()
print()
# parser.parse_args()
