a = 3
z = 6
q = [0]
q[0] = a

def f(a, g):
    print a
    z = 3
    def f(y):
        return a + z + y
    r = 8
    return a + y + z + g

y = 3
print f(z,9)
