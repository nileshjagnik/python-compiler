from compiler.ast import *
def generateX86(astlist,filename,varmap):
	preamble = ".globl main\nmain:\n\tpushl %ebp\n\tmovl %esp, %ebp\n\t"
	postemble = 'movl $0, %eax\n\tleave\n\tret\n'
	stackspace = "subl $" + str(len(varmap)*4)+",%esp\n\n\t"
	
	assemblyCode = preamble
	assemblyCode += stackspace

	for tree in astlist:
		if isinstance(tree,Assign):
			if isinstance(tree.expr,CallFunc):
				destination = str(varmap[tree.nodes.name])
				assemblyCode += "call input\n\tmovl %eax, "+destination+"(%ebp)\n\n\t"
			elif isinstance(tree.expr,UnarySub):
				if isinstance(tree.expr.expr,Name):
					source = str(varmap[tree.expr.expr.name])
					assemblyCode += "movl "+source+"(%ebp), %eax\n\t"
					destination = str(varmap[tree.nodes.name])
					assemblyCode += "movl %eax, "+destination+"(%ebp)\n\t"
					assemblyCode += "negl "+destination+"(%ebp)\n\n\t"
				elif isinstance(tree.expr.expr,Const):
					value = tree.expr.expr.value
					destination = str(varmap[tree.nodes.name])
					assemblyCode += "movl $"+value+", "+destination+"(%ebp)\n\t"
					assemblyCode += "negl "+destination+"(%ebp)\n\n\t"
			elif isinstance(tree.expr,Add):
					destination = str(varmap[tree.nodes.name])
					if isinstance(tree.expr.left,Name):
						source = str(varmap[tree.expr.left.name])
						assemblyCode += "movl "+source+"(%ebp), %eax\n\t"
						assemblyCode += "movl %eax, "+destination+"(%ebp)\n\t"
					elif isinstance(tree.expr.left,Const):
						value = str(tree.expr.left.value)
						assemblyCode += "movl $"+value+", "+destination+"(%ebp)\n\t"
					if isinstance(tree.expr.right,Name):
						source = str(varmap[tree.expr.right.name])
						assemblyCode += "movl "+source+"(%ebp), %eax\n\t"
						assemblyCode += "addl %eax, "+destination+"(%ebp)\n\n\t"
					if isinstance(tree.expr.right,Const):
						value = str(tree.expr.right.value)
						assemblyCode += "add $"+value+", "+destination+"(%ebp)\n\n\t"
		elif isinstance(tree,Printnl):
				if(tree.nodes,Name):
					source = str(varmap[tree.nodes.name])
					assemblyCode += "pushl "+source+"(%ebp)\n\tcall print_int_nl\n\taddl $4, %esp\n\n\t"
				elif(tree.nodes,Const):
					value = tree.nodes.value
					assemblyCode += "pushl $"+value+"\n\tcall print_int_nl\n\taddl $4, %esp\n\n\t"
	assemblyCode += postemble
	targetfile = open(filename+".s", "w")
	targetfile.truncate()
	targetfile.write(assemblyCode)
	targetfile.close()