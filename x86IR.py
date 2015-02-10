from compiler.ast import *
from x86Nodes import *

def generateInstructions(astList):
    
    IR = []

    for tree in astList:
        if isinstance(tree,Assign):
            assignmentVariable = Var(tree.nodes[0].name)
            if isinstance(tree.expr,Add):
                if isinstance(tree.expr.left,Name) and isinstance(tree.expr.right,Name):
                    tmp1 = Var(tree.expr.left.name)
                    tmp2 = Var(tree.expr.right.name)
                
                elif isinstance(tree.expr.left,Name):
                    tmp1 = Var(tree.expr.left.name)
                    tmp2 = Con(tree.expr.right.value)
                
                elif isinstance(tree.expr.right,Name):
                    tmp1 = Con(tree.expr.left.value)
                    tmp2 = Var(tree.expr.right.name)
                
                else:
                    tmp1 = Con(tree.expr.left.value)
                    tmp2 = Con(tree.expr.right.value)
            
                moveNode = MovL((tmp1,assignmentVariable))
                addNode = AddL((tmp2,assignmentVariable))
                #print moveNode
                
                IR.extend([moveNode,addNode])
        #print IR
        
            elif isinstance(tree.expr,UnarySub):
                tmp = ""
                if isinstance(tree.expr.expr,Name):
                    tmp = Var(tree.expr.expr.name)
                else:
                    tmp = Con(tree.expr.expr.value)
                moveNode = MovL((tmp,assignmentVariable))
                negNode = NegL(assignmentVariable)
                IR.extend([moveNode,negNode])

            elif isinstance(tree.expr,Const):
                moveNode = MovL((Con(tree.expr.value),assignmentVariable))
                IR.extend([moveNode])

            elif isinstance(tree.expr,Name):
                moveNode = MovL((Var(tree.expr.name),assignmentVariable))
                IR.extend([moveNode])
                    
            elif isinstance(tree.expr,CallFunc):
                    funcNode = Call("input")
                    moveNode = MovL((Register("%eax"),assignmentVariable))
                        
        elif isinstance(tree,Printnl):
            if isinstance(tree.nodes[0],Name):
                pushNode = Push(Var(tree.nodes[0].name))
            elif isinstance(tree.nodes[0],Const):
                pushNode = Push(Con(tree.nodes[0].value))

            printNode = Call("print_int_nl")
            popStack = AddL((Con(4),Register("%esp")))
            IR.extend([pushNode,printNode,popStack])
    

    return IR
















