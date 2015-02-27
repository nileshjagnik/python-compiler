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

    elif isinstance(e,UnarySub):
        return UnarySub(explicate_expression(e.expr))
    
    elif isinstance(e,CallFunc):
        return e

    elif isinstance(e,Or): #assuming only one argument per side
        or_ = []
        for exp in e.nodes:
            r = explicate_expression(exp)
            or_.append(r)
        return IfExp(getGuard(or_[0]),or_[0],or_[1])

    elif isinstance(e,And): #assuming only one argument per side
        #print e
        and_ = []
        for exp in e.nodes:
            r = explcaite_expression(exp)
            and_.append(r)
        return IfExp(getGuard(and_[0]),and_[1],and_[0])

    
    elif isinstance(e,Not):
        result = explicate_expression(e.expr)
        value = toPyobj(result)
        return IfExp(getGuard(value),Name('False'),Name('True'))

    elif isinstance(e,Subscript):
        expr = explicate_expression(e.expr)
        subs = explicate_expression(e.subs[0])
        #print Subscript(expr,'OP_APPLY',[subs])
        return Subscript(expr,'OP_APPLY',[subs])
                     

    elif isinstance(e,List):
        elements = []
        for exp in e:
            elements.append(explicate_expression(exp))
        return List(elements)
        '''
        instr = []
        varName = label + str(tempLabel)
        tempLabel+=1
        op = CallFunc(Name('create_list'),[len(e.nodes)])
        list = Assign([AssName(varName,'OP_ASSIGN')],op)
        instr.append(list)
        for (i,exp) in enumerate(e.nodes):
            (pre,value) = explicate_expression(exp)
            instr.extend(pre)
            instr.append(CallFunc(Name('set_subscript'),[InjectFrom('big',Name(varName)),
                                                         InjectFrom('int',Const(i)),
                                                         toPyobj(value)]))

        return(instr,Name(varName))
        '''
    elif isinstance(e,Dict):
        
        dict = [] #potentially supported the adding of keys?
        print e
        for exp in e.items:
            value = explicate_expression(exp[1])
            key = explicate_expression(exp[0])
            dict.append((key,value))
        
        return Dict(dict)

        '''
        dict = [] #potentially supported the adding of keys?
        #print e
        varName = label + str(tempLabel)
        tempLabel+=1
        list = Assign([(AssName(varName),'OP_ASSIGN')],CallFunc(Name('create_dict'),[]))
        dict.append(list)
        for exp in e.items:
            (pre,value) = explicate_expression(exp[1])
            dict.append(pre)
            dict.append(CallFunc(Name('set_subscript'),[InjectFrom('big',Name(varName)),
                                                         InjectFrom('int',Const(exp[0])),
                                                         toPyObj(value)]))
        return (dict,Name(varName))
        '''

    elif isinstance(e,IfExp): #ADD LETS
        test = explicate_expression(e.test)
        then = explicate_expression(e.then)
        else_ = explicate_expression(e.else_)
     
        return IfExp(getGuard(test),toPyobj(then),toPyObj(else_))

    elif isinstance(e,Add):
        e1 = e.left
        e2 = e.right
        #print "here"
        if isinstance(e1,Const) and isinstance(e2,Const):
            return AddInteger((e1,e2))
        
        elif isinstance(e1,Name) and isinstance(e2,Name):
            andBig = bothBig(e1,e2)
            andPrim = bothPrim(e1,e2)
                                  
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',e1),ProjectTo('big',e2)])),CallFunc(Name('error_pyobj'),"error: mismatch"))
            
            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',e1),ProjectTo('int',e2)))),elseNode)
                
            return ifNode

        elif isinstance(e1,Name) or isinstance(e1,Const):
            varNode = Name(label + str(tempLabel))
            tempLabel+=1
            
            andBig = bothBig(e1,varNode)
            andPrim = bothPrim(e1,varNode)
            
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',e1),ProjectTo('big',varNode)])),CallFunc(Name('error_pyobj'),"error: mismatch"))
            
            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',e1),ProjectTo('int',varNode)))),elseNode)
            
            result = explicate_Expression(e2)
            
            letNode = Let(varNode,result,ifNode)
                
            return letNode

        elif isinstance(e2,Name) or isinstance(e2,Const):
            varNode = Name(label + str(tempLabel))
            tempLabel+=1
            
            andBig = bothBig(varNode,e2)
            andPrim = bothPrim(varNode,e2)
            
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',varNode),ProjectTo('big',e2)])),CallFunc(Name('error_pyobj'),"error: mismatch"))
            
            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',varNode),ProjectTo('int',e2)))),elseNode)
            
            result = explicate_expression(e1)
            
            letNode = Let(varNode,result,ifNode)
            
            return letNode

        else:
            varNode1 = Name(label+str(tempLabel))
            tempLabel+=1
            varNode2 = Name(label+str(tempLabel))
            tempLabel+=1
            
            andBig = bothBig(varNode1,varNode2)
            andPrim = bothPrim(varNode1,varNode2)
                
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',varNode1),ProjectTo('big',varNode2)])),CallFunc(Name('error_pyobj'),"error: mismatch"))

            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',varNode1),ProjectTo('int',varNode2)))),elseNode)
            
            result1 = explicate_expression(e1)
            result2 = explicate_expression(e2)
            
            letNode = Let(varNode1,result1,Let(varNode2,result2,ifNode))
            
            return letNode

    elif isinstance(e,Compare): #add lets
        expL = explicate_expression(e.expr)
        expR = explicate_expression(e.ops[0][1])
        
        if e.ops[0][0]=='==' or e.ops[0][0]=='!=':
            return Compare(expL,[(e.ops[0][0],expR)])
        
        else: #dispatch
            return e


def toPyobj(value):
    return IfExp(Compare(GetTag(value),[('==',Const(0))]),InjectFrom('int',value),
                 IfExp(Compare(GetTag(value),[('==',Const(1))]),InjectFrom('bool',value),
                       InjectFrom('big',value)))

def getGuard(value):
    return ProjectTo('bool',CallFunc(Name('is_true'),[toPyobj(value)]))

def bothBig(v1,v2):
    return IfExp(Compare(GetTag(v1),[('==',Const(3))]),
                 IfExp(Compare(GetTag(v2),[('==',Const(3))]),Name('True'),Name('False')),
                 Name('False'))

def bothPrim(v1,v2):
    return IfExp(Compare(GetTag(v1),[('=!',Const(3))]),
                 IfExp(Compare(GetTag(v2),[('=!',Const(3))]),Name('True'),Name('False')),
                 Name('False'))

                         


    




