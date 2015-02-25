from compiler.ast import *

tempLabel=0
label="#tmp"

class GetTag(Node):
    def __init__(self,arg):
        self.arg = arg

    def getChildren(self):
        return self.arg
    
    def getChildNodes(self):
        return self.arg
    
    def __repr__(self):
        return "GetTag(%s)" % (repr(self.arg))

class InjectFrom(Node):
    def __init__(self,typ,arg):
        self.typ = typ
        self.arg = arg

    def getChildren(self):
        return self.typ, self.arg
    
    def getChildNodes(self):
        return self.typ, self.arg
    
    def __repr__(self):
        return "InjectFrom(%s, %s)" % (repr(self.typ), repr(self.arg))

class ProjectTo(Node):
    def __init__(self,typ,arg):
        self.typ = typ
        self.arg = arg

    def getChildren(self):
        return self.typ, self.arg
    
    def getChildNodes(self):
        return self.typ, self.arg
    
    def __repr__(self):
        return "ProjectTo(%s, %s)" % (repr(self.typ), repr(self.arg))

class Let(Node):
    def __init__(self,var,rhs,body):
        self.var = var
        self.rhs = rhs
        self.body = body

    def getChildren(self):
        children = []
        children.append(self.var)
        children.append(self.rhs)
        children.extend(flatten(self.body))
        return tuple(children)
    
    def getChildNodes(self):
        nodeList = []
        children.append(self.var)
        children.append(self.rhs)
        children.extend(flatten_nodes(self.body))
        return tuple(nodeList)
    
    def __repr__(self):
        return "Let(%s, %s, %s)" % (repr(self.var), repr(self.rhs),repr(self.body))

class AddInteger(Node):
    def __init__(self,(left,right)):
        self.left = left
        self.right = right

    def getChildren(self):
        return self.left, self.right

    def getChildNodes(self):
        return self.left, self.right
            
    def __repr__(self):
        return "AddInteger((%s, %s))" % (repr(self.left), repr(self.right))

def explicate(astNode):
    if isinstance(astNode,Module):
        return Module(None,explicate(astNode.node))
    
    elif isinstance(astNode,Stmt):
        stmts = []
        for n in astNode.nodes:
            stmts.append(explicate_statement(n))

        return Stmt(stmts)

def explicate_statement(s):
    if isinstance(s,Printnl):
        toPrint = []
        for exp in s.nodes:
            toPrint.append(explicate_expression(exp))
        return Printnl(toPrint,None)
    
    elif isinstance(s,Assign):
        #print s.nodes
        exp = explicate_expression(s.expr)
        #target = s.nodes[0] #what am I identifier or subscript?
        return Assign(s.nodes,exp)
    
    elif isinstance(s,Discard):
        return Discard(explicate_expression(s.expr))
    
def explicate_expression(e):
    global tempLabel
    if isinstance(e,Const):
        return e
    elif isinstance(e,Name):
        return e
    elif isinstance(e,Compare):
        expL = explicate_expression(e.expr)
        expR = explicate_expression(e.ops[1])
        e.ops[1] = expR
        return Compare(expL,e.ops)

    elif isinstance(e,Or): #assuming only one argument per side
        or_ = []
        for exp in e.nodes:
            or_.append(explicate_expression[exp])
        return Or(or_)

    elif isinstance(e,And): #assuming only one argument per side
        and_ = []
        for exp in e.nodes:
            and_.append(explicate_expression[exp])
        return And(and_)
    
    elif isinstance(e,Not):
        return Not(ProjectTo('bool',explicate_expression(e.expr)))

    elif isinstance(e,Subscript):
        expr = explicate_expression(e.expr)
        subs = explicate_expression(e.subs)
        return Subscript(expr,'OP_APPLY',subs)

    elif isinstance(e,List):
        elements = []
        for exp in e:
            elements.extend(explicate_expression(exp))
        return List(elements)

    elif isinstance(e,Dict):
        dict = [] #potentially supported the adding of keys?
        print e
        for exp in e.items:
            
            value = explicate_expression(exp[1])
            #print value
            dict.append((exp[0],value))

        return Dict(dict)

    elif isinstance(e,IfExp):
        test = ProjectTo('bool',explicate_expression(e.test))
        then = explicate_expression(e.then)
        else_ = explicate_expression(e.else_)
        return IfExp(test,then,else_)

    elif isinstance(e,Add):
        e1 = e.left
        e2 = e.right
        #print "here"
        if isinstance(e1,Const) and isinstance(e2,Const):
            return AddInteger((e1,e2))
        
        elif isinstance(e1,Name) and isinstance(e2,Name):
            andBig = And([Compare(GetTag(e1),[('==',Const(3))]),
                                  Compare(GetTag(e2),[('==',Const(3))])])
            andPrim = And([Or([Compare(GetTag(e1),[('==',Const(1))]),
                               Compare(GetTag(e1),[('==',Const(2))])]),
                           Or([Compare(GetTag(e2),[('==',Const(1))]),
                               Compare(GetTag(e2),[('==',Const(2))])])])
                                  
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',e1),ProjectTo('big',e2)])),CallFunc(Name('error_pyobj'),"error: mismatch"))
            
            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',e1),ProjectTo('int',e2)))),elseNode)
                
            return ifNode

        elif isinstance(e1,Name) or isinstance(e1,Const):
            varNode = Name(label + str(tempLabel))
            tempLabel+=1
            andBig = And([Compare(GetTag(e1),[('==',Const(3))]),
                          Compare(GetTag(varNode),[('==',Const(3))])])
            andPrim = And([Or([Compare(GetTag(e1),[('==',Const(1))]),
                               Compare(GetTag(e1),[('==',Const(2))])]),
                           Or([Compare(GetTag(varNode),[('==',Const(1))]),
                               Compare(GetTag(varNode),[('==',Const(2))])])])
            
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',e1),ProjectTo('big',varNode)])),CallFunc(Name('error_pyobj'),"error: mismatch"))
            
            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',e1),ProjectTo('int',varNode)))),elseNode)
            
            letNode = Let(varNode,explicate_expression(e2),ifNode)
                
            return letNode

        elif isinstance(e2,Name) or isinstance(e2,Const):
            varNode = Name(label + str(tempLabel))
            tempLabel+=1
            
            andBig = And([Compare(GetTag(varNode),[('==',Const(3))]),
                          Compare(GetTag(e2),[('==',Const(3))])])

            andPrim = And([Or([Compare(GetTag(varNode),[('==',Const(1))]),
                               Compare(GetTag(varNode),[('==',Const(2))])]),
                           Or([Compare(GetTag(e2),[('==',Const(1))]),
                               Compare(GetTag(e2),[('==',Const(2))])])])
            
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',varNode),ProjectTo('big',e2)])),CallFunc(Name('error_pyobj'),"error: mismatch"))
            
            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',varNode),ProjectTo('int',e2)))),elseNode)
            
            letNode = Let(varNode,explicate_expression(e1),ifNode)
            
            return letNode

        else:
            varNode1 = Name(label+str(tempLabel))
            tempLabel+=1
            varNode2 = Name(label+str(tempLabel))
            tempLabel+=1
            
            andBig = And([Compare(GetTag(varNode1),[('==',Const(3))]),
                          Compare(GetTag(varNode2),[('==',Const(3))])])
                             
            andPrim = And([Or([Compare(GetTag(varNode1),[('==',Const(1))]),
                               Compare(GetTag(varNode1),[('==',Const(2))])]),
                           Or([Compare(GetTag(varNode2),[('==',Const(1))]),
                               Compare(GetTag(varNode2),[('==',Const(2))])])])
                
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',varNode1),ProjectTo('big',varNode2)])),CallFunc(Name('error_pyobj'),"error: mismatch"))

            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',varNode1),ProjectTo('int',varNode2)))),elseNode)
            
            letNode = Let(varNode1,explicate_expression(e1),Let(varNode2,explicate_expression(e2),ifNode))
            
            return letNode
        
    elif isinstance(e,UnarySub):
        return UnarySub(explicate_expression(e.expr))
                             
    elif isinstance(e,CallFunc):
        return e
                                                                                








