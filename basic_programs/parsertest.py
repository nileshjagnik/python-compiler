from compiler import *

if __name__ == "__main__":
	#ast = parse('x={"hey":3, "whut":2}')
	#print ast
	ast = parseFile("iftest.py")
	print ast
