
class Window:
    def __init__(self):
        self._children = []
        self.parent = None
        self.offset = 0

    def add(self, child):
        self._children.append(child)
        child.parent = self

    def convertToParentOffset(self, pos):
        raise NotImplementedError

    def draw(self, depth=0):
        print("%sdraw content window" % ('   '*depth))

class RootWindow(Window):
    def convertToParentOffset(self, pos):
        return pos

class ChildWindow(Window):
    def __init__(self, offset):
        super().__init__()
        self.offset = offset

    def convertToParentOffset(self, pos):
        return self.parent.convertToParentOffset(self.offset) + pos

class WindowDecorator(Window):
    def __init__(self, content):
        self.content = content

    def draw(self, depth=0, **kwargs):
        print("%s{draw decorated content" % ('   ' * depth))
        self.content.draw(depth=depth+1, **kwargs)
        print("%s}" % ('   ' * depth))

class HorizontalScrollBarDecorator(WindowDecorator):
    def __init__(self, content):
        super().__init__(content)

    def drawHorizontalScrollBar(self, depth=0):
        print("%sdraw horizontal scroll bar" % ('   ' * depth))

    def draw(self, **kwargs):
        super().draw(**kwargs)
        self.drawHorizontalScrollBar(**kwargs)

class VerticalScrollBarDecorator(WindowDecorator):
    def __init__(self, content):
        super().__init__(content)

    def drawVerticalScrollBar(self, depth=0):
        print("%sdraw vertical scroll bar" % ('   ' * depth))

    def draw(self, **kwargs):
        super().draw(**kwargs)
        self.drawVerticalScrollBar(**kwargs)

def testConvertOffset():
    root = RootWindow()
    c1 = ChildWindow(3)
    root.add(c1)

    c2 = ChildWindow(2)
    c1.add(c2)

    parentOffset = c2.convertToParentOffset(6)
    print(parentOffset)

def testDecorator():
    decoratedWindow = HorizontalScrollBarDecorator(
        VerticalScrollBarDecorator(ChildWindow(0)
        )
    )
    decoratedWindow.draw()

testDecorator()



