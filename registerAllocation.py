from compiler.ast import *
from x86Nodes import *
from x86IR import *
from collections import defaultdict
import heapq

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

def interferenceGraph(instructionList,livenessSet,variables):
    #totalVariables = 10 #hack for working example
    #totalVariables = [Var('w'),Var('x'),Var('y'),Var('z'),Var('$tmp0'),Var('$tmp1'),Var('$tmp2')]
    interference = {k: set([]) for k in variables}
    #interference = {}
    programPoint = 1
    #add registers to interference graph, ignore ebp and esp (stack pointers)
    #interference[Register("%eax")] = set([])
    #interference[Register("%ebx")] = set([])
    #interference[Register("%ecx")] = set([])
    #interference[Register("%edx")] = set([])
    #interference[Register("%esi")] = set([])
    #interference[Register("%edi")] = set([])
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
                if interference.has_key(Register("%eax")):
                    interference[Register("%eax")].add(v)
                    interference[Register("%ecx")].add(v)
                    interference[Register("%edx")].add(v)
                else:
                    interference[Register("%eax")] = set([v])
                    interference[Register("%ecx")] = set([v])
                    interference[Register("%edx")] = set([v])

        programPoint=programPoint+1
    return interference


def graphColor(interferenceGraph):
    vertices = set(interferenceGraph.keys())
    
    #adjust node saturation, use heapq, make sure higher priority, return negative of the number
    coloring = defaultdict(int)
    coloring[Register("%eax")]=1
    coloring[Register("%ebx")]=2
    coloring[Register("%ecx")]=3
    coloring[Register("%edx")]=4
    coloring[Register("%esi")]=5
    coloring[Register("%edi")]=6
    print coloring[Register("%eax")]
    sat = saturation(vertices,interferenceGraph,coloring)
    while len(vertices) > 0:
        toColor = heapq.heappop(sat)
        varC = toColor[1]
        print varC
        if len(toColor[2])>0:
            color = findColor(toColor[2])
        else:
            color = 1
        coloring[varC]=color
        vertices.remove(varC)
        sat = saturation(vertices,interferenceGraph,coloring)

    return coloring

def findColor(colors):
    total = len(colors)
    if total==1:
        if heapq.heappop(colors) > 1:
            return 1
        else:
            return 2
    else:
        lo = heapq.heappop(colors)
        for c in range(total-1):
            hi = heapq.heappop(colors)
            if hi-lo > 1:
                return lo+1
            else:
                lo = hi
        return lo+1


def saturation(vertices,interferenceGraph,coloring):
    
    initSat = []
    for v in vertices:
        adj = interferenceGraph[v]
        sat = 0
        colors = []
        for n in adj:
            #   print coloring[n]
            if coloring[n]>0:
                sat = sat+1
                heapq.heappush(colors,coloring[n])
    #print "sat" +str(sat)
    #   print colors
    #   print v
        heapq.heappush(initSat,(-sat,v,colors))
#print initSat
#print initSat

    return initSat







#def interferenceGraph:
