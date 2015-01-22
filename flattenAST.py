#import compiler
from compiler.ast import *

tempLabel=0
label="_tmp"
stackLocal = -4

def flatten(n,map):
    global tempLabel
    global stackLocal
    if isinstance(n, Module):
        return flatten(n.node,map)
    elif isinstance(n, Stmt):
        flat = []
        for x in n.nodes:
            t1 = flatten(x,map)
            flat.extend(t1)
        return flat
    
    elif isinstance(n, Printnl):
        flat = []
        for x in n.nodes:
            t1 = flatten(x,map)
            t = t1[-1]
            if isinstance(t,Const) or isinstance(t,Name):
                flat.append(Printnl(t,None))
            else:
                flat.extend(t1)
                flat.append(Printnl(Name(t.nodes.name),None))
        return flat
    
    elif isinstance(n, Assign):
        flat = []
        for x in n.nodes:
            t1 = flatten(n.expr,map)
            #print t1
            t = t1[-1]
            #print t
            if isinstance(t,Assign):
                flat.extend(t1)
                n1 = AssName(x.name,'OP_ASSIGN')
                newNode = Assign(n1,t.nodes.name)
                flat.append(newNode)
                map[x.name] = stackLocal
                stackLocal = stackLocal - 4
                return flat
            else:
                flat.append(x)
                map[x.name] = stackLocal
                stackLocal = stackLocal - 4
                return flat



    elif isinstance(n, AssName):
        return [n]
#still need to handle this
    elif isinstance(n, Discard):
        t = flatten(n.expr,map)
        t1 = t[-1]
        if isinstance(t1,Assign):
            newNode = Assign(AssName(label+str(tempLabel),'OP_ASSIGN',Name(t1.nodes.name)))
            tempLabel = tempLabel + 1
            return t.append(newNode)
        else:
            newNode = Assign(AssName(label+str(tempLabel),'OP_ASSIGN',t1))
            tempLabel = tempLabel + 1
            return [newNode]


    elif isinstance(n, Const):
        return [n]

    elif isinstance(n, Name):
        return [n]

    elif isinstance(n, Add):
        l = flatten(n.left,map)
        r = flatten(n.right,map)
        l1 = l[-1]
        r1 = r[-1]
        #print l1
        #print r1
        if isinstance(l1,Assign) and isinstance(r1,Assign):
            l.extend(r)
            l.append(Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),Add(Name(l1.nodes.name),Name(r1.nodes.name))))
            map[label+str(tempLabel)] = stackLocal
            stackLocal = stackLocal - 4
            tempLabel = tempLabel+1
            return l

        elif isinstance(r1,Assign):
            r.append(Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),Add((l1,Name(r1.nodes.name)))))
            map[label+str(tempLabel)] = stackLocal
            stackLocal = stackLocal - 4
            tempLabel = tempLabel+1
            return r
        elif isinstance(l1,Assign):
            l.append(Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),Add((Name(l1.nodes.name),r1))))
            map[label+str(tempLabel)] = stackLocal
            stackLocal = stackLocal - 4
            tempLabel = tempLabel+1
            return l
        else:
            #newNode = Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),Add((l1,r1)))
            #tempLabel = tempLabel+1
            return [n]
        
    elif isinstance(n, UnarySub):
        #print "usub"
        t1 = flatten(n.expr,map)
        t = t1[-1]
        #print t
        if isinstance(t,Const) or isinstance(t,Name):
            return [n]
        else:
            t1.append(Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),UnarySub(Name(t.nodes.name))))
            map[label+str(tempLabel)] = stackLocal
            stackLocal = stackLocal - 4
            tempLabel = tempLabel +1
            return t1

    #Very specific for this assignment
    elif isinstance(n, CallFunc):
        store = Assign(AssName(label+str(tempLabel),'OP_ASSIGN'),n)
        map[label+str(tempLabel)] = stackLocal
        stackLocal = stackLocal - 4
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
            return "print "   +"\n"
        
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







