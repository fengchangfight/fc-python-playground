import gc
class A():
  def __init__(self):
    pass
  def __del__(self):
    pass

class B():
  def __init__(self):
    pass
  def __del__(self):
    pass

a = A()
b = B()
a._b = b
b._a = a
del a
del b

print(gc.collect())
print(gc.garbage )

