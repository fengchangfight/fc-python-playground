import sys

class Person(object):
    def __init__(self,name,age):
        self.name=name
        self.age=age

p1 = Person("Mike",25)
print(sys.getsizeof(p1))
