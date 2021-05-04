import inspect
from argparse import ArgumentParser

from polidoro_argument import Command
from polidoro_argument.argument import Argument
from polidoro_argument.polidoro_argument_parser import PolidoroArgumentParser


@staticmethod
@Command(help='help')
def command():
    print('command!')


@staticmethod
@Argument
def argument():
    print('argument!')


class TestCLI(object):
    help = 'cli help'
    description = 'descri'

    @staticmethod
    @Command(help='inner help')
    def inner_command():
        print('command!')

    @staticmethod
    @Argument
    def argument():
        print('argument!')


parser = PolidoroArgumentParser()
# subparsers = parser.add_subparsers()
# p1 = subparsers.add_parser('1')
# p2 = subparsers.add_parser('2')
parser.parse_args()
print()
# parser.parse_args()
