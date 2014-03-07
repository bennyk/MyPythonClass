

class KiasuListTransaction:
    def __init__(self, mylist):
        self.mylist = mylist

    def __enter__(self):
        self.workingcopy = list(self.mylist)
        return self.workingcopy

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None: # yeah!
            self.mylist[:] = self.workingcopy

        # False if any exception occur during exit is propagated out
        return False

from contextlib import contextmanager

@contextmanager
def KiasuListTransaction2(mylist):
    workingcopy = list(mylist)
    yield workingcopy
    # if exception has occurred inside with-block execution will not pass this line
    mylist[:] = workingcopy


a = [1,2,3]
with KiasuListTransaction2(a) as working:
    working.append(4)
    working.append(5)

# should print [1, 2, 3, 4, 5]
print(a)


a = [1,2,3]
try:
    with KiasuListTransaction2(a) as working:
        working.append(4)
        working.append(5)
        raise RuntimeError('uh oh! big big trouble')
except RuntimeError as e:
    print(e, "... alrite we are backing up")

# should print [1, 2, 3]
print(a)



