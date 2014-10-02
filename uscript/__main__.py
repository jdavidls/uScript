'''

'''

from uscript.process.source_code import scan_line, scan_stream, Parser
from uscript.source.tools import ASTPrinter
#from uscript.model import Root

def lexer_test():
	script = '''
		Esto es un comentario

foo: method
foo(a:int) = a +1

		Esto es un comentario para la funcion foo

foo(a:string	\ comentario al argumento
				mas comentario

): int
	+a



'''.splitlines()




	level = 0
	for token in lexer.scan_stream(script):
		if isinstance(token, model.End):
			level -= 1

		print("\t"*level, repr(token))

		if isinstance(token, model.Begin):
			level += 1


def line_test():
	script = '.alpha.beta[1, 3] / 6 && z'

	p = parser.Parser()
	printer = source.ASTPrinter()

	ast = p(lexer.scan_line(script), 'Expression')

	print(ast)
	printer(ast)

def block_test():
	script = '''


foo(a:int) = a +1
foo(a:int): int =
	a+1


'''.splitlines()


	p = Parser()
	printer = ASTPrinter()

	ast = p(scan_stream(script), 'Expression')

	#print(ast)
	for line in printer(ast):
		print(*line)



block_test()

#root = Root()
#root.addSourceDir('./runtime')
#root()
