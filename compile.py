import compiler
import sys
from flattenAST import *
from ast2x86 import *

# python compile.py test.py
	#test.s
# $gcc -m32 *.c test.s -o test.exe -lm
# cat test.in | -l test.exe

if __name__ == '__main__':
    exampleAST = compiler.parseFile(sys.argv[1])
    map = {}
    test1 = flatten(exampleAST,map)
    


    for t in test1:
        print t
    print map

    generateX86(test1,sys.argv[1].split('.')[0])
    # print
    # e1 = compiler.parse("x= 3 + input();y=4")
    # test2 = flatten(e1)
    # for t in test2:
    #     print t

    # for t in test1:
    #     prettyPrint(t)

    # for t in test2:
    #     prettyPrint(t)
