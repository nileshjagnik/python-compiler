import compiler
import sys
from flattenAST import *
from ast2x86 import *

# python compile.py example1.py
# $gcc -m32 *.c example1.s -o test.exe -lm
# ./text.exe
# cat test.in | -l test.exe

if __name__ == '__main__':
    exampleAST = compiler.parseFile(sys.argv[1])
    varmap = {}
    test1 = flatten_ast(exampleAST,varmap)
    


    for t in test1:
        print t
    print varmap

    generateX86(test1,sys.argv[1].split('.')[0],varmap)
    # print
    # e1 = compiler.parse("x= 3 + input();y=4")
    # test2 = flatten(e1)
    # for t in test2:
    #     print t

    # for t in test1:
    #     prettyPrint(t)

    # for t in test2:
    #     prettyPrint(t)
