from compiler.ast import *
from explicateNodes import *

def free_vars(n):
    if isinstance(n, Stmt):
        frev = set([])
        bound = set([])
        for x in n.nodes:
            frev |= free_vars(x)
            if isinstance(x,Assign):
                if isinstance(x.nodes[0],AssName):
                    bound |= set([x.nodes[0].name]) 
        return frev-bound
    
    elif isinstance(n, Printnl):
        frev = set([])
        for x in n.nodes:
            frev |= free_vars(x)
        return frev
    
    elif isinstance(n, Assign):
        return free_vars(n.expr) - set([n.nodes[0].name])
    
    elif isinstance(n,Discard):
        return free_vars(n.expr)
    
    elif isinstance(n,Const):
        return set([])
        
    elif isinstance(n, Name):
        if n.name in ['True' , 'False' ,'add', 'not_equal', 'equal']:
            return set([])
        else:
            return set([n.name])
        
    elif isinstance(n, AddInt):
        return free_vars(n.left) | free_vars(n.right)
    
    elif isinstance(n, CallFunc):
        fv_args = [free_vars(e) for e in n.args]
        free_in_args = reduce(lambda a, b: a | b, fv_args, set([]))
        return free_vars(n.node) | free_in_args
    
    elif isinstance(n, Lambda):
        return free_vars(n.code) - set(n.argnames)
    
    elif isinstance(n,UnarySub):
        return free_vars(n.expr)
    
    elif isinstance(n,IfExp):
        return free_vars(n.test) |  free_vars(n.then) | free_vars(n.else_)
    
    elif isinstance(n,Subscript):
        return free_vars(n.expr) | free_vars(n.subs[0])
    
    elif isinstance(n,ProjectTo):
        return free_vars(n.arg)
    
    elif isinstance(n,InjectFrom):
        return free_vars(n.arg)
        
    elif isinstance(n,GetTag):
        return free_vars(n.arg)
    
    elif isinstance(n,Let):
        return (free_vars(n.rhs) | free_vars(n.body)) - set([n.var.name])
        
    elif isinstance(n,List):
        return set([])
    
    elif isinstance(n,Dict):
        return set([])
    
    elif isinstance(n,Compare):
        return free_vars(n.expr) | free_vars(n.ops[0][1])
    
    elif isinstance(n,Return):
        return free_vars(n.value)
