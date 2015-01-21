#import compiler
from compiler.ast import *

tempLabel=0
label="_tmp"

def flatten(n):
    global tempLabel
    if isinstance(n, Module):
        return flatten(n.node)
    elif isinstance(n, Stmt):
        flat = []
        for x in n.nodes:
            t1 = flatten(x)
            flat.extend(t1)
        return flat

    elif isinstance(n, Printnl):
        flat = []
        for x in n.nodes:
            t1 = flatten(x)
            t = t1[-1]
            if isinstance(t,Const):
                flat.append(Printnl(t,None))
            else:
                flat.extend(t1)
                flat.append(Printnl(t.nodes.name,None))
        return flat

    elif isinstance(n, Assign):
        flat = []
        for x in n.nodes:
            t1 = flatten(n.expr)
            t = t1[-1]
            if isinstance(t,Const):
                flat.append(n)
            else:
                flat.extend(t1)
                flat.append(Assign(AssName(x.name,'OP_ASSIGN'),Name(t.nodes.name)))
        return flat
    elif isinstance(n, AssName):
        return [n]
#still need to handle this
    elif isinstance(n, Discard):
        return []
    elif isinstance(n, Const):
        return [n]
    elif isinstance(n, Name):
        return [n]
    elif isinstance(n, Add):
        l = flatten(n.left)
        r = flatten(n.right)
        l1 = l[-1]
        r1 = r[-1]
        if isinstance(l1,Const) and isinstance(r1,Const):
            newNode = Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),Add(l1,r1))
            tempLabel = tempLabel+1
            return newNode
        elif isinstance(l1,Const):
            r.append(Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),Add((l1,Name(r1.nodes.name)))))
            tempLabel = tempLabel+1
            return r
        elif isinstance(r1,Const):
            l.append(Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),Add((Name(l1.nodes.name),r1))))
            tempLabel = tempLabel+1
            return l
        else:
            l.extend(r)
            l.append(Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),Add(Name(l1.nodes.name),Name(r1.nodes.name))))
            tempLabel = tempLabel+1
            return l

    elif isinstance(n, UnarySub):
        t1 = flatten(n.expr)
        t = t1[-1]
        if isinstance(t,Const):
            return [n]
        else:
            t1.append(Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),UnarySub(Name(t.nodes.name))))
            tempLabel = tempLabel +1
            return t1

#Very specific for this assignment
    elif isinstance(n, CallFunc):
        store = Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),n)
        tempLabel = tempLabel+1
        return [store]
    else:
        print "error"


def prettyPrint(n):
    if isinstance(n, Module):
        return ""
    
    elif isinstance(n, Stmt):
        return ""

    elif isinstance(n, Printnl):
        return "print "  +"\n"
    
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
        print "error"







