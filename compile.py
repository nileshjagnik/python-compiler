import compiler
#from parse import *
import sys
from flattenNJ import *
from ast2x86 import *
from x86IR import *
from registerAllocation import *
from colorSpill import *
from explicateNJ import *
from explicateNodes import *
from typecheck import *
from flattenNJ import *
from uniquify import *


# python compile.py example1.py
# $gcc -m32 *.c example1.s -o test.exe -lm
# ./text.exe
# cat test.in | -l test.exe

if __name__ == '__main__':
    debug = 1
    startAST = compiler.parseFile(sys.argv[1])
    
    if (debug):
        
        print "STARTAST:"
        print startAST , "\n"
        
    uniqueAST = uniquify(startAST,{})
    
    if (debug):
        
        print "UNIQUEAST:"
        print uniqueAST, "\n"
    
    """
    explicator = explicateVisitor()
    
    explicateAST = explicator.walk(startAST)
    
    

    
    
    
    #flatast = flatten(explicateAST)
    
    #registerTest = 1
    
    flat = []
    
    if (debug):
        
        print "EXPLICATE_AST:"
        for x in explicateAST.node.nodes:
            print x
        
        print "\nTYPE CHECKER OUTPUT:"
        tchecker = typecheckVisitor()
        tchecker.walk(explicateAST)
    
        print "\nFLAT ASTs:"
        for a in flatast:
            for k in a:
                if(debug):
                    print k , "\n"
                flat.append(k)
    
    
    
    if(registerTest):
        IR,vars = generateInstructions(flat)
        
        print vars
        print "IR"
        for x in IR:
            print x
        
        counter = -4
        varmap = {}
        for v in vars:
            varmap[v] = counter
            counter -= 4

        print varmap
        done = False
        totalIter = 0
        tmp = 0
        
        filename = ""
        prev = sys.argv[1].split('.')[0]
        for k in sys.argv[1].split('.')[1:]:
        	filename += prev
        	prev = "."+k
    	
        outputCode(IR,len(vars),filename,varmap) # change these values

    #OUTPUT CODE
    IR,vars = generateInstructions(flat)

    counter = -4
    varmap = {}
    for v in vars:
        varmap[v] = counter
        counter -= 4


    done = False
    totalIter = 0
    tmp = 0
        
    filename = ""
    prev = sys.argv[1].split('.')[0]
    for k in sys.argv[1].split('.')[1:]:
        filename += prev
        prev = "."+k

    outputCode(IR,len(vars),filename,varmap)

    """


