
import abc

class Drawable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        print("draw in Drawable")

class HNode(Drawable, metaclass=abc.ABCMeta):

    def getChildren(self):
        raise NotImplementedError
    children = abc.abstractproperty(getChildren)

    @abc.abstractmethod
    def appendChild(self, child):
        raise NotImplementedError

    def getParent(self):
        raise NotImplementedError
    def setParent(self, parent):
        raise NotImplementedError
    parent = abc.abstractproperty(getParent, setParent)

    @abc.abstractmethod
    def size(self):
        raise NotImplementedError('missing size()')

    def draw(self):
        # super().draw()
        print("draw in HNode")

    def sumOfSize(self):
        pass

class SomeBaseNode(Drawable):

    def draw(self):
        super().draw()
        print("draw in SomeBaseNode")

class SomeNode(SomeBaseNode, HNode):
    def __init__(self):
        self._parent = None

    def getParent(self):
        return self._parent
    def setParent(self, parent):
        self._parent = parent
    parent = property(getParent, setParent)

    def getChildren(self):
        pass
    children = property(getChildren)

    def appendChild(self, child):
        pass

    def sumOfSize(self):
        total = 0
        for c in self.children:
            assert isinstance(c, HNode)
            total += c.sumOfSize()
        return total

    def draw(self):
        super().draw()
        print("draw in SomeNode")

class DerivedSomeNode(SomeNode):
    def draw(self):
        super().draw()
        print("draw in DerivedSomeNode")

def children(node):
    assert isinstance(node, HNode)
    return node.children

def parent(node):
    assert isinstance(node, HNode)
    return node.parent

a = SomeNode()
# a.size()

print("DerivedSomeNode mro is:", DerivedSomeNode.__mro__)
d = DerivedSomeNode()
d.draw()


import collections.abc

collections.abc.Set


