from compiler.ast import *
from compiler import *

//function to get ast height 
def p0_ast_heigth(ast):
		if isinstance(ast, Module):
			return 1 + p0_ast_heigth(ast.node)
		elif isinstance(ast, Stmt):
			return 1 + max([p0_ast_heigth(c) for c in ast.nodes])
		elif isinstance(ast,Printnl):
			return 1 + p0_ast_heigth(ast.nodes[0])
		elif isinstance(ast, Add):
			return 1 + max(p0_ast_heigth(ast.left),p0_ast_heigth(ast.right))
		elif isinstance(ast,Discard):
			return p0_ast_heigth(ast.expr)
		elif isinstance(ast,Const):
			return 1
		else:
			print "Unsupported",ast
			return -1

if __name__ == "__main__":
	ast = parse('3+4+5+6+7')
	print ast
	print p0_ast_heigth(ast)