from .syntax_tree import *

class Unit(Node):
	def __init__(self, parent, filename):
		self.parent = parent
		self.filename = filename




class Module(Node):
	def __init__(self, parent, identifier):
		self.parent = parent
		self.identifier = identifier
		self.source_dirs = []

		# childs
		self.modules = {}
		self.units = []


	def addSourceDir(self, path):
		from pathlib import Path
		if isinstance(path, str):
			path = Path(path)
		self.source_dirs.append(path)

	def module(self, identifier):
		if not identifier in self.modules:
			self.modules[identifier] = Module(self, identifier)
		return self.modules[identifier]

	def addUnit(self, filename):
		self.units.append(Unit(self, filename.resolve()))

	def visit(self, visitor):
		yield from visit_map(self.modules)
		yield from visit_seq(self.units)

