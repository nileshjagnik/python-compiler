from compiler.ast import *

unLabel = 0

def uniquify(n,varmap):
    global unLabel
    if isinstance(n,Module):
        return Module(n.doc,uniquify(n.node,varmap))
    
    elif isinstance(n,Stmt):
        uni = []
        for x in n.nodes:
            uni.append(uniquify(x,varmap))
        return Stmt(uni)
    
    elif isinstance(n,Printnl):
        uni = []
        for x in n.nodes:
            uni.append(uniquify(x,varmap))
        return Printnl(uni,n.dest)
    
    elif isinstance(n,Assign):
        if isinstance(n.nodes[0],AssName):
            varmap[n.nodes[0].name] = unLabel
            n.nodes[0].name = "$$" + n.nodes[0].name + str(unLabel)
            unLabel += 1
        return Assign(n.nodes,uniquify(n.expr,varmap))
    
    elif isinstance(n,Discard):
        return Discard(uniquify(n.expr,varmap))
    
    elif isinstance(n,Function):
        varmap[n.name] = unLabel
        n.name = "$$" + n.name + str(unLabel)
        unLabel += 1
        
        funcvarmap = varmap.copy()
        arg = []
        for x in n.argnames:
            funcvarmap[x] = unLabel
            x = "$$" + x + str(unLabel)
            unLabel += 1
            arg.append(x)
        return Function(n.decorators, n.name, arg, n.defaults, n.flags, n.doc, uniquify(n.code,funcvarmap))
    
    elif isinstance(n,Lambda):
        funcvarmap = varmap.copy()
        arg = []
        for x in n.argnames:
            funcvarmap[x] = unLabel
            x = "$$" + x + str(unLabel)
            unLabel += 1
            arg.append(x)
        return Lambda(arg, n.defaults, n.flags, uniquify(n.code,funcvarmap))
        
    elif isinstance(n,Return):
        return Return(uniquify(n.value,varmap))
    
    elif isinstance(n,Const):
        return n
    
    elif isinstance(n,Name):
        if n.name == 'True' or n.name == 'False':
            return n
        return Name('$$'+n.name+str(varmap[n.name]))
        
    elif isinstance(n,Add):
        return Add((uniquify(n.left,varmap),uniquify(n.right,varmap)))
    
    elif isinstance(n,UnarySub):
        return UnarySub(uniquify(n.expr,varmap))
    
    elif isinstance(n,IfExp):
        return IfExp(uniquify(n.test,varmap),uniquify(n.then,varmap),uniquify(n.else_,varmap))
    
    elif isinstance(n,Subscript):
        return Subscript(uniquify(n.expr,varmap),n.flags,[uniquify(n.subs[0],varmap)])
    
    elif isinstance(n,List):
        return n
    
    elif isinstance(n,Dict):
        return n
        
    elif isinstance(n,Compare):
        return Compare(uniquify(n.expr,varmap),[n.ops[0][0],uniquify(n.ops[0][1],varmap)])
    
    elif isinstance(n,Or):
        orlist = []
        for x in n.nodes:
            orlist.append(uniquify(x,varmap))
        return Or(orlist)
    
    elif isinstance(n,And):
        andlist = []
        for x in n.nodes:
            andlist.append(uniquify(x,varmap))
        return And(andlist)
    
    elif isinstance(n,Not):
        return Not(uniquify(n.expr,varmap))
        
    elif isinstance(n,CallFunc):
        if n.node.name == 'input':
            return n
        arglist = []
        for x in n.args:
            arglist.append(uniquify(x,varmap))
        return CallFunc(uniquify(n.node,varmap),arglist)
        
    else:
        return n
    
