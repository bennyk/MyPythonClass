
from types import FunctionType
from functools import partial

import operator


def isnumber(value):
    return any(map(partial(isinstance, value), [float, int]))

def closeenough(a, b):
    return True if abs(a - b) < 1e-7 else False

class BasicOp:
    def __add__(self, other):
        return self.apply(operator.add, other)
    def __sub__(self, other):
        return self.apply(operator.sub, other)
    def __mul__(self, other):
        return self.apply(operator.mul, other)
    def __truediv__(self, other):
        return self.apply(operator.truediv, other)
    def __pow__(self, power, modulo=None):
        return self.apply(operator.pow, power)

    def __radd__(self, other):
        return self.__add__(other)
    def __rmul__(self, other):
        return self.__mul__(other)

    # not reversible operator
    def __rsub__(self, other):
        return Number(other).__sub__(self)
    def __rtruediv__(self, other):
        return Number(other).__truediv__(self)
    def __rpow__(self, other, modulo=None):
        return Number(other).__pow__(self)


    def apply(self, op, other):
        raise NotImplementedError

class Terminal:
    pass

def isterminal(value):
    return isnumber(value) or isinstance(value, Terminal)

class Variable(BasicOp):
    def __init__(self, name):
        self._name = name

    def __str__(self):
        return "Symbol({})".format(self._name)

    def apply(self, op, other):

        # x * t
        if isterminal(other):
            def _(**kwargs):
                a = kwargs[self._name]
                return op(a, other)
            return Functor(_)

        # x * x
        if isinstance(other, Variable):
            def _(**kwargs):
                a = kwargs[self._name]
                b = kwargs[other._name]
                return op(a, b)
            return Functor(_)

        # x * f
        if isinstance(other, Functor):
            def _(**kwargs):
                a = kwargs[self._name]
                return op(a, other(**kwargs))
            return Functor(_)

        assert False, "{} invalid other {}".format(self, other)

    def __neg__(self):
        def _(**kwargs):
            a = kwargs[self._name]
            return -a
        return Functor(_)

class Functor(BasicOp):
    def __init__(self, value):
        assert isinstance(value, FunctionType)
        self._value = value

    def apply(self, op, other):
        # f * t
        if isterminal(other):
            def _(**kwargs):
                return op(self(**kwargs), other)
            return Functor(_)

        # f * x
        if isinstance(other, Variable):
            def _(**kwargs):
                a = kwargs[other._name]
                return op(self(**kwargs), a)
            return Functor(_)

        # f * f
        if isinstance(other, Functor):
            def _(**kwargs):
                return op(self(**kwargs), other(**kwargs))
            return Functor(_)

        assert False, "{} invalid other {}".format(self, other)

    def __call__(self, *args, **kwargs):
        return self._value(**kwargs)

    def __neg__(self):
        def _(**kwargs):
            a = self(**kwargs)
            return -a
        return Functor(_)

class Number(Terminal, BasicOp):
    def __init__(self, value):
        assert isnumber(value)
        self._value = value

    def __str__(self):
        return "Number({})".format(self._value)

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)

    def apply(self, op, other):
        # n * n
        if isinstance(other, Number):
            return Number(op(self._value, other._value))

        # n * d
        if isnumber(other):
            return Number(op(self._value, other))

        # n * t
        if isinstance(other, Vector2):
            # if op is reversible
            if op is operator.mul or op is operator.add:
                return op(other, self)

        # n * x
        if isinstance(other, Variable):
            def _(**kwargs):
                a = kwargs[other._name]
                return op(self._value, a)
            return Functor(_)

        # n * f
        if isinstance(other, Functor):
            def _(**kwargs):
                return op(self._value, other(**kwargs))
            return Functor(_)

        assert False, "{} invalid other {}".format(self, other)

    def __neg__(self):
        return Number(-self._value)

    def __eq__(self, other):
        if isinstance(other, int):
            return int(self) == other

        if isinstance(other, float):
            return float(self) == other

        if isinstance(other, Number):
            return self._value == other._value

        assert False, "{} invalid other {}".format(self, other)

class Vector2(Terminal):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def apply(self, op, other):
        # v * x
        if isinstance(other, Variable):
            def _(**kwargs):
                a = kwargs[other._name]
                return op(self, a)
            return Functor(_)

        # v * f
        if isinstance(other, Functor):
            def _(**kwargs):
                return op(self, other(**kwargs))
            return _

        assert False, "{} invalid other {}".format(self, other)

    def __str__(self):
        return "Vector2({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        assert isinstance(other, Vector2)
        return closeenough(self.x, other.x) and closeenough(self.y, other.y)

    def __radd__(self, other):
        return self.__add__(other)
    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        # v + v
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x,
                           self.y + other.y)

        return self.apply(operator.add, other)

    def __sub__(self, other):
        # v - v
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x,
                           self.y - other.y)

        return self.apply(operator.sub, other)

    def __mul__(self, other):
        # v * v
        if isinstance(other, Vector2):
            raise NotImplementedError("can't multiply two vector")

        # v * d
        if isnumber(other):
            return Vector2(self.x * other, self.y * other)

        if isinstance(other, Number):
            return Vector2(self.x * other._value, self.y * other._value)

        return self.apply(operator.mul, other)


    def __truediv__(self, other):
        # v * v
        if isinstance(other, Vector2):
            raise NotImplementedError("can't div two vector")

        # v / d
        if isnumber(other):
            return Vector2(self.x / other, self.y / other)

        if isinstance(other, Number):
            return Vector2(self.x / other._value, self.y / other._value)

        return self.apply(operator.truediv, other)

    def __pow__(self, power, modulo=None):
        raise NotImplementedError("can't power vector")

if __name__ == '__main__':
    x = Number(3) + 3
    assert x == 6

    x = Number(3) + Number(3)
    assert x == 6

    f = Number(3) + Variable('x')
    assert f(x=3) == 6

    x = -Number(3)
    assert x == -3

    f = Number(3) - Variable('x')
    assert f(x=3) == 0

    f = Variable('x') + Variable('x')
    assert f(x=3) == 6
    assert f(x=4) == 8

    # x + y + z
    g = Variable('y') + Variable('z')
    f = Variable('x') + g
    assert f(x=2, y=2, z=3) == 7

    # x + y + x
    f = Variable('x') + Variable('y') + Variable('x')
    assert f(x=2, y=1) == 5

    f = Variable('x') + Number(3)
    assert f(x=3) == 6

    f = Variable('x') - Number(3)
    assert f(x=3) == 0

    # x + y - z
    g = Variable('y') - Variable('z')
    f = Variable('x') + g
    assert f(x=3,y=4,z=5) == 2

    # x - y + z
    g = Variable('y') + Variable('z')
    f = Variable('x') - g
    assert f(x=3,y=4,z=5) == -6

    # 2*x + y
    f = Number(2) * Variable('x') + Variable('y')
    assert f(x=2, y=1) == 5

    f = Variable('x') * Number(2) + Variable('y') / Number(2)
    print(f(x=2, y=1))
    assert f(x=2, y=1) == 4.5

    assert Number(2) ** Number(3) == 8

    f = Variable('x') ** Number(2)
    assert f(x=2) == 4

    assert Number(1) / Number(2) == 0.5

    f = Vector2(2,3) * Variable('x')
    assert f(x=2) == Vector2(4,6)

    f = Variable('x') * Vector2(2,3)
    assert f(x=Number(2)) == Vector2(4,6)

    f = Variable('x') + Vector2(2,3)
    assert f(x=Vector2(1,2)) == Vector2(3,5)

    f = Variable('x') - Vector2(2,3)
    assert f(x=Vector2(1,2)) == Vector2(-1,-1)

    f = Vector2(2,3) / Variable('x')
    assert f(x=2) == Vector2(1,3/2)

    # FIXME matrix inversion not implemented
    # f = Symbol('x') / Vector2(2,3)
    # assert f(x=2) == Vector2(4,6)


    print('basic is ok')

