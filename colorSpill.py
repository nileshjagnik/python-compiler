from compiler.ast import *
from x86Nodes import *
from x86IR import *
import Queue

registers = [Register("%eax"), Register("%ebx"), Register("%ecx"), Register("%edx"), Register("%esi"), Register("%edi")]

class graphNode(object):
    def __init__(self, priority, vertex):
        self.priority = priority
        self.vertex = vertex
        return
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

def colorSpill(interferenceGraph,instructionList,livenessSet):
    counter = -4
    vertices = interferenceGraph.keys()
    coloring= colorGraph(interferenceGraph)
    foundIllegal = 0
    # NOTE - condition for while needs to change. But currently there are no registers in Interference graph, so I need to add the length of registers 
  #   while (len(coloring) < len(vertices) + len(registers)) and (foundIllegal==0):
  #   	#spill code here
  #   	for vertex in vertices:
  #   		if vertex not in coloring.keys():
  #   			coloring[vertex] = counter
  #   			counter = counter- 4
		# #check for illegal instructions
		# newinstList= []
		# for index,instruction in enumerate(instructionList):
		# 	if isinstance(instruction,AddL):
		# 		if (isinstance(instruction.left,Var)) and (isinstance(instruction.right,Var)) and (coloring[instruction.left] < 0) and (coloring[instruction.right] < 0):
		# 			newinstList.append(MovL((instruction.left,Var('$regtemp'))))
		# 			newinstList.append(AddL((Var('$regtemp'),instruction.right)))
		# 			foundIllegal = 1 
		# 		else:
		# 			newinstList.append(instruction)
		# 	elif isinstance(instruction,MovL):
		# 		if (isinstance(instruction.left,Var)) and (isinstance(instruction.right,Var)) and (coloring[instruction.left] < 0) and (coloring[instruction.right] < 0):
		# 			newinstList.append(MovL((instruction.left,Var('$regtemp'))))
		# 			newinstList.append(MovL((Var('$regtemp'),instruction.right)))
		# 			foundIllegal = 1 
		# 		else:
		# 			newinstList.append(instruction)
		# 	else:
		# 		newinstList.append(instruction)
    return coloring


def colorGraph(interferenceGraph):
	coloring = {} # dictionary store colors

	#default colors for registers
	i=1
	for reg in registers:
		coloring[reg]=i
		i=i+1
	vertices = interferenceGraph.keys()
	for reg in registers:
		if reg in vertices:
			vertices.remove(reg)
	
	#initialize saturation as a dictionary which stores initial saturation
	isat = {}

	for vertex in vertices:
		isat[vertex] = 0

	for reg in registers:
		if interferenceGraph.has_key(reg):
			for vertex in interferenceGraph[reg]:
				if isat.has_key(vertex):
					isat[vertex] = isat[vertex] - 1
				else:
					isat[vertex] = -1

	#now make it a priorityQueue
	qsat = Queue.PriorityQueue()
	for (key,value) in isat.items():
		qsat.put(graphNode(value,key))
	
	# DSATUR algorithm
	while len(vertices) > 0:
		#pick highest saturation
		vertex = qsat.get().vertex
		colors = [1,2,3,4,5,6]
		# find the lowest color c that is not in neighbours(c)
		for neighbor in interferenceGraph[vertex]:
			if coloring.has_key(neighbor):
				if coloring[neighbor] in colors:
					colors.remove(coloring[neighbor])
		if len(colors)>0:
			coloring[vertex] = colors[0]  #color(u) = c
		vertices.remove(vertex) #delete c from list
	
	return coloring