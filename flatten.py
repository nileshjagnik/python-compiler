#import compiler
from compiler.ast import *

tempLabel=0
label="$tmp"


def flatten(n):
   
    if isinstance(n, Module):
        return flatten(n.node,map)

    elif isinstance(n, Stmt):
        flat = []
        #print "number of statements"
        #print len(n.nodes)
        for x in n.nodes:
            pre = flatten_statement(x)
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
    
    elif isinstance(e, UnarySub):
        (pre,result) = flatten_expression(e.expr)
        newName = label+str(tempLabel)
        newNode = Assign([AssName(newName,'OP_ASSIGN')],UnarySub(result))
        tempLabel = tempLabel +1
        pre.append(newNode)
        return (pre,Name(newName))
    
    
    #Very specific for this assignment
    elif isinstance(e, CallFunc):
        newName = label+str(tempLabel)
        newNode = Assign([AssName(newName,'OP_ASSIGN')],e)
        tempLabel = tempLabel+1
        return ([newNode],Name(newName))
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







