a = 3

def f():
    print a
    def f(x):
        print x
    f(2) 
f()
