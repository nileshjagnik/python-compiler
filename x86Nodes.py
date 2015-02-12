#Instruction : String (movl, addl, negl, call), print
#List of arguments: Name, Const



class Instruction:
    """Abstract base class for instruction"""
    def getInputs(self):
        pass #implemented by subclasses

class AddL(Instruction):
    def __init__(self,leftright):
        self.instruction = "addl"
        self.left = leftright[0]
        self.right = leftright[1]

    def getInputs(self):
            return self.left,self.right

    def __repr__(self):
        return "%s %s, %s" % (repr(self.instruction),repr(self.left), repr(self.right))

class MovL(Instruction):
    def __init__(self,leftright):
        self.instruction = "movl"
        self.left = leftright[0]
        self.right = leftright[1]

    def getInputs(self):
        return self.left,self.right

    def __repr__(self):
        return "%s %s,%s" % (repr(self.instruction),repr(self.left), repr(self.right))

class NegL(Instruction):
    def __init__(self,value):
        self.instruction = "negl"
        self.value = value

    def getInputs(self):
        return self.value

    def __repr__(self):
        return "%s %s" % (repr(self.instruction),repr(self.value))


class Call(Instruction):
    def __init__(self, funcName):
        self.instruction = "call"
        self.funcName = funcName

    def getInputs(self):
        return self.funcName

    def __repr__(self):
            return "%s %s" % (repr(self.instruction),repr(self.funcName))

class Push(Instruction):
    def __init__(self,argument):
        self.instruction = "pushl"
        self.argument = argument
                          
    def getInputs(self):
        return self.argument
                          
    def __repr__(self):
        return "%s %s" % (repr(self.instruction),repr(self.argument))




class Operand:
    """Abstract base class for x86 operands"""


class Con(Operand):
    def __init__(self,value):
        self.value = value

    def __repr__(self):
        return "$%s" % repr(self.value)

    def __eq__(self,v):
        if isinstance(v,Con):
            return self.value == v.value
        else:
            return False
    
    def __ne__(self,v):
        if isinstance(v,Con):
            return self.value != v.value
        else:
            return True
    
    def __hash__(self):
        return hash(self.value)

class Var(Operand):
    def __init__(self,name):
        self.name = name
    
    def __repr__(self):
        return "%s" % repr(self.name)

    def __eq__(self,v):
        if isinstance(v,Var):
            return self.name == v.name
        else:
            return False
    
    def __ne__(self,v):
        if isinstance(v,Var):
            return self.name != v.name
        else:
            return True

    def __hash__(self):
        return hash(self.name)

class Register(Operand):
    def __init__(self,register):
        self.register = register

    def __repr__(self):
        return "%s" % repr(self.register)

    def __eq__(self,v):
        if isinstance(v,Register):
            return self.register == v.register
        else:
            return False
    
    def __ne__(self,v):
        if isinstance(v,Register):
            return self.register != v.register
        else:
            return True
    
    def __hash__(self):
        return hash(self.register)

class Address(Operand):
    def __init__(self,stackLocal):
        self.local = stackLocal
        self.address = str(local)+"%ebp"

    def __repr__(self):
        return "%s" % repr(self.address)
    
    def __eq__(self,v):
        if isinstance(v, Address):
            return self.address == v.address
        else:
            return False
    
    def __ne__(self,v):
        if isinstance(v, Address):
            return self.address != v.address
        else:
            return True
    
    def __hash__(self):
        return hash(self.address)




