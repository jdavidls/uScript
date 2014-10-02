from uscript.source import syntax_tree, tools

from .tokenizer import scan_line, scan_stream
from .parser import Parser

class SourceCodeProcessor(syntax_tree.Visitor):
	def __init__(self):
		super().__init__()

		self.parser = Parser()
		self.printer = tools.ASTPrinter()

	def preUnit(self, unit):
		print('processing ', unit.filename)

		with unit.filename.open() as file:
			unit.lines = file.readlines()

		unit.tokens = [ token for token in scan_stream(unit.lines) ]

		unit.ast = self.parser(iter(unit.tokens))

		for line in self.printer(unit.ast):
			print(*line)

		#return self.Skip

#Interactive unit processor