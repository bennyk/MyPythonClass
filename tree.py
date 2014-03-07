import random

class TreeNode:
    def __init__(self, name):
        self._children = []
        self.name = name
        self.parent = None
        # init other data associated with the node

    def __str__(self):
        return "TreeNode(%s)" % self.name

    def getChildren(self):
        return self._children

    def add(self, child):
        self._children.append(child)
        child.parent = self

    def dump(self, depth=0):
        print("%s%s %s" % (depth*'   ', self.__class__.__name__, self.name))
        for childNode in self._children:
            childNode.dump(depth=depth+1)

_id = 0
def buildTreeRandomly(parent, level=2, limit=5, depth=1):
    global _id
    for i in range(random.randint(1, limit)):
        _id += 1
        childNode = TreeNode('c%s' % _id)
        parent.add(childNode)

    if depth >= level:
        return

    for childNode in parent.getChildren():
        buildTreeRandomly(childNode, depth=depth+1, level=level, limit=limit)

def elementsInTree(n):
    """yield all nodes in a given tree node"""
    assert isinstance(n, TreeNode)

    yield n
    for childNode in n.getChildren():
        # < py3.3
        # for childNode2 in elementsInTree(childNode):
        #     yield childNode2
        # >= py3.3 only
        yield from elementsInTree(childNode)

def leavesInTree(n):
    """yield all leaves in a tree"""
    if len(n.getChildren()) == 0:
        yield n

    for childNode in n.getChildren():
        yield from leavesInTree(childNode)

def testRandomTree():
    root = TreeNode('root')
    buildTreeRandomly(root, level=2)
    root.dump()

def testIterator():
    root = TreeNode('root')
    buildTreeRandomly(root, level=2)
    root.dump()

    print("all nodes in tree:")
    for n in elementsInTree(root):
        print(n)

    print("all leaves in tree")
    for leaf in leavesInTree(root):
        print(leaf)

testIterator()