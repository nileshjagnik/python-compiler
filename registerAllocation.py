from compiler.ast import *
from x86Nodes import *
from x86IR import *

def livenessAnalysis(instructionList):
    live = [set() for index in range(len(instructionList)+1)]
    livePoint = len(instructionList)-1
    for i in reversed(instructionList):
        if isinstance(i,AddL):
            if isinstance(i.left,Var):
                live[livePoint] = (live[livePoint+1]-set([i.right]))|set([i.left,i.right])
            elif isinstance(i.right,Register):
                live[livePoint] = (live[livePoint+1]-set([i.right]))
            else:
                live[livePoint] = (live[livePoint+1]-set([i.right]))|set([i.right])
        elif isinstance(i,MovL):
            if isinstance(i.left,Var):
                live[livePoint]= (live[livePoint+1]-set([i.right]))|set([i.left])
            
            else:
                live[livePoint] = (live[livePoint+1]-set([i.right]))
        elif isinstance(i,NegL):
            live[livePoint] = (live[livePoint+1]-set([i.value]))|set([i.value])
        elif isinstance(i,Push):
            live[livePoint] = (live[livePoint+1])|set([i.argument])
        livePoint = livePoint-1

    return live

def interferenceGraph(instructionList,livenessSet):
    #totalVariables = 10 #hack for working example
    #totalVariables = [Var('w'),Var('x'),Var('y'),Var('z'),Var('$tmp0'),Var('$tmp1'),Var('$tmp2')]
    #interference = {k: set([]) for k in totalVariables}
    interference = {}
    programPoint = 1
    #add registers to interference graph, ignore ebp and esp (stack pointers)
    interference[Register("%eax")] = set([])
    interference[Register("%ebx")] = set([])
    interference[Register("%ecx")] = set([])
    interference[Register("%edx")] = set([])
    interference[Register("%esi")] = set([])
    interference[Register("%edi")] = set([])
    for i in instructionList:
        liveAfter = livenessSet[programPoint]
        if isinstance(i,MovL):
            s = i.left
            t = i.right
            if t in liveAfter:
                if (isinstance(s,Var) and isinstance(t,Var)) or \
                    (isinstance(s,Register) and isinstance(t,Register)) or \
                    (isinstance(s,Address) and isinstance(t,Address)): #is there a better way to do this?
                    for v in liveAfter:
                        if v!=t and v!=s:
                            if interference.has_key(v) and interference.has_key(t):
                                interference[v].add(t)
                                interference[t].add(v)
                            elif interference.has_key(v):
                                interference[v].add(t)
                                interference[t] = set([v])
                            elif interference.has_key(t):
                                interference[t].add(v)
                                interference[v] = set([t])
                            else:
                                interference[t] = set([v])
                                interference[v] = set([t])
                else:
                    for v in liveAfter:
                        if v!=t:
                            if interference.has_key(v) and interference.has_key(t):
                                interference[v].add(t)
                                interference[t].add(v)
                            elif interference.has_key(v):
                                interference[v].add(t)
                                interference[t] = set([v])
                            elif interference.has_key(t):
                                interference[t].add(v)
                                interference[v] = set([t])
                            else:
                                interference[t] = set([v])
                                interference[v] = set([t])

        elif isinstance(i,AddL) or isinstance(i,NegL):
            if isinstance(i,AddL):
                t = i.right
            else:
                t = i.value
            if t in liveAfter:
                for v in liveAfter:
                    if v!=t:
                        if interference.has_key(v) and interference.has_key(t):
                            interference[v].add(t)
                            interference[t].add(v)
                        elif interference.has_key(v):
                            interference[v].add(t)
                            interference[t] = set([v])
                        elif interference.has_key(t):
                            interference[t].add(v)
                            interference[v] = set([t])
                        else:
                            interference[t] = set([v])
                            interference[v] = set([t])

        elif isinstance(i,Call):
            for v in liveAfter:
                if interference.has_key(v):
                    interference[v].add(Register("%eax"))

                else:
                    interference[v] = set([Register("%eax")])

                interference[v].add(Register("%ecx"))
                interference[v].add(Register("%edx"))
                interference[Register("%eax")].add(v)
                interference[Register("%ecx")].add(v)
                interference[Register("%edx")].add(v)

        programPoint=programPoint+1
    return interference






#def interferenceGraph: