#import compiler
from compiler.ast import *
from explicate import *

tempLabel=0
label="$tmp"


def flatten_module(n):
   
    if isinstance(n, Module):
        return flatten_module(n.node)

    elif isinstance(n, Stmt):
        flat = []
        #print "number of statements"
        #print len(n.nodes)
        for x in n.nodes:
            print x
            print "here"
            print
            pre = flatten_statement(x)
            #print
            #print pre
            #print pre
            flat.extend(pre)
    
        return flat

def flatten_statement(s):
    if isinstance(s, Printnl):
        flat = []
        for x in s.nodes:
            (pre,result) = flatten_expression(x)
            #print result
            newNode = Printnl([result],None)
            flat.extend(pre)
            flat.append(newNode)
        return flat


    elif isinstance(s, Assign):
        (pre,result) = flatten_expression(s.expr)
        last = s.nodes[0].name
        for x in s.nodes:
            newNode = Assign([AssName(x.name,'OP_ASSIGN')],result)
            last = x.name
            pre.append(newNode)

        return pre

    elif isinstance(s,Discard):
        (pre,result) = flatten_expression(n.expr,map)
        return pre


def flatten_expression(e):
    global tempLabel
    if isinstance(e, AssName):
        return ([],e)

    elif isinstance(e, Const):
        return ([],e)
    
    elif isinstance(e, Name):
        return ([],e)
    
    elif isinstance(e, Add):
        (preLeft,rLeft) = flatten_expression(e.left)
        (preRight,rRight) = flatten_expression(e.right)
        preLeft.extend(preRight)
        newName = label+str(tempLabel)
        newNode = Assign([AssName(newName,'OP_ASSIGN')],Add((rLeft,rRight)))
        tempLabel = tempLabel+1
        preLeft.append(newNode)
        #print n
        return (preLeft,Name(newName))

    elif isinstance(e, AddInteger):
        (preLeft,rLeft) = flatten_expression(e.left)
        (preRight,rRight) = flatten_expression(e.right)
        preLeft.extend(preRight)
        newName = label+str(tempLabel)
        newNode = Assign([AssName(newName,'OP_ASSIGN')],AddInteger((rLeft,rRight)))
        tempLabel = tempLabel+1
        preLeft.append(newNode)
        #print n
        return (preLeft,Name(newName))
    
    elif isinstance(e, UnarySub):
        (pre,result) = flatten_expression(e.expr)
        newName = label+str(tempLabel)
        newNode = Assign([AssName(newName,'OP_ASSIGN')],UnarySub(result))
        tempLabel = tempLabel +1
        pre.append(newNode)
        return (pre,Name(newName))
    
    
    #Very specific for this assignment
    elif isinstance(e, CallFunc):
        print "HERE"
        newName = label+str(tempLabel)
        newNode = Assign([AssName(newName,'OP_ASSIGN')],e)
        print "new Node"
        print newNode
        tempLabel = tempLabel+1
        return ([newNode],Name(newName))


    elif isinstance(e,IfExp):
        (preTest,resultTest) = flatten_expression(e.test)
        #(preThen,resultThen) = flatten_expression(e.then)
        #(preElse,resultElse) = flatten_expression(e.else_)
        #newNameTest = label+str(tempLabel)
        #newNode = Assign([AssName(newNameTest,'OP_ASSIGN')],resultTest)
        #tempLabel+=1
        
        newNameResult = label+str(tempLabel)
        (preThen,resultThen) = flatten_expression(e.then)
        (preElse,resultElse) = flatten_expression(e.else_)
        newNodeThen = Assign([AssName(newNameResult,'OP_ASSIGN')],resultThen)
        newNodeElse = Assign([AssName(newNameResult,'OP_ASSIGN')],resultElse)
        tempLabel+=1
        preThen.append(newNodeThen)
        preElse.append(newNodeElse)
        ifNode = If([resultTest,Stmt(preThen)],Stmt(preElse))
        
        preTest.append(ifNode)
        return(preTest,Name(newNameResult))

    elif isinstance(e,Compare): #dispacth TODO
        #print e.ops[0]
        #print e.expr
        #print isinstance(e.expr,GetTag)
        (preLeft,rLeft) = flatten_expression(e.expr)
        
        (preRight,rRight) = flatten_expression(e.ops[0][1])
        newOps = (e.ops[0][0],rRight)
        #print newOps
        #e.ops[0][1] = rRight
        
        newName = label+str(tempLabel)
        newNode = Assign([AssName(newName,'OP_ASSIGN')],Compare(rLeft,newOps))
        tempLabel = tempLabel +1
    
        preLeft.extend(preRight)
        preLeft.append(newNode)
        return (preLeft,Name(newName)) #do i think this is correct?



    
    elif isinstance(e,Subscript):
        return ([],e)
    
    elif isinstance(e,ProjectTo):
        (pre,result) = flatten_expression(e.arg)
        #newName = label+str(tempLabel)
        #newNode = Assign([AssName(newName,'OP_ASSIGN')],ProjectTo(e.typ,result))
        #tempLabel = tempLabel +1
        newNode = ProjectTo(e.typ,result)
        #pre.append(newNode)
        return (pre,newNode)

    elif isinstance(e,InjectFrom):
        (pre,result) = flatten_expression(e.arg)
        '''
        newName = label+str(tempLabel)
        newNode = Assign([AssName(newName,'OP_ASSIGN')],InjectFrom(e.typ,result))
        tempLabel = tempLabel +1
        pre.append(newNode)

        return (pre,Name(newName))
        '''
        newNode = InjectFrom(e.typ,result)
        return (pre,newNode)

    elif isinstance(e,GetTag):
        #print e
        (pre,result) = flatten_expression(e.arg)
        '''
        newName = label+str(tempLabel)
        newNode = Assign([AssName(newName,'OP_ASSIGN')],GetTag(result))
        tempLabel = tempLabel +1
        pre.append(newNode)

        return (pre,Name(newName))
        '''

        newNode = GetTag(result)
        return (pre,newNode)

    elif isinstance(e,Let):
        (pre,resultLet) = flatten_expression(e.rhs)
        newNode = Assign([AssName(e.var,'OP_ASSIGN')],resultLet)
        pre.append(newNode)
        (preBody,resultBody) = flatten_expression(e.body)
        newName = label+str(tempLabel)
        newNodeResult = Assign([AssName(newName,'OP_ASSIGN')],resultBody)
        tempLabel = tempLabel +1
        pre.extend(preBody)
        pre.append(newNodeResult)
        return(pre,Name(newName))
    else:
        x = "nothing"
    
    
def prettyPrint(n):
    if isinstance(n, Module):
        return ""
        
    elif isinstance(n, Stmt):
        return ""
        
    elif isinstance(n, Printnl):
        return "print " + prettyPrint(n.nodes[0]) +"\n"
        
    elif isinstance(n, Assign):
        for x in n.nodes:
            return "name"+ " = " + prettyPrint(n.expr) +"\n"
    
    elif isinstance(n, AssName):
        return ""
#still need to handle this
    elif isinstance(n, Discard):
        return ""
    elif isinstance(n, Const):
        return str(n.value)
    elif isinstance(n, Name):
        return n.name
    elif isinstance(n, Add):
        return prettyPrint(n.left) + " + " +prettyPrint(n.right)
        
    elif isinstance(n, UnarySub):
        return "- " + prettyPrint(n.expr)
        
        
    #Very specific for this assignment
    elif isinstance(n, CallFunc):
        return "input() "
    else:
        x =  "error"

'''
    elif isinstance(e,And): #TODO
    
    (preLeft,resultLeft) = flatten_expression(e.nodes[0])
    (preRight,resultRight) = flatten_expression(e.nodes[1])
    preRight.append(resultRight) #may be unnecessary or wrong?
    
    ifNode = If([resultLeft,Stmt(preRight)],Stmt([resultLeft]))
    
    newName = label + str(tempLabel)
    newNode = Assign([AssName(newName,'OP_ASSIGN')],ifNode)
    tempLabel+=1
    
    preLeft.append(ifNode)
    preLeft.append(newNode)
    return (preLeft,Name(newName))
    
    elif isinstance(e,Or): #TODO
    
    (preLeft,resultLeft) = flatten_expression(e.nodes[0])
    (preRight,resultRight) = flatten_expression(e.nodes[1])
    preRight.append(resultRight) #may be unnecessary or wrong?
    
    ifNode = If([resultLeft,Stmt([resultLeft])],Stmt(preRight))
    
    newName = label + str(tempLabel)
    newNode = Assign([AssName(newName,'OP_ASSIGN')],ifNode)
    tempLabel+=1
    
    preLeft.append(ifNode)
    preLeft.append(newNode)
    return (preLeft,Name(newName))
    
    elif isinstance(e,Not):
    (pre,result) = flatten_expression(e.expr)
    newNode = Not(result)
    return (pre,newNode)
    
    elif isinstance(e,List):
    preProc = []
    flatList = []
    for n in e.nodes:
    (pre,result) = flatten_Expression(n)
    preProc.extend(pre)
    flatList.append(result)
    
    newName = label+str(tempLabel)
    newNode = Assign([AssName(newName,'OP_ASSIGN')],List(flatList))
    tempLabel = tempLabel +1
    preProc.append(newNode)
    
    return (preProc,Name(newName))
    
    elif isinstance(e,Dict): #TODO, is this unneccessary???
    newDict = []
    newPre = []
    for i in e.items:
    (pre,result) = flatten_expression(i[1])
    newDict.append((i[0],result))
    newPre.extend(pre)
    
    newName = label+str(tempLabel)
    newNode = Assign([AssName(newName,'OP_ASSIGN')],Dict(newDict))
    tempLabel = tempLabel +1
    
    return (newPre,Name(newName))
'''





