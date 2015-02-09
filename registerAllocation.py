from compiler.ast import *
from x86Nodes import *
from x86IR import *

def livenessAnalysis(instructionList):
    live = [set() for index in range(len(instructionList)+1)]
    livePoint = len(instructionList)-1
    for i in reversed(instructionList):
        if isinstance(i,AddL):
            if isinstance(i.left,Con):
                live[livePoint] = (live[livePoint+1]-set([i.right]))|set([i.right])
            else:
                live[livePoint] = (live[livePoint+1]-set([i.right]))|set([i.left,i.right])
        elif isinstance(i,MovL):
            if isinstance(i.left,Con):
                live[livePoint] = (live[livePoint+1]-set([i.right]))
            else:
                live[livePoint]= (live[livePoint+1]-set([i.right]))|set([i.left])
        elif ininstance(i,NegL):
            live[livePoint] = (live[livePoint+1]-set([i.value]))|set([i.value])
        livePoint = livePoint-1

    return live

def interferenceGraph(instructionList,livenessSet):
    #totalVariables = 10 #hack for working example
    totalVariables = [Var('w'),Var('x'),Var('y'),Var('z'),Var('$tmp0'),Var('$tmp1'),Var('$tmp2')]
    interference = {k: set([]) for k in totalVariables}
    programPoint = 1
    for i in instructionList:
        liveAfter = livenessSet[programPoint]
        if isinstance(i,MovL):
            s = i.left
            t = i.right
            if t in liveAfter:
                if isinstance(s,Name):
                    for v in liveAfter:

                        if v!=t and v!=s:
                            interference[v].add(t)
                            interference[t].add(v)
                else:
                    for v in liveAfter:
                        if v!=t:
                            interference[v].add(t)
                            interference[t].add(v)

        elif isinstance(i,AddL):
            t = i.right
            if t in liveAfter:
                for v in liveAfter:
                    if v!=t:
                        interference[v].add(t)
                        interference[t].add(v)

#elif isinstance(i,NegL):
        programPoint=programPoint+1
    return interference






#def interferenceGraph: