import gc

class ClassyClass(object):

    def __init__(self):
        print ("I live!")

    def __del__(self):
        print ("I have been garbage collected")

    def make_a_self_reference(self):
        self.self = self
        print ("I point to myself")

def no_self_reference():
    ClassyClass()

def self_reference():
    ClassyClass().make_a_self_reference()


if __name__ == "__main__":
    gc.set_debug(gc.DEBUG_LEAK)
    print("\n== Without self reference ==")
    no_self_reference()
    print ("Uncollectable garbage", gc.garbage)
    print ("\n== With self reference ==")
    self_reference()
    print ("Uncollectable garbage", gc.garbage)
    print ("= Forcing full collection =")
    gc.collect()
    print ("Uncollectable garbage", gc.garbage)