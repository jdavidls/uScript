from uscript.source import syntax_tree
from .tokenizer import scan_line, scan_stream
from .parser import Parser

class SourceCodeProcessor(syntax_tree.Visitor):
	def __init__(self, root):
		super().__init__(root)
		#from uscript.source import lexer, parser, ASTPrinter
		#self.lexer = lexer
		self.parser = Parser()
		#self.printer = ASTPrinter()

	def preUnit(self, unit):
		print('processing ', unit.filename)

		with unit.filename.open() as file:
			unit.lines = file.readlines()

		unit.tokens = [ token for token in scan_stream(unit.lines) ]

		unit.ast = self.parser(iter(unit.tokens))


		self.printer(unit.ast)

		#return self.Skip

#Interactive unit processor