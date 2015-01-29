#import compiler
from parse import *
import sys
from flattenAST import *
from ast2x86 import *



# python compile.py example1.py
# $gcc -m32 *.c example1.s -o test.exe -lm
# ./text.exe
# cat test.in | -l test.exe

if __name__ == '__main__':
    #exampleAST = compiler.parseFile(sys.argv[1])
    f = open(sys.argv[1])
    program = f.read()
    exampleAST = yacc.parse(program)
    #print exampleAST
    varmap = {}
    (test1,empty) = flatten_ast(exampleAST,varmap)
    
    debug = 1
    
    #exampleAST = compiler.parse("a = 5 + input() +-6 + input(); print a")
    #varmap = {}
    #(test1,empty) = flatten_ast(exampleAST,varmap)
    
    if(debug):
        # Give the lexer some input
        lex.input(program)

        # Tokenize
        while True:
            tok = lex.token()
            if not tok: break      # No more input
            print tok

        print len(test1)
        for t in test1:
            print t
        print varmap

    filename = ""
    prev = sys.argv[1].split('.')[0]
    for k in sys.argv[1].split('.')[1:]:
    	filename += prev
    	prev = "."+k
    generateX86(test1,filename,varmap)
    # print
    # e1 = compiler.parse("x= 3 + input();y=4")
    # test2 = flatten(e1)
    # for t in test2:
    #     print t

    # for t in test1:
    #     prettyPrint(t)

    # for t in test2:
    #     prettyPrint(t)
