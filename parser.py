import re
import collections.abc
from calculator2 import Number, Variable, Vector2, Functor

class Tokenizer:
    def __init__(self, expr):
        assert isinstance(expr, str)
        self._str = expr
        self._start = 0
        self._prev = 0
        self._token = None
        self._prevToken = None

        self._prevprev = None
        self._prevprevToken = None

    def __iter__(self):
        return self

    def getRemainingString(self):
        return self._str[self._start:]
    remainingString = property(getRemainingString)

    def getCurrentLiteral(self):
        return self._str[self._prev:self._start]
    currentLiteral = property(getCurrentLiteral)

    def getCurrentToken(self):
        return self._token
    currentToken = property(getCurrentToken)

    def getPrevToken(self):
        return self._prevToken
    prevToken = property(getPrevToken)

    def rewind(self):
        assert self._prevprev is not None
        self._start = self._prev
        self._prev = self._prevprev
        self._token = self._prevToken
        self._prevToken = self._prevprevToken

    def savePrev(self):
        self._prevprev = self._prev
        self._prevprevToken = self._prevToken

    def __next__(self):
        if len(self.remainingString) <= 0:
            raise StopIteration

        m = None
        result = None
        while len(self.remainingString) > 0:
            m = re.match(r"\s+", self.remainingString)
            if m is not None:
                self._start += m.end()
                continue

            m = re.match(r"(\d+)", self.remainingString)
            if m is not None:
                result = Number(int(m.group(1)))
                break

            m = re.match(r"([A-Za-z])", self.remainingString)
            if m is not None:
                result = Variable(m.group(1))
                break

            m = re.match(r"([\+\-\*\/\^])", self.remainingString)
            if m is not None:
                result = m.group(1)
                break

            m = re.match(r"([\(\);])", self.remainingString)
            if m is not None:
                result = m.group(1)
                break

            raise SyntaxError("invalid char at ^{}".format(self.remainingString))

        if m is not None:
            self.savePrev()
            self._prev = self._start
            self._prevToken = self._token
            self._token = result
            self._start += m.end()

        return result

if False:
    for x in Tokenizer(" 1 + 2+3+a"):
        print(x)

    print('---')
    t = Tokenizer(" 1 + 2+3")
    print(next(t))
    print(t.currentToken)
    print(next(t))
    print(t.currentToken)

from functools import singledispatch

@singledispatch
def accept(kind, tokenizer):
    assert isinstance(tokenizer, Tokenizer)
    if isinstance(tokenizer.currentToken, kind):
        next(tokenizer)
        return True
    return False

@accept.register(str)
def _(str, tokenizer):
    assert isinstance(tokenizer, Tokenizer)
    if str == tokenizer.currentLiteral:
        next(tokenizer)
        return True
    return False

@accept.register(tuple)
def _(tuplet, tokenizer):
    assert isinstance(tokenizer, Tokenizer)
    if tokenizer.currentLiteral in tuplet:
        next(tokenizer)
        return True
    return False

import operator
Operator = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '^' : operator.pow
}

def parseExpr(tokenizer):
    """
    implements E -> T { ( ‘+’ | ‘-’ ) E }
    """
    assert isinstance(tokenizer, Tokenizer)
    result = parseTerm(tokenizer)
    if accept(('+', '-'), tokenizer):
        apply = Operator[tokenizer.prevToken]
        expr1 = parseExpr(tokenizer)
        result = apply(result, expr1)

    return result

def parseTerm(tokenizer):
    """
    implements T -> F { ( ‘*’ | ‘/’ ) T }
    """
    assert isinstance(tokenizer, Tokenizer)

    result = parseFactor(tokenizer)
    if accept(('*', '/'), tokenizer):
        apply = Operator[tokenizer.prevToken]

        # {* /} T ...
        term = parseTerm(tokenizer)
        result = apply(result, term)

    return result

def parseFactor(tokenizer):
    """
    implements F -> L [ ‘^’ F ]
    """
    assert isinstance(tokenizer, Tokenizer)

    result = parseLiteral(tokenizer)

    if accept('^', tokenizer):
        apply = Operator[tokenizer.prevToken]

        # ^ factor
        factor = parseFactor(tokenizer)
        result = apply(result, factor)

    return result

def parseLiteral(tokenizer):
    """
    L -> var | digit | ‘(‘ E ‘)’ | ‘-’ T
    """
    assert isinstance(tokenizer, Tokenizer)

    if accept(Number, tokenizer):
        return tokenizer.prevToken

    if accept(Variable, tokenizer):
        return tokenizer.prevToken

    if accept('(', tokenizer):
        expr = parseExpr(tokenizer)
        if accept(')', tokenizer):
            return expr

    raise SyntaxError("syntax error at ^{}{} was expecting a factor"
                      .format(tokenizer.currentToken, tokenizer.remainingString))

def parse2(str):
    result = None
    try:
        tokenizer = Tokenizer(str + ';')
        next(tokenizer)
        result = parseExpr(tokenizer)

        if tokenizer.currentToken != ';':
            raise SyntaxError("syntax error at ^{}{}: expecting ;"
                              .format(tokenizer.currentLiteral, tokenizer.remainingString))

    except StopIteration:
        pass

    if len(tokenizer.remainingString) > 0:
        raise SyntaxError("syntax error at ^{}{} in expression"
                          .format(tokenizer.currentLiteral, tokenizer.remainingString))
    return result

count = 0

count += 1
assert parse2('1+2+3') == 6
print('ok {}'.format(count))

count += 1
assert parse2('1+2*3') == 7
print('ok {}'.format(count))

count += 1
assert parse2('3*(1+2)') == 9
print('ok {}'.format(count))

count += 1
assert parse2('((1+2)*3)*4') == 36
print('ok {}'.format(count))

count += 1
assert parse2('2*x+y')(x=2, y=3) == 7
print('ok {}'.format(count))

count += 1
assert parse2('2*x + y/3')(x=4, y=3) == 9
print('ok {}'.format(count))

count += 1
assert parse2('x*x*y')(x=4, y=2) == 32
print('ok {}'.format(count))

count += 1
assert parse2('x-2*y')(x=4, y=2) == 0
print('ok {}'.format(count))

count += 1
assert parse2('((1+x)*3)*4')(x=1) == 24
print('ok {}'.format(count))

count += 1
assert parse2('3 + x^3')(x=3) == 30
print('ok {}'.format(count))

def bezier3(t, a, b, c, d):
    return (1-t)**3*a + 3*(1-t)**2*t*b + 3*(1-t)*t**2*c + t**3*d

a = {'t' : 0.1,
     'a' : Vector2(120, 160),
     'b' : Vector2(35, 200),
     'c' : Vector2(220, 260),
     'd' : Vector2(220, 40)}
f = parse2('(1-t)^3*a + 3*(1-t)^2*t*b + 3*(1-t)*t^2*c + t^3*d')
assert f(**a) == bezier3(**a)

def arange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step

# test bezier curve in full range

def g(t):
    # print('t=', t)
    return f(t=t, a=Vector2(120, 160),
         b=Vector2(35, 200),
         c=Vector2(220, 260),
         d=Vector2(220, 40))
for x in map(g, arange(0, 1, 0.1)):
    print(x)

count += 1
try:
    parse2('1+2++3')
except SyntaxError as e:
    print(e)
    print('ok {}'.format(count))

count += 1
try:
    parse2('1+2^3')
except SyntaxError as e:
    print(e)
    print('ok {}'.format(count))

count += 1
try:
    parse2('1+(2')
except SyntaxError as e:
    print(e)
    print('ok {}'.format(count))

count += 1
try:
    parse2('2*+3')
except SyntaxError as e:
    print(e)
    print('ok {}'.format(count))


def parse(expr):
    m1 = re.match(r"(\d+)(\+)", expr)
    if m1 is not None:
        x = Number(int(m1.group(1)))
        return x + parse(expr[m1.end():])

    m2 = re.match(r"([A-Za-z])(\+)", expr)
    if m2 is not None:
        x = Variable(m2.group(1))
        return x + parse(expr[m2.end():])

    m3 = re.match(r"(\d+)", expr)
    if m3 is not None:
        return Number(int(m3.group(1)))

    m4 = re.match(r"([A-Za-z])", expr)
    if m4 is not None:
        return Variable(m4.group(1))

    assert False, "invalid condition"

x = parse("1+2")
assert x == 3

f = parse('1+x')
assert f(x=1) == 2

f = parse('x+1')
assert f(x=2) == 3

f = parse('x+y+z')
assert f(x=2,y=2,z=3) == 7

f = parse('x+y+x')
assert f(x=2,y=3) == 7

print('parse is ok')

# def g(a, b):
#     print(a, b)
#
# def f(**kwargs):
#     g(**kwargs)
#
# import inspect
# print(inspect.getargspec(f))

