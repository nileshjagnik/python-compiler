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
        preproc = []
        toPrint = []
        for exp in s.nodes:
            (pre,result) = explicate_expression(exp)
            preproc.extend(pre)
            toPrint.append(result)
        preproc + [Printnl(toPrint,None)]
    
    elif isinstance(s,Assign):
        #print s.nodes
        
        (pre,exp) = explicate_expression(s.expr)
        
        #target = s.nodes[0] #what am I identifier or subscript?
        #print isinstance(pre,list)
        #print len(pre)
        
        return pre + [Assign(s.nodes,exp)]

    
    elif isinstance(s,Discard):
        (pre,exp) = explicate_expression(s.expr)
        return pre + [(Discard(exp))]
    
def explicate_expression(e):
    global tempLabel
    if isinstance(e,Const):
        return ([],e)
    elif isinstance(e,Name):
        return ([],e)

    elif isinstance(e,UnarySub):
        (pre,result) = explicate_expression(e.expr)
        return (pre,UnarySub(explicate_expression(result)))
    
    elif isinstance(e,CallFunc):
        return ([],e)

    elif isinstance(e,Or): #assuming only one argument per side
        or_ = []
        pre = []
        for exp in e.nodes:
            (preE,r) = explicate_expression(exp)
            pre.extend(preE)
            or_.append(r)
        return (pre,IfExp(getGuard(or_[0]),or_[0],or_[1]))

    elif isinstance(e,And): #assuming only one argument per side
        #print e
        and_ = []
        pre = []
        for exp in e.nodes:
            (preE,r) = explcaite_expression(exp)
            pre.extend(preE)
            and_.append(r)
        return (pre,IfExp(getGuard(and_[0]),and_[1],and_[0]))

    
    elif isinstance(e,Not):
        (pre,result) = explicate_expression(e.expr)
        value = toPyobj(result)
        return ([],IfExp(getGuard(value),Name('False'),Name('True')))

    elif isinstance(e,Subscript):
        (preL,expr) = explicate_expression(e.expr)
        (preR,subs) = explicate_expression(e.subs)
        preL.extend(preR)
        return (preL,Subscript(expr,'OP_APPLY',subs))
                     

    elif isinstance(e,List):
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

    elif isinstance(e,Dict):
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

    elif isinstance(e,IfExp):
        (preT,test) = explicate_expression(e.test)
        (preTh,then) = explicate_expression(e.then)
        (preE,else_) = explicate_expression(e.else_)
        preT.extend(preTh)
        preT.extend(preE)
        return (preT,IfExp(getGuard(test),toPyobj(then),toPyObj(else_)))

    elif isinstance(e,Add):
        e1 = e.left
        e2 = e.right
        #print "here"
        if isinstance(e1,Const) and isinstance(e2,Const):
            return ([],AddInteger((e1,e2)))
        
        elif isinstance(e1,Name) and isinstance(e2,Name):
            andBig = bothBig(e1,e2)
            andPrimt = bothPrim(e1,e2)
                                  
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',e1),ProjectTo('big',e2)])),CallFunc(Name('error_pyobj'),"error: mismatch"))
            
            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',e1),ProjectTo('int',e2)))),elseNode)
                
            return ([],ifNode)

        elif isinstance(e1,Name) or isinstance(e1,Const):
            varNode = Name(label + str(tempLabel))
            tempLabel+=1
            
            andBig = bothBig(e1,varNode)
            andPrimt = bothPrim(e1,varNode)
            
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',e1),ProjectTo('big',varNode)])),CallFunc(Name('error_pyobj'),"error: mismatch"))
            
            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',e1),ProjectTo('int',varNode)))),elseNode)
            
            (pre,result) = explicate_Expression(e2)
            
            letNode = Let(varNode,result,ifNode)
                
            return (pre,letNode)

        elif isinstance(e2,Name) or isinstance(e2,Const):
            varNode = Name(label + str(tempLabel))
            tempLabel+=1
            
            andBig = bothBig(varNode,e2)
            andPrimt = bothPrim(varNode,e2)
            
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',varNode),ProjectTo('big',e2)])),CallFunc(Name('error_pyobj'),"error: mismatch"))
            
            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',varNode),ProjectTo('int',e2)))),elseNode)
            
            (pre,Result) = explicate_expression(e1)
            
            letNode = Let(varNode,result,ifNode)
            
            return (pre,letNode)

        else:
            varNode1 = Name(label+str(tempLabel))
            tempLabel+=1
            varNode2 = Name(label+str(tempLabel))
            tempLabel+=1
            
            andBig = bothBig(varNode1,varNode2)
            andPrim = bothPrim(varNode1,varNode2)
                
            elseNode = IfExp(andBig,InjectFrom('big',CallFunc(Name('add'),[ProjectTo('big',varNode1),ProjectTo('big',varNode2)])),CallFunc(Name('error_pyobj'),"error: mismatch"))

            ifNode = IfExp(andPrim,InjectFrom('int',AddInteger((ProjectTo('int',varNode1),ProjectTo('int',varNode2)))),elseNode)
            
            (pre1,result1) = explicate_expression(e1)
            (pre2,result2) = explicate_expression(e2)
            
            letNode = Let(varNode1,result1,Let(varNode2,result2,ifNode))
            
            return (pre1.extend(pre2),letNode)

    elif isinstance(e,Compare): #add lets
        (preL,expL) = explicate_expression(e.expr)
        (preR,expR) = explicate_expression(e.ops[0][1])
        
        if e.ops[0][0]=='==' or e.ops[0][0]=='!=':
            return (preL,extend(preR),Compare(expL,[(e.ops[0][0],expR)]))
        
        else: #dispatch
            return ([],e)


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

                         


    




