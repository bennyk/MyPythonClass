

def generateFibNum(limit=100):
    n2 = 1
    n1 = 2
    yield n2
    yield n1
    while True:
        x = n1 + n2
        # print(x)
        if x > limit:
            break
        yield x
        n2 = n1
        n1 = x

def generateEvenFibNum(**kwargs):
    for x in generateFibNum(**kwargs):
        if x % 2 == 0:
            yield x

for x in generateFibNum():
    print(x)

print("sum=", sum(generateEvenFibNum(limit=4000000)))