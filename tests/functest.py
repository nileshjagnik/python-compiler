a = 3
y = 4

def f(a):
    print a
    def f(x):
        print x
    f(2)
    return a + y

print f(y)
