
class Foo:
    classvar = 123

    def instanceMethod(self):
        pass

    @classmethod
    def staticMethod(cls):
        pass

def func():
    pass

print(func)
print(Foo)
print(Foo.classvar)
print(Foo.instanceMethod)
print(Foo.staticMethod)
a = Foo()
print(a.instanceMethod)


def closure(a):
    def inner():
        return a
    return inner


print(closure(3))

import sys

def trace(f):
    f.indent = 0
    def g(x):
        print('|  ' * f.indent + '|--', f.__name__, x)
        f.indent += 1
        value = f(x)
        print('|  ' * f.indent + '|--', 'return', repr(value))
        f.indent -= 1
        return value
    # register name of f to interpreter
    # setattr(sys.modules[__name__], f.__name__, g)
    return g

@trace
def fib(n):
    if n is 0 or n is 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# fib = trace(fib)
print(fib(4))

import functools

def trace(class_):
    original_init = class_.__init__
    def __init__(self, *args, **kws):
        print("Instantiating an object of class {}".format(class_.__name__))
        original_init(self, *args, **kws)
    class_.__init__ = __init__
    return class_

@trace
class Foo(object):
    def __init__(self, value):
        self.value = value

foo = Foo(5)
print("The value of foo is {}".format(foo.value))

