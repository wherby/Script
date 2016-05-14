
class partialFunInScala(object):
    funs=[]
    def __init__(self, f):
        #print dir(f),f.__name__
        self.f = f
        partialFunInScala.funs.append(f)

    def __call__(self,arg):
        #global funs
        #print "Entering", self.f.__name__
        for f in reversed(partialFunInScala.funs):
            if f(arg)==0:
                break


 

@partialFunInScala
def func1(a):
    print "inside func1()"


@partialFunInScala
def func2(a):  
    if a%2 ==0:
        print a
        print "inside func2()"
        return 0
    else:
        return -1
   
@partialFunInScala
def func3(a):
    if a%3 ==0:
        print a
        print "inside func3()"
        return 0
    else:
        return -1

func2(2)
print "====="
func2(1)
print "===="
func2(3)

