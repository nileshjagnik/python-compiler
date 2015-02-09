#Instruction : String (movl, addl, negl, call), print
#List of arguments: Name, Const



class Node:
    """Abstract base class for nodes"""
    def getInputs(self):
        pass #implemented by subclasses

class AddL(Node):
    def __init__(self,leftright):
        self.instruction = "addl"
        self.left = leftright[0]
        self.right = leftright[1]

    def getInputs(self):
            return self.left,self.right

    def __repr__(self):
        return "%s %s, %s" % (repr(self.instruction),repr(self.left), repr(self.right))

class MovL(Node):
    def __init__(self,leftright):
        self.instruction = "movl"
        self.left = leftright[0]
        self.right = leftright[1]

    def getInputs(self):
        return self.left,self.right

    def __repr__(self):
        return "%s %s,%s" % (repr(self.instruction),repr(self.left), repr(self.right))

class NegL(Node):
    def __init__(self,value):
        self.instruction = "negl"
        self.value = value

    def getInputs(self):
        return self.value

    def __repr__(self):
        return "%s %s" % (repr(self.instruction),repr(self.value))


class Call(Node):
    def __init__(self, funcName):
        self.instruction = "call"
        self.funcName = funcName

    def getInputs(self):
        return self.funcName

class Con(Node):
    def __init__(self,value):
        self.value = value

    def getInputs(self):
        return self.value

    def __repr__(self):
        return "$%s" % repr(self.value)

class Var(Node):
    def __init__(self,name):
        self.name = name
    
    def getInputs(self):
        return self.name
    
    def __repr__(self):
        return "%s" % repr(self.name)

    def __eq__(self,v):
        return self.name == v.name

    def __ne__(self,v):
        return self.name != v.name

    def __hash__(self):
        return hash(self.name)




