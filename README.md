# Polidoro Argument [![Latest](https://img.shields.io/github/release/heitorpolidoro/argument.svg?label=latest)](https://github.com/heitorpolidoro/argument/releases/latest)
Package to simplify creating command line arguments for scripts in Python.

#### How to use:

- Decorate the method you want to create an argument from with `@Argument`.
- Decorate the method you want to call from command line with `@Command`.
- Create a `PolidoroArgumentParser` 
- Call `parser.parse_args()`

All keywords arguments to `@Argument` and `@Command` are the same as in [argparse.ArgumentParser.add_argument](https://docs.python.org/3.7/library/argparse.html#the-add-argument-method) except for 'action' and 'nargs'.
'action' is a custom Action created to run the decorated method and 'nargs' is the number of parameters in the decorated method.

###### Examples:
foo.py
```

from polidoro_argument import Argument, PolidoroArgumentParser

@Argument
def bar():
    print('hi')
    
parser = ArgumentParser()
parser.parse_args()
```
Result:
```
$ python foo.py --bar
hi 
```

You can pass argument to the method
```
@Argument
def bar(baz=None):
    print(baz)
```
```
$ python foo.py --bar Hello
Hello
```
To create commands
```
@Command
def command():
    print('this is a command')
```
```
$ python foo.py command
this is a command
```
With arguments
```
@Command
def command_with_arg(arg, arg1=None):
    print('this the command arg: %s, arg1: %s' % (arg, arg1))
```
```
$ python foo.py command_with_arg Hello
this the command arg: Hello, arg1: None
$ python foo.py command_with_arg Hello --arg1 World
this the command arg: Hello, arg1: World
```
Using a Class
```
class ClassCommand:
    @staticmethod
    @Argument
    def argument_in_class():
        print('argument_in_class called')

    @staticmethod
    @Command
    def command_in_class(arg='Oi'):
        print('command_in_class called. arg=%s' % arg)
```
```
$ python foo.py classcommand --argument_in_class
argument_in_class called
$ python foo.py classcommand command_in_class
command_in_class called. arg=Oi
$ python foo.py classcommand command_in_class --arg=Ola
command_in_class called. arg=Ola
```



