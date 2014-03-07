
class Library:
    numOfCell = 0

    def __init__(self, name, version):
        self.name = name
        self.version = version

        # init a dict to keep all store entries
        self._cell = {}

        Library.numOfCell += 1

    def __del__(self):
        Library.numOfCell -= 1

    def hasCell(self, name):
        return name in self._cell

    def add(self, cell, name):
        if self.hasCell(name):
            print("Warning: cell with name %s already exists! replacing..." % name)
        self._cell[name] = cell

    def remove(self, name):
        if not self.hasCell(name):
            print("Error: can't find any cell name with %s to remove" % name)
            return
        del self._cell[name]

a = Library("ckt1.net", 1)
b = Library("ckt2.net", 3)
a.add('<<data>>', 'testCell')
print(a)
print(b)


