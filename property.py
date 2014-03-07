
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 2*math.pi*self.radius**2

    @property
    def perimeter(self):
        return 2*math.pi*self.radius


class Unnameable:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        assert isinstance(value, str)
        self.__name = value

    @name.deleter
    def name(self):
        raise TypeError("can't delete name")
