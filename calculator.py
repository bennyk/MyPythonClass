
from types import FunctionType

def bindAddToRightOf(lhs):
    def _(rhs):
        if isinstance(lhs, str) and isinstance(rhs, str):
            def __(a, b):
                return a + b
            print("<=", lhs, '+', rhs)
            return __

        if isinstance(rhs, FunctionType):
            def __(*args):
                return args[0] + rhs(*args[1:])
            print("<=", lhs, '+ func')
            return __

        if isinstance(rhs, str):
            def __(a1):
                return lhs + a1
            print("<=", lhs, '+', rhs)
            return __

        if isinstance(lhs, int):
            result = lhs + rhs
            print("<=", result, '=', lhs, '+', rhs)
            return result

        if isinstance(lhs, str):
            def __(a1):
                return a1 + rhs

            print("<=", lhs, '+', rhs)
            return __

        assert False, "invalid condition"

    return _

# x = bindAddToRightOf(5)
# y = bindAddToRightOf(2)
# print(x(y(3)))

import re
def parse(expr):
    m1 = re.match(r"(\d+)(\+)", expr)
    if m1 is not None:
        x = int(m1.group(1))
        f = bindAddToRightOf(x)
        return f(parse(expr[m1.end():]))

    m2 = re.match(r"([A-Za-z])(\+)", expr)
    if m2 is not None:
        x = m2.group(1)
        f = bindAddToRightOf(x)
        return f(parse(expr[m2.end():]))

    m3 = re.match(r"(\d+)", expr)
    if m3 is not None:
        return int(m3.group(1))

    m4 = re.match(r"([A-Za-z])", expr)
    if m4 is not None:
        return m4.group(1)

    assert False, "invalid condition"


# print(parse("1+2+3"))

# print(parse('x+1+2')(1))
# print(parse('1+2+x')(1))
# print(parse('x+y+z')(1, 2, 3))


def g(a, b):
    print(a, b)
def f(*args):
    print(args, g(*args[1:]))

# f(1,2,3)