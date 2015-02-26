import compiler
#from parse import *
import sys
from flattenAST import *
from ast2x86 import *
from x86IR import *
from registerAllocation import *
from colorSpill import *
from explicateNJ import *
from explicateNodes import *


# python compile.py example1.py
# $gcc -m32 *.c example1.s -o test.exe -lm
# ./text.exe
# cat test.in | -l test.exe

if __name__ == '__main__':
    startAST = compiler.parseFile(sys.argv[1])
    
    print startAST , "\n"
    explicator = explicateVisitor()
    
    explicateAST = explicator.walk(startAST)
    
    print explicateAST
    
    debug = 0
    
    registerTest = 0
        
    if(debug):
        print len(test1)
        for t in test1:
            print t
        print varmap
    
    if(registerTest):
        IR,variables = generateInstructions(test1)
        if debug:
            print
            print "IR"
            for x in IR:
                print x
            print
            print "liveness"
        liveness = livenessAnalysis(IR)
        if debug:
            for x in liveness:
                print x
            print
        iG = interferenceGraph(IR,liveness,variables)
        
        coloring, IR, iG = colorSpill(iG,IR,liveness)
        
        if debug:
            print "interference graph"
            for k in iG.keys():
                print str(k) +": " + str(iG[k])

        if debug:
            print "\ncoloring"
            print coloring
            
        stacksize = len([x for x in coloring.keys() if coloring[x]<0])
        filename = ""
        prev = sys.argv[1].split('.')[0]
        for k in sys.argv[1].split('.')[1:]:
        	filename += prev
        	prev = "."+k
        outputCode(convertInstr(IR,coloring),stacksize,filename)
