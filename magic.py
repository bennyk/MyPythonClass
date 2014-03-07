

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Position({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

import copy
c = Position(3,2) + Position(1,1)

def foo(c):
    c.x = 10

print(c)
foo(copy.copy(c))
print(c)

from collections import namedtuple

class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

def foo(c):
    assert isinstance(c, Point)
    c.x = 3
    print(c)

a = Point(3,2) + Point(1,1)
foo(a)
print(a)