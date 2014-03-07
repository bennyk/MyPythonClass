
class TypedProperty:

    def __init__(self, name, type):
        self.name = '_' + name
        self.type = type

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('Must be a {}'.format(self.type))

        setattr(instance, self.name, value)


class Foo:
    name = TypedProperty('name', str)
    num = TypedProperty('num', int)

if False:
    f = Foo()
    f.name = "ben"
    # f.name = 123
    print(f.name)
    print(Foo.name)

class Meter(object):
    '''Descriptor for a meter.'''

    def __init__(self, value=0.0):
        self.value = float(value)
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = float(value)

class Foot(object):
    '''Descriptor for a foot.'''

    def __get__(self, instance, owner):
        return instance.meter * 3.2808
    def __set__(self, instance, value):
        instance.meter = float(value) / 3.2808

class Distance(object):
    '''Class to represent distance holding two descriptors for feet and
    meters.'''
    meter = Meter()
    foot = Foot()

d = Distance()
d.meter = 1
print(d.meter, d.foot, "foot")
print(Distance.meter)