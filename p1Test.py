
import compiler
#from parse import *
import sys
from flattenAST import *
from ast2x86 import *
from x86IR import *
from registerAllocation import *
from explicate import *
#from allocation import *


def printAst(astNode):
    if isinstance(astNode,Module):
        print astNode
        print
        printAst(astNode.node)
    

    elif isinstance(astNode,Stmt):
        stmts = []
        print astNode
        for n in astNode.nodes:
            printAst_statement(n)
        


def printAst_statement(s):
    if isinstance(s,Printnl):
        print s
        print
        for exp in s.nodes:
            printAst_expression(exp)

    
    elif isinstance(s,Assign):
        print s
        print
        printAst_expression(s.expr)
    
    elif isinstance(s,Discard):
        print s
        print
        printAst_expression

def printAst_expression(e):
    print e
    print



if __name__ == '__main__':
    exampleAST = compiler.parseFile(sys.argv[1])
    print exampleAST
    
    print
    
    explicateAST = explicate(exampleAST)


    printAst(explicateAST)


