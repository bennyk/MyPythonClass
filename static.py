
class Foo:
    @staticmethod
    def me():
        pass

    @classmethod
    def me2(cls):
        pass

class A:
    _singleton = None

    @classmethod
    def me(cls):
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton

class B(A): pass

class C(A): pass

print(B.me())
print(C.me())
print(B.me())

print(id(A._singleton))
print(id(B._singleton))
print(id(C._singleton))
