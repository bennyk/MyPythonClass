import random

class Animal(object):
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError()

    def speak_twice(self):
        self.speak()
        self.speak()

    def showAffection(self):
        self.speak_twice()

class Dog(Animal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

    def speak(self):
        print("woff!")

class Cat(Animal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

    def speak(self):
        print("meow!")

    def showAffection(self):
        # apply pre-processing for purrr...meow! meow!
        print("purrr...")
        super().showAffection()

        # apply post processing


def generateAnimal(n):
    result = []
    for x in range(n):
        cls = random.choice([Cat, Dog])
        result.append(cls('xyz'))
    return result

for x in generateAnimal(3):
    assert isinstance(x, Animal)
    x.showAffection()
    x.speak_twice()
