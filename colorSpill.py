from compiler.ast import *
from x86Nodes import *
from x86IR import *
import heapq

from heapq import heapify, heappush, heappop

class priority_dict(dict):
    """Dictionary that can be used as a priority queue.

    Keys of the dictionary are items to be put into the queue, and values
    are their respective priorities. All dictionary methods work as expected.
    The advantage over a standard heapq-based priority queue is
    that priorities of items can be efficiently updated (amortized O(1))
    using code as 'thedict[item] = new_priority.'

    The 'smallest' method can be used to return the object with lowest
    priority, and 'pop_smallest' also removes it.

    The 'sorted_iter' method provides a destructive sorted iterator.
    """
    
    def __init__(self, *args, **kwargs):
        super(priority_dict, self).__init__(*args, **kwargs)
        self._rebuild_heap()

    def _rebuild_heap(self):
        self._heap = [(v, k) for k, v in self.iteritems()]
        heapify(self._heap)

    def smallest(self):
        """Return the item with the lowest priority.

        Raises IndexError if the object is empty.
        """
        
        heap = self._heap
        v, k = heap[0]
        while k not in self or self[k] != v:
            heappop(heap)
            v, k = heap[0]
        return k

    def pop_smallest(self):
        """Return the item with the lowest priority and remove it.

        Raises IndexError if the object is empty.
        """
        
        heap = self._heap
        v, k = heappop(heap)
        while k not in self or self[k] != v:
            v, k = heappop(heap)
        del self[k]
        return k

    def __setitem__(self, key, val):
        # We are not going to remove the previous value from the heap,
        # since this would have a cost O(n).
        
        super(priority_dict, self).__setitem__(key, val)
        
        if len(self._heap) < 2 * len(self):
            heappush(self._heap, (val, key))
        else:
            # When the heap grows larger than 2 * len(self), we rebuild it
            # from scratch to avoid wasting too much memory.
            self._rebuild_heap()

    def setdefault(self, key, val):
        if key not in self:
            self[key] = val
            return val
        return self[key]

    def update(self, *args, **kwargs):
        # Reimplementing dict.update is tricky -- see e.g.
        # http://mail.python.org/pipermail/python-ideas/2007-May/000744.html
        # We just rebuild the heap from scratch after passing to super.
        
        super(priority_dict, self).update(*args, **kwargs)
        self._rebuild_heap()

    def sorted_iter(self):
        """Sorted iterator of the priority dictionary items.

        Beware: this will destroy elements as they are returned.
        """
        
        while self:
            yield self.pop_smallest()


registers = [Register("%eax"), Register("%ebx"), Register("%ecx"), Register("%edx"), Register("%esi"), Register("%edi")]


def colorSpill(interferenceGraph,instructionList,livenessSet):
    vertices = interferenceGraph.keys()
    coloring={}
    foundIllegal = 0
    while foundIllegal==0:
        coloring=colorGraph(interferenceGraph)
        counter = -4
        for vertex in vertices:
            if vertex not in coloring.keys():
                coloring[vertex] = counter
                counter -= 4
        newinstList = []
        foundIllegal = 1
        for index,instruction in enumerate(instructionList):
            if isinstance(instruction,MovL):
                if coloring.has_key(instruction.left) and coloring.has_key(instruction.right):
                    if coloring[instruction.left]<0 and coloring[instruction.right]<0:
                        newinstList.append(MovL((instruction.left,Var('$regtemp'))))
                        newinstList.append(MovL((Var('$regtemp'),instruction.right)))
                        livevar = livenessSet[index+1]
                        if not interferenceGraph.has_key(Var('$regtemp')):
                            interferenceGraph[Var('$regtemp')] = set()
                        for vertex in [v for v in vertices if v!=Var('$regtemp') and v!= instruction.left]:
                            interferenceGraph[Var('$regtemp')] = interferenceGraph[Var('$regtemp')]| set([v])
                        foundIllegal=0
                    else:
                        newinstList.append(instruction)
                else:
                    newinstList.append(instruction)
            else:
                newinstList.append(instruction)
        instructionList = newinstList
    return coloring,newinstList,interferenceGraph

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
	    if vertex == Var('$regtemp'):
		    isat[vertex] = 3
	    else:
	        isat[vertex] = 6

	for reg in registers:
		if interferenceGraph.has_key(reg):
			for vertex in interferenceGraph[reg]:
				if isat.has_key(vertex):
					isat[vertex] = isat[vertex] - 1
				else:
					isat[vertex] = 5

	#now make it a priorityQueue
	qsat = priority_dict(isat)
	
	# DSATUR algorithm
	while len(vertices) > 0:
		#pick highest saturation
		vertex = qsat.pop_smallest()
		colors = [1,2,3,4,5,6]
		# find the lowest color c that is not in neighbours(c)
		for neighbor in interferenceGraph[vertex]:
			if coloring.has_key(neighbor):
				if coloring[neighbor] in colors:
					colors.remove(coloring[neighbor])
		for neighbor in interferenceGraph[vertex]:
			if not coloring.has_key(neighbor):
			    isat[neighbor] = isat[neighbor] - 1 
		qsat.update()
		if len(colors)>0:
			coloring[vertex] = colors[0]
		vertices.remove(vertex)
	return coloring
