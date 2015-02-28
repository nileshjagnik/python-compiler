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


# python compile.py example1.py
# $gcc -m32 *.c example1.s -o test.exe -lm
# ./text.exe
# cat test.in | -l test.exe

if __name__ == '__main__':
    startAST = compiler.parseFile(sys.argv[1])
    
    explicator = explicateVisitor()
    
    explicateAST = explicator.walk(startAST)
    
    

    
    debug = 1
    
    flatast = flatten(explicateAST)
    #print "\nFLATTENED ASTs:"
    
    registerTest = 1
    
    flat = []
    if (debug):
        
        print "STARTAST:"
        print startAST , "\n"
        
        print "EXPLICATE_AST:"
        for x in explicateAST.node.nodes:
            print x
        
        print "\nTYPE CHECKER OUTPUT:"
        tchecker = typecheckVisitor()
        tchecker.walk(explicateAST)
    
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

        done = False
        totalIter = 0
        tmp = 0


        while not done:
            liveness = livenessAnalysis(IR)
            print "liveness"
            for x in liveness:
                print x
            iG = interferenceGraph(IR,liveness,vars)
            print "interference graph"
            for k in iG.keys():
                print str(k) +": " + str(iG[k])
            coloring = graphColor(iG)
            print coloring
            spill = toSpill(coloring)
            good,IR,vars,done = allocateRegisters(spill,IR,vars,coloring)
            
        for g in good:
            print g

        print "Total Iters: " +str(totalIter)
        outputCode(good,len(spill),"test_1")
        """
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
        """
        filename = ""
        prev = sys.argv[1].split('.')[0]
        for k in sys.argv[1].split('.')[1:]:
        	filename += prev
        	prev = "."+k
        #outputCode(IR,70,filename) # change these values
        outputCode(good,len(spill),filename)

    filename = ""
    prev = sys.argv[1].split('.')[0]
    for k in sys.argv[1].split('.')[1:]:
        filename += prev
        prev = "."+k
    done = False
    IR,vars = generateInstructions(flat)
    tmp = 0
    #totalIter = 0
    #Basic Algorithm
    while not done:
        liveness = livenessAnalysis(IR)
        iG = interferenceGraph(IR,liveness,vars)
        coloring = graphColor(iG)
        spill = toSpill(coloring)
        good,IR,vars,done = allocateRegisters(spill,IR,vars,coloring)
    #print totalIter
    #totalIter+=1
    
    
    
    #Attempted optimization
    '''
        liveness = livenessAnalysis(IR)
        iG = interferenceGraph(IR,liveness,vars)
        while not done:
        coloring = graphColor(iG)
        spill = toSpill(coloring)
        good,IR,liveness,iG,done,tmp = allocateRegisters(spill,IR,liveness,iG,coloring,tmp)
        '''
    
    #print good
    
    
    outputCode(good,len(spill),filename)
        
        
        
        
