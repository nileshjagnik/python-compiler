from compiler.ast import *
from x86Nodes import *
from explicate import *



def generateOne(instr,assignmentVariable):

    vars = set([])

    if isinstance(instr,Add) or isinstance(instr, AddInt):
        if isinstance(instr.left,Name) and isinstance(instr.right,Name):
            tmp1 = Var(instr.left.name)
            tmp2 = Var(instr.right.name)
            vars.add(tmp1)
            vars.add(tmp2)
            moveNode = MovL((tmp1,assignmentVariable))
            addNode = AddL((tmp2,assignmentVariable))
            #return [moveNode,addNode],vars
            #IR.extend([moveNode,addNode])
                
        elif isinstance(instr.left,Name):
            tmp1 = Var(instr.left.name)
            tmp2 = Con(instr.right.value)
            vars.add(tmp1)
            moveNode = MovL((tmp1,assignmentVariable))
            addNode = AddL((tmp2,assignmentVariable))
            #return [moveNode,addNode],vars
            #IR.extend([moveNode,addNode])
    
        elif isinstance(instr.right,Name):
            tmp1 = Con(instr.left.value)
            tmp2 = Var(instr.right.name)
            vars.add(tmp2)
            moveNode = MovL((tmp1,assignmentVariable))
            addNode = AddL((tmp2,assignmentVariable))
            
            #IR.extend([moveNode,addNode])
        
        else:
            tmp1 = Con(instr.left.value)
            tmp2 = Con(instr.right.value)
            moveNode = MovL((tmp1,assignmentVariable))
            addNode = AddL((tmp2,assignmentVariable))
            #IR.extend([moveNode,addNode])
                
        return [moveNode,addNode],vars
    
            
    elif isinstance(instr,UnarySub):
        if isinstance(instr.expr,Name):
            tmp = Var(instr.expr.name)
            vars.add(tmp)
        else:
            tmp = Con(tree.expr.expr.value)

        moveNode = MovL((tmp,assignmentVariable))
        negNode = NegL(assignmentVariable)
        
        return [moveNode,negNode],vars
        
    elif isinstance(instr,Const):
        moveNode = MovL((Con(tree.expr.value),assignmentVariable))
        return [moveNode],vars
        
    elif isinstance(instr,Name):
        moveNode = MovL((Var(instr.name),assignmentVariable))
        vars.add(Var(instr.name))
        return [moveNode],vars
        
    
    elif isinstance(instr,CallFunc):
        funcNode = Call("input")
        moveNode = MovL((Register("%eax"),assignmentVariable))
        return [funcNode,moveNode],vars
        
    elif isinstance(instr,GetTag):
        if isinstance(instr.arg,Name):
            pushNode = Push(Var(instr.arg.name))
            vars.add(Var(instr.arg))
        elif isinstance(instr.arg,Const):
            pushNode = Push(Con(instr.arg))
            
        tagNode = Call("tag")
        popStack = AddL((Con(4),Register("%esp")))
        moveNode = MovL((Register("%eax"),assignmentVariable))
        return [pushNode,tagNode,popStack,moveNode],vars
        
    elif isinstance(instr,ProjectTo):
        type = instr.typ
        if isinstance(instr.arg,Name):
            pushNode = Push(Var(instr.arg.name))
            vars.add(Var(instr.arg.name))
        elif isinstance(instr.arg,Const):
            pushNode = Push(Con(instr.arg.value))
        if type == 'INT':
            projectNode = Call('project_int')
        elif type == 'BOOL':
            projectNode = Call('project_bool')
        else:
            projectNode = Call('project_big')
        
        popStack = AddL((Con(4),Register("%esp")))
        moveNode = MovL((Register("%eax"),assignmentVariable))
        return [pushNode,projectNode,popStack,moveNode],vars
    
    elif isinstance(instr,InjectFrom):
        type = instr.typ
        if isinstance(instr.arg,Name):
            pushNode = Push(Var(instr.arg.name))
            vars.add(Var(instr.arg.name))
        elif isinstance(instr.arg,Const):
            pushNode = Push(Con(instr.arg.value))
        if type == 'INT':
            injectNode = Call('inject_int')
        elif type == 'BOOL':
            injectNode = Call('inject_bool')
        else:
            injectNode = Call('inject_big')
        
        popStack = AddL((Con(4),Register("%esp")))
        moveNode = MovL((Register("%eax"),assignmentVariable))
        return ([pushNode,injectNode,popStack,moveNode],vars)
    
    elif isinstance(instr,Subscript):
        expr = instr.expr
        subs = instr.subs[0]
        pushCollection = Push(Var(expr))
        vars.add(Var(expr))
        
        if isinstance(subs,Name):
            pushNode = Push(Var(subs))
            vars.add(Var(subs))
        elif isinstance(subs,Const):
            pushNode = Push(Con(subs))
        subNode = Call('get_subscript')
        popStack = AddL((Con(4),Register("%esp")))
        moveNode = MovL((Register("%eax"),assignmentVariable))

        return [pushCollection,pushNode,subNode,popStack,moveNode]

    elif isinstance(instr,Dict):
        return [],vars #TODO
    elif isinstance(instr,List):
        createList = []
        nodes = instr.nodes
        pushNode = Push(Con(len(nodes)))
        callNode = Call('create_list')
        popStack = AddL((Con(4),Register("%esp")))
        moveNode = MovL((Register("%eax"),assignmentVariable))
        createList.extend([pushNode,callNode,popStack,moveNode])
        pushNode = Push(assignmentVariable)
        callNode = Call('inject_big') #make pyobj
        popStack = AddL((Con(4),Register("%esp")))
        moveNode = MovL((Register("%eax"),assignmentVariable))
        createList.extend([pushNode,callNode,popStack,moveNode])
        for (i,n) in enumerate(nodes):
            if isinstance(n,Name):
                vars.add(Var(n.name))
                pushNodeV = Push(Var(n.name))
            else:
                pushNodeV = Push(Con(n.value))
            pushNodeK = Push(Con(i))
            pushNodeL = Push(assignmentVariable)
            callNode = Call('set_subscript')
            popStack = AddL((Con(12),Register("%esp")))
            moveNode = MovL((Register("%eax"),assignmentVariable))
            createList.extend([pushNodeV,pushNodeK,pushNodeL,callNode,popStack,moveNode])

        return createList,vars
        


    elif isinstance(instr,Compare):
        print instr
        if instr.ops[0] == '==':
            if isinstance(instr.ops[1],Name) and isinstance(instr.expr,Name):
                compareNode = CmpL((Var(instr.expr.name),Var(instr.ops[1].name)))
                vars.add(Var(instr.expr.name))
                vars.add(Var(instr.ops[1].name))
            elif isinstance(instr.ops[1],Name):
                compareNode = CmpL((Con(instr.expr.value),Var(instr.ops[1].name)))
                vars.add(Var(instr.ops[1].name))
            elif isinstance(instr.expr,Name):
                compareNode = CmpL((Var(instr.expr.name),Con(instr.ops[1].value)))
                vars.add(Var(instr.expr.name))
            else:
                compareNode = CmpL((Con(instr.expr.name),Con(instr.ops[1])))

        elif instr.ops[0] == '!=':
            if isinstance(instr.ops[1],Name) and isinstance(instr.expr,Name):
                compareNode = CmpL((Var(instr.expr.name),Var(instr.ops[1].name)))
                vars.add(Var(instr.expr.name))
                vars.add(Var(instr.ops[1].name))
            elif isinstance(instr.ops[1],Name):
                compareNode = CmpL((Con(instr.expr.value),Var(instr.ops[1].name)))
                vars.add(Var(instr.ops[1].name))
            elif isinstance(instr.expr,Name):
                compareNode = CmpL((Var(instr.expr.name),Con(instr.ops[1].value)))
                vars.add(Var(instr.expr.name))
            else:
                compareNode = CmpL((Con(instr.expr.value),Con(instr.ops[1].value)))

        return [compareNode],vars

def generateAssign(tree):
   
    assignmentVariable = Var(tree.nodes[0].name)
       
    newIR,vars = generateOne(tree.expr,assignmentVariable)

    vars.add(assignmentVariable)
    return newIR,vars

def generatePrint(tree):
    vars = set([])
    if isinstance(tree.nodes[0],Name):
        pushNode = Push(Var(tree.nodes[0].name))
        vars.add(Var(tree.nodes[0].name))
    elif isinstance(tree.nodes[0],Const):
        pushNode = Push(Con(tree.nodes[0].value))
    
    printNode = Call("print_any")
    popStack = AddL((Con(4),Register("%esp")))
    return [pushNode,printNode,popStack],vars

def generateInstructions(astList):
    
    IR = []
    vars = set([])

    for tree in astList:
        if isinstance(tree,Assign):
            newIR,v = generateAssign(tree)
            IR.extend(newIR)
            vars = vars | v
        
        
        elif isinstance(tree,Printnl):
            newIR,v = generatePrint(tree)
            IR.extend(newIR)
            vars = vars | v
        

        elif isinstance(tree,If):
            newIR,newVars = generateIf(tree)
            IR.extend(newIR)
            vars = newVars | vars

                        
    return IR,vars

def generateIf(instr):
    
    vars = set([])
    s = []
    for x in instr.tests:
        
            
        if isinstance(x[0],Name):
            compare = CmpL((Con(0),Var(x[0].name)))
            vars.add(Var(x[0].name))
        else:
            compare = CmpL((Con(0),Con(x[0].value)))
        print "COMPARE"
        print compare
        IRif = []
        for n in x[1].nodes:
            if isinstance(n,Assign):
                print n
                newIR,v = generateAssign(n)
                IRif.extend(newIR)
                vars = vars | v
                print "NEW IR"
                print newIR
            elif isinstance(n,Printnl):
                newIR,v = generatePrint(n)
                IRif.extend(newIR)
                vars = vars | v
            
            else:
                newIR,newVars = generateIf(n)
                IRif.extend(newIR)
                vars = newVars | vars
            
        print "IR if"
        print IRif
        print "after dispact"
        print compare
        s.append((compare,IRif))

    IR=[]
    for e in instr.else_.nodes:
        if isinstance(n,Assign):
            newIR,v = generateAssign(n)
            
            IR.extend(newIR)
            vars = vars | v
        elif isinstance(n,Printnl):
            newIR,v = generatePrint(n)
            IR.extend(newIR)
            vars = vars | v
        
        else:
            newIR,newVars = generateIf(n)
            IR.extend(newIR)
            vars = newVars | vars


    return ([IfNode(s,IR)],vars)


def outputCode(instructionList,stackSize,filename):
    preamble = ".globl main\nmain:\n\tpushl %ebp\n\tmovl %esp, %ebp\n\t"
    postemble = 'movl $0, %eax\n\tleave\n\tret\n'
    stackspace = "subl $" + str(stackSize*4)+",%esp\n\n\t"
    
    assemblyCode = preamble
    assemblyCode += stackspace
    for i in instructionList:
        if i!=None:
            assemblyCode +=(str(i))+'\n\t'

    assemblyCode += postemble
    targetfile = open(filename+".s", "w")
    targetfile.truncate()
    targetfile.write(assemblyCode)
    targetfile.close()


'''
    elif isinstance(tree.expr,Subscript):
    #call func to get subscript
    
    elif isinstance(tree.expr,GetTag):
    #call func tag
    
    elif isinstance(tree.expr,ProjectTo):
    #call correct project function
    
    elif isinstance(tree.expr,InjectFrom):
    #call correct inject function
'''
















