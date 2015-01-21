import compiler
from flattenAST import *
#from compiler.ast import *

if __name__ == '__main__':
    exampleAST = compiler.parseFile("example1.py")
    test1 = flatten(exampleAST)
    
    for t in test1:
        print t
    
    print
    e1 = compiler.parse("x= 3 + input();y=4")
    test2 = flatten(e1)
    for t in test2:
        print t

    for t in test1:
        prettyPrint(t)

    for t in test2:
        prettyPrint(t)