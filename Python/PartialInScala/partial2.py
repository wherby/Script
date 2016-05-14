
class partialFunInScala(object):
    funs=[]
    def __init__(self, f):
        self.f = f
        partialFunInScala.funs.append(f)

    def __call__(self,arg):
        #global funs
        print "Entering", self.f.__name__
        for f in partialFunInScala.funs:
            f(arg)
        print "Exited", self.f.__name__

 

@partialFunInScala
def func1(a):
    print "inside func1()"

@partialFunInScala
def func2(a):
    print a
    print "inside func2()"


func2(2)

