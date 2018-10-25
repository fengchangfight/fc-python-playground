import objgraph
import random

class MyBigFatObject(object):
    pass

def computate_something(_cache={}):
     _cache[42] = dict(foo=MyBigFatObject(),
                       bar=MyBigFatObject())
     # a very explicit and easy-to-find "leak" but oh well
     x = MyBigFatObject() # this one doesn't leak

objgraph.show_growth(limit=3)

computate_something()
objgraph.show_growth()


objgraph.show_chain(
     objgraph.find_backref_chain(
         random.choice(objgraph.by_type('MyBigFatObject')),
         objgraph.is_proper_module),
     filename='chain.png')