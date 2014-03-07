
class Visitor:
    def __init__(self):
        self._seen = set()

    def hasSeen(self, obj):
        return obj in self._seen

    def markSeen(self, obj):
        self._seen.add(obj)

    def visitEdge(self, obj):
        pass

    def visitNode(self, obj):
        pass

    def visit(self, obj):
        print("visiting obj", obj)
        if isinstance(obj, GEdge):
            self.visitEdge(obj)

        elif isinstance(obj, GNode):
            self.visitNode(obj)

        else:
            raise NotImplemented('invalid object type in graph: %s' % type(obj))

import collections.abc

class Graph(collections.abc.Container):
    def __init__(self):
        self._nodes = {}
        self._edges = []

    def addNode(self, label):
        n = GNode(label)
        self._nodes[label] = n
        return n

    def addEdge(self):
        e = GEdge()
        self._edges.append(e)
        return e

    def hasNode(self, name):
        return name in self._nodes

    def getNode(self, name):
        return self._nodes[name]

    def getNodes(self):
        return self._nodes.values()

    def accept(self, visitor):
        for n in self.getNodes():
            if not visitor.hasSeen(n):
                n.accept(visitor)

    def writeDotFile(self, dotFile):
        with open(dotFile, 'wt') as fout:
            fout.write("""digraph G {
concentrate=true
//edge [dir="both"]
""")
            for e in self._edges:
                fout.write("%s\n" % e)
            fout.write('}\n')

class GNode:
    def __init__(self, name):
        self.name = name
        self._outEdges = []
        self._inEdges = []

    def accept(self, visitor):
        assert isinstance(visitor, Visitor)

        visitor.markSeen(self)
        for e in self._outEdges:
            e.accept(visitor)

        visitor.visit(self)

    def __str__(self):
        return self.name

class GEdge:
    def __init__(self, weight=0):
        self._inNode = None
        self._outNode = None
        self.weight = weight

    def connect(self, inNode, outNode):
        self._inNode = inNode
        self._outNode = outNode
        outNode._inEdges.append(self)
        inNode._outEdges.append(self)

    def accept(self, visitor):
        visitor.visit(self)
        if not visitor.hasSeen(self._outNode):
            self._outNode.accept(visitor)

    def __str__(self):
        return "%s -> %s" % (self._inNode.name, self._outNode.name)

class GraphVizWriter(Visitor):
    def __init__(self, outfile):
        super().__init__()
        self._out = open(outfile, 'wt')
        self._out.write("""digraph G {
concentrate=true
""")

    def __del__(self):
        self._out.write("}\n")

    def visitEdge(self, obj):
        assert isinstance(obj, GEdge)
        self._out.write("%s -> %s\n" % (obj._inNode, obj._outNode))

    def visitNode(self, obj):
        pass

def writeGraphVizFile(outfile, g):
    assert isinstance(g, Graph)
    writer = GraphVizWriter(outfile)
    g.accept(writer)

def addOrGetNode(g, label):
    assert isinstance(g, Graph)
    if g.hasNode(label):
        return g.getNode(label)
    else:
        newNode = g.addNode(label)
        return newNode

data = {'1': ['2', '5'],
        '2': ['1', '3', '5'],
        '3': ['2', '4'],
        '4': ['3', '5', '6'],
        '5': ['1', '2', '4'],
        '6': ['4'],
        }

def createGraphWithData(data):
    g = Graph()
    for srcLabel, entries in data.items():
        print(srcLabel, entries)
        srcNode = addOrGetNode(g, srcLabel)
        for dstLabel in entries:
            dstNode = addOrGetNode(g, dstLabel)
            edge = g.addEdge()
            edge.connect(srcNode, dstNode)

    g.writeDotFile('boo.dot')
    return g

import random
def createGraphRandomly(n=10, p=0.05):
    g = Graph()
    for x in range(n):
        newNode = g.addNode('n%d' % x)

    for nodeA in g.getNodes():
        for nodeB in g.getNodes():
            if random.random() < p:
                e = g.addEdge()
                e.connect(nodeA, nodeB)

    g.writeDotFile('boo.dot')
    return g

def testVisitor():
    g = createGraphWithData(data)
    myVisitor = Visitor()
    g.accept(myVisitor)

def testWriteGraphvizVisitor():
    g = createGraphRandomly(p=0.2, n=12)
    writeGraphVizFile("boo.dot", g)

# createGraphRandomly(p=0.2, n=5)
# createGraphWithData(data)
# testVisitor()

testWriteGraphvizVisitor()