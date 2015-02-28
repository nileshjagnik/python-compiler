from compiler.ast import *
from x86Nodes import *
from x86IR import *
from explicateNodes import *
from collections import defaultdict
import heapq


REMOVED = '<removed-task>'

class updatePriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        #self.counter = itertools.count()

    def add_task(self,task, count, priority=0): #use count to mark spill variables?
        #Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        #count = next(counter)
        #print isinstance(task,Var)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self,task):
        #'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = Var(REMOVED)

    def pop_task(self):
        #'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task != Var(REMOVED):
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

def total(instructionList): #count line for if statements
    t = 0
    for i in instructionList:
        if isinstance(i,IfNode):
            for test in i.tests:
                t += 1 + len(tests.tests[1])
            t += len(i.else_)
        else:
            t += 1
    return t

def computeLivenessPoint(i,liveAfter):
    liveBefore = set([])
    if isinstance(i,AddL):
        if isinstance(i.left,Var):
            lifeBefore = (liveAfter-set([i.right]))|set([i.left,i.right])
        elif isinstance(i.right,Register):
            liveBefore = (liveAfter-set([i.right]))
        else:
            liveBefore = (liveAfter-set([i.right]))|set([i.right])

    elif isinstance(i,MovL):
            if isinstance(i.left,Var):
                liveBefore= (liveAfter-set([i.right]))|set([i.left])
            
            else:
                liveBefore = (liveAfter-set([i.right]))

    elif isinstance(i,NegL):
            liveBefore = (liveAfter)
    
    elif isinstance(i,Push):
        if isinstance(i.argument,Var):
            liveBefore = (liveAfter)|set([i.argument])
        else:
            liveBefore = (liveAfter)

    elif isinstance(i,Call):
        liveBefore = liveAfter

    elif isinstance(i,CmpL):
        print i
        if isinstance(i.left,Var) and not isinstance(i.right,Con):
            liveBefore = (liveAfter-set([i.right]))|set([i.left,i.right])
        elif isinstance(i.right,Register) or isinstance(i.right,Con):
            liveBefore = (liveAfter-set([i.right]))
        else:
            liveBefore = (liveAfter-set([i.right]))|set([i.right])

    return liveBefore


def livenessAnalysis(instructionList):
    totalInstruction = total(instructionList)
    live = [set() for index in range(len(instructionList)+1)]
    livePoint = len(instructionList)-1
    for i in reversed(instructionList):
        liveAfter = live[livePoint+1]
        if isinstance(i,If): #need to fix to handle nested if statements
            liveAfterF = liveAfter
            liveAfterE = liveAfter
            for e in reversed(i.else_):
                liveBefore = computeLivenessPoint(e,liveAfterE)
                live[livePoint] = liveBefore
                livePoint = livePoint-1
                liveAfterE = liveBefore
        
            liveIf = set([])
            for t in reversed(i.tests):
                liveAfterF = liveAfter
                for stmt in t[1]:
                    liveB = computeLivenessPoint(i,liveAfterF)
                    live[livePoint] = liveB
                    livePoint = livePoint-1
                    liveAfterF = liveB
                
                liveIf = liveIf | set([t[0]])| liveAfterF
    
            live[livePoint] = liveAfterIf | liveAfterE
        else:
            #print i
            live[livePoint] = computeLivenessPoint(i,liveAfter)
        
        livePoint = livePoint-1
        
    return live

def interferenceGraph(instructionList,livenessSet,variables):
    #totalVariables = 10 #hack for working example
    #totalVariables = [Var('w'),Var('x'),Var('y'),Var('z'),Var('$tmp0'),Var('$tmp1'),Var('$tmp2')]
    interference = {k: set([]) for k in variables}
    interference[Register("%eax")] = set([])
    interference[Register("%ecx")] = set([])
    interference[Register("%edx")] = set([])
    programPoint = 1
    for i in instructionList:
        liveAfter = livenessSet[programPoint]
        if isinstance(i,If):
            for t in i.tests:
                programPoint = programPoint+1
                for stmt in t[1]:
                    liveAfterF = livenessSet[programPoint]
                    edges = interferencePoint(stmt,liveAfterF)
                    for (v1,v2) in edges:
                        interference[v1].add(v2)
                        interference[v2].add(v1)
                    programPoint=ProgramPoint+1
            for e in i.else_:
                liveAfterE = livenessSet[programPoint]
                edges = interferencePoint(e,liveAfterE)
                for (v1,v2) in edges:
                    interference[v1].add(v2)
                    interference[v2].add(v1)
                programPoint=ProgramPoint+1
        
        else:
            edges = interferencePoint(i,liveAfter)
            #print "edges"
            #print edges
            for (v1,v2) in edges:
                interference[v1].add(v2)
                interference[v2].add(v1)
            programPoint=programPoint+1
                
    return interference


def interferencePoint(i,liveAfter):
    #print i
    edges = set([])
    #print edges
    if isinstance(i,MovL):
        s = i.left
        t = i.right
        
        if isinstance(s,Var) and isinstance(t,Var):
            
            for v in liveAfter:
                if v!=t and v!=s:
                    edges.add((t,v))
        
        else:
            for v in liveAfter:
                if v!=t:
                    edges.add((t,v))


    elif isinstance(i,AddL) and isinstance(i.right,Var):
        t = i.right
        for v in liveAfter:
            if v!=t:
                edges.add((t,v))
    
    elif isinstance(i,NegL) and isinstance(i.value,Var):
        t = i.value
        for v in liveAfter:
            if v!=t:
                edges.add((t,v))

    elif isinstance(i,Call):
        for v in liveAfter:
            edges.add((Register("%eax"),v))
            edges.add((Register("%ecx"),v))
            edges.add((Register("%edx"),v))

    return edges


def graphColor(interferenceGraph):
    vertices = set(interferenceGraph.keys())
    
    vertices.remove(Register("%eax"))
    vertices.remove(Register("%ecx"))
    vertices.remove(Register("%edx"))
    
    #adjust node saturation, use heapq, make sure higher priority, return negative of the number
    coloring = defaultdict(int)
    coloring[Register("%eax")]=1
    coloring[Register("%ebx")]=2
    coloring[Register("%ecx")]=3
    coloring[Register("%edx")]=4
    coloring[Register("%esi")]=5
    coloring[Register("%edi")]=6
    #print coloring[Register("%eax")]
    
    
    sat,color_neighbors,count,countTmp = saturation(vertices,interferenceGraph,coloring)
    #print
    while len(vertices) > 0:
        toColor = sat.pop_task()
        varC = toColor
        color_n = color_neighbors[varC]
        #print varC
        if len(color_n)>0:
            color = findColor(color_n)
        else:
            color = 1
        coloring[varC]=color
        #print varC
        vertices.remove(varC)
        adj = interferenceGraph[varC]
        for n in adj:
            if n in vertices:
                heapq.heappush(color_neighbors[n],color)
                newSat = len(color_neighbors[n])
                if n.name[0]=="#":
                    sat.add_task(n,count,-newSat)
                    countTmp = countTmp-1
                else:
                    sat.add_task(n,count,-newSat)
                    count = count+1
        
        
        #sat = saturation(vertices,interferenceGraph,coloring)

    return coloring

def findColor(colors): #this is fine
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
    count = 1;
    countTmp = -1
    initSat = updatePriorityQueue()
    initColors = {}
    for v in vertices:
        adj = interferenceGraph[v]
        sat = 0
        colors = []
        for n in adj:
            #   print coloring[n]
            if coloring[n]>0:
                sat = sat+1
                heapq.heappush(colors,coloring[n])
    
        initColors[v] = colors
    #print "sat" +str(sat)
    #   print colors
    #print v
    
        print v
        print "Name"
        print v.name
        if v.name[0] == "#":
            initSat.add_task(v,-sat,countTmp)
            countTmp = countTmp-1
        else:
            initSat.add_task(v,-sat,count)
            count = count+1
#print initSat
#print initSat

    return initSat,initColors,count,countTmp

def toSpill(coloring):
    list = {}
    stackLocal = -4
    for k in coloring.iterkeys():
        if coloring[k]>6:
            list[k]=stackLocal
            stackLocal = stackLocal-4
    return list

def allocateRegisters(toSpill,instructionList,variables,coloring):
    colorMap = {}
    colorMap[1] = Register("%eax")
    colorMap[2] = Register("%ebx")
    colorMap[3] = Register("%ecx")
    colorMap[4] = Register("%edx")
    colorMap[5] = Register("%esi")
    colorMap[6] = Register("%edi")
    check = True
    #toSpillVar = toSpill.keys()
    good = []
    bad = []
    tmp = Var("#tmp")
    newVars = variables
    newVars.add(tmp)
    for i in instructionList:
        if isinstance(i,If):
            tests = i.tests
            pairG = []
            pairB = []
            elseG = []
            elseB = []
            
            else_ = i.else_
            for t in tests:
                intsG = []
                instB = []
                for stmt in t[1]:
                    (goodI,badI) = allocateInstruction(toSpill,stmt,variables,coloring,colorMap)
                    if len(badI)>1:
                        check = False
                    instG.append(goodI)
                    instB.extend(badI)
                pairG.append((t[0],instG))
                pairB.append((t[0],instB))
            for e in else_:
                (goodI,badI) = allocateInstruction(toSpill,stmt,variables,coloring,colorMap)
                if len(badI)>1:
                    check = False
                elseG.append(goodI)
                elseB.extend(goodB)

            good.append(If(pairG,elseG))
            bad.append(If(pairB,elseB))

        else:
            (goodI,badI) = allocateInstruction(toSpill,i,variables,coloring,colorMap)
            if len(badI)>1:
                check = False
            good.append(goodI)
            bad.extend(badI)
                
    return good,bad,newVars,check



def allocateInstruction(toSpill,i,variables,coloring,colorMap):
    tmp = Var("#tmp")
    if isinstance(i,AddL):
        regl = i.left
        regr = i.right
        localR = toSpill.has_key(regr)
        if isinstance(regr,Register):
            return (i,[i])
        elif isinstance(regl,Con):
            if localR:
                goodNode = AddL((regl,Address(toSpill[regr])))
            else:
                #print regr
                goodNode = AddL((regl,Register(colorMap[coloring[regr]])))
            return (goodNode,[i])
            
        else:
            localL = toSpill.has_key(regl)
        
            if localL and localR:
                check = False
                badNodeMove = MovL((regl,tmp))
                badNodeAdd = AddL((tmp,regr))
                #bad.extend([badNodeMove,badNodeAdd])
                return (i,[badNodeMove,badNodeAdd])
                #totalTmp+=1
                #newVars.add(tmp)
                #print "BAD VAR"
                #print i
            else:
                if localL:
                    goodNode = AddL((Address(toSpill[regl]),Register(colorMap[coloring[regr]])))
            
                elif localR:
                    goodNode = AddL((Register(colorMap[coloring[regl]]),Address(toSpill[regr])))
               
                else:
                    goodNode = AddL((Register(colorMap[coloring[regl]]),Register(colorMap[coloring[regr]])))
                
                return (goodNode,[i])
               
    elif isinstance(i,MovL):
        regl = i.left
        regr = i.right
        localR = toSpill.has_key(regr)
        if isinstance(regl,Con):
            if localR:
                goodNode = MovL((regl,Address(toSpill[regr])))
            else:
                goodNode = MovL((regl,Register(colorMap[coloring[regr]])))
            return (goodNode,[i])
    
        else:
            localL = toSpill.has_key(regl)
            if localL and localR:
                check = False
                badNodeMove = MovL((regl,tmp))
                badNodeAdd = MovL((tmp,regr))
                return (i,[badNodeMove,badNodeAdd])
            else:
                if localL:
                    goodNode = MovL((Address(toSpill[regl]),Register(colorMap[coloring[regr]])))
                    return (goodNode,[i])
                                  
                elif localR:
                    goodNode = MovL((Register(colorMap[coloring[regl]]),Address(toSpill[regr])))
                    return (goodNode,[i])
                
                else:
                    goodNode = MovL((Register(colorMap[coloring[regl]]),Register(colorMap[coloring[regr]])))
                    if goodNode.left != goodNode.right:
                        return (goodNode,[i])
                    else:
                        return (None,[i])
               
                                   
    elif isinstance(i,NegL):
        value = i.value
        goodNode = i
        if isinstance(value,Var):
            local = toSpill.has_key(value)
            if local:
                goodNode = NegL(Address(toSpill[value]))
            else:
                goodNode = NegL(Register(colorMap[coloring[value]]))
        return (goodNode,[i])

       

    elif isinstance(i,Call):
       return (i,[i])

    elif isinstance(i,Push):
        #print "found push"
        #print i
        value = i.argument
        goodNode = i
        if isinstance(value,Var):
            local = toSpill.has_key(value)
            if local:
                goodNode = Push(Address(toSpill[value]))
            else:
                goodNode = Push(Register(colorMap[coloring[value]]))
        
        return (goodNode,[i])





#generate everything, then check if anything is violated
#map of colors to registers
#for each instruction check if it will cause memory to memory operation
#otherwise allocate stack slot and color -1
#if it does generate tmp intstruction and rerun

'''
    def interferencePoint(instr,liveAfter,interference):
    programPoint = 1
    for i in instructionList:
    liveAfter = livenessSet[programPoint]
    if isinstance(i,MovL):
    s = i.left
    t = i.right
    
    if isinstance(s,Var) and isinstance(t,Var):
    
    for v in liveAfter:
    if v!=t and v!=s:
    interference[v].add(t)
    interference[t].add(v)
    
    else:
    for v in liveAfter:
    if v!=t:
    interference[v].add(t)
    interference[t].add(v)
    
    
    elif isinstance(i,AddL) and isinstance(i.right,Var):
    t = i.right
    for v in liveAfter:
    if v!=t:
    interference[v].add(t)
    interference[t].add(v)
    
    elif isinstance(i,NegL) and isinstance(i.value,Var):
    t = i.value
    for v in liveAfter:
    if v!=t:
    interference[v].add(t)
    interference[t].add(v)
    
    elif isinstance(i,Call):
    for v in liveAfter:
    interference[v].add(Register("%eax"))
    interference[v].add(Register("%ecx"))
    interference[v].add(Register("%edx"))
    
    
    interference[Register("%eax")].add(v)
    interference[Register("%ecx")].add(v)
    interference[Register("%edx")].add(v)
    
    programPoint=programPoint+1
    #print interference
    return interference
'''

