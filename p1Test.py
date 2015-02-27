from compiler.ast import *
from flatten import *
import compiler
#from parse import *
import sys
from flattenAST import *
from ast2x86 import *
from x86IR import *
from registerAllocation import *
from explicate import *
#from allocation import *
import sys


'''

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
    
'''

__all__ = ('printAst',)


def printAst(ast, indent='  ', stream=sys.stdout, initlevel=0):
    "Pretty-print an AST to the given output stream."
    rec_node(ast, initlevel, indent, stream.write)
    stream.write('\n')

def rec_node(node, level, indent, write):
    "Recurse through a node, pretty-printing it."
    pfx = indent * level
    if isinstance(node, Node):
        write(pfx)
        write(node.__class__.__name__)
        write('(')
        
        if any(isinstance(child, Node) for child in node.getChildren()):
            for i, child in enumerate(node.getChildren()):
                if i != 0:
                    write(',')
                write('\n')
                rec_node(child, level+1, indent, write)
            write('\n')
            write(pfx)
        else:
            # None of the children as nodes, simply join their repr on a single
            # line.
            write(', '.join(repr(child) for child in node.getChildren()))
        
        write(')')
    
    else:
        write(pfx)
        write(repr(node))

if __name__ == '__main__':
    exampleAST = compiler.parseFile(sys.argv[1])
    print exampleAST
    
    print
    
    explicateAST = explicate(exampleAST)
    printAst(explicateAST)
    print
    
    flatAst = flatten_module(explicateAST)
    
    for n in flatAst:
        print n
    
#print





