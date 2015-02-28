#Alex Gendreau
#Homework 3: Register Allocation
#Partner: Nilesh Jagnik

#Acknowledgement:
'''
    Python Documentaiton
    Proirty Queue Implementaiton modeled after this one
    https://docs.python.org/2/library/heapq.html
'''




import compiler
#from parse import *
import sys
from flatten import *
from ast2x86 import *
from x86IR import *
from registerAllocation import *
from explicate import *
#from allocation import *


# python compile.py example1.py
# $gcc -m32 *.c example1.s -o test.exe -lm
# ./text.exe
# cat test.in | -l test.exe

if __name__ == '__main__':
    exampleAST = compiler.parseFile(sys.argv[1])
    explicateAST = explicate(exampleAST)
    #print explicateAST
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


    test1 = flatten_module(explicateAST)
    #print
    #print test1
    debug = 1
    
    registerTest = 1
    
    #exampleAST = compiler.parse("a = 5 + input() +-6 + input(); print a")
    #varmap = {}
    #(test1,empty) = flatten_ast(exampleAST,varmap)
    
    if(debug):
        print "Flat"

        print len(test1)
        for t in test1:
            print t
            print

    if(registerTest):
        
        
        IR,vars = generateInstructions(test1)
        print vars
        print "IR"
        for x in IR:
            print x
        
        print
        done = False
        totalIter = 0
        tmp = 0
    
        #Basic Algorithm
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


        '''
        print
        print "liveness"
        liveness = livenessAnalysis(IR)
        for x in liveness:
            print x
        # print
        #    print "Vars"
                # for x in vars:
                #print x
        # print
        iG = interferenceGraph(IR,liveness,vars)
            # print "interference graph"
                # for k in iG.keys():
                #print str(k) +": " + str(iG[k])
        while not done:
            coloring = graphColor(iG)
            #print coloring
            # print "to spill"
            spill = toSpill(coloring)
            #print spill

            good,IR,livesness,iG,done,tmp = allocateRegisters(spill,IR,liveness,iG,coloring,tmp)
            print "newIR"
            for x in IR:
                print x
            totalIter+=1
                #if totalIter>1:
            '''
#done = True

        print "Total Iters: " +str(totalIter)
        outputCode(good,len(spill),"test_1")
        

#print

#print iG


    filename = ""
    prev = sys.argv[1].split('.')[0]
    for k in sys.argv[1].split('.')[1:]:
    	filename += prev
    	prev = "."+k
    done = False
    IR,vars = generateInstructions(test1)
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

#generateX86(test1,filename,varmap)
    # print
    # e1 = compiler.parse("x= 3 + input();y=4")
    # test2 = flatten(e1)
    # for t in test2:
    #     print t

    # for t in test1:
    #     prettyPrint(t)

    # for t in test2:
    #     prettyPrint(t)

