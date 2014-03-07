

def A():
    return B()

def B():
    return C()

def C():
    # raise KeyError('key error')
    raise OverflowError("can't compute something")


try:
    A()
except OverflowError as e:
    print(e)
# except:
#     print('got here')
#
finally:
    print('cleaning up')

