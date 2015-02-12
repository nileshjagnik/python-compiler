import compiler
#from parse import *
import sys
from flattenAST import *
from ast2x86 import *
from x86IR import *
from registerAllocation import *
from colorSpill import *



# python compile.py example1.py
# $gcc -m32 *.c example1.s -o test.exe -lm
# ./text.exe
# cat test.in | -l test.exe

if __name__ == '__main__':
    exampleAST = compiler.parseFile(sys.argv[1])
    #f = open(sys.argv[1])
    #program = f.read()
    #print program
        #program = '''
        #this is a comment
        #x=3 #this is a another comment
        #y=input()
        #print x'''
        #exampleAST = yacc.parse(program)
    #print exampleAST
    varmap = {}
    (test1,empty) = flatten_ast(exampleAST,varmap)
    
    debug = 1
    
    registerTest = 1
    
    #exampleAST = compiler.parse("a = 5 + input() +-6 + input(); print a")
    #varmap = {}
    #(test1,empty) = flatten_ast(exampleAST,varmap)
    
    if(debug):
        # Give the lexer some input
        #lex.input(program)

        # Tokenize
        #while True:
        #   tok = lex.token()
        #   if not tok: break      # No more input
        #    print tok

        print len(test1)
        for t in test1:
            print t
        print varmap
    
    if(registerTest):
        print
        IR = generateInstructions(test1)
        print "IR"
        for x in IR:
            print x
        print
        print "liveness"
        liveness = livenessAnalysis(IR)
        for x in liveness:
            print x
        print
        iG = interferenceGraph(IR,liveness)
        print "interference graph"
        for k in iG.keys():
            print str(k) +": " + str(iG[k])

        print "\ncoloring"
        coloring, IR = colorSpill(iG,IR,liveness)
        print coloring
#print

#print iG


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
