from compiler.ast import *
from explicateNodes import *

INT = 0
BOOL = 1
BIG = 3

class explicateVisitor():
    def __init__(self):
        self.node = None
        self._cache = {}
        self.numtemp = 0
        
        
    def default(self, node):
        return node
            
    def walk(self, node):
        self.node = node
        return self.visitModule(node)
    
    
    def dispatch(self, node):
        if node is None:
            return None
        klass = node.__class__
        meth = self._cache.get(klass, None)
        if meth is None:
            className = klass.__name__
            meth = getattr(self, 'visit' + className, self.default)
            self._cache[klass] = meth
        return meth(node)
            
    def visitModule(self,node):
        return Module(node.doc,self.dispatch(node.node))
    
    def visitStmt(self,node):
        nodelist = []
        for n in node.nodes:
            nodelist.append(self.dispatch(n))
        return Stmt(nodelist)
    
    def visitPrintnl(self,node):
        nodelist=[]
        for n in node.nodes:
            nodelist.append(self.dispatch(n))
        return Printnl(nodelist,node.dest)
        
    def visitAssign(self,node):
        nodelist=[]
        for n in node.nodes:
            nodelist.append(self.dispatch(n))
        return Assign(nodelist,self.dispatch(node.expr))
    
    def visitAssName(self,node):
        return node
    
    def visitDiscard(self,node):
        return Discard(self.dispatch(node.expr))
    
    def visitConst(self,node):
        if node.value == 'True' or node.value=='False':
            return InjectFrom('BOOL',node)
        return InjectFrom('INT', node)
    
    def visitName(self,node):
        if node.name == 'True' or node.name == 'False':
            return InjectFrom('BOOL',node)
        return node
        
    def visitUnarySub(self,node):
        return UnarySub(self.dispatch(node.expr))
        
    def visitCallFunc(self, node):
        nodelist=[]
        for n in node.args:
            nodelist.append(self.dispatch(n))
        if node.node.name == 'input':
            return InjectFrom('INT',CallFunc(self.dispatch(node.node),nodelist))
        return CallFunc(self.dispatch(node.node),nodelist)
        
    def visitAdd(self, node):
        letcount = 0
        
        lftexp = self.dispatch(node.left)
        if not (isinstance(node.left, Name) or isinstance(node.left, Const)):
            lft = Name('$addtemp'+str(self.numtemp))
            self.numtemp = self.numtemp + 1
            letcount = letcount + 1
        else:
            lft = lftexp
        
        rgtexp = self.dispatch(node.right)
        if not (isinstance(node.right, Name) or isinstance(node.right, Const)):
            rgt = Name('$addtemp'+str(self.numtemp))
            self.numtemp = self.numtemp + 1
            letcount = letcount + 1
        else:
            rgt = rgtexp
        
        n1 = Compare(GetTag(lft),[('==', Const(INT))])
        n2 = Compare(GetTag(lft),[('==', Const(BOOL))])
        ifvalcond1 = IfExp(CallFunc(Name('is_true'),[n1]),n1,n2)
        
        n1 = Compare(GetTag(rgt),[('==', Const(INT))])
        n2 = Compare(GetTag(rgt),[('==', Const(BOOL))])
        ifvalcond2 = IfExp(CallFunc(Name('is_true'),[n1]),n1,n2)
        ifval = IfExp(CallFunc(Name('is_true'),[ifvalcond1]),ifvalcond2,ifvalcond1)
        
        thenval = InjectFrom('INT', AddInt((ProjectTo('INT',lft),ProjectTo('INT',rgt))))
        
        n1 = Compare(GetTag(lft),[('==', Const(BIG))])
        n2 = Compare(GetTag(rgt),[('==', Const(BIG))])
        elseval = IfExp(IfExp(CallFunc(Name('is_true'),[n1]),n2,n1),InjectFrom('BIG', CallFunc(Name('add'),[ProjectTo('BIG',lft),ProjectTo('BIG',rgt)])) , CallFunc(Name('$error'),[]))
        
        if letcount == 1:
            if lft==lftexp:
                return Let(rgt,rgtexp,IfExp(ifval,thenval,elseval))
            else:
                return Let(lft,lftexp,IfExp(ifval,thenval,elseval))
        elif letcount == 2:
            return Let(lft,lftexp,Let(rgt,rgtexp,IfExp(ifval,thenval,elseval)))
        return IfExp(ifval,thenval,elseval)
    
    def visitList(self, node):
        nodelist=[]
        for n in node.nodes:
            nodelist.append(self.dispatch(n))
        if len(nodelist)==0:
            nodelist=node.nodes
        return InjectFrom('BIG',List(nodelist))
    
    def visitDict(self, node):
        nodelist=[]
        for n in node.items:
            nodelist.append((self.dispatch(n[0]),self.dispatch(n[1])))
        if len(nodelist)==0:
            nodelist=node.items
        return InjectFrom('BIG',Dict(nodelist))
        
    def visitOr(self,node):
        n1 = self.dispatch(node.nodes[0])
        n2 = self.dispatch(node.nodes[1])
        return IfExp(CallFunc(Name('is_true'),[n1]),n1,n2)
    
    def visitAnd(self,node):
        n1 = self.dispatch(node.nodes[0])
        n2 = self.dispatch(node.nodes[1])
        return IfExp(CallFunc(Name('is_true'),[n1]),n2,n1)
    
    def visitNot(self,node):
        return IfExp(CallFunc(Name('is_true'),[self.dispatch(node.expr)]), InjectFrom('BOOL', Name('False')),InjectFrom('BOOL', Name('True')))
    
    def visitIfExp(self,node):
        return IfExp(ProjectTo('BOOL',self.dispatch(node.test)),self.dispatch(node.then),self.dispatch(node.else_))
    
    def visitCompare(self,node):
        nodelist = []
        for n in node.ops:
            no = self.dispatch(n[1])
            tag = no.typ
            nodelist.append((n[0],ProjectTo(tag,no)))
        if len(nodelist)==0:
            nodelist=node.ops
        return InjectFrom('BOOL', Compare(ProjectTo('INT',self.dispatch(node.expr)),nodelist))
    
    def visitSubscript(self,node):
        nodelist = []
        for n in node.subs:
            nodelist.append(self.dispatch(n))
        if len(nodelist)==0:
            nodelist=node.subs
        return Subscript(self.dispatch(node.expr),'OP_ASSIGN',nodelist)
