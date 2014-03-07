import random
import functools

# @functools.total_ordering
class MyObject:
    def __init__(self, w):
        self._w = w

    def __repr__(self):
        return 'MyObject(%s)' % self._w

    # def __lt__(self, other):
    #     assert isinstance(other, MyObject)
    #     return self._w < other._w

def genObjects():
    for x in range(20):
        w = random.randint(1, 100)
        yield MyObject(w)

# for x in sorted(genObjects()):
#     print(x)

# print(max(genObjects()))

g = map(MyObject, [8, 3, 6, 9, 10, 1])
for x in sorted(g):
    print(x)

print(max(map(MyObject, [8, 3, 6, 9, 23, 1])))
pass