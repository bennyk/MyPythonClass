
def add(a, b):
    return a + b

def my_partial(f, *args):
    def _(*a):
        new_args = args + a
        return f(*new_args)
    return _

add5 = my_partial(add, 5)
print(add5(3))