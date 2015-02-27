from compiler.ast import *
from x86Nodes import *

def generateInstructions(astList):
    
    IR = []
    vars = set([])

    for tree in astList:
        if isinstance(tree,Assign):
            assignmentVariable = Var(tree.nodes[0].name)
            if isinstance(tree.expr,Add) or isinstance(tree.expr, AddInteger):
                if isinstance(tree.expr.left,Name) and isinstance(tree.expr.right,Name):
                    tmp1 = Var(tree.expr.left.name)
                    tmp2 = Var(tree.expr.right.name)
                    vars.add(tmp1)
                    vars.add(tmp2)
                        #if tmp1==tmp2:
                        #addNode = AddL((tmp1,tmp2))
                        #moveNode = MovL((tmp2,assignmentVariable))
                        #IR.extend([addNode,moveNode])
                        #else:
                    moveNode = MovL((tmp1,assignmentVariable))
                    addNode = AddL((tmp2,assignmentVariable))
                    IR.extend([moveNode,addNode])
                
                elif isinstance(tree.expr.left,Name):
                    tmp1 = Var(tree.expr.left.name)
                    tmp2 = Con(tree.expr.right.value)
                    vars.add(tmp1)
                    moveNode = MovL((tmp1,assignmentVariable))
                    addNode = AddL((tmp2,assignmentVariable))
                    IR.extend([moveNode,addNode])
                
                elif isinstance(tree.expr.right,Name):
                    tmp1 = Con(tree.expr.left.value)
                    tmp2 = Var(tree.expr.right.name)
                    vars.add(tmp2)
                    moveNode = MovL((tmp1,assignmentVariable))
                    addNode = AddL((tmp2,assignmentVariable))
                    IR.extend([moveNode,addNode])
                
                else:
                    tmp1 = Con(tree.expr.left.value)
                    tmp2 = Con(tree.expr.right.value)
                    moveNode = MovL((tmp1,assignmentVariable))
                    addNode = AddL((tmp2,assignmentVariable))
                    IR.extend([moveNode,addNode])
            
            
                vars.add(assignmentVariable)
                #print moveNode
                
                
        #print IR
        
            elif isinstance(tree.expr,UnarySub):
                if isinstance(tree.expr.expr,Name):
                    tmp = Var(tree.expr.expr.name)
                    vars.add(tmp)
                else:
                    tmp = Con(tree.expr.expr.value)
                moveNode = MovL((tmp,assignmentVariable))
                negNode = NegL(assignmentVariable)
                
                IR.extend([moveNode,negNode])
                vars.add(assignmentVariable)

            elif isinstance(tree.expr,Const):
                moveNode = MovL((Con(tree.expr.value),assignmentVariable))
                IR.extend([moveNode])
                vars.add(assignmentVariable)

            elif isinstance(tree.expr,Name):
                moveNode = MovL((Var(tree.expr.name),assignmentVariable))
                IR.extend([moveNode])
                vars.add(Var(tree.expr.name))
                vars.add(assignmentVariable)
            
            elif isinstance(tree.expr,Subscript):
            #call func to get subscript
            
            elif isinstance(tree.expr,GetTag):
            #call func tag
            
            elif isinstance(tree.expr,ProjectTo):
            #call correct project function
            
            elif isinstance(tree.expr,InjectFrom):
            #call correct inject function
            
            
                    
            elif isinstance(tree.expr,CallFunc):
                    args = tree.expr.args
                    name = tree.expr.args.node.name
                    funcNode = Call("name")
                    for a in args:
                        pushNode(a)
                    moveNode = MovL((Register("%eax"),assignmentVariable))
                    IR.extend([funcNode,moveNode])
                    vars.add(assignmentVariable)
                        
        elif isinstance(tree,Printnl):
            if isinstance(tree.nodes[0],Name):
                pushNode = Push(Var(tree.nodes[0].name))
                vars.add(Var(tree.nodes[0].name))
            elif isinstance(tree.nodes[0],Const):
                pushNode = Push(Con(tree.nodes[0].value))

            printNode = Call("print_any")
            popStack = AddL((Con(4),Register("%esp")))
            IR.extend([pushNode,printNode,popStack])

        elif isinstance(tree,If):
            if_ = []
            for x in tree.tests:
                s = []
                if isinstance(x[0],Name):
                    compare = Cmpl(Con(0),Var(x[0].name))
                    var.add(Var(x[0].name))
                else:
                    compare = Cmpl((Con(0),Con(x[0].value)))
                
                instrIf = []
                for stmt in x[1]:
                    (IRif,newVars).generateInstructions(stmt)
                    instr.add(IRif)
                    vars = vars | newVars
                s + [(compare,instrIf)]
        
            instrElse = []
            for e in tree.else_:
                (IRif,newVars).generateInstructions(e)
                instr.add(IRif)
                vars = vars | newVars

            IR.extend(If(s,instrElse))
                        

            

    return IR,vars

def outputCode(instructionList,stackSize,filename):
    preamble = ".globl main\nmain:\n\tpushl %ebp\n\tmovl %esp, %ebp\n\t"
    postemble = 'movl $0, %eax\n\tleave\n\tret\n'
    stackspace = "subl $" + str(stackSize*4)+",%esp\n\n\t"
    
    assemblyCode = preamble
    assemblyCode += stackspace
    for i in instructionList:
        assemblyCode +=(str(i))+'\n\t'

    assemblyCode += postemble
    targetfile = open(filename+".s", "w")
    targetfile.truncate()
    targetfile.write(assemblyCode)
    targetfile.close()

















