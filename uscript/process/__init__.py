'''



'''
from uscript import tools
from uscript.model.source.syntax_tree import *
from uscript.model.source.expression import *
from uscript.model.source.lexicon import *

from .tokenizer import scan_line, scan_stream
from .parser import Parser

class FileSystemInjector(Visitor):
	def preModule(self, module):
		# scan directories

		for dir in module.source_dirs:
			for entry in dir.iterdir():
				identifier = entry.stem

				if not identifier.startswith('.'):
					if entry.is_dir():
						submod = module
						for identifier in identifier.split('.'):
							submod = submod.module(identifier)
						submod.addSourceDir(entry)
						continue

					elif entry.is_file():
						if entry.suffix in ('.u', '.µ'):
							submod = module
							for identifier in identifier.split('.'):
								submod = submod.module(identifier)
							submod.addUnit(entry)
							continue

				print('source file "{}" ignored'.format(entry))

# SyntacticProcessor
class SyntacticProcessor(Visitor):
	def __init__(self):
		super().__init__()
		self.parser = Parser()
		self.printer = tools.ASTPrinter()


	def preUnit(self, unit):
		print(unit.filename)


		with unit.filename.open() as file:
			unit.lines = file.readlines()

		unit.tokens = [ token for token in scan_stream(unit.lines) ]

		tools.print_tokens(unit.tokens)

		unit.syntax = self.parser(iter(unit.tokens))

		for line in self.printer(unit.syntax):
			print(*line)

# parse Declarations
class SemanticProcessor(Visitor):
	def __init__(self):
		super().__init__()
		self.ancestors = []

	def preNode(self, node):
		self.ancestors.append(node)

	def postNode(self, node):
		self.ancestors.pop()

	def preUnit(self, unit):
		parent = self.ancestors[-1]

		for syntagma in unit.syntax:
			if isinstance(syntagma, Pair):
				pair = syntagma
				if isinstance(pair.lvalue, Identifier):
					identifier = pair.lvalue
					invariant = pair.rvalue
					parent.declare(identifier, invariant)

		self.ancestors.append(unit)


		'''

			elif isinstance(syntagma, Assignment):
				assign = syntagma
				if isinstance(assign.lvalue, Identifier):
					print('declare var', syntagma)
				elif isinstance(assign.lvalue, Pair):
					pair = assign.lvalue
					if isinstance(pair.lvalue, Identifier):
						print('declare contract', pair.lvalue, 'as', pair.rvalue, 'assigned to', assign.rvalue)
		'''


