def generateX86(astlist,filename):
	assemblyCode = '.globl main\nmain:\n\tpushl %'+'ebp\n\tmovl %'+'esp, %'+'ebp\n\tpushl $4\n\tcall print_int_nl\n\t'
	assemblyCode += 'leave\n\tret'
	targetfile = open(filename+".s", "w")
	targetfile.truncate()
	targetfile.write(assemblyCode)
	targetfile.close()