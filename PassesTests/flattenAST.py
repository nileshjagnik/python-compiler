#import compiler
from compiler.ast import *

tempLabel=0
label="$tmp"
stackLocal = -4

def flatten_ast(n,map):
    global tempLabel
    global stackLocal
    if isinstance(n, Module):
        return flatten_ast(n.node,map)
    
    elif isinstance(n, Stmt):
        flat = []
        #print "number of statements"
        #print len(n.nodes)
        for x in n.nodes:
            #print "statement"
            #print x
            (pre,result) = flatten_ast(x,map)
            #print "pre"
            #print pre
            
            flat.extend(pre)
            #print "FLAT"
            #for f in flat:
            #    print f
            #print
        return (flat,Name("DONE"))
    
    elif isinstance(n, Printnl):
        flat = []
        for x in n.nodes:
            (pre,result) = flatten_ast(x,map)
            #print result
            newNode = Printnl(result,None)
            flat.extend(pre)
            flat.append(newNode)
        return (flat,Name("Done Printing"))
            

    elif isinstance(n, Assign):
        (pre,result) = flatten_ast(n.expr,map)
        #print "pre"
        #print pre
        #print "result"
        #print result
        last = n.nodes[0].name
        for x in n.nodes:
            newNode = Assign(AssName(x.name,'OP_ASSIGN'),result)
            n = x.name
            pre.append(newNode)
            map[x.name] = stackLocal
            stackLocal = stackLocal - 4
        return (pre,last)

    elif isinstance(n, AssName):
        return ([],n)
#still need to handle this
    elif isinstance(n, Discard):
        (pre,result) = flatten_ast(n.expr,map)
        newName = label+str(tempLabel)
        newNode = Assign(AssName(newName,'OP_ASSIGN'),result)
        tempLabel = tempLabel+1
        pre.append(newNode)
        map[newName] = stackLocal
        stackLocal = stackLocal - 4
        return (pre,Name(newName))


    elif isinstance(n, Const):
        return ([],n)

    elif isinstance(n, Name):
        return ([],n)

    elif isinstance(n, Add):
        (preLeft,rLeft) = flatten_ast(n.left,map)
        (preRight,rRight) = flatten_ast(n.right,map)
        preLeft.extend(preRight)
        newName = label+str(tempLabel)
        newNode = Assign(AssName(newName,'OP_ASSIGN'),Add((rLeft,rRight)))
        map[newName] = stackLocal
        stackLocal = stackLocal - 4
        tempLabel = tempLabel+1
        preLeft.append(newNode)
        #print n
        return (preLeft,Name(newName))

    elif isinstance(n, UnarySub):
        (pre,result) = flatten_ast(n.expr,map)
        newName = label+str(tempLabel)
        newNode = Assign(AssName(newName,'OP_ASSIGN'),UnarySub(result))
        map[newName] = stackLocal
        stackLocal = stackLocal - 4
        tempLabel = tempLabel +1
        pre.append(newNode)
        return (pre,Name(newName))


    #Very specific for this assignment
    elif isinstance(n, CallFunc):
        newName = label+str(tempLabel)
        newNode = Assign(AssName(newName,'OP_ASSIGN'),n)
        map[newName] = stackLocal
        stackLocal = stackLocal - 4
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







